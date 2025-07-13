from pyrogram import Client, filters
from dotenv import load_dotenv
import os

load_dotenv()

api_id = int(os.getenv("API_ID"))      # int hona chahiye
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.document | filters.video | filters.audio)
async def save_file(client, message):
    media = message.document or message.video or message.audio
    file_id = str(message.id)
    file_name = media.file_name or f"{file_id}.bin"
    save_path = f"./downloads/{file_id}_{file_name}"

    await message.download(file_name=save_path)

    base_url = "https://yourapp.koyeb.app"  # ← yaha apna domain dalna
    download_url = f"{base_url}/{file_id}/{file_name}"
    watch_url = f"{base_url}/watch/{file_id}/{file_name}"

    await message.reply_text(
        f"📥 [Download Link]({download_url})\n▶️ [Watch Online]({watch_url})",
        disable_web_page_preview=True
    )

app.run()
