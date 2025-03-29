import os
from dotenv import load_dotenv

# .env faylidan o'zgaruvchilarni yuklash
load_dotenv()

# Telegram Bot tokeni
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Google Sheets ma'lumotlari
CREDENTIALS_FILE = 'credentials.json'
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
WORKSHEET_NAME = os.getenv('WORKSHEET_NAME', 'Clients')

# Jadval ustunlari
COLUMNS = [
    'Sana', 'FIO', 'Telefon', 'Foto/Logo URL', 'Faoliyat sohasi',
    'Kasbi', 'Telegram', 'Instagram', 'Veb-sayt'
]

# Bot xabarlari
MESSAGES = {
    'start': "Assalomu alaykum! Men ma'lumotlarni yig'ish uchun botman. /register buyrug'ini yuborib ro'yxatdan o'ting.",
    'help': "Buyruqlar ro'yxati:\n/start - Botni ishga tushirish\n/register - Ro'yxatdan o'tish\n/cancel - Ro'yxatdan o'tishni bekor qilish\n/help - Yordam",
    'register': "Ro'yxatdan o'tish boshlandi. Iltimos, ma'lumotlarni ketma-ket kiriting.\nIstalgan vaqtda /cancel buyrug'i bilan ro'yxatdan o'tishni bekor qilishingiz mumkin.",
    'cancel': "Ro'yxatdan o'tish bekor qilindi. Qaytadan boshlash uchun /register buyrug'ini yuboring.",
    'success': "Tabriklaymiz! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.",
    'error': "Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
}

# Ro'yxatdan o'tish bosqichlari
REGISTRATION_STEPS = {
    'FIO': 'Iltimos, to\'liq ismingizni kiriting (FIO):',
    'PHONE': 'Telefon raqamingizni kiriting:',
    'PHOTO': 'Foto yoki logotipingizni yuboring:',
    'SPHERE': 'Faoliyat sohangizni kiriting:',
    'JOB': 'Kim bo\'lib ishlaysiz? (Ixtiyoriy, o\'tkazib yuborish uchun /skip yuboring):',
    'TELEGRAM': 'Telegram usernamengizni kiriting (Ixtiyoriy, o\'tkazib yuborish uchun /skip yuboring):',
    'INSTAGRAM': 'Instagram profilingizni kiriting (Ixtiyoriy, o\'tkazib yuborish uchun /skip yuboring):',
    'WEBSITE': 'Veb-saytingizni kiriting (Ixtiyoriy, o\'tkazib yuborish uchun /skip yuboring):'
}