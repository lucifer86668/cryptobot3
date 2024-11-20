from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm working.")

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    await application.initialize()
    await application.start()
    print("Bot is running.")
    await application.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
