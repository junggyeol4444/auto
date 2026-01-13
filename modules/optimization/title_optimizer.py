"""
제목 최적화 모듈
SEO 친화적이고 클릭 유도 제목 자동 생성
"""

import json
import random
from datetime import datetime


class TitleOptimizer:
    """제목 최적화 클래스"""
    
    def __init__(self, config_path="config.json"):
        """
        초기화
        Args:
            config_path: 설정 파일 경로
        """
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.optimization_config = self.config.get('optimization', {})
        
        # 어그로 키워드
        self.clickbait_keywords = [
            '충격', '대박', '실화', '진짜', '레전드', '역대급',
            '미쳤다', '이거 모르면 손해', '프로도 모르는',
            '놀라운', '경악', '극찬', '화제', '폭발', '터졌다',
            '찢었다', '짜릿한', '압도적', '완벽한', '최고의'
        ]
        
        # 이모지
        self.emojis = [
            '🔥', '⚡', '💥', '🎯', '👑', '🎮', '🎪', '✨',
            '💯', '🚀', '⭐', '🌟', '💫', '🎉', '🎊', '🔴'
        ]
        
        # 트렌딩 키워드 (동적으로 업데이트 가능)
        self.trending_keywords = []
        
        print("[TitleOptimizer] 초기화 완료")
    
    def generate_title(self, game_name, content_type='gameplay', highlight_info=None):
        """
        제목 생성
        Args:
            game_name: 게임명
            content_type: 콘텐츠 타입 (gameplay/highlight/tutorial/funny)
            highlight_info: 하이라이트 정보
        Returns:
            list: 제목 후보 리스트
        """
        titles = []
        
        # 템플릿 기반 제목 생성
        if content_type == 'highlight':
            titles.extend(self._generate_highlight_titles(game_name, highlight_info))
        elif content_type == 'funny':
            titles.extend(self._generate_funny_titles(game_name))
        elif content_type == 'tutorial':
            titles.extend(self._generate_tutorial_titles(game_name))
        else:  # gameplay
            titles.extend(self._generate_gameplay_titles(game_name))
        
        # SEO 최적화 제목 추가
        titles.extend(self._generate_seo_titles(game_name, content_type))
        
        return titles[:10]  # 최대 10개 반환
    
    def _generate_highlight_titles(self, game_name, highlight_info):
        """하이라이트 제목 생성"""
        titles = []
        emoji = random.choice(self.emojis)
        clickbait = random.choice(self.clickbait_keywords)
        
        templates = [
            f"{emoji} {clickbait} {game_name} 하이라이트 모음",
            f"[{game_name}] {clickbait} 순간 모음 {emoji}",
            f"{game_name} 이거 봐야 함.. ({clickbait}) {emoji}",
            f"{emoji} {game_name} {clickbait} 플레이 모음",
            f"역대급 {game_name} 하이라이트 {emoji} {clickbait}"
        ]
        
        # 하이라이트 정보가 있으면 더 구체적으로
        if highlight_info:
            if highlight_info.get('type') == 'kill':
                templates.append(f"{emoji} {game_name} 킬 장면 모음 ({clickbait})")
            elif highlight_info.get('type') == 'laugh':
                templates.append(f"{emoji} {game_name} 빵터진 순간들 {clickbait}")
        
        titles.extend(templates)
        return titles
    
    def _generate_funny_titles(self, game_name):
        """재미 콘텐츠 제목 생성"""
        emoji = random.choice(['😂', '🤣', '😆', '💀'] + self.emojis)
        
        templates = [
            f"{emoji} {game_name} 웃긴 순간 모음",
            f"[{game_name}] 빵터진 순간 모음 {emoji}",
            f"{game_name} 이거 보고 안 웃으면 인간 아님 {emoji}",
            f"{emoji} {game_name} 개웃긴 장면 모음",
            f"{game_name} 웃음 참기 챌린지 {emoji}"
        ]
        
        return templates
    
    def _generate_tutorial_titles(self, game_name):
        """튜토리얼 제목 생성"""
        emoji = random.choice(['📚', '🎓', '💡'] + self.emojis)
        
        templates = [
            f"{emoji} {game_name} 초보자 가이드 (꿀팁 총정리)",
            f"[{game_name}] 프로가 알려주는 필수 팁 {emoji}",
            f"{game_name} 이거 모르면 손해! 핵심 공략 {emoji}",
            f"{emoji} {game_name} 빠르게 마스터하는 법",
            f"{game_name} 완벽 공략 가이드 {emoji} (입문자 필수)"
        ]
        
        return templates
    
    def _generate_gameplay_titles(self, game_name):
        """일반 게임플레이 제목 생성"""
        emoji = random.choice(self.emojis)
        clickbait = random.choice(self.clickbait_keywords)
        
        # 현재 날짜
        date_str = datetime.now().strftime('%Y.%m.%d')
        
        templates = [
            f"{emoji} {game_name} 실시간 게임플레이",
            f"[{game_name}] {clickbait} 플레이 {emoji} ({date_str})",
            f"{game_name} 라이브 방송 다시보기 {emoji}",
            f"{emoji} {clickbait} {game_name} 플레이",
            f"{game_name} 풀영상 {emoji} {date_str}"
        ]
        
        return templates
    
    def _generate_seo_titles(self, game_name, content_type):
        """SEO 최적화 제목 생성"""
        # 검색 최적화된 제목
        year = datetime.now().year
        
        templates = [
            f"{game_name} {content_type} {year}",
            f"{game_name} 게임플레이 공략 팁",
            f"{game_name} 하이라이트 베스트 모음",
            f"[한글] {game_name} 플레이 영상"
        ]
        
        # 트렌딩 키워드 추가
        if self.trending_keywords:
            keyword = random.choice(self.trending_keywords)
            templates.append(f"{game_name} {keyword}")
        
        return templates
    
    def optimize_title(self, title, add_emoji=True, add_clickbait=False):
        """
        기존 제목 최적화
        Args:
            title: 원본 제목
            add_emoji: 이모지 추가 여부
            add_clickbait: 어그로 키워드 추가 여부
        Returns:
            str: 최적화된 제목
        """
        optimized = title
        
        # 이모지 추가
        if add_emoji and not any(emoji in title for emoji in self.emojis):
            emoji = random.choice(self.emojis)
            optimized = f"{emoji} {optimized}"
        
        # 어그로 키워드 추가
        if add_clickbait:
            clickbait = random.choice(self.clickbait_keywords)
            optimized = f"[{clickbait}] {optimized}"
        
        # 길이 제한 (YouTube 제목 최대 100자)
        if len(optimized) > 100:
            optimized = optimized[:97] + '...'
        
        return optimized
    
    def add_trending_keyword(self, keyword):
        """트렌딩 키워드 추가"""
        if keyword not in self.trending_keywords:
            self.trending_keywords.append(keyword)
            print(f"[TitleOptimizer] 트렌딩 키워드 추가: {keyword}")
    
    def get_trending_keywords(self):
        """트렌딩 키워드 조회"""
        return self.trending_keywords
    
    def generate_shorts_title(self, game_name, highlight_type='general'):
        """
        쇼츠용 제목 생성 (짧고 임팩트 있게)
        Args:
            game_name: 게임명
            highlight_type: 하이라이트 타입
        Returns:
            list: 제목 후보
        """
        emoji = random.choice(self.emojis)
        
        templates = [
            f"{emoji} {game_name} 이 장면 실화냐",
            f"{game_name} 레전드 순간 {emoji}",
            f"{emoji} 이게 가능해? {game_name}",
            f"{game_name} 역대급 장면 {emoji}",
            f"{emoji} {game_name} 미쳤다"
        ]
        
        if highlight_type == 'kill':
            templates.extend([
                f"{emoji} {game_name} 킬 장면 미쳤네",
                f"{game_name} 이 킬 뭐야 {emoji}"
            ])
        elif highlight_type == 'funny':
            templates.extend([
                f"😂 {game_name} 빵터짐",
                f"{game_name} 이거 개웃김 😂"
            ])
        
        return templates[:5]
    
    def validate_title(self, title):
        """
        제목 유효성 검사
        Args:
            title: 제목
        Returns:
            dict: 검사 결과
        """
        issues = []
        
        # 길이 확인
        if len(title) > 100:
            issues.append('제목이 너무 깁니다 (최대 100자)')
        elif len(title) < 10:
            issues.append('제목이 너무 짧습니다 (최소 10자)')
        
        # 특수문자 확인
        if title.count('!') > 3:
            issues.append('느낌표가 너무 많습니다')
        
        if title.count('?') > 2:
            issues.append('물음표가 너무 많습니다')
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
