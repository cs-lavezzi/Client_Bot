import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from config import CREDENTIALS_FILE, SPREADSHEET_ID, WORKSHEET_NAME, COLUMNS

class SheetsManager:
    def __init__(self):
        # Google Sheets API uchun zarur bo'lgan scope(doira)lar
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        
        # Kredentiallarni yuklab olish
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
            self.client = gspread.authorize(credentials)
            
            # Google Sheets jadvaliga ulanish
            self.spreadsheet = self.client.open_by_key(SPREADSHEET_ID)
            
            # Ish varaqni olish yoki yaratish
            try:
                self.worksheet = self.spreadsheet.worksheet(WORKSHEET_NAME)
            except gspread.exceptions.WorksheetNotFound:
                self.worksheet = self.spreadsheet.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=20)
                # Jadval sarlavhalarini qo'shish
                self.worksheet.append_row(COLUMNS)
                
            print("Google Sheets ulandi!")
        except Exception as e:
            print(f"Google Sheets ulanishida xatolik: {e}")
            raise
            
    def save_client_data(self, client_data):
        """Mijoz ma'lumotlarini Google Sheets jadvaliga saqlash"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Joriy sanani olish
                current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
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
                
                # Ma'lumotlarni jadvalga qo'shish
                self.worksheet.append_row(row_data)
                print(f"Mijoz ma'lumotlari saqlandi: {client_data.get('FIO')}")
                return True
            
            except Exception as e:
                retry_count += 1
                print(f"Urinish {retry_count}/{max_retries}: Xatolik: {e}")
                
                # Kutish vaqti
                import time
                time.sleep(3)
                
                # Oxirgi urinish
                if retry_count == max_retries:
                    print("Barcha urinishlar muvaffaqiyatsiz yakunlandi")
                    return False