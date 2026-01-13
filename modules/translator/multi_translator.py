# -*- coding: utf-8 -*-
"""
다국어 번역기
여러 번역 API를 사용하여 텍스트를 번역합니다.
"""

from googletrans import Translator
from langdetect import detect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultiTranslator:
    """다국어 번역 클래스"""
    
    def __init__(self):
        self.translator = Translator()
        self.supported_languages = {
            'ko': '한국어',
            'en': '영어',
            'ja': '일본어',
            'zh-cn': '중국어(간체)',
            'zh-tw': '중국어(번체)',
            'es': '스페인어',
            'fr': '프랑스어',
            'de': '독일어',
            'ru': '러시아어'
        }
    
    def detect_language(self, text):
        """
        언어 자동 감지
        
        Args:
            text (str): 텍스트
            
        Returns:
            str: 언어 코드
        """
        try:
            lang = detect(text)
            logger.info(f"감지된 언어: {lang}")
            return lang
        except Exception as e:
            logger.error(f"언어 감지 실패: {e}")
            return 'unknown'
    
    def translate(self, text, dest='ko', src='auto'):
        """
        텍스트 번역
        
        Args:
            text (str): 번역할 텍스트
            dest (str): 목표 언어 코드
            src (str): 원본 언어 코드 ('auto'면 자동 감지)
            
        Returns:
            dict: 번역 결과
        """
        if not text or not text.strip():
            logger.warning("번역할 텍스트가 없습니다")
            return {
                'original': text,
                'translated': text,
                'src_lang': 'unknown',
                'dest_lang': dest
            }
        
        try:
            result = self.translator.translate(text, dest=dest, src=src)
            
            logger.info(f"번역 완료: {result.src} -> {dest}")
            
            return {
                'original': text,
                'translated': result.text,
                'src_lang': result.src,
                'dest_lang': dest
            }
            
        except Exception as e:
            logger.error(f"번역 실패: {e}")
            return {
                'original': text,
                'translated': text,
                'src_lang': 'error',
                'dest_lang': dest,
                'error': str(e)
            }
    
    def translate_batch(self, texts, dest='ko', src='auto'):
        """
        여러 텍스트 일괄 번역
        
        Args:
            texts (list): 텍스트 리스트
            dest (str): 목표 언어 코드
            src (str): 원본 언어 코드
            
        Returns:
            list: 번역 결과 리스트
        """
        results = []
        
        for text in texts:
            result = self.translate(text, dest=dest, src=src)
            results.append(result)
        
        logger.info(f"{len(results)}개 텍스트 번역 완료")
        return results
    
    def translate_to_korean(self, text):
        """
        한국어로 번역 (간편 메서드)
        
        Args:
            text (str): 번역할 텍스트
            
        Returns:
            str: 번역된 텍스트
        """
        result = self.translate(text, dest='ko', src='auto')
        return result['translated']
    
    def translate_to_english(self, text):
        """
        영어로 번역 (간편 메서드)
        
        Args:
            text (str): 번역할 텍스트
            
        Returns:
            str: 번역된 텍스트
        """
        result = self.translate(text, dest='en', src='auto')
        return result['translated']
    
    def is_korean(self, text):
        """
        한국어 여부 확인
        
        Args:
            text (str): 텍스트
            
        Returns:
            bool: 한국어 여부
        """
        try:
            lang = self.detect_language(text)
            return lang == 'ko'
        except:
            return False
    
    def get_language_name(self, lang_code):
        """
        언어 코드에서 언어 이름 가져오기
        
        Args:
            lang_code (str): 언어 코드
            
        Returns:
            str: 언어 이름
        """
        return self.supported_languages.get(lang_code, lang_code)


if __name__ == '__main__':
    # 테스트 코드
    translator = MultiTranslator()
    
    # 일본어 -> 한국어 번역
    japanese_text = "こんにちは、世界"
    result = translator.translate(japanese_text, dest='ko')
    print(f"원문 ({result['src_lang']}): {result['original']}")
    print(f"번역 ({result['dest_lang']}): {result['translated']}")
    
    # 영어 -> 한국어 번역
    english_text = "Artificial Intelligence is changing the world"
    korean = translator.translate_to_korean(english_text)
    print(f"\n영어: {english_text}")
    print(f"한국어: {korean}")
    
    # 언어 감지
    text = "안녕하세요"
    lang = translator.detect_language(text)
    lang_name = translator.get_language_name(lang)
    print(f"\n'{text}'의 언어: {lang_name} ({lang})")
