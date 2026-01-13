"""
채팅 번역 모듈
실시간 다국어 채팅 번역
"""

import json
from googletrans import Translator
import threading
from collections import deque


class ChatTranslator:
    """채팅 번역 클래스"""
    
    def __init__(self, config_path="config.json"):
        """
        초기화
        Args:
            config_path: 설정 파일 경로
        """
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.translation_config = self.config.get('translation', {})
        self.enabled = self.translation_config.get('enabled', True)
        self.target_languages = self.translation_config.get('target_languages', ['ko', 'en', 'ja'])
        
        # 번역기 초기화
        self.translator = Translator()
        
        # 번역 캐시 (동일 메시지 재번역 방지)
        self.cache = {}
        self.cache_max_size = 1000
        
        # 번역 큐
        self.translation_queue = deque(maxlen=100)
        
        # 번역 히스토리
        self.translation_history = deque(maxlen=500)
        
        print("[ChatTranslator] 초기화 완료")
    
    def detect_language(self, text):
        """
        언어 감지
        Args:
            text: 텍스트
        Returns:
            str: 언어 코드 (예: 'ko', 'en', 'ja')
        """
        try:
            detected = self.translator.detect(text)
            return detected.lang
        except Exception as e:
            print(f"[ChatTranslator] 언어 감지 실패: {e}")
            return 'unknown'
    
    def translate(self, text, dest='ko', src='auto'):
        """
        텍스트 번역
        Args:
            text: 번역할 텍스트
            dest: 목적 언어
            src: 원본 언어 ('auto'면 자동 감지)
        Returns:
            dict: 번역 결과
        """
        if not self.enabled:
            return None
        
        # 캐시 확인
        cache_key = f"{src}_{dest}_{text}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # 번역 실행
            result = self.translator.translate(text, dest=dest, src=src)
            
            translation_result = {
                'original': text,
                'translated': result.text,
                'src_lang': result.src,
                'dest_lang': dest,
                'confidence': getattr(result, 'confidence', None)
            }
            
            # 캐시에 저장
            if len(self.cache) >= self.cache_max_size:
                # 캐시 크기 초과시 오래된 항목 삭제
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
            
            self.cache[cache_key] = translation_result
            
            # 히스토리에 추가
            self.translation_history.append(translation_result)
            
            return translation_result
            
        except Exception as e:
            print(f"[ChatTranslator] 번역 실패: {e}")
            return {
                'original': text,
                'translated': text,
                'src_lang': src,
                'dest_lang': dest,
                'error': str(e)
            }
    
    def translate_message(self, username, message, auto_detect=True):
        """
        채팅 메시지 번역 (자동 언어 감지)
        Args:
            username: 사용자명
            message: 메시지
            auto_detect: 자동 언어 감지 여부
        Returns:
            dict: 번역 결과들
        """
        if not self.enabled:
            return None
        
        # 원본 언어 감지
        src_lang = self.detect_language(message) if auto_detect else 'auto'
        
        results = {
            'username': username,
            'original': message,
            'src_lang': src_lang,
            'translations': {}
        }
        
        # 각 목표 언어로 번역
        for target_lang in self.target_languages:
            # 원본 언어와 목표 언어가 같으면 스킵
            if src_lang == target_lang:
                continue
            
            translation = self.translate(message, dest=target_lang, src=src_lang)
            if translation:
                results['translations'][target_lang] = translation['translated']
        
        return results
    
    def translate_to_korean(self, text):
        """
        한국어로 번역 (간편 메서드)
        Args:
            text: 텍스트
        Returns:
            str: 번역된 텍스트
        """
        result = self.translate(text, dest='ko')
        return result['translated'] if result else text
    
    def translate_to_english(self, text):
        """
        영어로 번역 (간편 메서드)
        Args:
            text: 텍스트
        Returns:
            str: 번역된 텍스트
        """
        result = self.translate(text, dest='en')
        return result['translated'] if result else text
    
    def should_translate(self, text, user_lang='ko'):
        """
        번역이 필요한지 판단
        Args:
            text: 텍스트
            user_lang: 사용자 언어
        Returns:
            bool: 번역 필요 여부
        """
        detected_lang = self.detect_language(text)
        
        # 감지된 언어가 사용자 언어와 다르면 번역 필요
        if detected_lang != user_lang and detected_lang != 'unknown':
            return True
        
        return False
    
    def get_overlay_text(self, translation_result):
        """
        오버레이에 표시할 텍스트 생성
        Args:
            translation_result: 번역 결과
        Returns:
            str: 오버레이 텍스트
        """
        if not translation_result or not translation_result.get('translations'):
            return None
        
        # 한국어 번역이 있으면 우선 표시
        if 'ko' in translation_result['translations']:
            return f"[번역] {translation_result['translations']['ko']}"
        
        # 아니면 첫 번째 번역 표시
        first_lang = list(translation_result['translations'].keys())[0]
        return f"[번역] {translation_result['translations'][first_lang]}"
    
    def clear_cache(self):
        """캐시 초기화"""
        self.cache.clear()
        print("[ChatTranslator] 캐시 초기화됨")
    
    def get_stats(self):
        """통계 조회"""
        return {
            'cache_size': len(self.cache),
            'history_size': len(self.translation_history),
            'enabled': self.enabled,
            'target_languages': self.target_languages
        }
