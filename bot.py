import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN
from handlers import (
    start,
    help_command,
    register,
    cancel,
    set_language,
    get_fio,
    get_phone,
    get_photo,
    get_sphere,
    get_job,
    get_telegram,
    get_instagram,
    get_website,
    LANGUAGE, FIO, PHONE, PHOTO, SPHERE, JOB, TELEGRAM, INSTAGRAM, WEBSITE
)

# Logging ni sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Botni ishga tushirish funksiyasi"""
    # Bot applicationini yaratish
    application = Application.builder().token(BOT_TOKEN).build()

    # Ro'yxatdan o'tish uchun conversation handler
    registration_handler = ConversationHandler(
        entry_points=[
            CommandHandler("register", register),
            CommandHandler("start", start),
            MessageHandler(filters.TEXT & ~filters.COMMAND, start)  # Har qanday matn uchun start funksiyasi
        ],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)],
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fio)],
            PHONE: [
                MessageHandler(filters.CONTACT, get_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone),
            ],
            PHOTO: [
                MessageHandler(filters.PHOTO | filters.Document.MIME_TYPE("image/jpeg") | filters.Document.MIME_TYPE("image/png"), get_photo)
            ],
            SPHERE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sphere)],
            JOB: [MessageHandler(filters.TEXT, get_job)],
            TELEGRAM: [MessageHandler(filters.TEXT, get_telegram)],
            INSTAGRAM: [MessageHandler(filters.TEXT, get_instagram)],
            WEBSITE: [MessageHandler(filters.TEXT, get_website)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Asosiy conversation handler - /start siz ham ishlashi uchun
    main_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, start)

    # Handler(qayta ishlovchi)larni qo'shish
    application.add_handler(registration_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(main_handler)  # Agar hech qanday commandga mos kelmasa

    # Botni ishga tushirish
    application.run_polling()
    
    logger.info("Bot ishga tushirildi!")

if __name__ == '__main__':
    main()