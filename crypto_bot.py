from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Токен вашего бота из BotFather
TELEGRAM_BOT_TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your simple bot. How can I assist you?")

# Обработчик текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"You said: {user_message}")

# Главная функция для запуска бота
async def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота
    await application.initialize()
    await application.start()
    print("Bot is running. Press Ctrl+C to stop.")
    await application.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
