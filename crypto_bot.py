import requests
import schedule
import time
import asyncio
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Settings
TELEGRAM_BOT_TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'
CHAT_ID = '@QJyC8NbFDbhkYTk6'
#CRYPTO_API_URL = 'https://api.coingecko.com/api/v3/coins/markets'
#BTC_DOMINANCE_URL = 'https://api.coingecko.com/api/v3/global'
PARAMS = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 20,
    'page': 1,
}

# Logging setup
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

logging.info("Bot starting...")

# Function to get crypto data
#def get_crypto_data():
#    response = requests.get(CRYPTO_API_URL, params=PARAMS)
 #   if response.status_code == 200:
  #      return response.json()
   # return []

# Function to get Bitcoin dominance
#def get_btc_dominance():
#    response = requests.get(BTC_DOMINANCE_URL)
#    if response.status_code == 200:
#        return response.json()['data']['market_cap_percentage']['btc']
#    return None

# Function to send updates to Telegram
#async def send_crypto_update():
#    bot = Bot(token=TELEGRAM_BOT_TOKEN)
#    crypto_data = get_crypto_data()
#    btc_dominance = get_btc_dominance()

#    if crypto_data and btc_dominance is not None:
#        message = f"🌍 Bitcoin Dominance: {btc_dominance:.2f}%\n\nTop 20 Cryptocurrencies:\n"
#        for coin in crypto_data:
#            message += f"{coin['symbol'].upper()} ({coin['name']}): ${coin['current_price']:.2f}\n"
#        await bot.send_message(chat_id=CHAT_ID, text=message)
#        logging.info("Crypto update sent to channel.")
#    else:
#        await bot.send_message(chat_id=CHAT_ID, text="Failed to fetch cryptocurrency data.")
#        logging.error("Failed to fetch cryptocurrency data.")

# Command handler for /sendtop20
#async def handle_sendtop20(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    logging.info("Received /sendtop20 command.")
#    crypto_data = get_crypto_data()
#    btc_dominance = get_btc_dominance()
#
#    if crypto_data and btc_dominance is not None:
#        message = f"🌍 Bitcoin Dominance: {btc_dominance:.2f}%\n\nTop 20 Cryptocurrencies:\n"
#        for coin in crypto_data:
#            message += f"{coin['symbol'].upper()} ({coin['name']}): ${coin['current_price']:.2f}\n"
#        await context.bot.send_message(chat_id=CHAT_ID, text=message)
#        await update.message.reply_text("Update sent to the channel.")
#    else:
#        await update.message.reply_text("Failed to fetch cryptocurrency data.")
#        logging.error("Failed to fetch cryptocurrency data.")
#
# Command handler for /start
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your Crypto Bot. Use /sendtop20 to get the top 20 cryptocurrencies!")


# Schedule the daily updates
#def schedule_task():
#    schedule.every().day.at("10:00").do(lambda: asyncio.run(send_crypto_update()))
#    while True:
#        schedule.run_pending()
#        time.sleep(1)

# Start the bot with command handler
async def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", handle_start))
 #   application.add_handler(CommandHandler("sendtop20", handle_sendtop20))

    # Initialize and start the application
    await application.initialize()
    await application.start()
    logging.info("Bot started. Waiting for commands...")

    # Run the scheduler in the main loop
#    try:
#        handle_start_test()
#   finally:
        await application.stop()
        await application.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
