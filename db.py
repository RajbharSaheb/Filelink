from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["file2link_bot"]
users_col = db["users"]

def add_user(user_id):
    if not users_col.find_one({"_id": user_id}):
        users_col.insert_one({"_id": user_id, "banned": False})

def is_banned(user_id):
    user = users_col.find_one({"_id": user_id})
    return user and user.get("banned", False)

def total_users():
    return users_col.count_documents({})

def banned_users():
    return users_col.count_documents({"banned": True})

def ban_user(user_id):
    users_col.update_one({"_id": user_id}, {"$set": {"banned": True}}, upsert=True)

def unban_user(user_id):
    users_col.update_one({"_id": user_id}, {"$set": {"banned": False}}, upsert=True)

def get_all_users():
    return [user["_id"] for user in users_col.find({})]
