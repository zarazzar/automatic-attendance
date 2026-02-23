# Setup GitHub Actions untuk Otomasi Absen MagangHub

Panduan lengkap untuk menjalankan otomasi absen di GitHub Actions - **GRATIS dan tanpa perlu server!**

## Keuntungan GitHub Actions

✅ **Gratis**: Unlimited untuk public repo, 2,000 menit/bulan untuk private repo  
✅ **Tanpa Server**: Tidak perlu maintain VPS atau cloud server  
✅ **Otomatis**: Jalan sesuai jadwal tanpa perlu komputer menyala  
✅ **Reliable**: Infrastructure managed oleh GitHub  
✅ **Logging**: Semua logs tersimpan dan bisa diakses kapan saja  

## Cara Setup

### 1. Push Project ke GitHub

```bash
# Jika belum init git
git init
git add .
git commit -m "Initial commit"

# Buat repository baru di GitHub, lalu:
git remote add origin https://github.com/username/repo-name.git
git branch -M main
git push -u origin main
```

### 2. Setup GitHub Secrets

Secrets adalah cara aman untuk menyimpan data sensitif seperti password.

**Cara menambahkan Secrets:**
1. Buka repository di GitHub
2. Klik **Settings** → **Secrets and variables** → **Actions**
3. Klik **New repository secret**
4. Tambahkan secrets berikut:

#### Required Secrets:

| Secret Name | Description | Contoh Value |
|-------------|-------------|--------------|
| `MAGANGHUB_EMAIL` | Email login MagangHub | `your.email@example.com` |
| `MAGANGHUB_PASSWORD` | Password MagangHub | `yourpassword123` |
| `SENDER_EMAIL` | Email pengirim notifikasi | `your.email@gmail.com` |
| `SENDER_PASSWORD` | Password email atau App Password | `your_app_password` |
| `RECEIVER_EMAIL` | Email penerima notifikasi | `notification@example.com` |
| `GOOGLE_SHEET_CSV_URL` | *(Optional)* URL CSV dari Google Sheets | `https://docs.google.com/.../pub?output=csv` |

#### Cara Mendapatkan Google Sheets CSV URL:

**Project ini pakai cara SEDERHANA tanpa perlu credentials ribet!**

1. Buka Google Sheet yang sudah kamu isi dengan data laporan
2. Klik **File** → **Share** → **Publish to web**
3. Tab **Link**:
   - Dropdown 1: Pilih sheet yang mau dipublish
   - Dropdown 2: Pilih **Comma-separated values (.csv)**
4. Klik **Publish** → Copy URL yang muncul
5. Paste URL tersebut ke GitHub Secret `GOOGLE_SHEET_CSV_URL`

**Format Sheet** harus punya kolom:
- **Tanggal** (format: YYYY-MM-DD atau DD-MMM-YYYY)
- **Uraian Aktivitas** (minimal 100 karakter)
- **Pembelajaran** (minimal 100 karakter)  
- **Kendala** (minimal 100 karakter)

**Catatan:** 
- Secret `GOOGLE_SHEET_CSV_URL` bersifat **OPTIONAL**
- Jika tidak diset, akan menggunakan URL default yang ada di `google_sheets.py`
- Jika URL invalid atau Google Sheets tidak digunakan, script akan fallback ke template lokal

📖 Detail lengkap: Lihat [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)

### 3. Verifikasi Workflow File

File workflow sudah otomatis dibuat di `.github/workflows/attendance.yml`

**Konfigurasi default:**
- **Jadwal**: Senin-Jumat jam 16:00 WIB (09:00 UTC)
- **Manual Trigger**: Bisa dijalankan manual kapan saja

#### Mengubah Jadwal

Edit file `.github/workflows/attendance.yml`, ubah bagian cron:

```yaml
on:
  schedule:
    # Format: 'menit jam * * hari_dalam_minggu'
    # 0-6: Minggu=0, Senin=1, ..., Sabtu=6
    
    # Contoh: Senin-Jumat jam 08:00 WIB (01:00 UTC)
    - cron: '0 1 * * 1-5'
    
    # Contoh: Setiap hari jam 16:00 WIB (09:00 UTC)
    - cron: '0 9 * * *'
```

**Catatan Timezone:**
- GitHub Actions menggunakan UTC
- WIB = UTC+7, jadi kurangi 7 jam
- Contoh: 16:00 WIB = 09:00 UTC

### 4. Test Manual Execution

Sebelum menunggu jadwal otomatis, test dulu secara manual:

1. Buka repository di GitHub
2. Klik tab **Actions**
3. Pilih workflow **Automatic Attendance MagangHub**
4. Klik **Run workflow** → **Run workflow**
5. Tunggu beberapa menit dan lihat hasilnya

### 5. Monitor Execution

**Melihat Logs:**
1. Klik tab **Actions**
2. Klik pada workflow run yang ingin dilihat
3. Klik job **attendance**
4. Expand setiap step untuk melihat detail logs

**Download Logs:**
- Logs otomatis disimpan di artifacts
- Tersedia selama 30 hari
- Bisa didownload di bagian bawah workflow run

## Troubleshooting

### Workflow Tidak Jalan Sesuai Jadwal

**Penyebab umum:**
- Repository tidak aktif dalam 60 hari terakhir
- Scheduled workflows disabled untuk repository baru

**Solusi:**
1. Check Settings → Actions → General
2. Pastikan "Allow all actions and reusable workflows" enabled
3. Lakukan commit minimal sebulan sekali untuk keep repository active

### Error: Secrets Not Found

**Solusi:**
- Pastikan semua secrets sudah ditambahkan dengan nama yang TEPAT
- Nama secret case-sensitive
- Tidak ada spasi di awal/akhir value

### Error: Chrome/ChromeDriver Issues

**Error: "Process completed with exit code 8" pada Install ChromeDriver**

**Penyebab:**
- Google mengubah cara distribusi ChromeDriver (tidak lagi pakai URL lama)
- Method install ChromeDriver sudah tidak compatible

**Solusi:**
- ✅ **Sudah diperbaiki!** Workflow sekarang menggunakan `browser-actions/setup-chrome` action yang lebih reliable
- Action ini otomatis install Chrome + ChromeDriver yang matching
- Jika masih error, coba:
  1. Re-run workflow (kadang network issue temporary)
  2. Check logs untuk detail error spesifik
  3. Pastikan menggunakan workflow file yang terbaru

**Error lainnya:**
- Jika masih error, cek logs untuk detail errornya
- Biasanya karena compatibility issue antara Chrome dan driver

### Error: SyntaxError: invalid decimal literal

**Error pada "Create google_sheets.py with CSV URL" atau "Run attendance script"**

**Penyebab:**
- Sed command error karena special characters di URL
- File google_sheets.py corrupted

**Solusi:**
- ✅ **Sudah diperbaiki!** Sekarang menggunakan environment variable yang lebih reliable
- Google Sheets URL di-inject via environment variable, bukan di-edit dengan sed
- Jika masih error:
  1. Pastikan secret `GOOGLE_SHEET_CSV_URL` terisi dengan benar (atau kosongkan jika tidak pakai)
  2. Re-run workflow
  3. Check bahwa workflow file sudah yang terbaru (ada `GOOGLE_SHEET_CSV_URL: ${{ secrets.GOOGLE_SHEET_CSV_URL }}` di env)

### Login Gagal

**Penyebab:**
- Captcha terdeteksi (GitHub Actions IP berubah-ubah)
- Session cookies tidak persist di CI environment

**Solusi:**
- Script sudah pakai random delays untuk menghindari detection
- Jika sering gagal, pertimbangkan tambah delay atau gunakan proxy

## Tips & Best Practices

### 1. Security
- **Jangan** commit file `config.py` yang berisi credentials
- Gunakan `.gitignore` untuk exclude file sensitive
- Selalu gunakan GitHub Secrets untuk data sensitif

### 2. Testing
- Test manual execution dulu sebelum rely on schedule
- Monitor logs beberapa hari pertama
- Set notifikasi email untuk workflow failures

### 3. Optimization
- GitHub Actions punya limit 2,000 menit/bulan untuk private repo
- 1x run biasanya ~2-5 menit
- Dengan 5 hari kerja × 4 minggu = 20 runs/bulan
- Total: ~100 menit/bulan (masih jauh dari limit)

### 4. Notifications
- Enable email notifications untuk workflow failures
- Settings → Notifications → Actions
- Centang "Send notifications for failed workflows"

## Disable/Enable Automation

### Temporary Disable
Jika mau disable sementara (misalnya sedang cuti):

**Option 1: Disable Workflow**
1. Go to Actions tab
2. Pilih workflow "Automatic Attendance MagangHub"
3. Klik tombol "..." → Disable workflow

**Option 2: Comment Cron Schedule**
Edit `.github/workflows/attendance.yml`:
```yaml
on:
  # schedule:
  #   - cron: '0 9 * * 1-5'
  workflow_dispatch:  # Keep manual trigger
```

### Re-enable
- Uncomment schedule atau enable workflow kembali

## Biaya & Limits

### Free Tier (Public Repository)
- ✅ **Unlimited** minutes
- ✅ Tidak perlu kartu kredit
- ✅ Cocok untuk project open source

### Free Tier (Private Repository)
- 📦 2,000 minutes/month
- ✅ Cukup untuk ~400 runs
- ✅ Tidak perlu kartu kredit

### Paid Plans
- Bayar hanya jika melebihi free tier
- $0.008 per minute untuk private repo
- Public repo tetap unlimited

## FAQ

**Q: Apakah aman menyimpan password di GitHub Secrets?**  
A: Ya, GitHub Secrets dienkripsi dan tidak akan terlihat di logs atau oleh siapapun (termasuk collaborators).

**Q: Bisa dijalankan lebih dari 1x sehari?**  
A: Ya, tinggal tambahkan schedule baru di workflow file.

**Q: Bagaimana jika MagangHub maintenance?**  
A: Script akan mencoba dan mungkin gagal, tapi akan retry di schedule berikutnya.

**Q: Bisa lihat browser saat jalan?**  
A: Tidak, GitHub Actions jalan headless. Tapi bisa lihat screenshot jika perlu (tambahkan step untuk screenshot).

**Q: Repository harus public atau private?**  
A: Bisa keduanya. Public = unlimited, Private = 2,000 min/bulan.

## Monitoring & Maintenance

### Weekly Check
- ✅ Cek Actions tab untuk verify workflow success
- ✅ Check email notifications
- ✅ Review logs jika ada anomali

### Monthly Maintenance
- 🔄 Update dependencies jika ada security alerts
- 📊 Review workflow run history
- 🧹 Hapus logs artifacts lama jika perlu

## Support

Jika ada masalah:
1. Check workflow logs di Actions tab
2. Verify semua secrets sudah benar
3. Test manual execution untuk debugging
4. Check jam terakhir successful run

---

**🎉 Setup Complete!**

Setelah setup, script akan jalan otomatis sesuai jadwal. Anda tidak perlu melakukan apapun lagi!

Monitor via Actions tab untuk memastikan semuanya berjalan lancar. 🚀
