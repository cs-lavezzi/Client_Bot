import os
from dotenv import load_dotenv

# .env faylidan o'zgaruvchilarni yuklash
load_dotenv()

# Telegram Bot tokeni
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Google ma'lumotlari
CREDENTIALS_FILE = 'credentials.json'
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
WORKSHEET_NAME = os.getenv('WORKSHEET_NAME', 'Clients')
GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID', '')  # Ixtiyoriy Google Drive folder ID

# Jadval ustunlari
COLUMNS = [
    'Sana', 'FIO', 'Telefon', 'Foto/Logo URL', 'Faoliyat sohasi',
    'Kasbi', 'Telegram', 'Instagram', 'Veb-sayt'
]

# Bot xabarlari
MESSAGES = {
    'uz': {
        'start': "Assalomu alaykum! Men ma'lumotlarni yig'ish uchun botman. Iltimos, tilni tanlang.\n\nПривет! Я бот для сбора данных. Пожалуйста, выберите язык.",
        'select_language': "Iltimos, tilni tanlang:\nПожалуйста, выберите язык:",
        'help': "Buyruqlar ro'yxati:\n/start - Botni ishga tushirish\n/register - Ro'yxatdan o'tish\n/cancel - Ro'yxatdan o'tishni bekor qilish\n/help - Yordam",
        'register': "Ro'yxatdan o'tish boshlandi. Iltimos, ma'lumotlarni ketma-ket kiriting.\nIstalgan vaqtda /cancel buyrug'i bilan ro'yxatdan o'tishni bekor qilishingiz mumkin.",
        'cancel': "Ro'yxatdan o'tish bekor qilindi. Qaytadan boshlash uchun /register buyrug'ini yuboring.",
        'success': "Tabriklaymiz! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.",
        'error': "Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
    },
    'ru': {
        'start': "Привет! Я бот для сбора данных. Пожалуйста, выберите язык.\n\nAssalomu alaykum! Men ma'lumotlarni yig'ish uchun botman. Iltimos, tilni tanlang.",
        'select_language': "Пожалуйста, выберите язык:\nIltimos, tilni tanlang:",
        'help': "Список команд:\n/start - Запустить бота\n/register - Зарегистрироваться\n/cancel - Отменить регистрацию\n/help - Помощь",
        'register': "Начата регистрация. Пожалуйста, введите данные последовательно.\nВы можете отменить регистрацию в любой момент командой /cancel.",
        'cancel': "Регистрация отменена. Чтобы начать заново, отправьте команду /register.",
        'success': "Поздравляем! Вы успешно зарегистрировались.",
        'error': "Произошла ошибка. Пожалуйста, попробуйте еще раз."
    }
}

# Ro'yxatdan o'tish bosqichlari
REGISTRATION_STEPS = {
    'uz': {
        'FIO': 'Iltimos, to\'liq ismingizni kiriting (FIO):',
        'PHONE': 'Telefon raqamingizni kiriting:',
        'PHOTO': 'Foto yoki logotipingizni yuboring:',
        'SPHERE': 'Faoliyat sohangizni kiriting:',
        'JOB': 'Kim bo\'lib ishlaysiz? (Ixtiyoriy, o\'tkazib yuborish uchun /skip yuboring):',
        'TELEGRAM': 'Telegram usernamengizni kiriting (Ixtiyoriy, o\'tkazib yuborish uchun /skip yuboring):',
        'INSTAGRAM': 'Instagram profilingizni kiriting (Ixtiyoriy, o\'tkazib yuborish uchun /skip yuboring):',
        'WEBSITE': 'Veb-saytingizni kiriting (Ixtiyoriy, o\'tkazib yuborish uchun /skip yuboring):'
    },
    'ru': {
        'FIO': 'Пожалуйста, введите ваше полное имя (ФИО):',
        'PHONE': 'Введите ваш номер телефона:',
        'PHOTO': 'Отправьте ваше фото или логотип:',
        'SPHERE': 'Укажите сферу вашей деятельности:',
        'JOB': 'Кем вы работаете? (Необязательно, отправьте /skip чтобы пропустить):',
        'TELEGRAM': 'Введите ваш Telegram username (Необязательно, отправьте /skip чтобы пропустить):',
        'INSTAGRAM': 'Введите ваш профиль Instagram (Необязательно, отправьте /skip чтобы пропустить):',
        'WEBSITE': 'Введите ваш веб-сайт (Необязательно, отправьте /skip чтобы пропустить):'
    }
}