"""
라인 봇 모듈
LINE Bot with messaging features
"""
import logging
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextSendMessage, ImageSendMessage, VideoSendMessage,
    RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds,
    URIAction, MessageAction, PostbackAction
)
from linebot.exceptions import LineBotApiError
import json

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('line_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('line_bot')


class LineBot:
    """라인 봇 메인 클래스"""
    
    def __init__(self, channel_access_token=None, channel_secret=None):
        self.channel_access_token = channel_access_token
        self.channel_secret = channel_secret
        self.line_bot_api = None
        self.handler = None
        self.is_running = False
        
        if channel_access_token and channel_secret:
            self.initialize()
    
    def initialize(self):
        """봇 초기화"""
        try:
            self.line_bot_api = LineBotApi(self.channel_access_token)
            self.handler = WebhookHandler(self.channel_secret)
            logger.info('LINE Bot API 초기화 완료')
        except Exception as e:
            logger.error(f'초기화 오류: {str(e)}')
    
    def send_text_message(self, user_id: str, text: str):
        """텍스트 메시지 전송"""
        try:
            if not self.line_bot_api:
                logger.error('LINE Bot API가 초기화되지 않았습니다.')
                return False
            
            self.line_bot_api.push_message(
                user_id,
                TextSendMessage(text=text)
            )
            logger.info(f'메시지 전송 완료: {user_id}')
            return True
        except LineBotApiError as e:
            logger.error(f'메시지 전송 오류: {str(e)}')
            return False
    
    def send_image(self, user_id: str, image_url: str, preview_url: str = None):
        """이미지 메시지 전송"""
        try:
            if not self.line_bot_api:
                logger.error('LINE Bot API가 초기화되지 않았습니다.')
                return False
            
            if not preview_url:
                preview_url = image_url
            
            self.line_bot_api.push_message(
                user_id,
                ImageSendMessage(
                    original_content_url=image_url,
                    preview_image_url=preview_url
                )
            )
            logger.info(f'이미지 전송 완료: {user_id}')
            return True
        except LineBotApiError as e:
            logger.error(f'이미지 전송 오류: {str(e)}')
            return False
    
    def send_video(self, user_id: str, video_url: str, preview_url: str):
        """비디오 메시지 전송"""
        try:
            if not self.line_bot_api:
                logger.error('LINE Bot API가 초기화되지 않았습니다.')
                return False
            
            self.line_bot_api.push_message(
                user_id,
                VideoSendMessage(
                    original_content_url=video_url,
                    preview_image_url=preview_url
                )
            )
            logger.info(f'비디오 전송 완료: {user_id}')
            return True
        except LineBotApiError as e:
            logger.error(f'비디오 전송 오류: {str(e)}')
            return False
    
    def create_rich_menu(self):
        """리치 메뉴 생성"""
        try:
            if not self.line_bot_api:
                logger.error('LINE Bot API가 초기화되지 않았습니다.')
                return None
            
            rich_menu = RichMenu(
                size=RichMenuSize(width=2500, height=1686),
                selected=True,
                name="메인 메뉴",
                chat_bar_text="메뉴",
                areas=[
                    RichMenuArea(
                        bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                        action=MessageAction(label="뉴스", text="뉴스")
                    ),
                    RichMenuArea(
                        bounds=RichMenuBounds(x=833, y=0, width=834, height=843),
                        action=MessageAction(label="날씨", text="날씨")
                    ),
                    RichMenuArea(
                        bounds=RichMenuBounds(x=1667, y=0, width=833, height=843),
                        action=MessageAction(label="가격", text="가격")
                    ),
                    RichMenuArea(
                        bounds=RichMenuBounds(x=0, y=843, width=1250, height=843),
                        action=MessageAction(label="도움말", text="도움말")
                    ),
                    RichMenuArea(
                        bounds=RichMenuBounds(x=1250, y=843, width=1250, height=843),
                        action=URIAction(label="웹사이트", uri="https://example.com")
                    )
                ]
            )
            
            rich_menu_id = self.line_bot_api.create_rich_menu(rich_menu)
            logger.info(f'리치 메뉴 생성 완료: {rich_menu_id}')
            return rich_menu_id
        
        except LineBotApiError as e:
            logger.error(f'리치 메뉴 생성 오류: {str(e)}')
            return None
    
    def set_rich_menu_image(self, rich_menu_id: str, image_path: str):
        """리치 메뉴 이미지 설정"""
        try:
            if not self.line_bot_api:
                logger.error('LINE Bot API가 초기화되지 않았습니다.')
                return False
            
            with open(image_path, 'rb') as f:
                self.line_bot_api.set_rich_menu_image(
                    rich_menu_id,
                    'image/jpeg',
                    f
                )
            logger.info(f'리치 메뉴 이미지 설정 완료: {rich_menu_id}')
            return True
        
        except LineBotApiError as e:
            logger.error(f'리치 메뉴 이미지 설정 오류: {str(e)}')
            return False
    
    def handle_text_message(self, text: str) -> str:
        """텍스트 메시지 처리"""
        text = text.strip()
        
        # 키워드 기반 자동 응답
        if '안녕' in text:
            return '안녕하세요! 무엇을 도와드릴까요?'
        elif '날씨' in text:
            return '🌤️ 현재 날씨: 맑음, 15°C'
        elif '뉴스' in text:
            return '📰 최신 뉴스를 확인하세요!'
        elif '가격' in text:
            return '💰 가격 정보를 확인하세요!'
        elif '도움말' in text or '도움' in text:
            return '사용 가능한 키워드: 안녕, 날씨, 뉴스, 가격, 도움말'
        else:
            return '명령어를 이해하지 못했습니다. "도움말"을 입력하세요.'
    
    def handle_webhook(self, body: str, signature: str):
        """웹훅 처리"""
        try:
            if not self.handler:
                logger.error('Webhook Handler가 초기화되지 않았습니다.')
                return False
            
            self.handler.handle(body, signature)
            return True
        
        except Exception as e:
            logger.error(f'웹훅 처리 오류: {str(e)}')
            return False
    
    def send_push_notification(self, user_id: str, message: str):
        """푸시 알림 전송"""
        return self.send_text_message(user_id, f'🔔 알림: {message}')
    
    def get_profile(self, user_id: str):
        """사용자 프로필 가져오기"""
        try:
            if not self.line_bot_api:
                logger.error('LINE Bot API가 초기화되지 않았습니다.')
                return None
            
            profile = self.line_bot_api.get_profile(user_id)
            return {
                'display_name': profile.display_name,
                'user_id': profile.user_id,
                'picture_url': profile.picture_url,
                'status_message': profile.status_message
            }
        
        except LineBotApiError as e:
            logger.error(f'프로필 가져오기 오류: {str(e)}')
            return None


# Flask 웹 서버와 함께 사용하는 예시
"""
from flask import Flask, request, abort

app = Flask(__name__)
line_bot = LineBot(channel_access_token='YOUR_TOKEN', channel_secret='YOUR_SECRET')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        line_bot.handle_webhook(body, signature)
    except Exception as e:
        abort(400)
    
    return 'OK'

@line_bot.handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    response = line_bot.handle_text_message(event.message.text)
    line_bot.line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )

if __name__ == "__main__":
    app.run()
"""


if __name__ == '__main__':
    print("LINE 봇 모듈이 로드되었습니다.")
