"""
채팅 통계 모듈
시청자 수, 채팅 활성도, 인기 단어 등 분석
"""

import json
from collections import defaultdict, Counter, deque
from datetime import datetime, timedelta
import time


class ChatStats:
    """채팅 통계 클래스"""
    
    def __init__(self, config_path="config.json"):
        """
        초기화
        Args:
            config_path: 설정 파일 경로
        """
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 시청자 수 히스토리 (시간별)
        self.viewer_history = deque(maxlen=1000)
        
        # 채팅 메시지 히스토리
        self.message_history = deque(maxlen=10000)
        
        # 사용자별 메시지 카운트
        self.user_message_count = defaultdict(int)
        
        # 단어 빈도
        self.word_frequency = Counter()
        
        # 구독자/후원 통계
        self.subscriber_count = 0
        self.donation_count = 0
        self.total_donation_amount = 0
        
        # 시간대별 채팅 활성도
        self.hourly_activity = defaultdict(int)
        
        # 세션 시작 시간
        self.session_start = datetime.now()
        
        print("[ChatStats] 초기화 완료")
    
    def record_viewer_count(self, count):
        """
        시청자 수 기록
        Args:
            count: 시청자 수
        """
        self.viewer_history.append({
            'time': datetime.now(),
            'count': count
        })
    
    def record_message(self, username, message, user_id=None):
        """
        채팅 메시지 기록
        Args:
            username: 사용자명
            message: 메시지
            user_id: 사용자 ID
        """
        timestamp = datetime.now()
        
        # 메시지 히스토리에 추가
        self.message_history.append({
            'time': timestamp,
            'username': username,
            'user_id': user_id,
            'message': message
        })
        
        # 사용자별 카운트 증가
        self.user_message_count[username] += 1
        
        # 단어 분석 (한글, 영어만)
        words = self._extract_words(message)
        self.word_frequency.update(words)
        
        # 시간대별 활성도
        hour = timestamp.hour
        self.hourly_activity[hour] += 1
    
    def _extract_words(self, message):
        """
        메시지에서 단어 추출
        Args:
            message: 메시지
        Returns:
            list: 단어 목록
        """
        import re
        
        # 한글, 영어, 숫자만 추출
        words = re.findall(r'[가-힣a-zA-Z0-9]+', message)
        
        # 1글자, 2글자 단어 필터링
        words = [w for w in words if len(w) >= 2]
        
        return words
    
    def record_subscriber(self):
        """구독자 기록"""
        self.subscriber_count += 1
    
    def record_donation(self, amount):
        """
        후원 기록
        Args:
            amount: 후원 금액
        """
        self.donation_count += 1
        self.total_donation_amount += amount
    
    def get_viewer_trend(self, minutes=60):
        """
        시청자 수 추이 조회
        Args:
            minutes: 조회할 시간 범위 (분)
        Returns:
            list: 시청자 수 데이터
        """
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        recent_data = [
            data for data in self.viewer_history
            if data['time'] >= cutoff_time
        ]
        
        return recent_data
    
    def get_chat_activity(self, minutes=60):
        """
        채팅 활성도 조회
        Args:
            minutes: 조회할 시간 범위 (분)
        Returns:
            dict: 활성도 데이터
        """
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        recent_messages = [
            msg for msg in self.message_history
            if msg['time'] >= cutoff_time
        ]
        
        return {
            'total_messages': len(recent_messages),
            'unique_users': len(set(msg['username'] for msg in recent_messages)),
            'messages_per_minute': len(recent_messages) / max(minutes, 1)
        }
    
    def get_top_chatters(self, limit=10):
        """
        최다 채팅 사용자 조회
        Args:
            limit: 조회할 상위 수
        Returns:
            list: 사용자 목록
        """
        return sorted(
            self.user_message_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
    
    def get_popular_words(self, limit=50):
        """
        인기 단어 조회
        Args:
            limit: 조회할 상위 수
        Returns:
            list: 단어 목록
        """
        return self.word_frequency.most_common(limit)
    
    def get_chat_burst_rate(self, window_seconds=10):
        """
        채팅 폭발 비율 계산 (초당 메시지 수)
        Args:
            window_seconds: 시간 윈도우 (초)
        Returns:
            float: 초당 메시지 수
        """
        cutoff_time = datetime.now() - timedelta(seconds=window_seconds)
        
        recent_messages = sum(
            1 for msg in self.message_history
            if msg['time'] >= cutoff_time
        )
        
        return recent_messages / window_seconds if window_seconds > 0 else 0
    
    def get_hourly_activity_chart(self):
        """
        시간대별 활성도 차트 데이터
        Returns:
            dict: 시간대별 메시지 수
        """
        return dict(self.hourly_activity)
    
    def get_session_summary(self):
        """
        세션 요약 통계
        Returns:
            dict: 요약 데이터
        """
        session_duration = datetime.now() - self.session_start
        
        # 평균 시청자 수
        avg_viewers = 0
        if self.viewer_history:
            avg_viewers = sum(d['count'] for d in self.viewer_history) / len(self.viewer_history)
        
        # 최고 시청자 수
        peak_viewers = 0
        if self.viewer_history:
            peak_viewers = max(d['count'] for d in self.viewer_history)
        
        return {
            'session_duration': str(session_duration),
            'total_messages': len(self.message_history),
            'unique_chatters': len(self.user_message_count),
            'avg_viewers': round(avg_viewers, 2),
            'peak_viewers': peak_viewers,
            'subscribers': self.subscriber_count,
            'donations': self.donation_count,
            'total_donation_amount': self.total_donation_amount,
            'messages_per_minute': len(self.message_history) / max(session_duration.total_seconds() / 60, 1)
        }
    
    def export_stats(self, filepath):
        """
        통계 데이터 내보내기
        Args:
            filepath: 저장할 파일 경로
        """
        stats_data = {
            'session_summary': self.get_session_summary(),
            'top_chatters': self.get_top_chatters(20),
            'popular_words': self.get_popular_words(100),
            'hourly_activity': self.get_hourly_activity_chart()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"[ChatStats] 통계 데이터 저장됨: {filepath}")
    
    def reset_session(self):
        """세션 초기화"""
        self.viewer_history.clear()
        self.message_history.clear()
        self.user_message_count.clear()
        self.word_frequency.clear()
        self.subscriber_count = 0
        self.donation_count = 0
        self.total_donation_amount = 0
        self.hourly_activity.clear()
        self.session_start = datetime.now()
        print("[ChatStats] 세션 초기화됨")
