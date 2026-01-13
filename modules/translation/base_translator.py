"""Base translator abstract class"""
from abc import ABC, abstractmethod
from typing import List, Optional


class BaseTranslator(ABC):
    """Abstract base class for all translation APIs"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate a single text string
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        pass
    
    @abstractmethod
    def translate_batch(self, texts: List[str], source_lang: str, target_lang: str) -> List[str]:
        """
        Translate multiple text strings in a batch
        
        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            List of translated texts
        """
        pass
    
    def is_configured(self) -> bool:
        """Check if API is properly configured"""
        return self.api_key is not None and len(self.api_key.strip()) > 0
