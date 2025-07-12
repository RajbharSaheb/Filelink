from flask import Flask, redirect
import os

app = Flask(__name__)
BASE_URL = "https://api.telegram.org/file/bot"
BOT_TOKEN = os.getenv("BOT_TOKEN")

@app.route("/d/<file_id>")
def get_file(file_id):
    if not BOT_TOKEN:
        return "Token not set", 500
    return redirect(f"{BASE_URL}{BOT_TOKEN}/{file_id}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
