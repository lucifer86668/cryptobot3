import requests
import asyncio
import schedule
import time
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Telegram Bot Settings
TELEGRAM_BOT_TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'
CHAT_ID = '@QJyC8NbFDbhkYTk6'

# Binance API URL
BINANCE_API_URL = 'https://api.binance.com/api/v3/ticker/price'

# Logging setup
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

logging.info("Bot starting...")

# Function to get the price of a cryptocurrency from Binance
def get_price_from_binance(symbol):
    try:
        response = requests.get(BINANCE_API_URL, params={'symbol': symbol})
        if response.status_code == 200:
            data = response.json()
            return float(data['price'])
        else:
            logging.error(f"Error fetching data for {symbol}: {response.status_code}")
            return 'N/A'
    except Exception as e:
        logging.error(f"Exception fetching price for {symbol}: {e}")
        return 'N/A'

# Function to handle commands with cryptocurrency tickers
async def handle_crypto_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()
    ticker = message[1:].upper() + "USDT"  # Append USDT for Binance
    price = get_price_from_binance(ticker)
    if price != 'N/A':
        await update.message.reply_text(f"{ticker[:-4]} - ${price:.2f}")
    else:
        await update.message.reply_text(f"Could not fetch the price for {ticker[:-4]}.")

# Function to send morning update with predefined cryptocurrencies
async def send_morning_update():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    cryptos = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'DOTUSDT', 'ADAUSDT', 'APEUSDT', 'APTUSDT', 'ATOMUSDT']
    message = "🌅 Morning Update:\n\n"
    for crypto in cryptos:
        price = get_price_from_binance(crypto)
        if price != 'N/A':
            message += f"{crypto[:-4]} - ${price:.2f}\n"
    await bot.send_message(chat_id=CHAT_ID, text=message)
    logging.info("Morning update sent.")

# Schedule the morning update
def schedule_task():
    schedule.every().day.at("10:00").do(lambda: asyncio.run(send_morning_update()))
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the bot with command handler
async def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handler for any slash command (e.g., /btc, /eth)
    application.add_handler(CommandHandler(None, handle_crypto_price))

    # Initialize and start the application
    await application.initialize()
    await application.start()
    logging.info("Bot started. Waiting for commands...")

    # Run the scheduler in the main loop
    try:
        schedule_task()
    finally:
        await application.stop()
        await application.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
