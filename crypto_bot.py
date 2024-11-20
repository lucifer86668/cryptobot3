from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import requests

TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'
BINANCE_API_URL = 'https://api.binance.com/api/v3/ticker/price'

# Функция для получения цены криптовалюты
def get_price_from_binance(symbol: str):
    try:
        response = requests.get(BINANCE_API_URL, params={'symbol': symbol})
        response.raise_for_status()
        data = response.json()
        return float(data['price'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Обработчик команд в канале
async def handle_channel_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.strip()[1:].split('@')[0].upper()  # Извлекаем команду
    ticker = f"{command}USDT"  # Преобразуем в формат Binance API
    price = get_price_from_binance(ticker)

    if price is not None:
        await update.message.reply_text(f"💰 {command} - ${price:.2f}")
    else:
        await update.message.reply_text(f"❌ Could not fetch the price for {command}. Please check the ticker.")

# Главная функция
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL & filters.COMMAND, handle_channel_commands))
    application.run_polling()

if __name__ == "__main__":
    main()
