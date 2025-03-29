from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from config import MESSAGES, REGISTRATION_STEPS
from utils import save_photo, validate_phone, validate_url
from sheets_manager import SheetsManager

# Ro'yxatdan o'tish bosqichlari uchun holatlar
FIO, PHONE, PHOTO, SPHERE, JOB, TELEGRAM, INSTAGRAM, WEBSITE = range(8)

# Google Sheets menejerini yaratish
sheets_manager = SheetsManager()

# Boshlang'ich buyruqlar uchun handlerlar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Botni boshlash buyrug'i uchun handler"""
    await update.message.reply_text(MESSAGES['start'])

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yordam buyrug'i uchun handler"""
    await update.message.reply_text(MESSAGES['help'])

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ro'yxatdan o'tishni bekor qilish uchun handler"""
    # Kontekst ma'lumotlarini tozalash
    if 'user_data' in context.chat_data:
        del context.chat_data['user_data']
    
    await update.message.reply_text(
        MESSAGES['cancel'], 
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Ro'yxatdan o'tish handerlari
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ro'yxatdan o'tishni boshlash"""
    # Yangi foydalanuvchi ma'lumotlarini saqlash uchun lug'at
    context.chat_data['user_data'] = {}
    
    await update.message.reply_text(
        MESSAGES['register'],
        reply_markup=ReplyKeyboardRemove()
    )
    
    # FIO so'rash
    await update.message.reply_text(REGISTRATION_STEPS['FIO'])
    return FIO

async def get_fio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """FIO ni olish va telefon raqamni so'rash"""
    # FIO ni saqlash
    context.chat_data['user_data']['FIO'] = update.message.text
    
    # Telefon raqamni so'rash
    await update.message.reply_text(REGISTRATION_STEPS['PHONE'])
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Telefon raqamni olish va fotoni so'rash"""
    phone_number = update.message.text
    
    # Telefon raqamni tekshirish
    if not validate_phone(phone_number):
        await update.message.reply_text("Noto'g'ri telefon raqam formati. Iltimos, qaytadan kiriting:")
        return PHONE
    
    # Telefon raqamni saqlash
    context.chat_data['user_data']['PHONE'] = phone_number
    
    # Fotoni so'rash
    await update.message.reply_text(REGISTRATION_STEPS['PHOTO'])
    return PHOTO

async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Fotoni olish va faoliyat sohasini so'rash"""
    # Fotoni saqlash
    photo_url = await save_photo(update, context)
    
    if not photo_url:
        await update.message.reply_text("Foto yuklashda xatolik yuz berdi. Iltimos, qaytadan yuboring:")
        return PHOTO
    
    # Foto URL ni saqlash
    context.chat_data['user_data']['PHOTO'] = photo_url
    
    # Faoliyat sohasini so'rash
    await update.message.reply_text(REGISTRATION_STEPS['SPHERE'])
    return SPHERE

async def get_sphere(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Faoliyat sohasini olish va kasbni so'rash"""
    # Faoliyat sohasini saqlash
    context.chat_data['user_data']['SPHERE'] = update.message.text
    
    # Kasbni so'rash
    reply_keyboard = [['/skip']]
    await update.message.reply_text(
        REGISTRATION_STEPS['JOB'],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return JOB

async def get_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Kasbni olish va Telegram usernameni so'rash"""
    # Agar o'tkazib yuborilsa
    if update.message.text == '/skip':
        context.chat_data['user_data']['JOB'] = ''
    else:
        # Kasbni saqlash
        context.chat_data['user_data']['JOB'] = update.message.text
    
    # Telegram usernameni so'rash
    reply_keyboard = [['/skip']]
    await update.message.reply_text(
        REGISTRATION_STEPS['TELEGRAM'],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return TELEGRAM

async def get_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Telegram usernameni olish va Instagram profilni so'rash"""
    # Agar o'tkazib yuborilsa
    if update.message.text == '/skip':
        context.chat_data['user_data']['TELEGRAM'] = ''
    else:
        # Telegram usernameni saqlash
        username = update.message.text
        # @ belgisini qo'shish agar yo'q bo'lsa
        if not username.startswith('@'):
            username = '@' + username
        context.chat_data['user_data']['TELEGRAM'] = username
    
    # Instagram profilni so'rash
    reply_keyboard = [['/skip']]
    await update.message.reply_text(
        REGISTRATION_STEPS['INSTAGRAM'],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return INSTAGRAM

async def get_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Instagram profilni olish va veb-saytni so'rash"""
    # Agar o'tkazib yuborilsa
    if update.message.text == '/skip':
        context.chat_data['user_data']['INSTAGRAM'] = ''
    else:
        # Instagram profilni saqlash
        context.chat_data['user_data']['INSTAGRAM'] = update.message.text
    
    # Veb-saytni so'rash
    reply_keyboard = [['/skip']]
    await update.message.reply_text(
        REGISTRATION_STEPS['WEBSITE'],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return WEBSITE

async def get_website(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Veb-saytni olish va ro'yxatdan o'tishni yakunlash"""
    # Agar o'tkazib yuborilsa
    if update.message.text == '/skip':
        context.chat_data['user_data']['WEBSITE'] = ''
    else:
        # Veb-saytni saqlash va formatni tekshirish
        website = update.message.text
        if not validate_url(website):
            await update.message.reply_text("Noto'g'ri URL format. Iltimos, qaytadan kiriting:")
            return WEBSITE
        
        context.chat_data['user_data']['WEBSITE'] = website
    
    # Google Sheets ga ma'lumotlarni saqlash
    try:
        success = sheets_manager.save_client_data(context.chat_data['user_data'])
        
        if success:
            await update.message.reply_text(
                MESSAGES['success'],
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            # Log qo'shish
            print("Google Sheets ga saqlash muvaffaqiyatsiz bo'ldi")
            await update.message.reply_text(
                MESSAGES['error'],
                reply_markup=ReplyKeyboardRemove()
            )
    except Exception as e:
        # Xatolikni tushunish uchun qo'shimcha log
        print(f"Ma'lumotlarni saqlashda tafsilotli xatolik: {e}")
        await update.message.reply_text(
            f"{MESSAGES['error']} Xatolik: {str(e)[:100]}...",
            reply_markup=ReplyKeyboardRemove()
        )
    
    # Kontekst ma'lumotlarini tozalash
    if 'user_data' in context.chat_data:
        del context.chat_data['user_data']
    
    return ConversationHandler.END