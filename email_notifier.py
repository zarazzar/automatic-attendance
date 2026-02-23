import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os

class EmailNotifier:
    def __init__(self, smtp_email, smtp_password, recipient_email):
        self.smtp_email = smtp_email
        self.smtp_password = smtp_password
        self.recipient_email = recipient_email
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_notification(self, status, details, screenshot_path=None):
        """
        Kirim notifikasi email tentang hasil absen
        
        Args:
            status (str): "SUCCESS" atau "FAILED"
            details (dict): Detail informasi absen
            screenshot_path (str): Path ke screenshot (optional)
        """
        try:
            # Buat email message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"[MagangHub] Absen {status} - {datetime.now().strftime('%d %B %Y')}"
            
            # Buat body email
            body = self._create_email_body(status, details)
            msg.attach(MIMEText(body, 'html'))
            
            # Attach screenshot jika ada
            if screenshot_path and os.path.exists(screenshot_path):
                self._attach_file(msg, screenshot_path)
            
            # Kirim email via Gmail SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_email, self.smtp_password)
            text = msg.as_string()
            server.sendmail(self.smtp_email, self.recipient_email, text)
            server.quit()
            
            print(f"✓ Notifikasi email berhasil dikirim ke {self.recipient_email}")
            return True
            
        except Exception as e:
            print(f"✗ Gagal mengirim email: {str(e)}")
            return False
    
    def _create_email_body(self, status, details):
        """Buat HTML body untuk email"""
        status_color = "#4CAF50" if status == "SUCCESS" else "#F44336"
        status_icon = "✓" if status == "SUCCESS" else "✗"
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: {status_color}; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ background-color: #f9f9f9; padding: 20px; margin-top: 20px; border-radius: 5px; }}
                .info-row {{ margin: 10px 0; padding: 10px; background-color: white; border-left: 3px solid {status_color}; }}
                .label {{ font-weight: bold; color: #555; }}
                .footer {{ margin-top: 20px; text-align: center; color: #888; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{status_icon} Absen {status}</h1>
                    <p>{details.get('timestamp', 'N/A')}</p>
                </div>
                
                <div class="content">
                    <h2>Detail Absen</h2>
                    
                    <div class="info-row">
                        <span class="label">Status:</span> {details.get('status_text', 'N/A')}
                    </div>
                    
                    <div class="info-row">
                        <span class="label">Tanggal:</span> {details.get('date', 'N/A')}
                    </div>
                    
                    <div class="info-row">
                        <span class="label">Sumber Data:</span> {details.get('data_source', 'N/A')}
                    </div>
                    
                    <div class="info-row">
                        <span class="label">Uraian Aktivitas:</span><br>
                        {details.get('uraian', 'N/A')[:150]}{'...' if len(details.get('uraian', '')) > 150 else ''}
                        <br><small>({len(details.get('uraian', ''))} karakter)</small>
                    </div>
                    
                    <div class="info-row">
                        <span class="label">Pembelajaran:</span><br>
                        {details.get('pembelajaran', 'N/A')[:150]}{'...' if len(details.get('pembelajaran', '')) > 150 else ''}
                        <br><small>({len(details.get('pembelajaran', ''))} karakter)</small>
                    </div>
                    
                    <div class="info-row">
                        <span class="label">Kendala:</span><br>
                        {details.get('kendala', 'N/A')[:150]}{'...' if len(details.get('kendala', '')) > 150 else ''}
                        <br><small>({len(details.get('kendala', ''))} karakter)</small>
                    </div>
                    
                    {f'<div class="info-row"><span class="label">Error:</span><br>{details.get("error", "")}</div>' if details.get('error') else ''}
                </div>
                
                <div class="footer">
                    <p>Automated Attendance System - MagangHub Kemnaker</p>
                    <p>Email ini dikirim otomatis, tidak perlu dibalas</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def _attach_file(self, msg, filepath):
        """Attach file ke email"""
        try:
            with open(filepath, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                filename = os.path.basename(filepath)
                part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                msg.attach(part)
        except Exception as e:
            print(f"⚠ Gagal attach file: {str(e)}")

def send_attendance_notification(status, details, screenshot_path=None):
    """
    Fungsi helper untuk mengirim notifikasi
    Akan check config terlebih dahulu
    """
    try:
        from config import NOTIFICATION_EMAIL, NOTIFICATION_PASSWORD, RECIPIENT_EMAIL, ENABLE_EMAIL_NOTIFICATION
        
        if not ENABLE_EMAIL_NOTIFICATION:
            print("⚠ Notifikasi email dinonaktifkan di config")
            return False
        
        if not NOTIFICATION_EMAIL or not NOTIFICATION_PASSWORD:
            print("⚠ Email credentials tidak diset di config.py")
            return False
        
        notifier = EmailNotifier(NOTIFICATION_EMAIL, NOTIFICATION_PASSWORD, RECIPIENT_EMAIL)
        return notifier.send_notification(status, details, screenshot_path)
        
    except ImportError as e:
        print(f"⚠ Config email belum disetup: {str(e)}")
        return False
    except Exception as e:
        print(f"⚠ Error mengirim notifikasi: {str(e)}")
        return False
