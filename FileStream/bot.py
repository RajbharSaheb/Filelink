from pyrogram import Client
from FileStream.config import API_ID, API_HASH, BOT_TOKEN

app = Client("filestreambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def run_bot():
    from FileStream.handlers import upload_handler  # ensure handlers are loaded
    app.run()
