from flask import Flask, send_file, render_template
import os

app = Flask(__name__)

@app.route("/<file_id>/<filename>")
def serve_file(file_id, filename):
    path = f"./downloads/{file_id}_{filename}"
    if not os.path.exists(path):
        return "File not found", 404
    return send_file(path)

@app.route("/watch/<file_id>/<filename>")
def stream_file(file_id, filename):
    path = f"./downloads/{file_id}_{filename}"
    if not os.path.exists(path):
        return "File not found", 404
    return render_template("watch.html", video_url=f"/{file_id}/{filename}")
