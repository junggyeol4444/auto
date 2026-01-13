"""Translation Engine Factory - Auto-select best translator"""
from typing import Optional
from .base_translator import BaseTranslator
from .deepl_api import DeepLTranslator
from .google_api import GoogleTranslator
from .papago_api import PapagoTranslator
from .gpt4_api import GPT4Translator


class TranslationEngine:
    """Factory class for creating and selecting translation engines"""
    
    def __init__(self, config: dict):
        """
        Initialize translation engine with API configurations
        
        Args:
            config: Dictionary containing API keys
        """
        self.config = config
        self.translators = {}
        self._initialize_translators()
    
    def _initialize_translators(self):
        """Initialize all available translators"""
        api_keys = self.config.get('api_keys', {})
        
        # DeepL
        if api_keys.get('deepl'):
            self.translators['deepl'] = DeepLTranslator(api_keys['deepl'])
        
        # Google Translate
        self.translators['google'] = GoogleTranslator()
        
        # Papago
        if api_keys.get('papago_client_id') and api_keys.get('papago_client_secret'):
            self.translators['papago'] = PapagoTranslator(
                api_keys['papago_client_id'],
                api_keys['papago_client_secret']
            )
        
        # GPT-4
        if api_keys.get('openai'):
            self.translators['gpt4'] = GPT4Translator(api_keys['openai'])
    
    def get_translator(self, engine_type: str) -> Optional[BaseTranslator]:
        """
        Get specific translator by type
        
        Args:
            engine_type: Type of translator (deepl, google, papago, gpt4)
            
        Returns:
            BaseTranslator instance or None if not available
        """
        translator = self.translators.get(engine_type)
        if translator and translator.is_configured():
            return translator
        return None
    
    def auto_select_engine(self, source_lang: str, target_lang: str, domain: str = "general") -> BaseTranslator:
        """
        Automatically select the best translation engine
        
        Logic:
        - Korean ↔ English: DeepL (best quality)
        - Korean ↔ Japanese: Papago (specialized)
        - Technical/specialized content: GPT-4 (context-aware)
        - Fallback: Google Translate (universal)
        
        Args:
            source_lang: Source language code
            target_lang: Target language code
            domain: Content domain (general, medical, legal, it)
            
        Returns:
            BaseTranslator instance
        """
        # Korean-English: prefer DeepL
        if {source_lang, target_lang} == {'ko', 'en'}:
            translator = self.get_translator('deepl')
            if translator:
                return translator
        
        # Korean-Japanese: prefer Papago
        if {source_lang, target_lang} == {'ko', 'ja'}:
            translator = self.get_translator('papago')
            if translator:
                return translator
        
        # Specialized domains: prefer GPT-4
        if domain in ['medical', 'legal', 'it']:
            translator = self.get_translator('gpt4')
            if translator:
                return translator
        
        # Try DeepL as high-quality option
        translator = self.get_translator('deepl')
        if translator:
            return translator
        
        # Fallback to Google Translate
        translator = self.get_translator('google')
        if translator:
            return translator
        
        raise ValueError("No translation engine available. Please configure API keys.")
    
    def get_available_engines(self) -> list:
        """Get list of available/configured engines"""
        return [name for name, translator in self.translators.items() 
                if translator.is_configured()]
