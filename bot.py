from pyrogram import Client, filters
from pyrogram.types import Message
import os, uuid, time, json
from pymongo import MongoClient

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080")
OWNER_ID = int(os.environ.get("OWNER_ID"))

# MongoDB setup
MONGO_URL = os.environ.get("MONGO_URL")
mongo = MongoClient(MONGO_URL)
db = mongo["filetolink"]
users_col = db["users"]

app = Client("filetolink-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

FILE_DB = "files.json"
if not os.path.exists(FILE_DB):
    with open(FILE_DB, "w") as f:
        json.dump({}, f)

def save_file_info(file_id, file_info):
    with open(FILE_DB, "r") as f:
        data = json.load(f)
    data[file_id] = file_info
    with open(FILE_DB, "w") as f:
        json.dump(data, f)

@app.on_message(filters.command("start"))
async def start(c, m):
    user_id = m.from_user.id
    if not users_col.find_one({"_id": user_id}):
        users_col.insert_one({"_id": user_id})
    await m.reply_text("👋 मुझे कोई फाइल भेजो और मैं तुम्हें उसका लिंक दे दूँगा — Stream + Download")

@app.on_message(filters.document | filters.video | filters.audio)
async def handle_file(c: Client, m: Message):
    file = m.document or m.video or m.audio
    file_id = str(uuid.uuid4())[:8]
    timestamp = int(time.time())
    if not os.path.exists("temp"):
        os.makedirs("temp")
    file_path = await c.download_media(file, file_name=f"temp/{file_id}_{file.file_name}")

    save_file_info(file_id, {
        "path": file_path,
        "filename": file.file_name,
        "timestamp": timestamp
    })

    stream_link = f"{BASE_URL}/watch/{file_id}"
    direct_link = f"{BASE_URL}/file/{file_id}"
    await m.reply_text(f"✅ File Saved\n▶️ Stream: {stream_link}\n⬇️ Download: {direct_link}")

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(c, m):
    if len(m.command) < 2:
        return await m.reply("ℹ️ Broadcast text दो:\n`/broadcast Hello all!`")

    text = m.text.split(" ", 1)[1]
    users = users_col.find()
    sent, fail = 0, 0

    for user in users:
        try:
            await c.send_message(user["_id"], text)
            sent += 1
        except:
            fail += 1
            users_col.delete_one({"_id": user["_id"]})  # Auto cleanup

    await m.reply(f"📢 Broadcast Complete\n✅ Sent: {sent}\n❌ Failed: {fail}")

app.run()
