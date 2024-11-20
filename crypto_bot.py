import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Telegram Bot Token (полученный от BotFather)
TELEGRAM_BOT_TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'

# Binance API URL для получения цены
BINANCE_API_URL = 'https://api.binance.com/api/v3/ticker/price'

# Функция для получения цены из Binance API
def get_price_from_binance(symbol):
    try:
        response = requests.get(BINANCE_API_URL, params={'symbol': symbol})
        response.raise_for_status()
        data = response.json()
        return float(data['price'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Обработчик команд (например, /btc)
async def handle_crypto_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.strip()[1:].upper()  # Убираем "/" и преобразуем в верхний регистр
    ticker = f"{command}USDT"  # Формат тикера для Binance (например, BTCUSDT)
    price = get_price_from_binance(ticker)

    if price is not None:
        await update.message.reply_text(f"💰 {command} - ${price:.2f}")
    else:
        await update.message.reply_text(f"❌ Could not fetch the price for {command}. Please check the ticker.")

# Главная функция для запуска бота
async def main():
    # Создаем приложение Telegram
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрируем обработчик команд
    application.add_handler(CommandHandler("btc", handle_crypto_price))  # Для BTC
    application.add_handler(CommandHandler("eth", handle_crypto_price))  # Для ETH
    application.add_handler(CommandHandler("sol", handle_crypto_price))  # Для SOL
    application.add_handler(CommandHandler("dot", handle_crypto_price))  # Для DOT
    application.add_handler(CommandHandler("ada", handle_crypto_price))  # Для ADA
    application.add_handler(CommandHandler("ape", handle_crypto_price))  # Для APE
    application.add_handler(CommandHandler("apt", handle_crypto_price))  # Для APT
    application.add_handler(CommandHandler("atom", handle_crypto_price))  # Для ATOM

    # Запускаем бота
    await application.initialize()
    await application.start()
    print("Bot is running. Press Ctrl+C to stop.")
    await application.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
