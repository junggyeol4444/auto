"""gTTS (Google Text-to-Speech) engine implementation."""
import os
from gtts import gTTS
from typing import Optional
from utils.logger import get_logger

logger = get_logger()


class GTTSEngine:
    """Google TTS engine using gTTS library."""
    
    # Supported languages
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'ko': 'Korean',
        'ja': 'Japanese',
        'zh-cn': 'Chinese (Simplified)',
        'zh-tw': 'Chinese (Traditional)',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'th': 'Thai',
        'vi': 'Vietnamese',
        'id': 'Indonesian',
        'tr': 'Turkish',
        'pl': 'Polish',
        'nl': 'Dutch',
        'sv': 'Swedish'
    }
    
    def __init__(self):
        """Initialize gTTS engine."""
        self.name = "gTTS"
        logger.info("gTTS engine initialized")
    
    def synthesize(
        self,
        text: str,
        output_path: str,
        language: str = 'en',
        slow: bool = False,
        **kwargs
    ) -> bool:
        """
        Synthesize speech from text.
        
        Args:
            text: Text to synthesize
            output_path: Output audio file path
            language: Language code (e.g., 'en', 'ko', 'ja')
            slow: Speak slowly
            **kwargs: Additional parameters (ignored for gTTS)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not text or not text.strip():
                logger.error("Empty text provided")
                return False
            
            # Validate language
            if language not in self.SUPPORTED_LANGUAGES:
                logger.warning(f"Language {language} not supported, using 'en'")
                language = 'en'
            
            # Create TTS object
            logger.info(f"Synthesizing text with gTTS (language={language}, slow={slow})")
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Save to file
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            tts.save(output_path)
            
            logger.info(f"Audio saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error in gTTS synthesis: {e}")
            return False
    
    def get_supported_languages(self):
        """Get list of supported languages."""
        return self.SUPPORTED_LANGUAGES
    
    def is_language_supported(self, language: str) -> bool:
        """Check if language is supported."""
        return language in self.SUPPORTED_LANGUAGES
