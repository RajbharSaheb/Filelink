from flask import Flask, send_file, render_template, abort
import os, json, time
from threading import Thread

app = Flask(__name__, template_folder="templates")
FILE_DB = "files.json"
EXPIRY_SECONDS = 36000  # 10 hours

if not os.path.exists("temp"):
    os.makedirs("temp")

def load_file_info(file_id):
    with open(FILE_DB, "r") as f:
        data = json.load(f)
    return data.get(file_id)

@app.route("/file/<file_id>")
def download_file(file_id):
    info = load_file_info(file_id)
    if not info or not os.path.exists(info["path"]):
        return abort(404)
    return send_file(info["path"], download_name=info["filename"], as_attachment=True)

@app.route("/watch/<file_id>")
def stream_file(file_id):
    info = load_file_info(file_id)
    if not info or not os.path.exists(info["path"]):
        return abort(404)
    stream_url = f"/file/{file_id}"
    return render_template("video.html", filename=info["filename"], stream_url=stream_url)

def cleanup_old_files():
    while True:
        now = int(time.time())
        with open(FILE_DB, "r") as f:
            data = json.load(f)
        updated = {}
        for fid, info in data.items():
            if now - info["timestamp"] < EXPIRY_SECONDS:
                updated[fid] = info
            else:
                try:
                    os.remove(info["path"])
                except: pass
        with open(FILE_DB, "w") as f:
            json.dump(updated, f)
        time.sleep(3600)  # Clean every hour

Thread(target=cleanup_old_files, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
