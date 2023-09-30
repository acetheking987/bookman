import pymongo as pm
import os, dotenv

class Database:
    def __init__(self) -> None:
        dotenv.load_dotenv()
        if os.getenv('MONGODB_URI') is None:
            raise Exception("MONGO_URI not found")
        self.client = pm.MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client['bookman']

    def add_book_cache(self, books: list) -> None:
        for book in books:
            if len(self.query_book_cache(book)) == 0:
                self.db['book_cache'].insert_one(book)

    def query_book_cache(self, book: dict) -> list:
        query = {}
        for key in book:
            if book[key] == "":
                continue
            elif type(book[key]) == str:
                query[key] = {"$regex": book[key], "$options": "i"}
            else:
                query[key] = book[key]
        return list(self.db['book_cache'].find(query))