from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
import os, uuid, time

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
MONGO_URL = os.getenv("MONGO_URL")

app = Client("filetolink", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URL)
db = mongo["filetolink"]
users = db["users"]
files = db["files"]

@app.on_message(filters.command("start"))
async def start(c, m):
    if not users.find_one({"_id": m.from_user.id}):
        users.insert_one({"_id": m.from_user.id})
    await m.reply_text("👋 फाइल भेजो, मैं तुम्हें डाउनलोड और स्ट्रीम लिंक दूँगा।")

@app.on_message(filters.document | filters.video | filters.audio)
async def handle_file(c, m: Message):
    media = m.document or m.video or m.audio
    if not os.path.exists("temp"):
        os.makedirs("temp")

    file_id = str(uuid.uuid4())[:8]
    file_path = await m.download(file_name=f"temp/{file_id}_{media.file_name}")

    files.insert_one({
        "file_id": file_id,
        "user_id": m.from_user.id,
        "file_name": media.file_name,
        "timestamp": int(time.time())
    })

    stream_link = f"{BASE_URL}/watch/{file_id}"
    direct_link = f"{BASE_URL}/file/{file_id}"

    await m.reply_text(
        f"✅ फाइल सेव हो गई।\n▶️ Stream: {stream_link}\n⬇️ Download: {direct_link}"
    )

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(c, m):
    if len(m.command) < 2:
        return await m.reply("📢 मैसेज दो: `/broadcast Hello`")

    text = m.text.split(" ", 1)[1]
    sent, failed = 0, 0

    for user in users.find():
        try:
            await c.send_message(user["_id"], text)
            sent += 1
        except:
            failed += 1
            users.delete_one({"_id": user["_id"]})

    await m.reply(f"📣 Broadcast Done\n✅ Sent: {sent}\n❌ Failed: {failed}")

app.run()
