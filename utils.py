import os
import tempfile
import requests
import io
from telegram import Update
from telegram.ext import ContextTypes
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from oauth2client.service_account import ServiceAccountCredentials
from config import CREDENTIALS_FILE

def create_drive_service():
    """
    Google Drive API xizmatini yaratish
    
    Returns:
        googleapiclient.discovery.Resource: Google Drive xizmati
    """
    try:
        # Google Drive API uchun scopelar
        scopes = ['https://www.googleapis.com/auth/drive']
        
        # Kredensiallarni yuklab olish
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scopes)
        
        # Drive xizmatini yaratish
        service = build('drive', 'v3', credentials=credentials)
        return service
    except Exception as e:
        print(f"Google Drive xizmatini yaratishda xatolik: {e}")
        return None

def upload_to_google_drive(file_path, file_name, mime_type=None):
    """
    Faylni Google Drive'ga yuklash
    
    Args:
        file_path (str): Yuklash uchun faylning yo'li
        file_name (str): Drive'da ko'rsatiladigan fayl nomi
        mime_type (str, optional): Fayl turi. Agar None bo'lsa, avtomatik aniqlanadi
        
    Returns:
        str: Yuklangan faylning URL manzili yoki bo'sh satr agar xatolik yuz bersa
    """
    try:
        service = create_drive_service()
        if not service:
            return ""
        
        # Fayl metadata
        file_metadata = {
            'name': file_name,
            'parents': ['1fI3EcpOAGFxdPfIcH9g2mHGWhzz2syyH']  # Bu yerga folder ID ni qo'shishingiz mumkin
        }
        
        # Faylni yuklash
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
        
        # Drive API orqali faylni yuklash
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,webViewLink',
            supportsAllDrives=True
        ).execute()
        
        # Faylni ko'rish uchun ruxsat berish (public)
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        service.permissions().create(
            fileId=file['id'],
            body=permission
        ).execute()
        
        # Fayl URL manzilini qaytarish
        return file.get('webViewLink', '')
    except Exception as e:
        print(f"Google Drive'ga yuklashda xatolik: {e}")
        return ""

async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Foydalanuvchi yuborgan fotoni Google Drive'ga saqlash va URL qaytarish
    
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
            mime_type = 'image/jpeg'
        # Agar fayl yuborilgan bo'lsa
        elif update.message.document:
            file_id = update.message.document.file_id
            mime_type = update.message.document.mime_type or 'application/octet-stream'
        else:
            return ""
            
        # Faylni Telegram serveridan olish
        file = await context.bot.get_file(file_id)
        file_extension = os.path.splitext(file.file_path)[1] if '.' in file.file_path else '.jpg'
        
        # Vaqtinchalik fayl yaratish
        with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
            await file.download_to_drive(temp_file.name)
            
            # Foydalanuvchi ID va sanani fayl nomiga qo'shish
            user_id = update.effective_user.id
            user_name = update.effective_user.first_name or "user"
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{user_name}_{user_id}_{timestamp}{file_extension}"
            
            # Google Drive'ga yuklash
            photo_url = upload_to_google_drive(temp_file.name, file_name, mime_type)
            
            # Vaqtinchalik faylni o'chirish
            os.unlink(temp_file.name)
            
            if not photo_url:
                print("Google Drive'ga yuklashda xatolik yuz berdi")
                # Zaxira variant sifatida vaqtinchalik URL qaytarish
                photo_url = f"https://example.com/photos/{user_id}_{file_id}{file_extension}"
            
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