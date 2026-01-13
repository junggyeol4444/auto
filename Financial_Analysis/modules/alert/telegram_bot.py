"""
텔레그램 봇 알림 모듈
"""
import asyncio
from typing import Optional


class TelegramAlert:
    def __init__(self, bot_token: str = "", chat_id: str = ""):
        """텔레그램 알림 초기화"""
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.enabled = bool(bot_token and chat_id)
    
    async def send_message_async(self, message: str) -> bool:
        """비동기 메시지 전송"""
        if not self.enabled:
            print("텔레그램 설정이 없습니다.")
            return False
        
        try:
            import aiohttp
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, timeout=10) as response:
                    if response.status == 200:
                        print(f"텔레그램 메시지 전송 성공: {message[:50]}")
                        return True
                    else:
                        print(f"텔레그램 전송 실패: {response.status}")
                        return False
        except Exception as e:
            print(f"텔레그램 전송 오류: {e}")
            return False
    
    def send_message(self, message: str) -> bool:
        """동기 메시지 전송"""
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.send_message_async(message))
        except RuntimeError:
            # 이벤트 루프가 없는 경우 새로 생성
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.send_message_async(message))
            loop.close()
            return result
    
    def send_alert(self, title: str, content: str, alert_type: str = "INFO") -> bool:
        """알림 전송"""
        emoji = {
            "INFO": "ℹ️",
            "WARNING": "⚠️",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "PRICE": "💰",
            "TREND": "📈"
        }.get(alert_type, "📢")
        
        message = f"{emoji} <b>{title}</b>\n\n{content}"
        return self.send_message(message)
    
    def send_price_alert(self, asset: str, current_price: float, target_price: float) -> bool:
        """가격 알림 전송"""
        title = f"{asset} 가격 알림"
        content = f"목표가: {target_price:,.2f}원\n현재가: {current_price:,.2f}원\n\n목표가에 도달했습니다!"
        return self.send_alert(title, content, "PRICE")
