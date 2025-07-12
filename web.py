from flask import Flask, send_file, render_template, abort from pymongo import MongoClient import os, time

app = Flask(name)

MONGO_URL = os.getenv("MONGO_URL") mongo = MongoClient(MONGO_URL) db = mongo["filetolink"] files = db["files"]

@app.route("/file/<file_id>") def serve_file(file_id): file_data = files.find_one({"file_id": file_id}) if not file_data: return abort(404)

path = f"temp/{file_id}_{file_data['file_name']}"
if os.path.exists(path):
    return send_file(path, as_attachment=True)
return abort(404)

@app.route("/watch/<file_id>") def stream_file(file_id): file_data = files.find_one({"file_id": file_id}) if not file_data: return abort(404)

path = f"temp/{file_id}_{file_data['file_name']}"
if os.path.exists(path):
    return render_template("watch.html", filename=file_data['file_name'], file_id=file_id)
return abort(404)

def cleanup_expired_files(): now = int(time.time()) expired = files.find({"timestamp": {"$lt": now - 36000}})  # 10 hours for file in expired: path = f"temp/{file['file_id']}_{file['file_name']}" if os.path.exists(path): os.remove(path) files.delete_one({"file_id": file['file_id']})

if name == "main": cleanup_expired_files() app.run(host="0.0.0.0", port=8080)

