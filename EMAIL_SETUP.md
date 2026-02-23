# Setup Email Notification

Panduan setup notifikasi email untuk sistem absen otomatis MagangHub.

## 📧 Fitur Email Notification

Sistem akan mengirim email otomatis setiap kali:
- ✅ Absen berhasil disubmit
- ❌ Absen gagal (validasi error, login gagal, dll)
- 📊 Include detail lengkap (data yang disubmit, timestamp, screenshot)

---

## 🔐 Setup Gmail App Password

Google tidak mengizinkan login dengan password biasa untuk aplikasi pihak ketiga. Anda harus menggunakan **App Password**.

### Langkah-langkah:

#### 1. Aktifkan 2-Step Verification
- Buka: https://myaccount.google.com/security
- Scroll ke **"Signing in to Google"**
- Klik **"2-Step Verification"** → **"Get Started"**
- Ikuti petunjuk untuk setup verifikasi 2 langkah

#### 2. Buat App Password
- Buka: https://myaccount.google.com/apppasswords
- Atau dari halaman Security → 2-Step Verification → scroll bawah ke **"App passwords"**
- Klik **"Select app"** → pilih **"Mail"**
- Klik **"Select device"** → pilih **"Other"** → ketik: `MagangHub Attendance`
- Klik **"Generate"**
- Google akan menampilkan **16-digit password** (contoh: `abcd efgh ijkl mnop`)
- **COPY password ini!** (tidak termasuk spasi)

#### 3. Masukkan ke config.py
```python
# config.py
ENABLE_EMAIL_NOTIFICATION = True
NOTIFICATION_EMAIL = "email@gmail.com"  # Email Gmail Anda
NOTIFICATION_PASSWORD = "abcdefghijklmnop"  # 16-digit App Password (tanpa spasi)
RECIPIENT_EMAIL = "email@gmail.com"  # Email penerima notifikasi
```

---

## ⚙️ Konfigurasi

Edit file `config.py`:

```python
# Enable/disable notifikasi (True = aktif, False = nonaktif)
ENABLE_EMAIL_NOTIFICATION = True

# Email pengirim (Gmail yang punya App Password)
NOTIFICATION_EMAIL = "your-email@gmail.com"

# App Password (16 digit, tanpa spasi)
NOTIFICATION_PASSWORD = "abcdefghijklmnop"

# Email penerima (bisa sama dengan pengirim)
RECIPIENT_EMAIL = "recipient@gmail.com"
```

---

## 📋 Format Email

Email yang dikirim berisi:

### Header
- Status: SUCCESS ✅ atau FAILED ❌
- Timestamp lengkap

### Detail
- Tanggal absen
- Sumber data (Google Sheets / Local Template)
- Uraian Aktivitas (preview + jumlah karakter)
- Pembelajaran (preview + jumlah karakter)
- Kendala (preview + jumlah karakter)
- Error message (jika gagal)

### Attachment
- Screenshot bukti absen (jika sukses)

---

## 🧪 Testing

Test notifikasi email:

```bash
python3 -c "from email_notifier import send_attendance_notification; send_attendance_notification('SUCCESS', {'timestamp': '2026-02-23 16:00:00', 'date': '23 February 2026', 'status_text': 'Test notification', 'data_source': 'Test', 'uraian': 'Test uraian', 'pembelajaran': 'Test pembelajaran', 'kendala': 'Test kendala'})"
```

---

## ❗ Troubleshooting

### Error: "Username and Password not accepted"
- ✅ Pastikan 2-Step Verification sudah aktif
- ✅ Gunakan App Password, bukan password Gmail biasa
- ✅ Copy App Password tanpa spasi

### Error: "SMTPAuthenticationError"
- ✅ App Password salah atau expired
- ✅ Buat App Password baru

### Notifikasi tidak terkirim
- ✅ Cek `ENABLE_EMAIL_NOTIFICATION = True` di config.py
- ✅ Cek koneksi internet
- ✅ Cek email tidak masuk spam

### Email masuk ke Spam
- Buka email di folder Spam
- Klik "Not Spam" / "Report not spam"
- Email berikutnya akan masuk ke Inbox

---

## 🔒 Keamanan

- ✅ `config.py` sudah ada di `.gitignore` (tidak akan ter-commit ke Git)
- ✅ App Password hanya bisa dipakai untuk email, tidak bisa login ke akun Gmail
- ✅ Anda bisa revoke App Password kapan saja di: https://myaccount.google.com/apppasswords
- ⚠️ Jangan share `config.py` atau App Password ke siapapun

---

## 📝 Non-aktivasi Notifikasi

Jika tidak ingin pakai notifikasi email:

```python
# config.py
ENABLE_EMAIL_NOTIFICATION = False
```

Atau kosongkan credentials:

```python
NOTIFICATION_EMAIL = ""
NOTIFICATION_PASSWORD = ""
```

---

## 💡 Tips

- Gunakan email terpisah khusus untuk notifikasi (opsional)
- Buat filter/label otomatis di Gmail untuk email dari sistem ini
- Buat multiple recipient dengan separator koma (belum support, bisa dikembangkan)

---

**Happy Automating! 🚀**
