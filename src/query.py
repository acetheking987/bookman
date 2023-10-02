import ao3Api, googleBookApi, dotenv, os, database

class Query:
    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.ao3 = ao3Api.Api()
        self.google = googleBookApi.Api()

    def ao3Search(self, title:str="", author:str="", fandoms:str="", language:str="") -> list:
        return self.ao3.search(title=title, author=author, fandoms=fandoms, language=language)
    
    def ao3GetWork(self, work_id:int) -> dict:
        return self.ao3.workToDict(self.ao3.get_work(work_id))
    
    def ao3GetWorkQuick(self, work_id:int) -> dict:
        work = self.ao3.get_work(work_id)
        return {
            "title": work.title,
            "authors": [author.username for author in work.authors],
            "fandoms": work.fandoms,
            "language": work.language,
            "rating": work.rating,
            "words": work.words,
            "id": work.id,
            "from": "ao3"
        }
    
    def filterGoogleResults(self, results:list) -> list:
        filtered = []
        for result in results:
            try:
                filtered.append({
                    "title": result["volumeInfo"]["title"],
                    "authors": result["volumeInfo"]["authors"],
                    "pageCount": result["volumeInfo"]["pageCount"],
                    "rating": result["volumeInfo"]["averageRating"],
                    "language": result["volumeInfo"]["language"],
                    "id": "GOOG" + result["id"],
                    "from": "google"
                })
            except KeyError:
                continue # this has only happened once errored once and I forgot what specificly caused it so i put this here to blanket fix it for now. 
                         # If someone can reproduce this (the key error with "result["volumeInfo"]["authors"]") error please open an issue on github
        return filtered
    
    def googleSearch(self, keyword:str) -> list:
        return self.google.searchBook(keyword)
    
    def getBook(self, book_id:str) -> dict:
        if str(book_id)[:4] == "GOOG":
            book = self.google.getBook(book_id[4:])
            book["from"] = "google"
            book["id"] = book_id
            return book
        
        else:
            book = self.ao3GetWork(book_id)
            book["from"] = "ao3"
            return book
    
    def query(self, title:str="", author:str="", fandoms:str="", language:str="", dontSearchCache:bool=False, dontSaveCache:bool=False) -> list:
        if not dontSearchCache:
            db = database.Database()
            cache = db.query_book_cache_non_fuzz({
                "title": title,
                "author": author,
                "fandoms": fandoms,
                "language": language
            })
            if len(cache) > 0:
                for book in cache:
                    if "_id" in book:
                        del book["_id"]
                return cache
        
        if title != "" or author != "": google_results = self.filterGoogleResults(self.googleSearch(title + " " + author))
        else: google_results = []
        ao3_results = [self.ao3GetWorkQuick(work) for work in self.ao3Search(title=title, author=author, fandoms=fandoms, language=language)]
        results = google_results + ao3_results

        if not dontSaveCache:
            db = database.Database()
            db.add_book_cache(results)
        for result in results:
            if "_id" in result:
                del result["_id"]

        return results