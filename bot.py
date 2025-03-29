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
        entry_points=[CommandHandler("register", register)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)],
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fio)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            PHOTO: [
                MessageHandler(filters.PHOTO | filters.Document.IMAGE, get_photo)
            ],
            SPHERE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sphere)],
            JOB: [MessageHandler(filters.TEXT, get_job)],
            TELEGRAM: [MessageHandler(filters.TEXT, get_telegram)],
            INSTAGRAM: [MessageHandler(filters.TEXT, get_instagram)],
            WEBSITE: [MessageHandler(filters.TEXT, get_website)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Start buyrug'i uchun conversation handler (til tanlash uchun)
    start_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)],
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fio)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            PHOTO: [
                MessageHandler(filters.PHOTO | filters.Document.IMAGE, get_photo)
            ],
            SPHERE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sphere)],
            JOB: [MessageHandler(filters.TEXT, get_job)],
            TELEGRAM: [MessageHandler(filters.TEXT, get_telegram)],
            INSTAGRAM: [MessageHandler(filters.TEXT, get_instagram)],
            WEBSITE: [MessageHandler(filters.TEXT, get_website)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Handler(qayta ishlovchi)larni qo'shish
    application.add_handler(start_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(registration_handler)

    # Botni ishga tushirish
    application.run_polling()
    
    logger.info("Bot ishga tushirildi!")

if __name__ == '__main__':
    main()