import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler, filters,
                          ContextTypes, CallbackQueryHandler)

from db import add_user, is_banned, total_users, banned_users, ban_user, unban_user, get_all_users

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
CHANNEL_LINK = os.getenv("CHANNEL_LINK")
BASE_URL = os.getenv("BASE_URL")

START_TEXT = """
🌟 Welcome, {name}! 🌟

I'm Thunder File to Link Bot ⚡
I generate direct download and streaming links for your files.

How to use:
1. Send any file to me for private links.
2. In groups, reply to a file with /link.

» Use /help for all commands and detailed information.

🚀 Send a file to begin!
"""

START_BUTTONS = [
    [InlineKeyboardButton("📖 Get Help", callback_data="help"),
     InlineKeyboardButton("ℹ️ About Bot", callback_data="about")],
    [InlineKeyboardButton("🛠 GitHub", url="https://github.com/yourrepo"),
     InlineKeyboardButton("❌ Close", callback_data="close")],
    [InlineKeyboardButton("📣 Join MOVIES ISLAND", url=CHANNEL_LINK)]
]

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id)
    if is_banned(user.id):
        return
    await update.message.reply_text(
        START_TEXT.format(name=user.first_name.upper()),
        reply_markup=InlineKeyboardMarkup(START_BUTTONS)
    )

# /help command
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start and send a file to get started.")

# /broadcast (admin only)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    text = update.message.text.split(' ', 1)
    if len(text) < 2:
        await update.message.reply_text("Use: /broadcast your message")
        return
    count = 0
    for user_id in get_all_users():
        try:
            await context.bot.send_message(chat_id=user_id, text=text[1])
            count += 1
        except:
            pass
    await update.message.reply_text(f"Broadcast sent to {count} users.")

# /stats (admin only)
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    await update.message.reply_text(f"👥 Users: {total_users()}\n⛔ Banned: {banned_users()}")

# /ban <user_id>
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    try:
        uid = int(context.args[0])
        ban_user(uid)
        await update.message.reply_text(f"User {uid} banned.")
    except:
        await update.message.reply_text("Use: /ban <user_id>")

# /unban <user_id>
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    try:
        uid = int(context.args[0])
        unban_user(uid)
        await update.message.reply_text(f"User {uid} unbanned.")
    except:
        await update.message.reply_text("Use: /unban <user_id>")

# When user sends a file
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id)
    if is_banned(user.id):
        return
    media = update.message.document or update.message.video or update.message.audio or update.message.photo[-1]
    if not media:
        await update.message.reply_text("❌ Unsupported media.")
        return
    file_id = media.file_id
    secure_url = f"{BASE_URL}/d/{file_id}"
    await update.message.reply_text(
        f"✅ Link Ready\n\n📥 [Download / Watch]({secure_url})",
        disable_web_page_preview=True
    )

# Inline button callback handler
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "help":
        await query.edit_message_text("This bot helps you get direct links. Just send a file.")
    elif query.data == "about":
        await query.edit_message_text("Created by Thunder Dev. Secure and Fast.")
    elif query.data == "close":
        await query.delete_message()

# Main runner
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.ALL & (filters.Document.ALL | filters.Video.ALL | filters.Audio.ALL | filters.PHOTO), handle_file))
    print("🤖 Bot running...")
    app.run_polling()
