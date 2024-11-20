from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm working.")

# Главная функция для запуска бота
async def main():
    # Создаём приложение Telegram
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    await application.initialize()
    await application.start()
    print("Bot is running. Press Ctrl+C to stop.")

    # Поддержание работы бота через бесконечный асинхронный цикл
    try:
        while True:
            await asyncio.sleep(3600)  # Проверка раз в час
    except KeyboardInterrupt:
        print("Bot stopped manually.")

    # Корректное завершение работы бота
    await application.stop()
    await application.shutdown()

from telegram.ext import MessageHandler, filters

# Логирование всех входящих сообщений
async def log_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Received update: {update.to_dict()}")

# Добавьте обработчик в main():
application.add_handler(MessageHandler(filters.ALL, log_update))

if __name__ == "__main__":
    asyncio.run(main())
