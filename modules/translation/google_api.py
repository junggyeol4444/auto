"""Google Translate API implementation"""
from typing import List, Optional
from .base_translator import BaseTranslator

try:
    from googletrans import Translator
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    GOOGLETRANS_AVAILABLE = False


class GoogleTranslator(BaseTranslator):
    """Google Translate API - Best for general purpose and many languages"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        if GOOGLETRANS_AVAILABLE:
            self.translator = Translator()
        else:
            self.translator = None
    
    def is_configured(self) -> bool:
        """Google Translate (googletrans) doesn't require API key"""
        return GOOGLETRANS_AVAILABLE
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate single text using Google Translate"""
        if not self.is_configured():
            raise ValueError("googletrans library not available")
        
        if not text.strip():
            return text
        
        try:
            result = self.translator.translate(
                text,
                src=self._map_language_code(source_lang),
                dest=self._map_language_code(target_lang)
            )
            return result.text
            
        except Exception as e:
            raise Exception(f"Google Translate failed: {str(e)}")
    
    def translate_batch(self, texts: List[str], source_lang: str, target_lang: str) -> List[str]:
        """Translate multiple texts using Google Translate"""
        if not self.is_configured():
            raise ValueError("googletrans library not available")
        
        if not texts:
            return []
        
        try:
            results = self.translator.translate(
                texts,
                src=self._map_language_code(source_lang),
                dest=self._map_language_code(target_lang)
            )
            return [r.text for r in results]
            
        except Exception as e:
            raise Exception(f"Google Translate batch failed: {str(e)}")
    
    def _map_language_code(self, lang_code: str) -> str:
        """Map language codes to Google Translate format"""
        mapping = {
            'zh-CN': 'zh-cn',
            'zh-TW': 'zh-tw'
        }
        return mapping.get(lang_code, lang_code.lower())
