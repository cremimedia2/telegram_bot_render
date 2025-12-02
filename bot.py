# bot.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request
import asyncio
import os

# --- CONFIG ---
TOKEN = os.environ.get("BOT_TOKEN")  # Set your bot token as an environment variable on Render
WEBHOOK_PATH = "/webhook"
PORT = int(os.environ.get("PORT", 5000))

# --- FLASK APP ---
app = Flask(__name__)

# --- TELEGRAM APPLICATION (WEBHOOK MODE) ---
application = ApplicationBuilder().token(TOKEN).build()

# Example command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Hello! Bot is running on Render.")

application.add_handler(CommandHandler("start", start))

# --- FLASK ROUTE FOR WEBHOOK ---
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    """Handle incoming webhook POST from Telegram."""
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"

# --- OPTIONAL HEALTH CHECK ---
@app.route("/", methods=["GET"])
def index():
    return "Bot is alive!"

# --- RUN FLASK LOCALLY (for testing) ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
