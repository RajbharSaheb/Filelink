from pyrogram import Client, filters
from dotenv import load_dotenv
import os
import urllib.parse

# Load .env
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DOMAIN = os.getenv("DOMAIN")

bot = Client("media_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def handle_media(client, message):
    media = message.document or message.video or message.audio
    file_id = media.file_id
    file_name = media.file_name or "file"

    # Encode file name for URL
    safe_name = urllib.parse.quote(file_name)
    message_id = message.id

    # Custom link like: https://yourdomain.com/12345/CapCut+Pro.apk?hash=AgAD...
    custom_link = f"{DOMAIN}/{message_id}/{safe_name}?hash={file_id}"

    await message.reply_text(
        f"🔗 **Your Link is Ready:**\n"
        f"[📥 Download or ▶️ Watch Here]({custom_link})",
        disable_web_page_preview=True
    )

bot.run()
