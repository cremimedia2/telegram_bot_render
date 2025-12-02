# bot.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request
import asyncio
import os

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)

# Telegram bot in webhook mode
application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running on Render!")

application.add_handler(CommandHandler("start", start))

# Webhook route
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"

# Optional health check
@app.route("/", methods=["GET"])
def index():
    return "Bot is alive!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
