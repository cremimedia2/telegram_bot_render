import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Telegram Bot Token ===
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")  # set in Render Environment Variables

# === Webhook Path ===
WEBHOOK_PATH = "/webhook"

# === Initialize Flask app ===
app = Flask(__name__)

# === Initialize Telegram bot application ===
application = ApplicationBuilder().token(TOKEN).build()

# === Example command handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Hello! Bot is running via webhook on Render.")

application.add_handler(CommandHandler("start", start))

# === Flask route for Telegram webhook ===
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    """Receive updates from Telegram and push them to the bot."""
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "OK"

# === Main entry point ===
if __name__ == "__main__":
    # Render sets the port via environment variable
    PORT = int(os.environ.get("PORT", 5000))
    # Bind to all interfaces
    app.run(host="0.0.0.0", port=PORT)
