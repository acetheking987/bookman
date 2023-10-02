import query, ao3Api, os, dotenv, database
from flask import Flask, request

def downloadAo3(data:dict) -> bytes:
    if "id" not in data: return {"error": "id not found"}
    if str(data["id"]).startswith("GOOG"): return {"error": "id is from google"}
    if "format" not in data: ftype = "PDF"
    elif data["format"] not in ["AZW3", "EPUB", "HTML", "MOBI", "PDF"]: ftype = "PDF"
    else: ftype = data["format"]
    work = ao3Api.Api()
    return work.downloadWork(data["id"], ftype)

def getWork(data:dict) -> dict:
    if "id" not in data: return {"error": "id not found"}
    return query.Query().getBook(data["id"])

def search(data:dict) -> list:
    if "title" not in data: title = ""
    else: title = data["title"]
    if "author" not in data: author = ""
    else: author = data["author"]
    if "fandoms" not in data: fandoms = ""
    else: fandoms = data["fandoms"]
    if "language" not in data: language = ""
    else: language = data["language"]
    if "noSearchCache" not in data: noCache = False
    else: noCache = data["noSearchCache"]
    return query.Query().query(title=title, author=author, fandoms=fandoms, language=language, noCache=noCache)

if __name__ == "__main__":
    dotenv.load_dotenv()
    if os.getenv('USE_URL_IN') == "true": urlIn = True
    else: urlIn = False
    if os.getenv('AUTO_SAVE_QUERY') == "true":
        print("auto save query is enabled")
        db = database.Database()
        cache = db.query_book_cache({})
        print(f"cache size: {len(cache)}")

    app = Flask(__name__)

    @app.route("/download", methods=["GET"])
    def download():
        if urlIn:
            if "id" not in request.args: return {"error": "id not found"}
            return downloadAo3({"id": request.args["id"]})
        else:
            if not request.json: return {"error": "no json"}
            return downloadAo3(request.json)

    @app.route("/get", methods=["GET"])
    def get():
        if urlIn:
            if "id" not in request.args: return {"error": "id not found"}
            return getWork({"id": request.args["id"]})
        else:
            if not request.json: return {"error": "no json"}
            return getWork(request.json)

    @app.route("/search", methods=["GET"])
    def searchRoute():
        if urlIn:
            if "title" not in request.args: title = ""
            else: title = request.args["title"]
            if "author" not in request.args: author = ""
            else: author = request.args["author"]
            if "fandoms" not in request.args: fandoms = ""
            else: fandoms = request.args["fandoms"]
            if "language" not in request.args: language = ""
            else: language = request.args["language"]
            if "noSearchCache" not in request.args: noCache = False
            else: noCache = request.args["noSearchCache"]
            return search({"title": title, "author": author, "fandoms": fandoms, "language": language, "noSearchCache": noCache})
        else:
            if not request.json: return {"error": "no json"}
            return search(request.json)

    @app.route("/cache/size", methods=["GET"])
    def cacheSize():
        db = database.Database()
        cache = db.query_book_cache({})
        return {"size": len(cache)}

    @app.route("/cache/clear", methods=["DELETE"])
    def cacheClear():
        db = database.Database()
        db.query_book_cache_by_clear()
        return {"success": True}
        
    app.run(host="0.0.0.0", port=27018)