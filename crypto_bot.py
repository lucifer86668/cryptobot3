import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'

# Binance API URL
BINANCE_API_URL = 'https://api.binance.com/api/v3/ticker/price'

# Function to get the price of a cryptocurrency from Binance
def get_price_from_binance(symbol):
    try:
        response = requests.get(BINANCE_API_URL, params={'symbol': symbol})
        response.raise_for_status()
        data = response.json()
        return float(data['price'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Command handler for getting cryptocurrency price
async def handle_crypto_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.strip()[1:].upper()  # Remove "/" and convert to uppercase
    ticker = f"{command}USDT"  # Format the ticker for Binance (e.g., BTCUSDT)
    price = get_price_from_binance(ticker)

    if price is not None:
        await update.message.reply_text(f"💰 {command} - ${price:.2f}")
    else:
        await update.message.reply_text(f"❌ Could not fetch the price for {command}. Please check the ticker.")

# Main function to start the bot
async def main():
    # Create the bot application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers for specific cryptocurrencies
    application.add_handler(CommandHandler("btc", handle_crypto_price))
    application.add_handler(CommandHandler("eth", handle_crypto_price))
    application.add_handler(CommandHandler("sol", handle_crypto_price))
    application.add_handler(CommandHandler("dot", handle_crypto_price))
    application.add_handler(CommandHandler("ada", handle_crypto_price))
    application.add_handler(CommandHandler("ape", handle_crypto_price))
    application.add_handler(CommandHandler("apt", handle_crypto_price))
    application.add_handler(CommandHandler("atom", handle_crypto_price))

    # Start the bot
    await application.initialize()
    await application.start()
    print("Bot is running. Press Ctrl+C to stop.")

    # Keep the bot running
    try:
        while True:
            await asyncio.sleep(3600)  # Keep the bot alive indefinitely
    except KeyboardInterrupt:
        print("Bot stopped manually.")
        await application.stop()
        await application.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
