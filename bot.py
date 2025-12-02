# bot.py
import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get bot token from environment
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
PORT = int(os.environ.get("PORT", 5000))

# Create Flask app
app = Flask(__name__)

# Create Telegram bot application (webhook-only, no polling)
application = ApplicationBuilder().token(TOKEN).build()

# Example command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running on Render!")

application.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"

# Optional health check
@app.route("/", methods=["GET"])
def index():
    return "Bot is alive!"

# Only for local testing (not needed on Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
