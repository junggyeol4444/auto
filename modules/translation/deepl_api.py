"""DeepL Translation API implementation"""
from typing import List, Optional
import requests
from .base_translator import BaseTranslator


class DeepLTranslator(BaseTranslator):
    """DeepL API translator - Best for Korean-English"""
    
    API_URL = "https://api-free.deepl.com/v2/translate"
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate single text using DeepL API"""
        if not self.is_configured():
            raise ValueError("DeepL API key not configured")
        
        if not text.strip():
            return text
        
        try:
            # Map language codes to DeepL format
            source = self._map_language_code(source_lang)
            target = self._map_language_code(target_lang)
            
            headers = {
                "Authorization": f"DeepL-Auth-Key {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "text": [text],
                "source_lang": source,
                "target_lang": target
            }
            
            response = requests.post(self.API_URL, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["translations"][0]["text"]
            
        except Exception as e:
            raise Exception(f"DeepL translation failed: {str(e)}")
    
    def translate_batch(self, texts: List[str], source_lang: str, target_lang: str) -> List[str]:
        """Translate multiple texts using DeepL API"""
        if not self.is_configured():
            raise ValueError("DeepL API key not configured")
        
        if not texts:
            return []
        
        try:
            source = self._map_language_code(source_lang)
            target = self._map_language_code(target_lang)
            
            headers = {
                "Authorization": f"DeepL-Auth-Key {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "text": texts,
                "source_lang": source,
                "target_lang": target
            }
            
            response = requests.post(self.API_URL, json=data, headers=headers, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return [t["text"] for t in result["translations"]]
            
        except Exception as e:
            raise Exception(f"DeepL batch translation failed: {str(e)}")
    
    def _map_language_code(self, lang_code: str) -> str:
        """Map general language codes to DeepL format"""
        mapping = {
            'ko': 'KO',
            'en': 'EN',
            'ja': 'JA',
            'zh-CN': 'ZH',
            'zh-TW': 'ZH',
            'es': 'ES',
            'fr': 'FR',
            'de': 'DE',
            'it': 'IT',
            'pt': 'PT',
            'ru': 'RU',
            'pl': 'PL',
            'nl': 'NL'
        }
        return mapping.get(lang_code, lang_code.upper())
