from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request
import asyncio

TOKEN = "YOUR_BOT_TOKEN"
WEBHOOK_PATH = "/webhook"

app = Flask(__name__)

# Create Application (without polling)
application = ApplicationBuilder().token(TOKEN).build()

# Command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Bot is running on Render.")

application.add_handler(CommandHandler("start", start))

# Flask route to process webhook
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"
