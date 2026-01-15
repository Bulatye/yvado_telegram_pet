from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import config
import downloader
import os

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик сообщений"""
    text = update.message.text.strip()
    
    # Проверяем, что это YouTube ссылка
    if not "youtube.com" in text and not "youtu.be" in text:
        await update.message.reply_text("peep, peep, send the YouTube link >_<")
        return
    
    try:
        # Скачиваем
        audio_path = downloader.download_audio(text)
        
        # Отправляем файл
        with open(audio_path, 'rb') as f:
            await update.message.reply_audio(audio=f)
        
        # Удаляем временные файлы
        temp_dir = os.path.dirname(audio_path)
        os.remove(audio_path)
        os.rmdir(temp_dir)
        await update.message.delete()
    except Exception as e:
        await update.message.reply_text(f"{str(e)[:100]}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    await update.message.reply_text("peep, peep, send the YouTube link >_<")

def main():
    """Запуск бота"""
    app = Application.builder().token(config.TOKEN).build()
    app.add_handler(MessageHandler(filters.Command("start"), start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
