"""Papago Translation API implementation"""
from typing import List, Optional
import requests
from .base_translator import BaseTranslator


class PapagoTranslator(BaseTranslator):
    """Papago API translator - Best for Korean-Japanese"""
    
    API_URL = "https://openapi.naver.com/v1/papago/n2mt"
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        super().__init__(None)
        self.client_id = client_id
        self.client_secret = client_secret
    
    def is_configured(self) -> bool:
        """Check if Papago credentials are configured"""
        return (self.client_id is not None and len(self.client_id.strip()) > 0 and
                self.client_secret is not None and len(self.client_secret.strip()) > 0)
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate single text using Papago API"""
        if not self.is_configured():
            raise ValueError("Papago credentials not configured")
        
        if not text.strip():
            return text
        
        try:
            headers = {
                "X-Naver-Client-Id": self.client_id,
                "X-Naver-Client-Secret": self.client_secret,
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            data = {
                "source": self._map_language_code(source_lang),
                "target": self._map_language_code(target_lang),
                "text": text
            }
            
            response = requests.post(self.API_URL, headers=headers, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["message"]["result"]["translatedText"]
            
        except Exception as e:
            raise Exception(f"Papago translation failed: {str(e)}")
    
    def translate_batch(self, texts: List[str], source_lang: str, target_lang: str) -> List[str]:
        """Translate multiple texts using Papago API (one by one)"""
        if not texts:
            return []
        
        results = []
        for text in texts:
            results.append(self.translate(text, source_lang, target_lang))
        return results
    
    def _map_language_code(self, lang_code: str) -> str:
        """Map language codes to Papago format"""
        mapping = {
            'zh-CN': 'zh-CN',
            'zh-TW': 'zh-TW'
        }
        return mapping.get(lang_code, lang_code.lower())
