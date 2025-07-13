from flask import Flask, request, render_template
from pyrogram import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

# Pyrogram client
bot = Client("stream_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.route("/<int:msg_id>/<filename>")
def serve_file(msg_id, filename):
    file_id = request.args.get("hash")
    if not file_id:
        return "❌ Invalid or missing file_id", 400

    # Get Telegram CDN link
    async def get_link():
        async with bot:
            file = await bot.get_file(file_id)
            return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

    tg_url = bot.loop.run_until_complete(get_link())

    # Render template with video
    return render_template("watch.html", tg_cdn_url=tg_url)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
