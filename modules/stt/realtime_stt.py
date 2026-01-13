"""Real-time Speech-to-Text implementation."""
from typing import Optional, Callable
from utils.logger import get_logger

logger = get_logger()

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    logger.warning("SpeechRecognition not installed. Install with: pip install SpeechRecognition")


class RealtimeSTT:
    """Real-time Speech-to-Text using microphone."""
    
    def __init__(self):
        """Initialize real-time STT."""
        if not SPEECH_RECOGNITION_AVAILABLE:
            logger.warning("SpeechRecognition not available")
            self.recognizer = None
            self.microphone = None
        else:
            self.recognizer = sr.Recognizer()
            self.microphone = None
        
        self.name = "Real-time STT"
        logger.info("Real-time STT initialized")
    
    def _get_microphone(self):
        """Get or create microphone instance."""
        if not SPEECH_RECOGNITION_AVAILABLE:
            return None
        
        if self.microphone is None:
            try:
                self.microphone = sr.Microphone()
            except Exception as e:
                logger.error(f"Failed to initialize microphone: {e}")
                return None
        return self.microphone
    
    def listen(
        self,
        duration: Optional[int] = None,
        language: str = 'en-US',
        engine: str = 'google'
    ) -> Optional[str]:
        """
        Listen and transcribe from microphone.
        
        Args:
            duration: Maximum duration to listen (None = unlimited)
            language: Language code
            engine: Recognition engine ('google', 'sphinx')
            
        Returns:
            Transcribed text or None if error
        """
        microphone = self._get_microphone()
        if not microphone:
            return None
        
        try:
            with microphone as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                logger.info("Listening...")
                if duration:
                    audio = self.recognizer.listen(source, timeout=duration)
                else:
                    audio = self.recognizer.listen(source)
                
                logger.info("Processing audio...")
                
                # Recognize speech
                if engine == 'google':
                    text = self.recognizer.recognize_google(audio, language=language)
                elif engine == 'sphinx':
                    text = self.recognizer.recognize_sphinx(audio)
                else:
                    logger.error(f"Unknown engine: {engine}")
                    return None
                
                logger.info(f"Recognized: {text}")
                return text
                
        except sr.WaitTimeoutError:
            logger.warning("Listening timed out")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error in real-time STT: {e}")
            return None
    
    def listen_continuous(
        self,
        callback: Callable[[str], None],
        language: str = 'en-US',
        engine: str = 'google'
    ) -> None:
        """
        Listen continuously and call callback with recognized text.
        
        Args:
            callback: Function to call with recognized text
            language: Language code
            engine: Recognition engine
        """
        microphone = self._get_microphone()
        if not microphone:
            return
        
        try:
            with microphone as source:
                logger.info("Starting continuous listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                while True:
                    try:
                        audio = self.recognizer.listen(source, timeout=5)
                        
                        if engine == 'google':
                            text = self.recognizer.recognize_google(audio, language=language)
                        elif engine == 'sphinx':
                            text = self.recognizer.recognize_sphinx(audio)
                        else:
                            continue
                        
                        callback(text)
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except KeyboardInterrupt:
                        logger.info("Stopping continuous listening")
                        break
                        
        except Exception as e:
            logger.error(f"Error in continuous listening: {e}")
    
    def transcribe_file(
        self,
        audio_path: str,
        language: str = 'en-US',
        engine: str = 'google'
    ) -> Optional[str]:
        """
        Transcribe audio file.
        
        Args:
            audio_path: Path to audio file
            language: Language code
            engine: Recognition engine
            
        Returns:
            Transcribed text or None if error
        """
        try:
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
                
                if engine == 'google':
                    text = self.recognizer.recognize_google(audio, language=language)
                elif engine == 'sphinx':
                    text = self.recognizer.recognize_sphinx(audio)
                else:
                    logger.error(f"Unknown engine: {engine}")
                    return None
                
                logger.info(f"Transcribed: {text}")
                return text
                
        except Exception as e:
            logger.error(f"Error transcribing file: {e}")
            return None
