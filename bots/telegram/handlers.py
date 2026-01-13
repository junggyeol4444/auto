"""
텔레그램 봇 핸들러 및 스케줄러
Telegram bot handlers and scheduled notifications
"""
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, time
import asyncio

logger = logging.getLogger('telegram_handlers')


class TelegramScheduler:
    """텔레그램 정기 알림 스케줄러"""
    
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.scheduled_chats = []  # 알림을 받을 채팅 ID 리스트
    
    def setup_scheduled_jobs(self):
        """정기 작업 설정"""
        
        # 매일 오전 8시 뉴스 알림
        self.scheduler.add_job(
            self.send_morning_news,
            'cron',
            hour=8,
            minute=0,
            id='morning_news'
        )
        
        # 매일 오전 7시 날씨 알림
        self.scheduler.add_job(
            self.send_morning_weather,
            'cron',
            hour=7,
            minute=0,
            id='morning_weather'
        )
        
        # 시장 개장 시 주식 가격 알림 (오전 9시)
        self.scheduler.add_job(
            self.send_market_open,
            'cron',
            hour=9,
            minute=0,
            day_of_week='mon-fri',
            id='market_open'
        )
        
        # 1시간마다 가격 체크
        self.scheduler.add_job(
            self.check_price_alerts,
            'interval',
            hours=1,
            id='price_check'
        )
        
        logger.info('스케줄 작업이 설정되었습니다.')
    
    async def send_morning_news(self):
        """아침 뉴스 알림"""
        news_text = """
📰 오늘의 뉴스 브리핑

1. 주요 기술 뉴스
2. 경제 뉴스
3. 국제 뉴스

좋은 하루 되세요! ☀️
        """
        await self.broadcast_message(news_text)
        logger.info('아침 뉴스 전송 완료')
    
    async def send_morning_weather(self):
        """아침 날씨 알림"""
        weather_text = """
🌤️ 오늘의 날씨

서울: 맑음, 15°C
날씨 좋은 하루 되세요! 😊
        """
        await self.broadcast_message(weather_text)
        logger.info('아침 날씨 전송 완료')
    
    async def send_market_open(self):
        """시장 개장 알림"""
        market_text = """
📈 주식 시장 개장

코스피: 2,500 (+1.2%)
코스닥: 850 (+0.8%)

좋은 투자 되세요! 💰
        """
        await self.broadcast_message(market_text)
        logger.info('시장 개장 알림 전송 완료')
    
    async def check_price_alerts(self):
        """가격 알림 체크"""
        # 실제 구현에서는 데이터베이스에서 가격 조건을 확인
        logger.info('가격 알림 체크 실행')
        
        # 예시: 비트코인 가격이 목표가 도달 시
        # if bitcoin_price >= target_price:
        #     alert_text = f"🚨 비트코인이 목표가에 도달했습니다!\n현재가: {bitcoin_price}"
        #     await self.broadcast_message(alert_text)
    
    async def broadcast_message(self, message: str):
        """등록된 모든 채팅에 메시지 전송"""
        for chat_id in self.scheduled_chats:
            try:
                if self.bot.application and self.bot.application.bot:
                    await self.bot.application.bot.send_message(
                        chat_id=chat_id,
                        text=message
                    )
            except Exception as e:
                logger.error(f'메시지 전송 실패 ({chat_id}): {str(e)}')
    
    def add_chat(self, chat_id: int):
        """알림 수신 채팅 추가"""
        if chat_id not in self.scheduled_chats:
            self.scheduled_chats.append(chat_id)
            logger.info(f'채팅 추가: {chat_id}')
    
    def remove_chat(self, chat_id: int):
        """알림 수신 채팅 제거"""
        if chat_id in self.scheduled_chats:
            self.scheduled_chats.remove(chat_id)
            logger.info(f'채팅 제거: {chat_id}')
    
    def start(self):
        """스케줄러 시작"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info('스케줄러가 시작되었습니다.')
    
    def stop(self):
        """스케줄러 중지"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info('스케줄러가 중지되었습니다.')


class MessageHandler:
    """메시지 처리 헬퍼 클래스"""
    
    @staticmethod
    def format_news(news_data):
        """뉴스 데이터 포맷팅"""
        if not news_data:
            return "뉴스를 가져올 수 없습니다."
        
        formatted = "📰 최신 뉴스\n\n"
        for i, news in enumerate(news_data[:5], 1):
            formatted += f"{i}. {news.get('title', '제목 없음')}\n"
        
        return formatted
    
    @staticmethod
    def format_weather(weather_data):
        """날씨 데이터 포맷팅"""
        if not weather_data:
            return "날씨 정보를 가져올 수 없습니다."
        
        return f"""
🌤️ 날씨 정보

도시: {weather_data.get('city', '알 수 없음')}
날씨: {weather_data.get('condition', '알 수 없음')}
기온: {weather_data.get('temperature', 'N/A')}°C
습도: {weather_data.get('humidity', 'N/A')}%
        """
    
    @staticmethod
    def format_price(price_data):
        """가격 데이터 포맷팅"""
        if not price_data:
            return "가격 정보를 가져올 수 없습니다."
        
        return f"""
💰 가격 정보

종목: {price_data.get('name', '알 수 없음')}
현재가: {price_data.get('price', 'N/A')}원
변동률: {price_data.get('change', 'N/A')}%
        """


if __name__ == '__main__':
    print("텔레그램 핸들러 모듈이 로드되었습니다.")
