import schedule
import time
import subprocess
from datetime import datetime

def run_attendance():
    """Jalankan script attendance"""
    print("\n" + "=" * 60)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Memulai absen otomatis...")
    print("=" * 60 + "\n")
    
    try:
        # Jalankan main.py
        result = subprocess.run(['python3', 'main.py'], 
                              capture_output=False, 
                              text=True, 
                              check=True)
        print("\n✓ Absen berhasil dijalankan!")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error menjalankan absen: {e}")
    except Exception as e:
        print(f"\n✗ Error: {e}")

def main():
    print("=" * 60)
    print("SCHEDULER OTOMASI ABSEN MAGANGHUB")
    print("=" * 60)
    print("Schedule: Setiap hari Senin-Jumat jam 16:00 WIB")
    print("Tekan Ctrl+C untuk menghentikan scheduler")
    print("=" * 60 + "\n")
    
    # Schedule untuk jam 16:00 setiap hari kerja
    schedule.every().monday.at("16:00").do(run_attendance)
    schedule.every().tuesday.at("16:00").do(run_attendance)
    schedule.every().wednesday.at("16:00").do(run_attendance)
    schedule.every().thursday.at("16:00").do(run_attendance)
    schedule.every().friday.at("16:00").do(run_attendance)
    
    print(f"Scheduler aktif! Menunggu jadwal berikutnya...")
    print(f"Waktu sekarang: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Loop untuk cek schedule
    while True:
        schedule.run_pending()
        time.sleep(60)  # Cek setiap 1 menit

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScheduler dihentikan oleh user.")
        print("=" * 60)
