import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Токен вашего бота из BotFather
TELEGRAM_BOT_TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received /start command from {update.effective_user.first_name}")
    await update.message.reply_text("Hello! I'm your simple bot. How can I assist you?")

# Обработчик текстовых сообщений (Эхо-бот)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logging.info(f"Received message: {user_message} from {update.effective_user.first_name}")
    await update.message.reply_text(f"You said: {user_message}")

# Главная функция для запуска бота
async def main():
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))  # Команда /start
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))  # Обработчик текстовых сообщений

    # Инициализация и запуск бота
    logging.info("Starting bot...")
    await application.initialize()
    await application.start()
    logging.info("Bot is running. Press Ctrl+C to stop.")
    await application.idle()  # Ожидание завершения

if __name__ == "__main__":
    asyncio.run(main())
