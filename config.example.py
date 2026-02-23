# Konfigurasi Credentials
# COPY file ini ke config.py dan isi dengan credential Anda

# Login credentials untuk MagangHub
EMAIL = "your_email@example.com"
PASSWORD = "your_password"

# ============================================================
# Email Notification Settings
# ============================================================

# Enable/disable email notification
ENABLE_EMAIL_NOTIFICATION = True

# Gmail credentials untuk mengirim notifikasi
# PENTING: Gunakan App Password, bukan password Gmail biasa
# Cara setup App Password:
# 1. Buka https://myaccount.google.com/security
# 2. Aktifkan 2-Step Verification
# 3. Buka https://myaccount.google.com/apppasswords
# 4. Buat App Password baru untuk "Mail"
# 5. Copy 16-digit password dan paste di bawah
NOTIFICATION_EMAIL = "your_email@gmail.com"  # Email pengirim
NOTIFICATION_PASSWORD = "your_16_digit_app_password"  # App Password (16 digit)

# Email tujuan notifikasi (bisa sama dengan NOTIFICATION_EMAIL)
RECIPIENT_EMAIL = "receiver@example.com"

# ============================================================
# Google Sheets Settings (Optional)
# ============================================================

# Google Sheets CSV URL untuk menyimpan laporan
# Cara mendapatkan URL:
# 1. Buka Google Sheet yang berisi laporan
# 2. File → Share → Publish to web
# 3. Pilih "Comma-separated values (.csv)"
# 4. Copy URL yang muncul dan paste di bawah
# Lihat GOOGLE_SHEETS_SETUP.md untuk panduan lengkap
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/YOUR_SHEET_ID/pub?output=csv"
