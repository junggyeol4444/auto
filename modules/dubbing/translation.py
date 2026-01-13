"""Translation service for dubbing."""
from typing import Optional
from utils.logger import get_logger

logger = get_logger()


class TranslationService:
    """Translation service for text and subtitles."""
    
    def __init__(self):
        """Initialize translation service."""
        self.name = "Translation Service"
        logger.info("Translation service initialized")
    
    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        service: str = 'google'
    ) -> Optional[str]:
        """
        Translate text.
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            service: Translation service ('google' or 'deepl')
            
        Returns:
            Translated text or None if error
        """
        try:
            if not text or not text.strip():
                logger.error("Empty text provided")
                return None
            
            logger.info(f"Translating from {source_lang} to {target_lang} using {service}")
            
            if service == 'google':
                return self._translate_google(text, source_lang, target_lang)
            elif service == 'deepl':
                return self._translate_deepl(text, source_lang, target_lang)
            else:
                logger.error(f"Unknown service: {service}")
                return None
                
        except Exception as e:
            logger.error(f"Error in translation: {e}")
            return None
    
    def _translate_google(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Optional[str]:
        """Translate using Google Translate."""
        try:
            from deep_translator import GoogleTranslator
            
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated = translator.translate(text)
            
            logger.info("Translation completed")
            return translated
            
        except Exception as e:
            logger.error(f"Google Translate error: {e}")
            return None
    
    def _translate_deepl(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Optional[str]:
        """Translate using DeepL."""
        try:
            from deep_translator import DeeplTranslator
            from utils.config_manager import get_config_manager
            
            config = get_config_manager()
            api_key = config.get_api_key('deepl_api_key')
            
            if not api_key:
                logger.error("DeepL API key not configured")
                return None
            
            translator = DeeplTranslator(api_key=api_key, source=source_lang, target=target_lang)
            translated = translator.translate(text)
            
            logger.info("Translation completed")
            return translated
            
        except Exception as e:
            logger.error(f"DeepL error: {e}")
            return None
