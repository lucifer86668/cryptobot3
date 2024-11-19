import asyncio
import schedule
import time
from tvDatafeed import TvDatafeed, Interval
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Settings
TELEGRAM_BOT_TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'
CHAT_ID = '@QJyC8NbFDbhkYTk6'
USERNAME = ViktorMartuniyk  # Ваш логин от TradingView (None для анонимного входа)
PASSWORD = hgyhgj2512  # Ваш пароль от TradingView

# Initialize TradingView datafeed
tv = TvDatafeed(USERNAME, PASSWORD)

# Logging setup
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

logging.info("Bot starting...")

# Function to get top 20 crypto data from TradingView
def get_top_cryptos():
    cryptos = [
        "BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT",
        "SOLUSDT", "DOGEUSDT", "DOTUSDT", "MATICUSDT", "LTCUSDT",
        "SHIBUSDT", "TRXUSDT", "AVAXUSDT", "UNIUSDT", "ATOMUSDT",
        "ETCUSDT", "XMRUSDT", "XLMUSDT", "BCHUSDT", "APTUSDT"
    ]
    data = []
    for symbol in cryptos:
        try:
            # Fetch last price from TradingView
            bars = tv.get_hist(symbol, "BINANCE", Interval.in_daily, n_bars=1)
            if not bars.empty:
                last_price = bars['close'].iloc[-1]
                data.append((symbol, last_price))
        except Exception as e:
            logging.error(f"Error fetching data for {symbol}: {e}")
    return data

# Function to send updates to Telegram
async def send_crypto_update():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    crypto_data = get_top_cryptos()

    if crypto_data:
        message = "🌍 Top 20 Cryptocurrencies (TradingView):\n\n"
        for symbol, price in crypto_data:
            message += f"{symbol}: ${price:.2f}\n"
        await bot.send_message(chat_id=CHAT_ID, text=message)
        logging.info("Crypto update sent to channel.")
    else:
        await bot.send_message(chat_id=CHAT_ID, text="Failed to fetch cryptocurrency data.")
        logging.error("Failed to fetch cryptocurrency data.")

# Command handler for /sendtop20
async def handle_sendtop20(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Received /sendtop20 command.")
    crypto_data = get_top_cryptos()

    if crypto_data:
        message = "🌍 Top 20 Cryptocurrencies (TradingView):\n\n"
        for symbol, price in crypto_data:
            message += f"{symbol}: ${price:.2f}\n"
        await context.bot.send_message(chat_id=CHAT_ID, text=message)
        await update.message.reply_text("Update sent to the channel.")
    else:
        await update.message.reply_text("Failed to fetch cryptocurrency data.")
        logging.error("Failed to fetch cryptocurrency data.")

# Command handler for /start
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your Crypto Bot. Use /sendtop20 to get the top 20 cryptocurrencies!")

# Schedule the daily updates
def schedule_task():
    schedule.every().day.at("10:00").do(lambda: asyncio.run(send_crypto_update()))
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the bot with command handler
async def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(CommandHandler("sendtop20", handle_sendtop20))

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
