"""Language detection utility"""


class LanguageDetector:
    """Detect language of text"""
    
    def __init__(self):
        self.detector = None
        self._init_detector()
    
    def _init_detector(self):
        """Initialize language detector"""
        try:
            from langdetect import detect, detect_langs
            self.detect = detect
            self.detect_langs = detect_langs
        except ImportError:
            print("langdetect not available. Install with: pip install langdetect")
            self.detect = None
            self.detect_langs = None
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of text
        
        Args:
            text: Text to detect language of
            
        Returns:
            Language code (e.g., 'en', 'ko', 'ja')
        """
        if not self.detect or not text or not text.strip():
            return 'unknown'
        
        try:
            return self.detect(text)
        except Exception as e:
            print(f"Language detection error: {e}")
            return 'unknown'
    
    def detect_languages_with_confidence(self, text: str) -> list:
        """
        Detect languages with confidence scores
        
        Args:
            text: Text to detect language of
            
        Returns:
            List of (language, confidence) tuples
        """
        if not self.detect_langs or not text or not text.strip():
            return []
        
        try:
            results = self.detect_langs(text)
            return [(str(r.lang), r.prob) for r in results]
        except Exception as e:
            print(f"Language detection error: {e}")
            return []
    
    def is_available(self) -> bool:
        """Check if language detector is available"""
        return self.detect is not None
