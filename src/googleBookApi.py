from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import dotenv, os

class Api:
    def __init__(self) -> None:
        dotenv.load_dotenv()
        if os.getenv('GOOGLE_API_KEY') is None:
            raise Exception("API_KEY not found")
        self.service = build('books', 'v1', developerKey=os.getenv('GOOGLE_API_KEY'))

    def searchBook(self, keyword:str) -> dict:
        try:
            request = self.service.volumes().list(source='public', q=keyword)
            response = request.execute()
            if "items" not in response: return []
            return response["items"]
        except HttpError as err:
            return []
        
    def getBook(self, book_id:str) -> dict:
        try:
            request = self.service.volumes().get(volumeId=book_id)
            response = request.execute()
            return response
        except HttpError as err:
            return {}