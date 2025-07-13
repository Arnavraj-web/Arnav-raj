from telegram.ext import Updater, CommandHandler
from price_tracker import add_product, check_prices
from scheduler import start_scheduler

BOT_TOKEN = '7087738263:AAGZCK-AOLB8qF2-ua-Bd070TSV2aj14PMs'  # Replace with your actual bot token

def start(update, context):
    update.message.reply_text("👋 Welcome to the 24x7 Price Tracker Bot!\nUse /track <product link> to track Amazon, Flipkart, or Meesho products.")

def track(update, context):
    if len(context.args) == 0:
        update.message.reply_text("❌ Please send a product URL.")
        return
    url = context.args[0]
    user_id = update.effective_user.id
    success, message = add_product(user_id, url)
    update.message.reply_text(message)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('track', track))

    start_scheduler(updater.bot)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
