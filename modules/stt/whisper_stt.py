"""Whisper-based Speech-to-Text implementation."""
import os
from typing import Optional, Dict, List
from utils.logger import get_logger

logger = get_logger()

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    logger.warning("Whisper not installed. Install with: pip install openai-whisper")


class WhisperSTT:
    """Speech-to-Text using OpenAI Whisper."""
    
    MODEL_SIZES = ['tiny', 'base', 'small', 'medium', 'large']
    
    def __init__(self, model_size: str = 'base'):
        """
        Initialize Whisper STT.
        
        Args:
            model_size: Model size (tiny, base, small, medium, large)
        """
        if model_size not in self.MODEL_SIZES:
            logger.warning(f"Invalid model size {model_size}, using 'base'")
            model_size = 'base'
        
        self.model_size = model_size
        self.model = None
        self.name = f"Whisper ({model_size})"
        
        if not WHISPER_AVAILABLE:
            logger.warning("Whisper not available. Install with: pip install openai-whisper")
        else:
            logger.info(f"Whisper STT initialized (model={model_size})")
    
    def _load_model(self):
        """Load Whisper model if not already loaded."""
        if not WHISPER_AVAILABLE:
            logger.error("Whisper not installed")
            return False
        
        if self.model is None:
            try:
                logger.info(f"Loading Whisper {self.model_size} model...")
                self.model = whisper.load_model(self.model_size)
                logger.info("Model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load Whisper model: {e}")
                return False
        return True
    
    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        task: str = 'transcribe',
        **kwargs
    ) -> Optional[Dict]:
        """
        Transcribe audio file.
        
        Args:
            audio_path: Path to audio file
            language: Language code (None for auto-detect)
            task: 'transcribe' or 'translate' (to English)
            **kwargs: Additional Whisper options
            
        Returns:
            Transcription result dictionary or None if error
        """
        if not self._load_model():
            return None
        
        try:
            if not os.path.exists(audio_path):
                logger.error(f"Audio file not found: {audio_path}")
                return None
            
            logger.info(f"Transcribing {audio_path} (language={language}, task={task})")
            
            # Transcribe
            result = self.model.transcribe(
                audio_path,
                language=language,
                task=task,
                **kwargs
            )
            
            logger.info(f"Transcription completed (detected language: {result.get('language', 'unknown')})")
            return result
            
        except Exception as e:
            logger.error(f"Error in transcription: {e}")
            return None
    
    def transcribe_with_timestamps(
        self,
        audio_path: str,
        language: Optional[str] = None
    ) -> Optional[List[Dict]]:
        """
        Transcribe audio with word-level timestamps.
        
        Args:
            audio_path: Path to audio file
            language: Language code (None for auto-detect)
            
        Returns:
            List of segments with timestamps or None if error
        """
        result = self.transcribe(audio_path, language=language)
        
        if result:
            return result.get('segments', [])
        return None
    
    def generate_srt(
        self,
        audio_path: str,
        output_path: str,
        language: Optional[str] = None
    ) -> bool:
        """
        Generate SRT subtitle file.
        
        Args:
            audio_path: Path to audio file
            output_path: Path to output SRT file
            language: Language code (None for auto-detect)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            segments = self.transcribe_with_timestamps(audio_path, language)
            
            if not segments:
                logger.error("No segments to write")
                return False
            
            # Write SRT file
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(segments, start=1):
                    start_time = self._format_timestamp(segment['start'])
                    end_time = self._format_timestamp(segment['end'])
                    text = segment['text'].strip()
                    
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")
            
            logger.info(f"SRT file saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating SRT: {e}")
            return False
    
    def _format_timestamp(self, seconds: float) -> str:
        """
        Format timestamp for SRT format.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted timestamp (HH:MM:SS,mmm)
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def detect_language(self, audio_path: str) -> Optional[str]:
        """
        Detect language of audio file.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Detected language code or None
        """
        if not self._load_model():
            return None
        
        try:
            # Load audio and pad/trim it to fit 30 seconds
            audio = whisper.load_audio(audio_path)
            audio = whisper.pad_or_trim(audio)
            
            # Make log-Mel spectrogram
            mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
            
            # Detect language
            _, probs = self.model.detect_language(mel)
            detected_language = max(probs, key=probs.get)
            
            logger.info(f"Detected language: {detected_language} (confidence: {probs[detected_language]:.2f})")
            return detected_language
            
        except Exception as e:
            logger.error(f"Error detecting language: {e}")
            return None
