import AO3, dotenv, os, datetime

class Api:
    def __init__(self):
        dotenv.load_dotenv()
        if os.getenv('AO3_USERNAME') is None or os.getenv('AO3_PASSWORD') is None:
            self.session = AO3.GuestSession()
        else:
            self.session = AO3.Session(os.getenv('AO3_USERNAME'), os.getenv('AO3_PASSWORD'))

    def search(self, title:str="", author:str="", fandoms:str="", language:str="") -> list:
        search = AO3.Search(session=self.session, title=title, author=author, fandoms=fandoms, language=language)
        search.update()
        return [work_id.id for work_id in search.results]
    
    def get_work(self, work_id:int) -> AO3.Work:
        return AO3.Work(work_id, session=self.session)
    
    def workToDict(self, work:AO3.Work) -> dict:
        work.reload()
        authors = [self.authorToDict(author) for author in work.authors]
        chapters = [self.chapterToDict(chapter) for chapter in work.chapters]
        series = self.seriesToDict(work.series)
        return {
            "title": work.title,
            "authors": authors,
            "fandoms": work.fandoms,
            "rating": work.rating,
            "warnings": work.warnings,
            "categories": work.categories,
            "relationships": work.relationships,
            "characters": work.characters,
            "words": work.words,
            "chapters": chapters,
            "comments": work.comments,
            "kudos": work.kudos,
            "bookmarks": work.bookmarks,
            "hits": work.hits,
            "published": datetime.datetime.strftime(work.date_published, "%Y-%m-%d %H:%M"),
            "updated": datetime.datetime.strftime(work.date_updated, "%Y-%m-%d %H:%M"),
            "summary": work.summary,
            "start_notes": work.start_notes,
            "end_notes": work.end_notes,
            "language": work.language,
            "status": work.status,
            "complete": work.complete,
            "series": series,   
            "url" : work.url,
            "id": work.id
        }
    
    def getAuthor(self, author_id:int) -> AO3.User:
        return AO3.User(author_id, session=self.session)
    
    def authorToDict(self, author:AO3.User) -> dict:
        author.reload()
        return {
            "name": author.username,
            "id": author.id,
            "works": author.works,
            "bio": author.bio,
            "url": author.url
        }
    
    def getChapter(self, work_id:int, chapter_id:int) -> AO3.Chapter:
        return AO3.Chapter(work_id, chapter_id, session=self.session)

    def chapterToDict(self, chapter:AO3.Chapter) -> dict:
        chapter.reload()
        return {
            "title": chapter.title,
            "work_id": chapter.work.id,
            "id": chapter.id,
            "url": chapter.url
        }
    
    def getSeries(self, series_id:int) -> AO3.Series:
        return AO3.Series(series_id, session=self.session)
    
    def seriesToDict(self, series:AO3.Series) -> dict:
        series_list = []
        for item in series:
            item:AO3.Series = item
            item.reload()
            works = [{"id": work.id, "title": work.title} for work in item.work_list]
            series_list.append({
                "title": item.name,
                "id": item.id,
                "url": item.url,
                "works": works
            })
        return series_list
    
    def downloadWork(self, work_id:int, filetype:str="PDF") -> str:
        work = self.get_work(work_id)
        work.reload()
        return work.download(filetype=filetype)