"""
하이라이트 감지 모듈
킬, 웃음, 채팅 폭발, 볼륨 급증 감지
"""

import json
import numpy as np
from datetime import datetime
from collections import deque
import os


class HighlightDetector:
    """하이라이트 감지 클래스"""
    
    def __init__(self, config_path="config.json", keywords_path="data/keywords.txt"):
        """
        초기화
        Args:
            config_path: 설정 파일 경로
            keywords_path: 키워드 파일 경로
        """
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.detection_config = self.config.get('highlight_detection', {})
        
        # 키워드 로드
        self.keywords = self._load_keywords(keywords_path)
        
        # 감지된 하이라이트
        self.highlights = []
        
        # 오디오 레벨 히스토리
        self.audio_history = deque(maxlen=100)
        
        # 채팅 버스트 히스토리
        self.chat_history = deque(maxlen=100)
        
        # 각 감지 타입 활성화 상태
        self.kill_detection_enabled = self.detection_config.get('kill_detection', True)
        self.laugh_detection_enabled = self.detection_config.get('laugh_detection', True)
        self.chat_burst_enabled = self.detection_config.get('chat_burst_detection', True)
        self.volume_spike_enabled = self.detection_config.get('volume_spike_detection', True)
        
        print("[HighlightDetector] 초기화 완료")
    
    def _load_keywords(self, path):
        """
        키워드 목록 로드
        Args:
            path: 키워드 파일 경로
        Returns:
            dict: 카테고리별 키워드 목록
        """
        if not os.path.exists(path):
            print(f"[Warning] 키워드 파일을 찾을 수 없습니다: {path}")
            return {'kill': [], 'reaction': [], 'game_event': []}
        
        keywords = {
            'kill': [],
            'reaction': [],
            'game_event': []
        }
        
        current_category = None
        
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    # 카테고리 판단
                    if '킬' in line or 'kill' in line.lower():
                        current_category = 'kill'
                    elif '반응' in line or 'reaction' in line.lower():
                        current_category = 'reaction'
                    elif '게임' in line or 'game' in line.lower():
                        current_category = 'game_event'
                    continue
                
                if current_category:
                    keywords[current_category].append(line.lower())
        
        print(f"[HighlightDetector] 키워드 로드됨 - kill: {len(keywords['kill'])}, reaction: {len(keywords['reaction'])}, game: {len(keywords['game_event'])}")
        return keywords
    
    def detect_kill(self, transcribed_text):
        """
        킬 감지 (STT 텍스트 기반)
        Args:
            transcribed_text: 음성 인식 텍스트
        Returns:
            bool: 킬 감지 여부
        """
        if not self.kill_detection_enabled:
            return False
        
        text_lower = transcribed_text.lower()
        
        # 킬 키워드 매칭
        for keyword in self.keywords['kill']:
            if keyword in text_lower:
                self._add_highlight('kill', f'킬 감지: {keyword}')
                return True
        
        # 게임 이벤트 키워드 매칭
        for keyword in self.keywords['game_event']:
            if keyword in text_lower:
                self._add_highlight('game_event', f'게임 이벤트: {keyword}')
                return True
        
        return False
    
    def detect_laugh(self, audio_data, sample_rate=44100):
        """
        웃음 감지 (오디오 분석)
        Args:
            audio_data: 오디오 데이터 (numpy array)
            sample_rate: 샘플레이트
        Returns:
            bool: 웃음 감지 여부
        """
        if not self.laugh_detection_enabled:
            return False
        
        try:
            # 간단한 웃음 감지 (주파수 및 에너지 기반)
            # 실제로는 librosa를 사용한 더 정교한 분석 필요
            
            # RMS 에너지 계산
            rms = np.sqrt(np.mean(audio_data**2))
            
            # 주파수 분석 (FFT)
            fft = np.fft.fft(audio_data)
            frequencies = np.fft.fftfreq(len(fft), 1/sample_rate)
            magnitude = np.abs(fft)
            
            # 웃음소리는 주로 250-4000Hz 범위
            laugh_freq_range = (frequencies >= 250) & (frequencies <= 4000)
            laugh_energy = np.sum(magnitude[laugh_freq_range])
            
            total_energy = np.sum(magnitude)
            laugh_ratio = laugh_energy / total_energy if total_energy > 0 else 0
            
            sensitivity = self.detection_config.get('laugh_sensitivity', 0.7)
            
            if laugh_ratio > sensitivity:
                self._add_highlight('laugh', f'웃음 감지 (신뢰도: {laugh_ratio:.2f})')
                return True
            
        except Exception as e:
            print(f"[HighlightDetector] 웃음 감지 오류: {e}")
        
        return False
    
    def detect_volume_spike(self, current_volume):
        """
        볼륨 급증 감지
        Args:
            current_volume: 현재 볼륨 레벨
        Returns:
            bool: 볼륨 급증 감지 여부
        """
        if not self.volume_spike_enabled:
            return False
        
        self.audio_history.append(current_volume)
        
        if len(self.audio_history) < 10:
            return False
        
        # 평균 볼륨 계산
        avg_volume = np.mean(list(self.audio_history)[:-1])
        
        # 볼륨 급증 임계값
        threshold = self.detection_config.get('volume_threshold', 1.5)
        
        if current_volume > avg_volume * threshold:
            self._add_highlight('volume_spike', f'볼륨 급증 감지 (현재: {current_volume:.2f}, 평균: {avg_volume:.2f})')
            return True
        
        return False
    
    def detect_chat_burst(self, messages_per_second):
        """
        채팅 폭발 감지
        Args:
            messages_per_second: 초당 메시지 수
        Returns:
            bool: 채팅 폭발 감지 여부
        """
        if not self.chat_burst_enabled:
            return False
        
        self.chat_history.append(messages_per_second)
        
        threshold = self.detection_config.get('chat_burst_threshold', 10)
        
        if messages_per_second >= threshold:
            self._add_highlight('chat_burst', f'채팅 폭발 감지 (초당 {messages_per_second}개)')
            return True
        
        return False
    
    def detect_reaction_keywords(self, message):
        """
        반응 키워드 감지 (채팅 메시지)
        Args:
            message: 채팅 메시지
        Returns:
            bool: 반응 키워드 감지 여부
        """
        message_lower = message.lower()
        
        for keyword in self.keywords['reaction']:
            if keyword in message_lower:
                return True
        
        return False
    
    def _add_highlight(self, highlight_type, description):
        """
        하이라이트 추가
        Args:
            highlight_type: 하이라이트 타입
            description: 설명
        """
        highlight = {
            'type': highlight_type,
            'description': description,
            'timestamp': datetime.now(),
            'unix_time': datetime.now().timestamp()
        }
        
        self.highlights.append(highlight)
        print(f"[HighlightDetector] 하이라이트 감지: {description}")
    
    def get_recent_highlights(self, minutes=60):
        """
        최근 하이라이트 조회
        Args:
            minutes: 조회할 시간 범위 (분)
        Returns:
            list: 하이라이트 목록
        """
        from datetime import timedelta
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        recent = [
            h for h in self.highlights
            if h['timestamp'] >= cutoff_time
        ]
        
        return recent
    
    def get_highlights_by_type(self, highlight_type):
        """
        타입별 하이라이트 조회
        Args:
            highlight_type: 하이라이트 타입
        Returns:
            list: 하이라이트 목록
        """
        return [h for h in self.highlights if h['type'] == highlight_type]
    
    def get_all_highlights(self):
        """모든 하이라이트 조회"""
        return self.highlights
    
    def clear_highlights(self):
        """하이라이트 초기화"""
        self.highlights.clear()
        print("[HighlightDetector] 하이라이트 초기화됨")
    
    def export_highlights(self, filepath):
        """
        하이라이트 내보내기
        Args:
            filepath: 저장할 파일 경로
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.highlights, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"[HighlightDetector] 하이라이트 저장됨: {filepath}")
    
    def get_stats(self):
        """통계 조회"""
        stats = {
            'total_highlights': len(self.highlights),
            'by_type': {}
        }
        
        for highlight_type in ['kill', 'laugh', 'volume_spike', 'chat_burst', 'game_event']:
            stats['by_type'][highlight_type] = len(self.get_highlights_by_type(highlight_type))
        
        return stats
