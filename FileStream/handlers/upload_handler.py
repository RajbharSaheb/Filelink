from pyrogram import filters
from FileStream.bot import app
from FileStream.config import DOWNLOAD_DIR, FQDN
import os

@app.on_message(filters.document | filters.video | filters.audio)
async def upload_handler(client, message):
    media = message.document or message.video or message.audio
    file_path = await message.download(file_name=os.path.join(DOWNLOAD_DIR, media.file_name))
    file_link = f"{FQDN}/file/{media.file_name}"
    await message.reply_text(f"🔗 **Your link:** [Click to Download]({file_link})", disable_web_page_preview=True)
