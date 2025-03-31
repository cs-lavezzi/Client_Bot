import json
import logging
import os
import base64
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler

# Handlerlarni import qilish
from handlers import (
    start, help_command, register, cancel, set_language, 
    get_fio, get_phone, get_photo, get_sphere, get_job, 
    get_telegram, get_instagram, get_website,
    LANGUAGE, FIO, PHONE, PHOTO, SPHERE, JOB, TELEGRAM, INSTAGRAM, WEBSITE
)

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram bot va dispatcher yaratish
TOKEN = os.environ.get('BOT_TOKEN')
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

# Google credentials faylini o'rnatish (agar muhit o'zgaruvchidan kelgan bo'lsa)
if 'GOOGLE_CREDENTIALS' in os.environ:
    credentials_json = base64.b64decode(os.environ['GOOGLE_CREDENTIALS']).decode('utf-8')
    with open('credentials.json', 'w') as f:
        f.write(credentials_json)
    logger.info("Google Credentials fayli yaratildi")

# Handlerlarni o'rnatish
def setup_dispatcher():
    # Ro'yxatdan o'tish uchun conversation handler
    registration_handler = ConversationHandler(
        entry_points=[CommandHandler("register", register)],
        states={
            LANGUAGE: [MessageHandler(Filters.text & ~Filters.command, set_language)],
            FIO: [MessageHandler(Filters.text & ~Filters.command, get_fio)],
            PHONE: [
                MessageHandler(Filters.contact, get_phone),
                MessageHandler(Filters.text & ~Filters.command, get_phone),
            ],
            PHOTO: [
                MessageHandler(Filters.photo | Filters.document.image, get_photo)
            ],
            SPHERE: [MessageHandler(Filters.text & ~Filters.command, get_sphere)],
            JOB: [MessageHandler(Filters.text, get_job)],
            TELEGRAM: [MessageHandler(Filters.text, get_telegram)],
            INSTAGRAM: [MessageHandler(Filters.text, get_instagram)],
            WEBSITE: [MessageHandler(Filters.text, get_website)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        name="registration",
        persistent=False
    )
    
    # Start handler
    start_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(Filters.text & ~Filters.command, set_language)],
            FIO: [MessageHandler(Filters.text & ~Filters.command, get_fio)],
            PHONE: [
                MessageHandler(Filters.contact, get_phone),
                MessageHandler(Filters.text & ~Filters.command, get_phone),
            ],
            PHOTO: [
                MessageHandler(Filters.photo | Filters.document.image, get_photo)
            ],
            SPHERE: [MessageHandler(Filters.text & ~Filters.command, get_sphere)],
            JOB: [MessageHandler(Filters.text, get_job)],
            TELEGRAM: [MessageHandler(Filters.text, get_telegram)],
            INSTAGRAM: [MessageHandler(Filters.text, get_instagram)],
            WEBSITE: [MessageHandler(Filters.text, get_website)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        name="start",
        persistent=False
    )
    
    # Handlerlarni qo'shish
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(registration_handler)
    
    return dispatcher

# Handlerlarni o'rnatish
setup_dispatcher()

def lambda_handler(event, context):
    """AWS Lambda handler"""
    try:
        logger.info(f"Event received: {event}")
        
        # API Gateway'dan kelgan ma'lumotlarni olish
        if 'body' in event:
            try:
                body = json.loads(event['body'])
            except:
                logger.error("JSON faylini ochishda xatolik")
                return {
                    'statusCode': 400,
                    'body': json.dumps('Bad Request: Invalid JSON')
                }
        else:
            logger.error("So'rovda 'body' topilmadi")
            return {
                'statusCode': 400,
                'body': json.dumps('Bad Request: No body found')
            }
        
        # Telegram Update'ni yaratish
        update = Update.de_json(body, bot)
        
        # Update'ni qayta ishlash
        dispatcher.process_update(update)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Success')
        }
    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }