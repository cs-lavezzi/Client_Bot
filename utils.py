import os
import tempfile
import requests
from telegram import Update
from telegram.ext import ContextTypes

async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Foydalanuvchi yuborgan fotoni saqlash va URL qaytarish
    
    Args:
        update (Update): Telegram Update obyekti
        context (ContextTypes.DEFAULT_TYPE): CallbackContext
        
    Returns:
        str: Saqlangan fotoning URL manzili
    """
    try:
        # Agar foto mavjud bo'lsa
        if update.message.photo:
            # Eng katta o'lchamdagi fotoni olish
            photo = update.message.photo[-1]
            file_id = photo.file_id
        # Agar fayl yuborilgan bo'lsa
        elif update.message.document:
            file_id = update.message.document.file_id
        else:
            return ""
            
        # Faylni Telegram serveridan olish
        file = await context.bot.get_file(file_id)
        file_extension = os.path.splitext(file.file_path)[1] if '.' in file.file_path else '.jpg'
        
        # Vaqtinchalik fayl yaratish
        with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
            await file.download_to_drive(temp_file.name)
            
            # Bu yerda fayl cloudga yuklash kerak
            # Hozircha URL ni qaytarish uchun faraz qilgan URL qaytaramiz
            # Haqiqiy loyihada bu yerda Google Drive, Firebase Storage yoki
            # boshqa fayl saqlash xizmatiga foto yuklash kodini yozish kerak
            
            # Misol uchun, shartli URL qaytarish:
            user_id = update.effective_user.id
            photo_url = f"https://example.com/photos/{user_id}_{file_id}{file_extension}"
            
            # Real loyihada cloudga yuklash kodi:
            # photo_url = upload_to_cloud_storage(temp_file.name)
            
            # Vaqtinchalik faylni o'chirish
            os.unlink(temp_file.name)
            
            return photo_url
    except Exception as e:
        print(f"Fotoni saqlashda xatolik: {e}")
        return ""

def validate_phone(phone_number: str) -> bool:
    """
    Telefon raqamni tekshirish
    
    Args:
        phone_number (str): Telefon raqami
        
    Returns:
        bool: Raqam to'g'ri formatda bo'lsa True, aks holda False
    """
    # Oddiy tekshirish: raqam faqat raqamlardan iborat bo'lishi va uzunligi kamida 9 bo'lishi kerak
    cleaned_number = ''.join(filter(str.isdigit, phone_number))
    return len(cleaned_number) >= 9

def validate_url(url: str) -> bool:
    """
    URL manzilni tekshirish
    
    Args:
        url (str): URL manzil
        
    Returns:
        bool: URL to'g'ri formatda bo'lsa True, aks holda False
    """
    # Bo'sh bo'lishi mumkin
    if not url or url == '/skip':
        return True
        
    # URL http:// yoki https:// bilan boshlanishi kerak
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://' + url
        
    try:
        # URL manzilini tekshirish (faqat format bo'yicha)
        return True
    except:
        return False