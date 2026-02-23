# Setup Google Sheets untuk Laporan Otomatis

## Langkah Setup Google Sheets:

### 1. Buat Google Sheet Baru

Buka [Google Sheets](https://sheets.google.com) dan buat sheet baru dengan format:

| Tanggal    | Uraian Aktivitas                                      | Pembelajaran                                          | Kendala                                              |
|------------|------------------------------------------------------|------------------------------------------------------|-----------------------------------------------------|
| 2026-02-23 | Melakukan review kode dan testing aplikasi...        | Mempelajari design patterns dan best practices...    | Tidak ada kendala berarti...                        |
| 2026-02-24 | Mengembangkan fitur baru untuk sistem...             | Memahami lebih dalam tentang database optimization..  | Sedikit kendala di konfigurasi server...            |

**Penting:**
- Kolom A: **Tanggal** (format: YYYY-MM-DD)
- Kolom B: **Uraian Aktivitas** (minimal 100 karakter)
- Kolom C: **Pembelajaran** (minimal 100 karakter)
- Kolom D: **Kendala** (minimal 100 karakter)
- Baris 1 adalah header

### 2. Publish Sheet as CSV

1. Di Google Sheets, klik **File** → **Share** → **Publish to web**
2. Pilih **Link** tab
3. Pada dropdown pertama, pilih sheet yang ingin dipublish
4. Pada dropdown kedua, pilih **Comma-separated values (.csv)**
5. Klik **Publish**
6. Copy URL yang muncul (contoh: `https://docs.google.com/spreadsheets/d/e/2PACX-...../pub?output=csv`)

### 3. Update google_sheets.py

Edit file `google_sheets.py` dan ganti `GOOGLE_SHEET_CSV_URL` dengan URL yang sudah di-copy:

```python
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/YOUR_SHEET_ID/pub?output=csv"
```

### 4. Install Dependency

```bash
pip install requests
```

### 5. Test Connection

```bash
python3 google_sheets.py
```

## Cara Kerja:

1. **Script akan cari data untuk tanggal hari ini**
   - Jika ada → gunakan data tersebut
   - Jika tidak ada → gunakan data paling baru di sheet

2. **Fallback ke Local Template**
   - Jika Google Sheets error atau tidak bisa diakses
   - Script otomatis gunakan `laporan_template.py`

3. **Update Laporan**
   - Tinggal edit Google Sheets
   - Tidak perlu edit code atau restart script
   - Perubahan langsung terpakai di run berikutnya

## Tips:

- Isi data untuk beberapa hari ke depan di Google Sheets
- Script akan otomatis ambil data sesuai tanggal
- Pastikan minimal 100 karakter untuk setiap kolom
- Bisa share Google Sheets dengan tim untuk kolaborasi

## Testing:

1. Isi 1 baris data dengan tanggal hari ini
2. Jalankan: `python3 google_sheets.py`
3. Pastikan data terambil dengan benar
4. Jalankan: `python3 main.py` untuk test full flow

## Troubleshooting:

**Error "Failed to fetch":**
- Pastikan sheet sudah di-publish dengan benar
- Cek URL CSV sudah benar
- Pastikan ada koneksi internet

**Data tidak sesuai:**
- Periksa format tanggal (harus YYYY-MM-DD)
- Periksa nama kolom header sesuai (Tanggal, Uraian Aktivitas, Pembelajaran, Kendala)
- Pastikan tidak ada spasi extra di nama kolom
