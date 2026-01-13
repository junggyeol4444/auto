"""
태그 생성 모듈
자동 태그 및 해시태그 생성
"""

import json
import random
from datetime import datetime


class TagGenerator:
    """태그 생성 클래스"""
    
    def __init__(self, config_path="config.json"):
        """초기화"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 기본 태그
        self.common_tags = [
            '게임', 'gaming', '게임방송', 'gameplay', '라이브', 'live',
            '스트리머', 'streamer', '방송', 'broadcast', 'twitch', 'youtube'
        ]
        
        # 게임별 태그 매핑
        self.game_tags = {
            'lol': ['롤', '리그오브레전드', 'leagueoflegends', 'lol', '협곡'],
            'valorant': ['발로란트', 'valorant', 'fps', '전술fps'],
            'overwatch': ['오버워치', 'overwatch', 'ow2', 'fps'],
            'minecraft': ['마인크래프트', 'minecraft', '마크', '샌드박스'],
        }
        
        print("[TagGenerator] 초기화 완료")
    
    def generate_tags(self, game_name, content_type='gameplay', keywords=None):
        """
        태그 생성
        Args:
            game_name: 게임명
            content_type: 콘텐츠 타입
            keywords: 추가 키워드
        Returns:
            list: 태그 목록
        """
        tags = []
        
        # 기본 태그
        tags.extend(self.common_tags)
        
        # 게임명 태그
        if game_name:
            tags.append(game_name.lower())
            tags.append(game_name)
            
            # 게임별 특화 태그
            game_key = game_name.lower().replace(' ', '')
            if game_key in self.game_tags:
                tags.extend(self.game_tags[game_key])
        
        # 콘텐츠 타입별 태그
        type_tags = {
            'highlight': ['하이라이트', 'highlight', '명장면', 'best'],
            'funny': ['웃긴', 'funny', '재미', 'comedy', '개그'],
            'tutorial': ['공략', 'guide', 'tutorial', '팁', 'tips'],
            'gameplay': ['플레이', 'playthrough', '풀영상']
        }
        
        if content_type in type_tags:
            tags.extend(type_tags[content_type])
        
        # 추가 키워드
        if keywords:
            tags.extend(keywords)
        
        # 날짜 태그
        tags.append(str(datetime.now().year))
        
        # 중복 제거 및 반환 (최대 30개)
        tags = list(dict.fromkeys(tags))[:30]
        
        return tags
    
    def generate_hashtags(self, tags):
        """
        해시태그 생성
        Args:
            tags: 태그 목록
        Returns:
            str: 해시태그 문자열
        """
        hashtags = [f'#{tag.replace(" ", "")}' for tag in tags[:15]]
        return ' '.join(hashtags)
