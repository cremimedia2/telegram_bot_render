from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request

TOKEN = "YOUR_BOT_TOKEN"
WEBHOOK_PATH = "/webhook"

app = Flask(__name__)

# Create the Telegram application
application = ApplicationBuilder().token(TOKEN).build()

# Define your command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Bot is running on Render.")

# Add command handler
application.add_handler(CommandHandler("start", start))

# Flask route to handle Telegram webhook
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    """Process incoming webhook from Telegram."""
    update = Update.de_json(request.get_json(force=True), application.bot)
    # Process update asynchronously
    import asyncio
    asyncio.run(application.process_update(update))
    return "ok"
