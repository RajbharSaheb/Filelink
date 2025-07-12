import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, CallbackQueryHandler
)

from db import add_user, is_banned, total_users, banned_users, ban_user, unban_user, get_all_users

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
CHANNEL_LINK = os.getenv("CHANNEL_LINK")
DOMAIN = os.getenv("DOMAIN")

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id)
    if is_banned(user.id):
        return
    await update.message.reply_text(
        START_TEXT.format(name=user.first_name.upper()),
        reply_markup=InlineKeyboardMarkup(START_BUTTONS)
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ Just send a file to get instant streaming & download links.")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    if len(context.args) == 0:
        await update.message.reply_text("Use: /broadcast Your message here")
        return
    count = 0
    message = " ".join(context.args)
    for user_id in get_all_users():
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            count += 1
        except:
            continue
    await update.message.reply_text(f"✅ Broadcast sent to {count} users.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        await update.message.reply_text(f"👥 Users: {total_users()}\n⛔ Banned: {banned_users()}")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        try:
            uid = int(context.args[0])
            ban_user(uid)
            await update.message.reply_text(f"⛔ User {uid} banned.")
        except:
            await update.message.reply_text("Use: /ban <user_id>")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        try:
            uid = int(context.args[0])
            unban_user(uid)
            await update.message.reply_text(f"✅ User {uid} unbanned.")
        except:
            await update.message.reply_text("Use: /unban <user_id>")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id)
    if is_banned(user.id):
        return
    media = update.message.document or update.message.video or update.message.audio
    if not media and update.message.photo:
        media = update.message.photo[-1]
    if not media:
        await update.message.reply_text("❌ Unsupported media type.")
        return
    file_id = media.file_id
    link = f"{DOMAIN}/d/{file_id}"
    await update.message.reply_text(
        f"✅ Link Ready!\n\n📥 [Download / Watch]({link})",
        disable_web_page_preview=True
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "help":
        await query.edit_message_text("Send any file to get links.\n\nUse in groups: /link reply to file")
    elif query.data == "about":
        await query.edit_message_text("🤖 Created by Thunder Dev.\nFast, Secure & Private")
    elif query.data == "close":
        await query.delete_message()

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

    print("🤖 Bot Running...")
    app.run_polling()
