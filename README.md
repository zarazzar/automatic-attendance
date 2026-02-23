# Otomasi Absen MagangHub

Script Python untuk otomasi absensi di platform MagangHub menggunakan Selenium.

## Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Chrome WebDriver (jika belum ada):
```bash
# Atau download manual dari https://chromedriver.chromium.org/
```

## Konfigurasi

Edit file `main.py` dan ganti credential Anda:
```python
EMAIL = "your_email@example.com"
PASSWORD = "your_password"
```

## Cara Menggunakan

Jalankan script:
```bash
python main.py
```

## Catatan Penting

⚠️ **PERHATIAN**: Script ini perlu disesuaikan dengan struktur HTML web MagangHub yang sebenarnya:

1. **Selector Element**: Periksa selector untuk:
   - Field email: `By.NAME, "email"`
   - Field password: `By.NAME, "password"`
   - Tombol login: `button[type='submit']`
   - Tombol absen: `button.attendance-button`

2. **URL**: Sesuaikan URL:
   - Login page: `https://maganghub.com/login`
   - Attendance page: `https://maganghub.com/attendance`

3. **Cara Menemukan Selector yang Benar**:
   - Buka web MagangHub di browser
   - Klik kanan pada elemen → Inspect
   - Lihat HTML structure untuk menemukan selector yang tepat (id, class, name, dll)

## Fitur

- ✅ Auto login ke MagangHub
- ✅ Auto absen (clock in/out)
- ✅ Screenshot otomatis sebagai bukti
- ✅ Error handling
- ✅ Timestamp pada setiap screenshot

## Automasi dengan Cron/Task Scheduler

### Opsi 1: Menggunakan Scheduler Python (Recommended)

1. Install dependency schedule:
```bash
pip install schedule
```

2. Jalankan scheduler (akan berjalan terus di background):
```bash
python3 scheduler.py
```

Scheduler akan menjalankan absen otomatis setiap hari kerja (Senin-Jumat) jam 16:00 WIB.

### Opsi 2: macOS Cron Job

1. Buat folder logs:
```bash
mkdir -p logs
```

2. Berikan permission execute ke script:
```bash
chmod +x run_attendance.sh
```

3. Edit crontab:
```bash
crontab -e
```

4. Tambahkan line berikut (absen jam 16:00 setiap hari kerja):
```bash
0 16 * * 1-5 cd /Users/capyzara/Desktop/automation/automatic-attendance && ./run_attendance.sh
```

5. Simpan dan keluar (ESC lalu :wq di vim)

6. Verifikasi cron sudah terdaftar:
```bash
crontab -l
```

### Opsi 3: macOS launchd (Recommended untuk macOS)

Akan menjalankan lebih reliable daripada cron di macOS.

1. Buat file plist di `~/Library/LaunchAgents/com.maganghub.attendance.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.maganghub.attendance</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/capyzara/Desktop/automation/automatic-attendance/main.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>16</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/capyzara/Desktop/automation/automatic-attendance/logs/attendance.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/capyzara/Desktop/automation/automatic-attendance/logs/attendance_error.log</string>
</dict>
</plist>
```

2. Load launchd agent:
```bash
launchctl load ~/Library/LaunchAgents/com.maganghub.attendance.plist
```

3. Untuk unload (stop):
```bash
launchctl unload ~/Library/LaunchAgents/com.maganghub.attendance.plist
```

### Windows (Task Scheduler):

1. Buka Task Scheduler
2. Create Basic Task
3. Set trigger (waktu absen)
4. Action: Start a program → python.exe
5. Arguments: path ke main.py

## Troubleshooting

- **Chrome driver error**: Pastikan Chrome browser terinstall dan driver compatible
- **Element not found**: Periksa selector HTML yang digunakan
- **Login failed**: Verifikasi credential dan URL login
- **Headless mode**: Uncomment baris `chrome_options.add_argument('--headless')` untuk menjalankan tanpa UI

## Disclaimer

Script ini untuk keperluan pembelajaran. Pastikan penggunaan otomasi ini sesuai dengan kebijakan MagangHub.
