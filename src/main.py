import query, ao3Api, database
from flask import Flask, request

def downloadAo3(data:dict) -> bytes:
    if "id" not in data: return {"error": "id not found"}
    if str(data["id"]).startswith("GOOG"): return {"error": "id is from google"}
    if "format" not in data: ftype = "HTML"
    elif str(data["format"]).upper() not in ["AZW3", "EPUB", "HTML", "MOBI", "PDF"]: ftype = "HTML"
    else: ftype = str(data["format"]).upper()
    try: return ao3Api.Api().downloadWork(str(data["id"]), ftype)
    except Exception as e: return {"error": str(e.with_traceback())}

def getWork(data:dict) -> dict:
    if "id" not in data: return {"error": "id not found"}
    try: return query.Query().getBook(str(data["id"]))
    except Exception as e: return {"error": str(e.with_traceback())}

def search(data:dict) -> list:
    try: 
        return query.Query().query(
        title=data.get("title", ""), 
        author=data.get("author", ""), 
        fandoms=data.get("fandoms", ""), 
        language=data.get("language", ""), 
        dontSearchCache=data.get("dontSearchCache", False), 
        dontSaveCache=data.get("dontSaveCache", False)
        )
    except Exception as e: 
        return {"error": str(e.with_traceback())}

if __name__ == "__main__":
    app = Flask(__name__)

    @app.route("/download", methods=["GET"])
    def download():
        if len(request.args) > 0: return downloadAo3(request.args)
        elif request.headers.get("Content-Type", "") == "application/json": return downloadAo3(request.json)
        elif len(request.form) > 0: return downloadAo3(request.form)
        else: return {"error": "no data"}

    @app.route("/get", methods=["GET"])
    def get():
        if len(request.args) > 0: return getWork(request.args)
        elif request.headers.get("Content-Type", "") == "application/json": return getWork(request.json)
        elif len(request.form) > 0: return getWork(request.form)
        else: return {"error": "no data"}

    @app.route("/search", methods=["GET"])
    def searchRoute():
        if len(request.args) > 0: return search(request.args)
        elif request.headers.get("Content-Type", "") == "application/json": return search(request.json)
        elif len(request.form) > 0: return search(request.form)
        else: return {"error": "no data"}
           
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