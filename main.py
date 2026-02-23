from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import os
import random
from datetime import datetime
from config import EMAIL, PASSWORD
from google_sheets import get_laporan
from email_notifier import send_attendance_notification

# Path ke Edge Driver (untuk lokal)
EDGE_DRIVER_PATH = "/Users/capyzara/Downloads/edgedriver_mac64/msedgedriver"

# Detect environment (GitHub Actions atau lokal)
IS_CI = os.getenv('CI') == 'true' or os.getenv('GITHUB_ACTIONS') == 'true'

def human_delay(min_seconds=1, max_seconds=3):
    """Delay random untuk menghindari deteksi bot"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

class MagangHubAttendance:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        
    def setup_driver(self):
        """Setup browser driver (Chrome untuk CI, Edge untuk lokal)"""
        
        if IS_CI:
            # Gunakan Chrome headless untuk GitHub Actions
            print("Running in CI environment, using Chrome headless...")
            chrome_options = ChromeOptions()
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            # Gunakan Edge untuk development lokal
            print("Running locally, using Edge...")
            edge_options = EdgeOptions()
            
            # Gunakan user profile untuk menyimpan session
            user_data_dir = os.path.expanduser('~/Library/Application Support/EdgeAutomation')
            edge_options.add_argument(f'--user-data-dir={user_data_dir}')
            edge_options.add_argument('--profile-directory=Default')
            
            # Uncomment baris di bawah jika ingin menjalankan headless di lokal juga
            # edge_options.add_argument('--headless=new')
            edge_options.add_argument('--no-sandbox')
            edge_options.add_argument('--disable-dev-shm-usage')
            edge_options.add_argument('--start-maximized')
            
            # Setup Edge service dengan path driver
            service = EdgeService(EDGE_DRIVER_PATH)
            self.driver = webdriver.Edge(service=service, options=edge_options)
        
        self.driver.implicitly_wait(10)
        
    def login(self):
        """Login ke MagangHub (skip jika sudah login)"""
        try:
            print("Membuka dashboard MagangHub...")
            # Coba akses dashboard dulu
            self.driver.get("https://monev.maganghub.kemnaker.go.id/dashboard")
            human_delay(3, 5)
            
            # Cek apakah sudah login (kalau ada kalender berarti sudah login)
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".calendar-container")
                print("Session masih aktif, sudah login!")
                return True
            except:
                print("Session expired, perlu login...")
            
            # Kalau belum login, akses halaman login
            print("Membuka halaman login Kemnaker...")
            self.driver.get("https://account.kemnaker.go.id/auth/login")
            
            # Tunggu halaman load
            human_delay(2, 4)
            
            print("Mengisi email dan password...")
            # Cari field username (email/nomor HP)
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            human_delay(0.5, 1.5)
            email_field.clear()
            human_delay(0.3, 0.8)
            email_field.send_keys(self.email)
            
            human_delay(1, 2)
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            human_delay(0.3, 0.8)
            password_field.send_keys(self.password)
            
            human_delay(1, 2)
            # Klik tombol login
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
            login_button.click()
            
            print("Login berhasil!")
            human_delay(3, 5)
            
            return True
            
        except Exception as e:
            print(f"Error saat login: {str(e)}")
            return False
    
    def do_attendance(self):
        """Melakukan absen dengan klik tanggal hari ini di kalender dan isi form"""
        data_source = "Unknown"
        URAIAN_AKTIVITAS = ""
        PEMBELAJARAN = ""
        KENDALA = ""
        
        try:
            print("Membuka dashboard MagangHub...")
            
            # Ambil data laporan (dari Google Sheets atau local template)
            URAIAN_AKTIVITAS, PEMBELAJARAN, KENDALA = get_laporan()
            
            # Tentukan data source untuk logging
            # Cek apakah data dari Google Sheets atau template
            from google_sheets import get_laporan_from_sheet
            test_uraian, _, _ = get_laporan_from_sheet()
            data_source = "Google Sheets" if test_uraian == URAIAN_AKTIVITAS else "Local Template"
            
            # Navigasi ke dashboard setelah login
            self.driver.get("https://monev.maganghub.kemnaker.go.id/dashboard")
            human_delay(3, 5)
            
            print("Mencari kalender laporan harian...")
            
            # Tunggu kalender muncul
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".calendar-container"))
            )
            human_delay(1, 2)
            
            print("Mencari tanggal hari ini di kalender...")
            # Cari tanggal hari ini (ditandai dengan class today-highlight dan clickable-day)
            today_cell = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "td.today-highlight.clickable-day"))
            )
            
            human_delay(1, 2)
            print("Klik tanggal hari ini untuk absen...")
            today_cell.click()
            human_delay(2, 4)
            
            # Tunggu modal form muncul
            print("Menunggu form laporan muncul...")
            human_delay(2, 3)
            
            print("Mengisi form laporan harian...")
            
            # Isi textarea Uraian aktivitas
            uraian_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "input-v-0-9"))
            )
            human_delay(0.5, 1.5)
            uraian_field.clear()
            human_delay(0.5, 1)
            uraian_field.send_keys(URAIAN_AKTIVITAS)
            print("✓ Uraian aktivitas terisi")
            human_delay(1.5, 3)
            
            # Isi textarea Pembelajaran yang diperoleh
            pembelajaran_field = self.driver.find_element(By.ID, "input-v-0-12")
            pembelajaran_field.clear()
            human_delay(0.5, 1)
            pembelajaran_field.send_keys(PEMBELAJARAN)
            print("✓ Pembelajaran terisi")
            human_delay(1.5, 3)
            
            # Isi textarea Kendala yang dialami
            kendala_field = self.driver.find_element(By.ID, "input-v-0-15")
            kendala_field.clear()
            human_delay(0.5, 1)
            kendala_field.send_keys(KENDALA)
            print("✓ Kendala terisi")
            human_delay(2, 3)
            
            # Centang checkbox konfirmasi
            checkbox = self.driver.find_element(By.ID, "checkbox-v-0-17")
            if not checkbox.is_selected():
                checkbox.click()
                print("✓ Checkbox konfirmasi dicentang")
            human_delay(1, 2)
            
            # Validasi panjang karakter sebelum submit
            print("\nMemvalidasi panjang konten...")
            MIN_CHARACTERS = 100
            validation_passed = True
            
            if len(URAIAN_AKTIVITAS) < MIN_CHARACTERS:
                print(f"✗ Uraian Aktivitas terlalu pendek: {len(URAIAN_AKTIVITAS)} karakter (minimal {MIN_CHARACTERS})")
                validation_passed = False
            else:
                print(f"✓ Uraian Aktivitas: {len(URAIAN_AKTIVITAS)} karakter")
            
            if len(PEMBELAJARAN) < MIN_CHARACTERS:
                print(f"✗ Pembelajaran terlalu pendek: {len(PEMBELAJARAN)} karakter (minimal {MIN_CHARACTERS})")
                validation_passed = False
            else:
                print(f"✓ Pembelajaran: {len(PEMBELAJARAN)} karakter")
            
            if len(KENDALA) < MIN_CHARACTERS:
                print(f"✗ Kendala terlalu pendek: {len(KENDALA)} karakter (minimal {MIN_CHARACTERS})")
                validation_passed = False
            else:
                print(f"✓ Kendala: {len(KENDALA)} karakter")
            
            if not validation_passed:
                print("\n⚠ SUBMIT DIBATALKAN - Ada konten yang kurang dari 100 karakter")
                print("Silakan perbaiki data di Google Sheets atau laporan_template.py")
                print("Tekan Ctrl+C untuk menutup atau tunggu 30 detik...")
                time.sleep(30)
                return {
                    'success': False,
                    'error': 'Validasi gagal: Ada konten kurang dari 100 karakter',
                    'uraian': URAIAN_AKTIVITAS,
                    'pembelajaran': PEMBELAJARAN,
                    'kendala': KENDALA,
                    'data_source': data_source
                }
            
            # Klik tombol Submit
            print("\n✓ Validasi berhasil! Melanjutkan submit...")
            
            # Ambil screenshot sebelum submit untuk debugging
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                debug_screenshot = f"before_submit_{timestamp}.png"
                self.driver.save_screenshot(debug_screenshot)
                print(f"📸 Debug screenshot: {debug_screenshot}")
            except:
                pass
            
            print("Mencari tombol submit...")
            submit_button = None
            
            # Coba berbagai selector untuk tombol submit
            submit_selectors = [
                "button.v-btn.v-btn--elevated[type='submit']",
                "button[type='submit']",
                "button.v-btn[type='submit']",
                "//button[contains(text(), 'Submit')]",
                "//button[contains(text(), 'Kirim')]",
                "//button[contains(text(), 'Simpan')]",
                "button.v-btn.v-btn--elevated",
                "button.btn-primary[type='submit']"
            ]
            
            for selector in submit_selectors:
                try:
                    if selector.startswith("//"):
                        # XPath selector
                        submit_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        # CSS selector
                        submit_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    if submit_button:
                        print(f"✓ Tombol submit ditemukan dengan selector: {selector}")
                        break
                except:
                    continue
            
            if not submit_button:
                # Coba cari semua button dan pilih yang paling relevan
                try:
                    all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    print(f"Total buttons ditemukan: {len(all_buttons)}")
                    
                    for idx, btn in enumerate(all_buttons):
                        btn_text = btn.text.strip().lower()
                        btn_type = btn.get_attribute("type")
                        print(f"  Button {idx+1}: text='{btn_text}', type='{btn_type}'")
                        
                        if btn_type == "submit" or any(keyword in btn_text for keyword in ["submit", "kirim", "simpan"]):
                            submit_button = btn
                            print(f"✓ Tombol submit dipilih: Button {idx+1}")
                            break
                except Exception as e:
                    print(f"⚠ Error mencari manual: {e}")
            
            if not submit_button:
                raise Exception("Tombol submit tidak ditemukan dengan semua selector yang tersedia")
            
            human_delay(1, 2)
            print("Mengklik tombol submit...")
            
            # Coba click dengan JavaScript jika regular click gagal
            try:
                submit_button.click()
            except Exception as e:
                print(f"⚠ Regular click gagal, mencoba JavaScript click...")
                self.driver.execute_script("arguments[0].click();", submit_button)
            
            # Tunggu konfirmasi submit
            human_delay(3, 5)
            
            print("\n✓ Form laporan berhasil disubmit!")
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Absen selesai pada {current_time}")
            
            # Tunggu sebentar untuk memastikan submit berhasil
            time.sleep(3)
            return {
                'success': True,
                'uraian': URAIAN_AKTIVITAS,
                'pembelajaran': PEMBELAJARAN,
                'kendala': KENDALA,
                'data_source': data_source
            }
            
        except Exception as e:
            print(f"Error saat absen: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'uraian': URAIAN_AKTIVITAS,
                'pembelajaran': PEMBELAJARAN,
                'kendala': KENDALA,
                'data_source': data_source
            }
    
    def take_screenshot(self, filename="screenshot.png"):
        """Ambil screenshot sebagai bukti"""
        try:
            self.driver.save_screenshot(filename)
            print(f"Screenshot disimpan: {filename}")
        except Exception as e:
            print(f"Error saat mengambil screenshot: {str(e)}")
    
    def close(self):
        """Tutup browser"""
        if self.driver:
            self.driver.quit()
            print("Browser ditutup")

def main():
    # Credentials di-import dari config.py (sudah masuk .gitignore)
    
    print("=" * 50)
    print("Otomasi Absen MagangHub")
    print("=" * 50)
    
    # Buat instance
    attendance = MagangHubAttendance(EMAIL, PASSWORD)
    screenshot_path = None
    result = None
    
    try:
        # Setup browser
        attendance.setup_driver()
        
        # Login
        if attendance.login():
            # Lakukan absen
            result = attendance.do_attendance()
            
            if result and result.get('success'):
                # Ambil screenshot sebagai bukti
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"attendance_{timestamp}.png"
                attendance.take_screenshot(screenshot_path)
                print("\n✓ Absen berhasil dilakukan!")
                
                # Kirim notifikasi sukses
                print("\nMengirim notifikasi email...")
                email_details = {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'date': datetime.now().strftime('%d %B %Y'),
                    'status_text': 'Absen berhasil disubmit',
                    'data_source': result.get('data_source', 'Unknown'),
                    'uraian': result.get('uraian', ''),
                    'pembelajaran': result.get('pembelajaran', ''),
                    'kendala': result.get('kendala', '')
                }
                send_attendance_notification('SUCCESS', email_details, screenshot_path)
            else:
                print("\n✗ Gagal melakukan absen")
                
                # Kirim notifikasi gagal
                print("\nMengirim notifikasi email...")
                email_details = {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'date': datetime.now().strftime('%d %B %Y'),
                    'status_text': 'Absen gagal',
                    'data_source': result.get('data_source', 'Unknown') if result else 'Unknown',
                    'uraian': result.get('uraian', '') if result else '',
                    'pembelajaran': result.get('pembelajaran', '') if result else '',
                    'kendala': result.get('kendala', '') if result else '',
                    'error': result.get('error', 'Unknown error') if result else 'Unknown error'
                }
                send_attendance_notification('FAILED', email_details)
        else:
            print("\n✗ Gagal login")
            
            # Kirim notifikasi login gagal
            print("\nMengirim notifikasi email...")
            email_details = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'date': datetime.now().strftime('%d %B %Y'),
                'status_text': 'Login gagal',
                'data_source': 'N/A',
                'uraian': '',
                'pembelajaran': '',
                'kendala': '',
                'error': 'Gagal login ke sistem MagangHub'
            }
            send_attendance_notification('FAILED', email_details)
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        
        # Kirim notifikasi error
        print("\nMengirim notifikasi email...")
        email_details = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'date': datetime.now().strftime('%d %B %Y'),
            'status_text': 'Error sistem',
            'data_source': 'N/A',
            'uraian': '',
            'pembelajaran': '',
            'kendala': '',
            'error': str(e)
        }
        send_attendance_notification('FAILED', email_details)
        
    finally:
        # Tutup browser
        time.sleep(3)
        attendance.close()
        
    print("=" * 50)

if __name__ == "__main__":
    main()
