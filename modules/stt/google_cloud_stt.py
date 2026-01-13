"""Google Cloud Speech-to-Text implementation."""
import os
from typing import Optional, List, Dict
from google.cloud import speech
from utils.logger import get_logger
from utils.config_manager import get_config_manager

logger = get_logger()


class GoogleCloudSTT:
    """Google Cloud Speech-to-Text engine."""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google Cloud STT.
        
        Args:
            credentials_path: Path to Google Cloud credentials JSON
        """
        config_manager = get_config_manager()
        self.credentials_path = credentials_path or config_manager.get_api_key('google_cloud_credentials_path')
        self.name = "Google Cloud STT"
        
        if self.credentials_path and os.path.exists(self.credentials_path):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials_path
            logger.info("Google Cloud STT initialized")
        else:
            logger.warning("Google Cloud credentials not configured")
        
        self.client = None
    
    def _get_client(self):
        """Get or create STT client."""
        if self.client is None:
            try:
                self.client = speech.SpeechClient()
            except Exception as e:
                logger.error(f"Failed to create Google Cloud STT client: {e}")
                return None
        return self.client
    
    def transcribe(
        self,
        audio_path: str,
        language: str = 'en-US',
        enable_word_time_offsets: bool = True,
        **kwargs
    ) -> Optional[Dict]:
        """
        Transcribe audio file.
        
        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'en-US', 'ko-KR')
            enable_word_time_offsets: Enable word-level timestamps
            **kwargs: Additional options
            
        Returns:
            Transcription result dictionary or None if error
        """
        client = self._get_client()
        if not client:
            return None
        
        try:
            if not os.path.exists(audio_path):
                logger.error(f"Audio file not found: {audio_path}")
                return None
            
            # Load audio content
            with open(audio_path, 'rb') as f:
                content = f.read()
            
            audio = speech.RecognitionAudio(content=content)
            
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                language_code=language,
                enable_word_time_offsets=enable_word_time_offsets,
                enable_automatic_punctuation=True,
            )
            
            logger.info(f"Transcribing {audio_path} with Google Cloud STT")
            
            # Perform transcription
            response = client.recognize(config=config, audio=audio)
            
            # Process results
            full_transcript = ""
            segments = []
            
            for result in response.results:
                alternative = result.alternatives[0]
                full_transcript += alternative.transcript + " "
                
                if enable_word_time_offsets:
                    for word_info in alternative.words:
                        segments.append({
                            'word': word_info.word,
                            'start_time': word_info.start_time.total_seconds(),
                            'end_time': word_info.end_time.total_seconds()
                        })
            
            result_dict = {
                'text': full_transcript.strip(),
                'segments': segments
            }
            
            logger.info("Transcription completed")
            return result_dict
            
        except Exception as e:
            logger.error(f"Error in Google Cloud STT transcription: {e}")
            return None
