from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from config import MESSAGES, REGISTRATION_STEPS
from utils import save_photo, validate_phone, validate_url
from sheets_manager import SheetsManager

# Ro'yxatdan o'tish bosqichlari uchun holatlar
LANGUAGE, FIO, PHONE, PHOTO, SPHERE, JOB, TELEGRAM, INSTAGRAM, WEBSITE = range(9)

# Google Sheets menejerini yaratish
sheets_manager = SheetsManager()

# Barcha funksiyalarni asinxron qilish
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Botni boshlash buyrug'i uchun handler"""
    # Standart tilni o'rnatish (default: 'uz')
    if 'language' not in context.user_data:
        context.user_data['language'] = 'uz'
    
    # Start xabarini yuborish
    await update.message.reply_text(MESSAGES[context.user_data['language']]['start'])
    
    # Til tanlash funksiyasiga o'tish
    return await select_language(update, context)

# Til tanlash uchun handler
async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Foydalanuvchiga til tanlash imkoniyatini berish"""
    # Tugmalar yaratish
    keyboard = [
        [KeyboardButton('🇺🇿 O\'zbek tili'), KeyboardButton('🇷🇺 Русский язык')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    # Standart tilni o'rnatish (default: 'uz')
    if 'language' not in context.user_data:
        context.user_data['language'] = 'uz'
    
    # Til tanlash xabarini yuborish
    await update.message.reply_text(
        MESSAGES[context.user_data['language']]['select_language'],
        reply_markup=reply_markup
    )
    return LANGUAGE


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Foydalanuvchi tilini saqlash"""
    text = update.message.text
    
    # Tugma bosilgan matniga qarab tilni aniqlash
    if '🇺🇿' in text or 'zbek' in text:
        context.user_data['language'] = 'uz'
    elif '🇷🇺' in text or 'усск' in text:
        context.user_data['language'] = 'ru'
    else:
        # Agar til aniqlash imkoni bo'lmasa, o'zbek tili bilan davom etish
        context.user_data['language'] = 'uz'
    
    lang = context.user_data['language']
    
    # Agar user_data mavjud bo'lmasa, yangi lug'at yaratish
    if 'user_data' not in context.chat_data:
        context.chat_data['user_data'] = {}
    
    # Ro'yxatdan o'tish boshlanishi haqida xabar
    await update.message.reply_text(
        MESSAGES[lang]['register'],
        reply_markup=ReplyKeyboardRemove()
    )
    
    # FIO so'rash
    await update.message.reply_text(REGISTRATION_STEPS[lang]['FIO'])
    return FIO

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yordam buyrug'i uchun handler"""
    # Agar til tanlanmagan bo'lsa, standart tilni o'rnatish
    if 'language' not in context.user_data:
        context.user_data['language'] = 'uz'
    
    lang = context.user_data['language']
    await update.message.reply_text(MESSAGES[lang]['help'])

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ro'yxatdan o'tishni bekor qilish uchun handler"""
    # Kontekst ma'lumotlarini tozalash
    if 'user_data' in context.chat_data:
        del context.chat_data['user_data']
    
    # Agar til tanlanmagan bo'lsa, standart tilni o'rnatish
    if 'language' not in context.user_data:
        context.user_data['language'] = 'uz'
    
    lang = context.user_data['language']
    
    await update.message.reply_text(
        MESSAGES[lang]['cancel'], 
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Ro'yxatdan o'tish handerlari
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ro'yxatdan o'tishni boshlash"""
    # Yangi foydalanuvchi ma'lumotlarini saqlash uchun lug'at
    context.chat_data['user_data'] = {}
    
    # Agar til tanlanmagan bo'lsa, standart tilni o'rnatish
    if 'language' not in context.user_data:
        context.user_data['language'] = 'uz'
    
    # Til tanlash funksiyasiga o'tish
    return await select_language(update, context)

async def get_fio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """FIO ni olish va telefon raqamni so'rash"""
    # Agar user_data mavjud bo'lmasa, yangi lug'at yaratish
    if 'user_data' not in context.chat_data:
        context.chat_data['user_data'] = {}
    
    # FIO ni saqlash
    context.chat_data['user_data']['FIO'] = update.message.text
    
    # Agar til tanlanmagan bo'lsa, standart tilni o'rnatish
    if 'language' not in context.user_data:
        context.user_data['language'] = 'uz'
        
    lang = context.user_data['language']
    
    # Telefon raqamni so'rash
    # Kontakt baham ko'rish tugmasini yaratish
    contact_keyboard = KeyboardButton(
        text="📱 Kontaktni baham ko'rish" if lang == 'uz' else "📱 Поделиться контактом", 
        request_contact=True
    )
    
    reply_markup = ReplyKeyboardMarkup(
        [[contact_keyboard]], 
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    # Telefon raqam so'rovi
    message = REGISTRATION_STEPS[lang]['PHONE'] + "\n" + (
        "Kontaktni baham ko'rish uchun quyidagi tugmani bosing yoki raqamni qo'lda kiriting:" if lang == 'uz' else 
        "Нажмите кнопку ниже, чтобы поделиться контактом, или введите номер вручную:"
    )
    
    await update.message.reply_text(message, reply_markup=reply_markup)
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Telefon raqamni olish va fotoni so'rash"""
    # Til olish
    lang = context.user_data.get('language', 'uz')
    
    # Kontakt orqali kelgan telefon raqamini tekshirish
    if update.message.contact:
        phone_number = update.message.contact.phone_number
    else:
        phone_number = update.message.text
    
    # Telefon raqamni tekshirish
    if not validate_phone(phone_number):
        # Tanlangan tilga qarab xatolik xabari
        error_msg = "Noto'g'ri telefon raqam formati. Iltimos, qaytadan kiriting:" if lang == 'uz' else "Неверный формат номера телефона. Пожалуйста, введите еще раз:"
        
        # Kontakt baham ko'rish tugmasini qayta yaratish
        contact_keyboard = KeyboardButton(
            text="📱 Kontaktni baham ko'rish" if lang == 'uz' else "📱 Поделиться контактом", 
            request_contact=True
        )
        
        reply_markup = ReplyKeyboardMarkup(
            [[contact_keyboard]], 
            resize_keyboard=True,
            one_time_keyboard=True
        )
        
        await update.message.reply_text(error_msg, reply_markup=reply_markup)
        return PHONE
    
    # Telefon raqamni saqlash
    context.chat_data['user_data']['PHONE'] = phone_number
    
    # Fotoni so'rash
    await update.message.reply_text(
        REGISTRATION_STEPS[lang]['PHOTO'],
        reply_markup=ReplyKeyboardRemove()
    )
    return PHOTO

async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Fotoni olish va faoliyat sohasini so'rash"""
    # Til olish
    lang = context.user_data.get('language', 'uz')
    
    # Rasm formatini tekshirish
    valid_photo = False
    photo_file_id = None
    
    if update.message.photo:
        # Telegram photo - bu har doim jpeg formatida bo'ladi
        valid_photo = True
        photo_file_id = update.message.photo[-1].file_id
    elif update.message.document:
        # Hujjat mime turini tekshirish
        mime_type = update.message.document.mime_type
        if mime_type in ['image/jpeg', 'image/png']:
            valid_photo = True
            photo_file_id = update.message.document.file_id
    
    # Agar rasm formati noto'g'ri bo'lsa
    if not valid_photo:
        error_msg = "Iltimos, faqat JPEG yoki PNG formatidagi rasm yuboring." if lang == 'uz' else "Пожалуйста, отправьте только изображение в формате JPEG или PNG."
        await update.message.reply_text(error_msg)
        return PHOTO
    
    # Fotoni saqlash
    photo_url = await save_photo(update, context)
    
    if not photo_url:
        # Tanlangan tilga qarab xatolik xabari
        error_msg = "Foto yuklashda xatolik yuz berdi. Iltimos, qaytadan yuboring:" if lang == 'uz' else "Произошла ошибка при загрузке фото. Пожалуйста, отправьте еще раз:"
        await update.message.reply_text(error_msg)
        return PHOTO
    
    # Foto URL ni saqlash
    context.chat_data['user_data']['PHOTO'] = photo_url
    
    # Faoliyat sohasini so'rash
    await update.message.reply_text(REGISTRATION_STEPS[lang]['SPHERE'])
    return SPHERE
async def get_sphere(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Faoliyat sohasini olish va kasbni so'rash"""
    # Til olish
    lang = context.user_data.get('language', 'uz')
    
    # Faoliyat sohasini saqlash
    context.chat_data['user_data']['SPHERE'] = update.message.text
    
    # Kasbni so'rash
    reply_keyboard = [['/skip']]
    await update.message.reply_text(
        REGISTRATION_STEPS[lang]['JOB'],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return JOB

async def get_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Kasbni olish va Telegram usernameni so'rash"""
    # Til olish
    lang = context.user_data.get('language', 'uz')
    
    # Agar o'tkazib yuborilsa
    if update.message.text == '/skip':
        context.chat_data['user_data']['JOB'] = ''
    else:
        # Kasbni saqlash
        context.chat_data['user_data']['JOB'] = update.message.text
    
    # Telegram usernameni so'rash
    reply_keyboard = [['/skip']]
    await update.message.reply_text(
        REGISTRATION_STEPS[lang]['TELEGRAM'],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return TELEGRAM

async def get_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Telegram usernameni olish va Instagram profilni so'rash"""
    # Til olish
    lang = context.user_data.get('language', 'uz')
    
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
        REGISTRATION_STEPS[lang]['INSTAGRAM'],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return INSTAGRAM

async def get_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Instagram profilni olish va veb-saytni so'rash"""
    # Til olish
    lang = context.user_data.get('language', 'uz')
    
    # Agar o'tkazib yuborilsa
    if update.message.text == '/skip':
        context.chat_data['user_data']['INSTAGRAM'] = ''
    else:
        # Instagram profilni saqlash
        context.chat_data['user_data']['INSTAGRAM'] = update.message.text
    
    # Veb-saytni so'rash
    reply_keyboard = [['/skip']]
    await update.message.reply_text(
        REGISTRATION_STEPS[lang]['WEBSITE'],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return WEBSITE

async def get_website(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Veb-saytni olish va ro'yxatdan o'tishni yakunlash"""
    # Til olish
    lang = context.user_data.get('language', 'uz')
    
    # Agar o'tkazib yuborilsa
    if update.message.text == '/skip':
        context.chat_data['user_data']['WEBSITE'] = ''
    else:
        # Veb-saytni saqlash va formatni tekshirish
        website = update.message.text
        if not validate_url(website):
            # Tanlangan tilga qarab xatolik xabari
            error_msg = "Noto'g'ri URL format. Iltimos, qaytadan kiriting:" if lang == 'uz' else "Неверный формат URL. Пожалуйста, введите еще раз:"
            await update.message.reply_text(error_msg)
            return WEBSITE
        
        context.chat_data['user_data']['WEBSITE'] = website
    
    # Google Sheets ga ma'lumotlarni saqlash
    try:
        success = sheets_manager.save_client_data(context.chat_data['user_data'])
        
        if success:
            await update.message.reply_text(
                MESSAGES[lang]['success'],
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            # Log qo'shish
            print("Google Sheets ga saqlash muvaffaqiyatsiz bo'ldi")
            await update.message.reply_text(
                MESSAGES[lang]['error'],
                reply_markup=ReplyKeyboardRemove()
            )
    except Exception as e:
        # Xatolikni tushunish uchun qo'shimcha log
        print(f"Ma'lumotlarni saqlashda tafsilotli xatolik: {e}")
        await update.message.reply_text(
            MESSAGES[lang]['error'],
            reply_markup=ReplyKeyboardRemove()
        )
    
    # Kontekst ma'lumotlarini tozalash
    if 'user_data' in context.chat_data:
        del context.chat_data['user_data']
    
    return ConversationHandler.END