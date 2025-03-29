import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import os
from config import CREDENTIALS_FILE, SPREADSHEET_ID, WORKSHEET_NAME, COLUMNS

class SheetsManager:
    def __init__(self):
        # Google Sheets API uchun zarur bo'lgan scope(doira)lar
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        
        # Kredentiallarni yuklab olish
        try:
            # Kredential fayl mavjudligini tekshirish
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"XATOLIK: {CREDENTIALS_FILE} fayli mavjud emas!")
                raise FileNotFoundError(f"{CREDENTIALS_FILE} fayli topilmadi")
                
            credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
            self.client = gspread.authorize(credentials)
            
            # Spreadsheet ID bo'sh emasligini tekshirish
            if not SPREADSHEET_ID:
                print("XATOLIK: SPREADSHEET_ID bo'sh!")
                raise ValueError("SPREADSHEET_ID ko'rsatilmagan")
            
            # Google Sheets jadvaliga ulanish
            try:
                self.spreadsheet = self.client.open_by_key(SPREADSHEET_ID)
                print(f"Spreadsheet '{self.spreadsheet.title}' ga ulandi")
            except gspread.exceptions.APIError as e:
                print(f"Spreadsheet ochishda xatolik: {e}")
                if "Requested entity was not found" in str(e):
                    print("Bunday ID li jadval mavjud emas yoki service account uchun ruxsat yo'q")
                raise
            
            # Ish varaqni olish yoki yaratish
            try:
                self.worksheet = self.spreadsheet.worksheet(WORKSHEET_NAME)
                print(f"Ish varaq '{WORKSHEET_NAME}' topildi")
            except gspread.exceptions.WorksheetNotFound:
                print(f"Ish varaq '{WORKSHEET_NAME}' topilmadi, yangisini yaratilmoqda...")
                self.worksheet = self.spreadsheet.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=20)
                # Jadval sarlavhalarini qo'shish
                self.worksheet.append_row(COLUMNS)
                print(f"Yangi ish varaq '{WORKSHEET_NAME}' yaratildi va sarlavhalar qo'shildi")
                
            print("Google Sheets muvaffaqiyatli ulandi!")
        except Exception as e:
            print(f"Google Sheets ulanishida xatolik: {e}")
            raise
            
    def save_client_data(self, client_data):
        """
        Mijoz ma'lumotlarini Google Sheets jadvaliga saqlash
        
        Args:
            client_data (dict): Mijoz ma'lumotlari
            
        Returns:
            bool: Amaliyot muvaffaqiyatli bajarilgan bo'lsa True, aks holda False
        """
        try:
            # Joriy sanani olish
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Ma'lumotlarni tekshirish
            print("Saqlash uchun ma'lumotlar:")
            for key, value in client_data.items():
                print(f"{key}: {value}")
            
            # Yozish uchun ma'lumotlarni tayyorlash
            row_data = [
                current_date,  # Sana
                client_data.get('FIO', ''),  # FIO
                client_data.get('PHONE', ''),  # Telefon
                client_data.get('PHOTO', ''),  # Foto/Logo URL
                client_data.get('SPHERE', ''),  # Faoliyat sohasi
                client_data.get('JOB', ''),  # Kasbi
                client_data.get('TELEGRAM', ''),  # Telegram
                client_data.get('INSTAGRAM', ''),  # Instagram
                client_data.get('WEBSITE', '')  # Veb-sayt
            ]
            
            print(f"Google Sheets ga yoziladigan qator: {row_data}")
            
            # Ma'lumotlarni jadvalga qo'shish
            try:
                self.worksheet.append_row(row_data)
                print(f"Mijoz ma'lumotlari muvaffaqiyatli saqlandi: {client_data.get('FIO')}")
                return True
            except gspread.exceptions.APIError as e:
                if "Quota exceeded" in str(e):
                    print("Google API chekloviga yetib kelindi. Iltimos, keyinroq qayta urining.")
                else:
                    print(f"Google API xatoligi: {e}")
                return False
            
        except Exception as e:
            print(f"Ma'lumotlarni saqlashda xatolik: {e}")
            return False