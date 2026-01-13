"""
소셜 미디어 공유 모듈
Twitter, Discord, 기타 SNS 공유
"""

import json


class SocialShare:
    """소셜 미디어 공유 클래스"""
    
    def __init__(self, config_path="config.json"):
        """초기화"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.twitter_config = self.config.get('twitter', {})
        self.discord_config = self.config.get('discord', {})
        
        print("[SocialShare] 초기화 완료")
    
    def tweet(self, message, media_path=None):
        """
        트위터 트윗
        Args:
            message: 트윗 내용
            media_path: 미디어 파일 경로
        Returns:
            dict: 트윗 결과
        """
        print(f"[SocialShare] 트윗: {message[:50]}...")
        
        # Twitter API 로직 (실제 구현 필요)
        return {'success': True, 'tweet_id': None}
    
    def send_discord_webhook(self, message, embed=None):
        """
        Discord 웹훅 전송
        Args:
            message: 메시지
            embed: 임베드 데이터
        Returns:
            dict: 전송 결과
        """
        webhook_url = self.discord_config.get('webhook_url')
        
        if not webhook_url:
            return {'success': False, 'message': 'Discord 웹훅 URL이 설정되지 않았습니다.'}
        
        print(f"[SocialShare] Discord 알림: {message}")
        
        # Discord 웹훅 전송 로직 (실제 구현 필요)
        return {'success': True}
    
    def notify_stream_start(self, title, game):
        """방송 시작 알림"""
        message = f"🔴 방송 시작! {game} - {title}"
        
        self.tweet(message)
        self.send_discord_webhook(message)
        
        print(f"[SocialShare] 방송 시작 알림 전송됨")
    
    def share_clip(self, clip_url, title):
        """클립 공유"""
        message = f"🎬 {title}\n{clip_url}"
        
        self.tweet(message)
        self.send_discord_webhook(message)
        
        print(f"[SocialShare] 클립 공유됨: {title}")
