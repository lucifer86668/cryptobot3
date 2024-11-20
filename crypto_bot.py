import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Telegram Bot Token
TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'

# Binance API URL
BINANCE_API_URL = 'https://api.binance.com/api/v3/ticker/price'

# Функция для получения цены из Binance API
def get_price_from_binance(symbol: str):
    try:
        response = requests.get(BINANCE_API_URL, params={'symbol': symbol})
        response.raise_for_status()
        data = response.json()
        return float(data['price'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Обработчик команды для получения цены
async def handle_crypto_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем команду без символа '/'
    command = update.message.text.strip()[1:].upper()  # Пример: '/btc' -> 'BTC'
    ticker = f"{command}USDT"  # Формируем тикер для Binance (например, BTCUSDT)

from telegram.ext import MessageHandler, filters

# Фильтр для команд в канале
async def handle_channel_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.strip()[1:].split('@')[0].upper()  # Извлекаем команду без '@'
    ticker = f"{command}USDT"
    price = get_price_from_binance(ticker)

    if price is not None:
        await update.message.reply_text(f"💰 {command} - ${price:.2f}")
    else:
        await update.message.reply_text(f"❌ Could not fetch the price for {command}. Please check the ticker.")

# Добавляем обработчик
application.add_handler(MessageHandler(filters.ChatType.CHANNEL & filters.COMMAND, handle_channel_commands))
    
    # Запрашиваем цену
    price = get_price_from_binance(ticker)

    if price is not None:
        await update.message.reply_text(f"💰 {command} - ${price:.2f}")
    else:
        await update.message.reply_text(f"❌ Could not fetch the price for {command}. Please check the ticker.")

# Главная функция
def main():
    # Создаём приложение Telegram
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики для криптовалют
    application.add_handler(CommandHandler("btc", handle_crypto_price))  # Для Bitcoin
    application.add_handler(CommandHandler("eth", handle_crypto_price))  # Для Ethereum
    application.add_handler(CommandHandler("sol", handle_crypto_price))  # Для Solana
    application.add_handler(CommandHandler("dot", handle_crypto_price))  # Для Polkadot
    application.add_handler(CommandHandler("ada", handle_crypto_price))  # Для Cardano
    application.add_handler(CommandHandler("ape", handle_crypto_price))  # Для ApeCoin
    application.add_handler(CommandHandler("apt", handle_crypto_price))  # Для Aptos
    application.add_handler(CommandHandler("atom", handle_crypto_price))  # Для Cosmos

    # Запускаем приложение
    application.run_polling()

if __name__ == '__main__':
    main()
