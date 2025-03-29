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
            # Heroku muhit o'zgaruvchisidan kredentialni tekshirish
            import os
            import base64
            import json
            
            credentials_env = os.getenv('GOOGLE_CREDENTIALS')
            
            if credentials_env and not os.path.exists(CREDENTIALS_FILE):
                # Kredential ma'lumotlarini base64 dan dekodlash
                try:
                    credentials_json = base64.b64decode(credentials_env).decode('utf-8')
                    
                    # Faylga saqlash
                    with open(CREDENTIALS_FILE, 'w') as f:
                        f.write(credentials_json)
                    print(f"Credentials.json fayli muhit o'zgaruvchisidan yaratildi")
                except Exception as e:
                    print(f"Kredentialni dekodlashda xatolik: {e}")
            
            credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
            self.client = gspread.authorize(credentials)

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