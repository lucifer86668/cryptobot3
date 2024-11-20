from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm working.")

# Главная функция
async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # Запуск приложения
    await application.initialize()
    await application.start()
    print("Bot is running. Press Ctrl+C to stop.")

    # Поддержание работы бота
    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        print("Bot stopped manually.")
        await application.stop()
        await application.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
