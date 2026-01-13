"""Emotion-based TTS using SSML."""
import os
from typing import Optional
from utils.logger import get_logger

logger = get_logger()


class EmotionTTS:
    """Emotion-based Text-to-Speech using SSML."""
    
    EMOTIONS = {
        'neutral': {'style': 'neutral', 'intensity': 1.0},
        'happy': {'style': 'cheerful', 'intensity': 1.5},
        'sad': {'style': 'sad', 'intensity': 1.0},
        'angry': {'style': 'angry', 'intensity': 1.5},
        'excited': {'style': 'excited', 'intensity': 2.0},
        'friendly': {'style': 'friendly', 'intensity': 1.2},
    }
    
    def __init__(self, base_engine):
        """
        Initialize emotion TTS wrapper.
        
        Args:
            base_engine: Base TTS engine (Azure or Google Cloud)
        """
        self.base_engine = base_engine
        self.name = f"{base_engine.name} (Emotion)"
        logger.info(f"Emotion TTS initialized with {base_engine.name}")
    
    def build_ssml(
        self,
        text: str,
        voice_name: str,
        language: str,
        emotion: str = 'neutral',
        rate: float = 1.0,
        pitch: float = 1.0
    ) -> str:
        """
        Build SSML with emotion tags.
        
        Args:
            text: Text to synthesize
            voice_name: Voice name
            language: Language code
            emotion: Emotion type
            rate: Speech rate
            pitch: Speech pitch
            
        Returns:
            SSML string
        """
        emotion_data = self.EMOTIONS.get(emotion, self.EMOTIONS['neutral'])
        style = emotion_data['style']
        
        rate_percent = f"{int((rate - 1.0) * 100):+d}%"
        pitch_percent = f"{int((pitch - 1.0) * 50):+d}%"
        
        # Azure SSML format with emotion/style
        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' 
               xmlns:mstts='https://www.w3.org/2001/mstts' xml:lang='{language}'>
            <voice name='{voice_name}'>
                <mstts:express-as style='{style}'>
                    <prosody rate='{rate_percent}' pitch='{pitch_percent}'>
                        {text}
                    </prosody>
                </mstts:express-as>
            </voice>
        </speak>
        """
        
        return ssml
    
    def synthesize(
        self,
        text: str,
        output_path: str,
        language: str = 'en-US',
        voice_name: Optional[str] = None,
        emotion: str = 'neutral',
        rate: float = 1.0,
        pitch: float = 1.0,
        **kwargs
    ) -> bool:
        """
        Synthesize speech with emotion.
        
        Args:
            text: Text to synthesize
            output_path: Output audio file path
            language: Language code
            voice_name: Voice name
            emotion: Emotion type
            rate: Speech rate
            pitch: Speech pitch
            **kwargs: Additional parameters
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not text or not text.strip():
                logger.error("Empty text provided")
                return False
            
            # Validate emotion
            if emotion not in self.EMOTIONS:
                logger.warning(f"Emotion '{emotion}' not supported, using 'neutral'")
                emotion = 'neutral'
            
            logger.info(f"Synthesizing with emotion: {emotion}")
            
            # Use base engine with emotion parameters
            return self.base_engine.synthesize(
                text=text,
                output_path=output_path,
                language=language,
                voice_name=voice_name,
                rate=rate,
                pitch=pitch,
                **kwargs
            )
            
        except Exception as e:
            logger.error(f"Error in emotion TTS synthesis: {e}")
            return False
    
    def get_supported_emotions(self):
        """Get list of supported emotions."""
        return list(self.EMOTIONS.keys())
