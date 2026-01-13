"""
텔레그램 봇 메인 모듈
Telegram Bot with comprehensive features
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ContextTypes, CallbackQueryHandler
)
from datetime import datetime, time
import asyncio

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('telegram_bot')


class TelegramBot:
    """텔레그램 봇 메인 클래스"""
    
    def __init__(self, token=None):
        self.token = token
        self.application = None
        self.is_running = False
        
        # 자동 응답 키워드
        self.auto_responses = {
            '안녕': '안녕하세요! 무엇을 도와드릴까요?',
            '도움': '명령어: /start, /help, /weather, /news, /price',
            '날씨': '날씨 정보를 원하시면 /weather 도시명 을 입력하세요.'
        }
    
    def setup_handlers(self):
        """핸들러 설정"""
        if not self.application:
            return
        
        # 명령어 핸들러
        self.application.add_handler(CommandHandler('start', self.start_command))
        self.application.add_handler(CommandHandler('help', self.help_command))
        self.application.add_handler(CommandHandler('weather', self.weather_command))
        self.application.add_handler(CommandHandler('news', self.news_command))
        self.application.add_handler(CommandHandler('price', self.price_command))
        self.application.add_handler(CommandHandler('button', self.button_command))
        self.application.add_handler(CommandHandler('menu', self.menu_command))
        
        # 콜백 쿼리 핸들러
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # 메시지 핸들러
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        
        # 사진 핸들러
        self.application.add_handler(
            MessageHandler(filters.PHOTO, self.handle_photo)
        )
        
        # 문서 핸들러
        self.application.add_handler(
            MessageHandler(filters.Document.ALL, self.handle_document)
        )
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """시작 명령어"""
        user = update.effective_user
        welcome_text = (
            f'안녕하세요, {user.first_name}님! 🎉\n\n'
            '텔레그램 봇에 오신 것을 환영합니다.\n'
            '사용 가능한 명령어를 보려면 /help를 입력하세요.'
        )
        await update.message.reply_text(welcome_text)
        logger.info(f'사용자 시작: {user.username}')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """도움말 명령어"""
        help_text = """
📚 사용 가능한 명령어:

/start - 봇 시작
/help - 도움말 보기
/weather [도시] - 날씨 정보
/news - 최신 뉴스
/price [종목] - 가격 정보
/button - 인라인 버튼 예시
/menu - 메뉴 버튼

💬 자동 응답 키워드:
- 안녕, 도움, 날씨
        """
        await update.message.reply_text(help_text)
    
    async def weather_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """날씨 명령어"""
        if context.args:
            city = ' '.join(context.args)
        else:
            city = '서울'
        
        weather_text = f"""
🌤️ {city} 날씨 정보

날씨: 맑음
기온: 15°C
습도: 60%
풍속: 2m/s

* 실제 API 연동 시 실시간 데이터 제공
        """
        await update.message.reply_text(weather_text)
    
    async def news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """뉴스 명령어"""
        news_text = """
📰 최신 뉴스

1. 기술 뉴스 헤드라인 1
2. 경제 뉴스 헤드라인 2
3. 정치 뉴스 헤드라인 3

* 실제 뉴스 API 연동 시 실시간 뉴스 제공
        """
        await update.message.reply_text(news_text)
    
    async def price_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """가격 정보 명령어"""
        if context.args:
            item = ' '.join(context.args)
        else:
            item = '비트코인'
        
        price_text = f"""
💰 {item} 가격 정보

현재가: 50,000,000원
24시간 변동: +5.2%
거래량: 1,234 BTC

* 실제 API 연동 시 실시간 가격 제공
        """
        await update.message.reply_text(price_text)
    
    async def button_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """인라인 버튼 예시"""
        keyboard = [
            [
                InlineKeyboardButton("옵션 1", callback_data='option1'),
                InlineKeyboardButton("옵션 2", callback_data='option2')
            ],
            [InlineKeyboardButton("옵션 3", callback_data='option3')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            '버튼을 선택하세요:',
            reply_markup=reply_markup
        )
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """메뉴 버튼"""
        keyboard = [
            [
                InlineKeyboardButton("📰 뉴스", callback_data='news'),
                InlineKeyboardButton("🌤️ 날씨", callback_data='weather')
            ],
            [
                InlineKeyboardButton("💰 가격", callback_data='price'),
                InlineKeyboardButton("ℹ️ 도움말", callback_data='help')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            '메뉴를 선택하세요:',
            reply_markup=reply_markup
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """버튼 콜백 처리"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        if callback_data == 'news':
            await query.edit_message_text('📰 최신 뉴스를 가져오는 중...')
        elif callback_data == 'weather':
            await query.edit_message_text('🌤️ 날씨 정보를 가져오는 중...')
        elif callback_data == 'price':
            await query.edit_message_text('💰 가격 정보를 가져오는 중...')
        elif callback_data == 'help':
            await query.edit_message_text('ℹ️ /help 명령어를 사용하세요.')
        else:
            await query.edit_message_text(f'선택: {callback_data}')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """일반 메시지 처리"""
        message_text = update.message.text
        
        # 자동 응답
        for keyword, response in self.auto_responses.items():
            if keyword in message_text:
                await update.message.reply_text(response)
                return
        
        # 에코 (기본 응답)
        # await update.message.reply_text(f'받은 메시지: {message_text}')
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """사진 처리"""
        await update.message.reply_text('📷 사진을 받았습니다!')
        logger.info('사진 수신')
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """문서 처리"""
        file_name = update.message.document.file_name
        await update.message.reply_text(f'📄 문서를 받았습니다: {file_name}')
        logger.info(f'문서 수신: {file_name}')
    
    async def send_notification(self, chat_id: int, message: str):
        """푸시 알림 전송"""
        if self.application and self.application.bot:
            await self.application.bot.send_message(
                chat_id=chat_id,
                text=message
            )
            logger.info(f'알림 전송: {chat_id}')
    
    async def start_async(self):
        """비동기 봇 시작"""
        if not self.token:
            logger.error('토큰이 설정되지 않았습니다.')
            return
        
        try:
            self.application = Application.builder().token(self.token).build()
            self.setup_handlers()
            
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            
            self.is_running = True
            logger.info('텔레그램 봇이 시작되었습니다.')
            
            # 봇이 실행되는 동안 대기
            while self.is_running:
                await asyncio.sleep(1)
        
        except Exception as e:
            logger.error(f'봇 시작 오류: {str(e)}')
            self.is_running = False
    
    async def stop(self):
        """봇 중지"""
        if self.application:
            self.is_running = False
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            logger.info('텔레그램 봇이 중지되었습니다.')
    
    def run(self):
        """봇 실행 (동기)"""
        if not self.token:
            logger.error('토큰이 설정되지 않았습니다.')
            return False
        
        try:
            self.application = Application.builder().token(self.token).build()
            self.setup_handlers()
            
            self.is_running = True
            logger.info('텔레그램 봇이 시작되었습니다.')
            
            self.application.run_polling()
            return True
        
        except Exception as e:
            logger.error(f'봇 실행 오류: {str(e)}')
            self.is_running = False
            return False


if __name__ == '__main__':
    bot = TelegramBot()
    print("텔레그램 봇 모듈이 로드되었습니다.")
