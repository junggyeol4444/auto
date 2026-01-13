"""
알림 전송 모듈
Notification Sender
"""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import asyncio

logger = logging.getLogger('notifier')


class Notifier:
    """알림 전송 클래스"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.email_enabled = False
        self.telegram_enabled = False
        
        # 이메일 설정
        if 'email' in self.config:
            self.email_host = self.config['email'].get('host', 'smtp.gmail.com')
            self.email_port = self.config['email'].get('port', 587)
            self.email_user = self.config['email'].get('user')
            self.email_password = self.config['email'].get('password')
            self.email_from = self.config['email'].get('from', self.email_user)
            self.email_to = self.config['email'].get('to', [])
            
            if self.email_user and self.email_password:
                self.email_enabled = True
        
        # 텔레그램 설정
        if 'telegram' in self.config:
            self.telegram_token = self.config['telegram'].get('token')
            self.telegram_chat_ids = self.config['telegram'].get('chat_ids', [])
            
            if self.telegram_token and self.telegram_chat_ids:
                self.telegram_enabled = True
    
    def send_email(self, subject: str, body: str, to_addresses: List[str] = None):
        """이메일 전송"""
        if not self.email_enabled:
            logger.warning('이메일 설정이 없습니다.')
            return False
        
        if not to_addresses:
            to_addresses = self.email_to
        
        if not to_addresses:
            logger.warning('수신자가 없습니다.')
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_from
            msg['To'] = ', '.join(to_addresses)
            
            # HTML 본문
            html_body = f"""
            <html>
              <body>
                <h2>{subject}</h2>
                <div>{body}</div>
              </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # SMTP 서버 연결
            with smtplib.SMTP(self.email_host, self.email_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            logger.info(f'이메일 전송 성공: {subject}')
            return True
        
        except Exception as e:
            logger.error(f'이메일 전송 실패: {str(e)}')
            return False
    
    async def send_telegram(self, message: str, chat_ids: List[int] = None):
        """텔레그램 메시지 전송"""
        if not self.telegram_enabled:
            logger.warning('텔레그램 설정이 없습니다.')
            return False
        
        if not chat_ids:
            chat_ids = self.telegram_chat_ids
        
        try:
            import aiohttp
            
            url = f'https://api.telegram.org/bot{self.telegram_token}/sendMessage'
            
            async with aiohttp.ClientSession() as session:
                for chat_id in chat_ids:
                    data = {
                        'chat_id': chat_id,
                        'text': message,
                        'parse_mode': 'HTML'
                    }
                    
                    async with session.post(url, json=data) as response:
                        if response.status == 200:
                            logger.info(f'텔레그램 전송 성공: {chat_id}')
                        else:
                            logger.error(f'텔레그램 전송 실패: {chat_id}')
            
            return True
        
        except Exception as e:
            logger.error(f'텔레그램 전송 실패: {str(e)}')
            return False
    
    def send_price_alert(self, product: Dict, current_price: float, target_price: float):
        """가격 알림 전송"""
        subject = f'🔔 가격 알림: {product["name"]}'
        
        body = f"""
가격이 목표가에 도달했습니다!

상품명: {product['name']}
현재가: {current_price:,.0f}원
목표가: {target_price:,.0f}원
할인율: {((target_price - current_price) / target_price * 100):.1f}%

상품 URL: {product['url']}

지금 바로 확인하세요!
        """
        
        # 이메일 전송
        if self.email_enabled:
            self.send_email(subject, body)
        
        # 텔레그램 전송
        if self.telegram_enabled:
            telegram_message = f"""
<b>🔔 가격 알림</b>

<b>{product['name']}</b>

현재가: <b>{current_price:,.0f}원</b>
목표가: {target_price:,.0f}원

<a href="{product['url']}">상품 보러가기</a>
            """
            asyncio.run(self.send_telegram(telegram_message))
    
    def send_stock_alert(self, product: Dict):
        """재고 알림 전송"""
        subject = f'📦 재고 알림: {product["name"]}'
        
        body = f"""
재고가 다시 들어왔습니다!

상품명: {product['name']}
상품 URL: {product['url']}

지금 바로 구매하세요!
        """
        
        # 이메일 전송
        if self.email_enabled:
            self.send_email(subject, body)
        
        # 텔레그램 전송
        if self.telegram_enabled:
            telegram_message = f"""
<b>📦 재고 알림</b>

<b>{product['name']}</b>

재고가 다시 들어왔습니다!

<a href="{product['url']}">상품 보러가기</a>
            """
            asyncio.run(self.send_telegram(telegram_message))
    
    def send_discount_alert(self, product: Dict, discount_rate: float):
        """할인 알림 전송"""
        subject = f'💰 할인 알림: {product["name"]}'
        
        body = f"""
큰 할인이 시작되었습니다!

상품명: {product['name']}
할인율: {discount_rate:.1f}%
상품 URL: {product['url']}

놓치지 마세요!
        """
        
        # 이메일 전송
        if self.email_enabled:
            self.send_email(subject, body)
        
        # 텔레그램 전송
        if self.telegram_enabled:
            telegram_message = f"""
<b>💰 할인 알림</b>

<b>{product['name']}</b>

할인율: <b>{discount_rate:.1f}%</b>

<a href="{product['url']}">상품 보러가기</a>
            """
            asyncio.run(self.send_telegram(telegram_message))
    
    def send_test_notification(self):
        """테스트 알림 전송"""
        subject = '테스트 알림'
        body = '알림 시스템이 정상적으로 작동하고 있습니다.'
        
        if self.email_enabled:
            return self.send_email(subject, body)
        elif self.telegram_enabled:
            return asyncio.run(self.send_telegram(body))
        else:
            logger.warning('설정된 알림 채널이 없습니다.')
            return False


if __name__ == '__main__':
    # 테스트
    notifier = Notifier()
    print("알림 모듈이 로드되었습니다.")
