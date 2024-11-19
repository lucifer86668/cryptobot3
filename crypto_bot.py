import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Telegram Bot Settings
TELEGRAM_BOT_TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'

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
    command = update.message.text.strip()[1:].upper()  # Remove the '/' and convert to uppercase
    ticker = command + "USDT"  # Binance format
    price = get_price_from_binance(ticker)
    if price != 'N/A':
        await update.message.reply_text(f"{command} - ${price:.2f}")
    else:
        await update.message.reply_text(f"Could not fetch the price for {command}.")

# Main function
async def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers for specific tickers
    application.add_handler(CommandHandler("btc", handle_crypto_price))
    application.add_handler(CommandHandler("eth", handle_crypto_price))
    application.add_handler(CommandHandler("sol", handle_crypto_price))
    application.add_handler(CommandHandler("dot", handle_crypto_price))
    application.add_handler(CommandHandler("ada", handle_crypto_price))
    application.add_handler(CommandHandler("ape", handle_crypto_price))
    application.add_handler(CommandHandler("apt", handle_crypto_price))
    application.add_handler(CommandHandler("atom", handle_crypto_price))

    # Initialize and start the application
    await application.initialize()
    await application.start()
    logging.info("Bot started. Waiting for commands...")

    # Keep the bot running
    try:
        while True:
            await asyncio.sleep(3600)  # Sleep indefinitely in 1-hour intervals
    except KeyboardInterrupt:
        logging.info("Bot stopped.")

    # Stop the application gracefully
    await application.stop()
    await application.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
