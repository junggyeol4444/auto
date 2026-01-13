"""
이메일 알림 모듈
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional


class EmailAlert:
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587,
                 sender_email: str = "", sender_password: str = ""):
        """이메일 알림 초기화"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.enabled = bool(sender_email and sender_password)
    
    def send_email(self, recipient: str, subject: str, body: str, is_html: bool = False) -> bool:
        """이메일 전송"""
        if not self.enabled:
            print("이메일 설정이 없습니다.")
            return False
        
        try:
            # 이메일 메시지 생성
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient
            
            # 본문 추가
            mime_type = "html" if is_html else "plain"
            part = MIMEText(body, mime_type)
            message.attach(part)
            
            # SMTP 서버 연결 및 전송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient, message.as_string())
            
            print(f"이메일 전송 성공: {recipient}")
            return True
            
        except Exception as e:
            print(f"이메일 전송 오류: {e}")
            return False
    
    def send_alert(self, recipient: str, title: str, content: str, alert_type: str = "INFO") -> bool:
        """알림 이메일 전송"""
        subject = f"[금융 알림] {title}"
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: #4CAF50; color: white; padding: 10px; }}
                .content {{ padding: 20px; }}
                .footer {{ font-size: 12px; color: #888; padding: 10px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>{title}</h2>
            </div>
            <div class="content">
                <p>{content.replace(chr(10), '<br>')}</p>
            </div>
            <div class="footer">
                <p>이 메시지는 금융 데이터 분석 시스템에서 자동 발송되었습니다.</p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(recipient, subject, html_body, is_html=True)
    
    def send_price_alert(self, recipient: str, asset: str, current_price: float, target_price: float) -> bool:
        """가격 알림 이메일 전송"""
        title = f"{asset} 가격 알림"
        content = f"""
        목표가: {target_price:,.2f}원
        현재가: {current_price:,.2f}원
        
        목표가에 도달했습니다!
        """
        return self.send_alert(recipient, title, content, "PRICE")
