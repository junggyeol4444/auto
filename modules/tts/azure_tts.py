"""Azure Text-to-Speech engine implementation."""
import os
import azure.cognitiveservices.speech as speechsdk
from typing import Optional
from utils.logger import get_logger
from utils.config_manager import get_config_manager

logger = get_logger()


class AzureTTSEngine:
    """Azure Text-to-Speech engine."""
    
    # Sample voices for different languages
    SAMPLE_VOICES = {
        'en-US': {'male': 'en-US-GuyNeural', 'female': 'en-US-JennyNeural'},
        'ko-KR': {'male': 'ko-KR-InJoonNeural', 'female': 'ko-KR-SunHiNeural'},
        'ja-JP': {'male': 'ja-JP-KeitaNeural', 'female': 'ja-JP-NanamiNeural'},
        'zh-CN': {'male': 'zh-CN-YunxiNeural', 'female': 'zh-CN-XiaoxiaoNeural'},
        'es-ES': {'male': 'es-ES-AlvaroNeural', 'female': 'es-ES-ElviraNeural'},
        'fr-FR': {'male': 'fr-FR-HenriNeural', 'female': 'fr-FR-DeniseNeural'},
        'de-DE': {'male': 'de-DE-ConradNeural', 'female': 'de-DE-KatjaNeural'},
    }
    
    def __init__(self, api_key: Optional[str] = None, region: Optional[str] = None):
        """
        Initialize Azure TTS engine.
        
        Args:
            api_key: Azure Speech API key
            region: Azure region (e.g., 'eastus')
        """
        config_manager = get_config_manager()
        
        self.api_key = api_key or config_manager.get_api_key('azure_speech_key')
        self.region = region or config_manager.get('api_keys.azure_speech_region', 'eastus')
        self.name = "Azure TTS"
        
        if not self.api_key:
            logger.warning("Azure Speech API key not configured")
        else:
            logger.info(f"Azure TTS engine initialized (region={self.region})")
    
    def synthesize(
        self,
        text: str,
        output_path: str,
        language: str = 'en-US',
        voice_name: Optional[str] = None,
        gender: str = 'female',
        rate: float = 1.0,
        pitch: float = 1.0,
        **kwargs
    ) -> bool:
        """
        Synthesize speech from text.
        
        Args:
            text: Text to synthesize
            output_path: Output audio file path
            language: Language locale (e.g., 'en-US', 'ko-KR')
            voice_name: Specific voice name (overrides gender)
            gender: 'male' or 'female'
            rate: Speech rate (0.5 to 2.0)
            pitch: Speech pitch (0.5 to 2.0)
            **kwargs: Additional parameters
            
        Returns:
            True if successful, False otherwise
        """
        if not self.api_key:
            logger.error("Azure API key not configured")
            return False
        
        try:
            if not text or not text.strip():
                logger.error("Empty text provided")
                return False
            
            # Configure speech
            speech_config = speechsdk.SpeechConfig(
                subscription=self.api_key,
                region=self.region
            )
            
            # Select voice
            if not voice_name:
                if language in self.SAMPLE_VOICES:
                    voice_name = self.SAMPLE_VOICES[language].get(gender, 
                                                                  self.SAMPLE_VOICES[language]['female'])
                else:
                    voice_name = 'en-US-JennyNeural'
            
            speech_config.speech_synthesis_voice_name = voice_name
            
            # Create output directory
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            # Configure audio output
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
            
            # Create synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            # Build SSML if rate or pitch is modified
            if rate != 1.0 or pitch != 1.0:
                rate_percent = f"{int((rate - 1.0) * 100):+d}%"
                pitch_percent = f"{int((pitch - 1.0) * 50):+d}%"  # Pitch range is more limited
                
                ssml_text = f"""
                <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{language}'>
                    <voice name='{voice_name}'>
                        <prosody rate='{rate_percent}' pitch='{pitch_percent}'>
                            {text}
                        </prosody>
                    </voice>
                </speak>
                """
                
                logger.info(f"Synthesizing with Azure TTS (voice={voice_name}, rate={rate_percent}, pitch={pitch_percent})")
                result = synthesizer.speak_ssml_async(ssml_text).get()
            else:
                logger.info(f"Synthesizing with Azure TTS (voice={voice_name})")
                result = synthesizer.speak_text_async(text).get()
            
            # Check result
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info(f"Audio saved to {output_path}")
                return True
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                logger.error(f"Speech synthesis canceled: {cancellation_details.reason}")
                if cancellation_details.error_details:
                    logger.error(f"Error details: {cancellation_details.error_details}")
                return False
            else:
                logger.error(f"Unexpected result reason: {result.reason}")
                return False
                
        except Exception as e:
            logger.error(f"Error in Azure TTS synthesis: {e}")
            return False
    
    def get_voice(self, language: str, gender: str = 'female') -> Optional[str]:
        """Get voice name for language and gender."""
        if language in self.SAMPLE_VOICES:
            return self.SAMPLE_VOICES[language].get(gender)
        return None
