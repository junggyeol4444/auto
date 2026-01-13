"""pyttsx3 (offline TTS) engine implementation."""
import os
import pyttsx3
from typing import Optional, List, Dict
from utils.logger import get_logger

logger = get_logger()


class Pyttsx3Engine:
    """Offline TTS engine using pyttsx3."""
    
    def __init__(self):
        """Initialize pyttsx3 engine."""
        try:
            self.engine = pyttsx3.init()
            self.name = "pyttsx3"
            logger.info("pyttsx3 engine initialized")
        except Exception as e:
            logger.error(f"Failed to initialize pyttsx3: {e}")
            self.engine = None
    
    def synthesize(
        self,
        text: str,
        output_path: str,
        voice_id: Optional[str] = None,
        rate: int = 150,
        volume: float = 1.0,
        **kwargs
    ) -> bool:
        """
        Synthesize speech from text.
        
        Args:
            text: Text to synthesize
            output_path: Output audio file path
            voice_id: Voice ID (None for default)
            rate: Speech rate (words per minute, default 150)
            volume: Volume level (0.0 to 1.0)
            **kwargs: Additional parameters
            
        Returns:
            True if successful, False otherwise
        """
        if not self.engine:
            logger.error("Engine not initialized")
            return False
        
        try:
            if not text or not text.strip():
                logger.error("Empty text provided")
                return False
            
            # Set voice if specified
            if voice_id:
                self.engine.setProperty('voice', voice_id)
            
            # Set rate and volume
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
            
            # Create output directory
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            # Save to file
            logger.info(f"Synthesizing text with pyttsx3 (rate={rate}, volume={volume})")
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
            logger.info(f"Audio saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error in pyttsx3 synthesis: {e}")
            return False
    
    def get_voices(self) -> List[Dict[str, str]]:
        """
        Get available voices.
        
        Returns:
            List of voice dictionaries with 'id', 'name', 'languages', 'gender'
        """
        if not self.engine:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            voice_list = []
            
            for voice in voices:
                voice_info = {
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages if hasattr(voice, 'languages') else [],
                    'gender': voice.gender if hasattr(voice, 'gender') else 'unknown'
                }
                voice_list.append(voice_info)
            
            return voice_list
        except Exception as e:
            logger.error(f"Error getting voices: {e}")
            return []
    
    def get_male_voice(self) -> Optional[str]:
        """Get first male voice ID."""
        voices = self.get_voices()
        for voice in voices:
            if 'male' in voice['name'].lower() or voice['gender'] == 'male':
                return voice['id']
        return None
    
    def get_female_voice(self) -> Optional[str]:
        """Get first female voice ID."""
        voices = self.get_voices()
        for voice in voices:
            if 'female' in voice['name'].lower() or voice['gender'] == 'female':
                return voice['id']
        return None
