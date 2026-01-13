"""Google Cloud Text-to-Speech engine implementation."""
import os
from typing import Optional
from utils.logger import get_logger
from utils.config_manager import get_config_manager

logger = get_logger()

try:
    from google.cloud import texttospeech
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False
    logger.warning("Google Cloud not installed. Install with: pip install google-cloud-texttospeech")


class GoogleCloudTTSEngine:
    """Google Cloud Text-to-Speech engine."""
    
    # Sample voices
    SAMPLE_VOICES = {
        'en-US': {'male': 'en-US-Standard-D', 'female': 'en-US-Standard-C'},
        'ko-KR': {'male': 'ko-KR-Standard-C', 'female': 'ko-KR-Standard-A'},
        'ja-JP': {'male': 'ja-JP-Standard-C', 'female': 'ja-JP-Standard-A'},
        'zh-CN': {'male': 'cmn-CN-Standard-C', 'female': 'cmn-CN-Standard-A'},
    }
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google Cloud TTS engine.
        
        Args:
            credentials_path: Path to Google Cloud credentials JSON
        """
        config_manager = get_config_manager()
        self.credentials_path = credentials_path or config_manager.get_api_key('google_cloud_credentials_path')
        self.name = "Google Cloud TTS"
        
        if not GOOGLE_CLOUD_AVAILABLE:
            logger.warning("Google Cloud SDK not available")
        elif self.credentials_path and os.path.exists(self.credentials_path):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials_path
            logger.info("Google Cloud TTS engine initialized")
        else:
            logger.warning("Google Cloud credentials not configured")
        
        self.client = None
    
    def _get_client(self):
        """Get or create TTS client."""
        if not GOOGLE_CLOUD_AVAILABLE:
            return None
        
        if self.client is None:
            try:
                self.client = texttospeech.TextToSpeechClient()
            except Exception as e:
                logger.error(f"Failed to create Google Cloud TTS client: {e}")
                return None
        return self.client
    
    def synthesize(
        self,
        text: str,
        output_path: str,
        language: str = 'en-US',
        voice_name: Optional[str] = None,
        gender: str = 'female',
        pitch: float = 0.0,
        speaking_rate: float = 1.0,
        **kwargs
    ) -> bool:
        """
        Synthesize speech from text.
        
        Args:
            text: Text to synthesize
            output_path: Output audio file path
            language: Language code (e.g., 'en-US', 'ko-KR')
            voice_name: Specific voice name (overrides gender)
            gender: 'male' or 'female'
            pitch: Pitch adjustment in semitones (-20.0 to 20.0)
            speaking_rate: Speaking rate (0.25 to 4.0)
            **kwargs: Additional parameters
            
        Returns:
            True if successful, False otherwise
        """
        client = self._get_client()
        if not client:
            logger.error("Google Cloud TTS client not initialized")
            return False
        
        try:
            if not text or not text.strip():
                logger.error("Empty text provided")
                return False
            
            # Set the text input
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Select voice
            if not voice_name:
                if language in self.SAMPLE_VOICES:
                    voice_name = self.SAMPLE_VOICES[language].get(gender,
                                                                  self.SAMPLE_VOICES[language]['female'])
                else:
                    voice_name = 'en-US-Standard-C'
            
            # Build voice params
            voice_gender = (texttospeech.SsmlVoiceGender.MALE 
                           if gender == 'male' 
                           else texttospeech.SsmlVoiceGender.FEMALE)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=language,
                name=voice_name,
                ssml_gender=voice_gender
            )
            
            # Configure audio
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                pitch=pitch,
                speaking_rate=speaking_rate
            )
            
            # Perform synthesis
            logger.info(f"Synthesizing with Google Cloud TTS (voice={voice_name}, rate={speaking_rate})")
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Save to file
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            with open(output_path, 'wb') as out:
                out.write(response.audio_content)
            
            logger.info(f"Audio saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error in Google Cloud TTS synthesis: {e}")
            return False
