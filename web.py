from flask import Flask, send_file, render_template
import os, time, json, threading

app = Flask(__name__)
FILE_DB = "files.json"
EXPIRY_SECONDS = 36000  # 10 hours
TEMP_DIR = "temp"

def cleanup_old_files():
    while True:
        if os.path.exists(FILE_DB):
            with open(FILE_DB, "r") as f:
                data = json.load(f)
            to_delete = []
            for file_id, info in data.items():
                if time.time() - info["timestamp"] > EXPIRY_SECONDS:
                    try:
                        os.remove(info["path"])
                    except:
                        pass
                    to_delete.append(file_id)
            for file_id in to_delete:
                del data[file_id]
            with open(FILE_DB, "w") as f:
                json.dump(data, f)
        time.sleep(600)

@app.route('/watch/<file_id>')
def stream(file_id):
    if not os.path.exists(FILE_DB):
        return "File DB not found", 404
    with open(FILE_DB, "r") as f:
        data = json.load(f)
    if file_id not in data:
        return "File not found", 404
    return render_template("watch.html", filename=data[file_id]["filename"], file_id=file_id)

@app.route('/file/<file_id>')
def download(file_id):
    if not os.path.exists(FILE_DB):
        return "File DB not found", 404
    with open(FILE_DB, "r") as f:
        data = json.load(f)
    if file_id not in data or not os.path.exists(data[file_id]["path"]):
        return "File not found", 404
    return send_file(data[file_id]["path"], as_attachment=True)

if __name__ == "__main__":
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    threading.Thread(target=cleanup_old_files, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
