import requests
import csv
from datetime import datetime
from io import StringIO
import os

# URL Google Sheet yang sudah di-publish as CSV
# Bisa di-override dengan environment variable GOOGLE_SHEET_CSV_URL
# atau set di config.py
try:
    from config import GOOGLE_SHEET_CSV_URL as CONFIG_URL
except ImportError:
    CONFIG_URL = None

GOOGLE_SHEET_CSV_URL = os.getenv('GOOGLE_SHEET_CSV_URL', 
                                  CONFIG_URL or 
                                  "https://docs.google.com/spreadsheets/d/e/2PACX-1vR_WWdO2CZMU5CJxZTPoznjsUqGV91p5JWzRcqzzmOjZMVS8q2yhx4SFXMQlQZmamZ7AV8jZohJas7j/pub?gid=0&single=true&output=csv")

def parse_date(date_str):
    """
    Parse berbagai format tanggal menjadi datetime object
    Support: 2026-02-23, 23-Feb-2026, 02/23/2026, dll
    """
    if not date_str:
        return None
    
    formats = [
        "%Y-%m-%d",      # 2026-02-23
        "%d-%b-%Y",      # 23-Feb-2026
        "%d-%B-%Y",      # 23-February-2026
        "%m/%d/%Y",      # 02/23/2026
        "%d/%m/%Y",      # 23/02/2026
        "%Y/%m/%d",      # 2026/02/23
        "%d-%m-%Y",      # 23-02-2026
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    
    return None

def get_laporan_from_sheet():
    """
    Ambil data laporan dari Google Sheets
    
    Format Google Sheet (kolom A-D):
    | Tanggal    | Uraian Aktivitas | Pembelajaran | Kendala |
    | 23-Feb-2026 | Text...          | Text...      | Text... |
    
    Returns:
        tuple: (uraian, pembelajaran, kendala)
    """
    try:
        print("Mengambil data dari Google Sheets...")
        
        # Fetch CSV dari Google Sheets
        response = requests.get(GOOGLE_SHEET_CSV_URL, timeout=10)
        response.raise_for_status()
        
        # Parse CSV
        csv_content = StringIO(response.text)
        reader = csv.DictReader(csv_content)
        
        today = datetime.now().date()
        
        # Cari data untuk tanggal hari ini
        latest_valid_data = None
        for row in reader:
            # Skip row kosong
            if not row.get('Tanggal'):
                continue
            
            # Parse tanggal
            row_date = parse_date(row.get('Tanggal', ''))
            if not row_date:
                continue
            
            # Skip jika data kosong atau hanya "-"
            uraian = row.get('Uraian Aktivitas', '').strip()
            pembelajaran = row.get('Pembelajaran', '').strip()
            kendala = row.get('Kendala', '').strip()
            
            if not uraian or uraian == '-':
                continue
            if not pembelajaran or pembelajaran == '-':
                continue
            if not kendala or kendala == '-':
                continue
            
            # Simpan data valid terbaru
            latest_valid_data = (row_date, uraian, pembelajaran, kendala)
            
            # Jika ada data untuk hari ini, gunakan itu
            if row_date.date() == today:
                print(f"✓ Ditemukan data untuk tanggal {today}")
                return (uraian, pembelajaran, kendala)
        
        # Jika tidak ada data hari ini, gunakan data valid terbaru
        if latest_valid_data:
            row_date, uraian, pembelajaran, kendala = latest_valid_data
            print(f"⚠ Data untuk {today} tidak ditemukan, menggunakan data terbaru dari {row_date.strftime('%Y-%m-%d')}")
            return (uraian, pembelajaran, kendala)
        
        # Jika sheet kosong atau semua data invalid
        print("✗ Tidak ada data valid di Google Sheets")
        return None, None, None
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error mengambil data dari Google Sheets: {e}")
        print("⚠ Menggunakan data dari laporan_template.py")
        return None, None, None
    except Exception as e:
        print(f"✗ Error parsing data: {e}")
        print("⚠ Menggunakan data dari laporan_template.py")
        return None, None, None

def get_laporan():
    """
    Ambil data laporan (prioritas: Google Sheets -> Local Template)
    
    Returns:
        tuple: (uraian, pembelajaran, kendala)
    """
    # Coba ambil dari Google Sheets dulu
    uraian, pembelajaran, kendala = get_laporan_from_sheet()
    
    # Jika gagal, fallback ke local template
    if not uraian or not pembelajaran or not kendala:
        print("Menggunakan template lokal...")
        from laporan_template import URAIAN_AKTIVITAS, PEMBELAJARAN, KENDALA
        return URAIAN_AKTIVITAS, PEMBELAJARAN, KENDALA
    
    return uraian, pembelajaran, kendala

if __name__ == "__main__":
    # Testing
    print("Testing Google Sheets integration...")
    uraian, pembelajaran, kendala = get_laporan()
    print(f"\nUraian: {uraian[:50]}...")
    print(f"Pembelajaran: {pembelajaran[:50]}...")
    print(f"Kendala: {kendala[:50]}...")
