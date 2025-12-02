# bot.py
import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ======== Config ========
TOKEN = os.environ.get("BOT_TOKEN")  # Set in Render environment variables
WEBHOOK_PATH = "/webhook"  # Must match the webhook URL path
PORT = int(os.environ.get("PORT", 5000))  # Render provides this automatically

# ======== Flask app ========
app = Flask(__name__)

# ======== Telegram bot (webhook-only) ========
application = ApplicationBuilder().token(TOKEN).build()

# Example command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running on Render!")

application.add_handler(CommandHandler("start", start))

# ======== Webhook route ========
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"

# ======== Health check route ========
@app.route("/", methods=["GET"])
def index():
    return "Bot is alive!"

# ======== Local testing ========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
