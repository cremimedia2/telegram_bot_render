from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from flask import Flask, request

# Your bot token from @BotFather
TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)

# Command handler
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Bot is running on Render.")

dispatcher.add_handler(CommandHandler("start", start))

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    dispatcher.process_update(Update.de_json(request.get_json(force=True), bot))
    return "ok"

# Optional local test
if __name__ == "__main__":
    app.run(port=5000)
