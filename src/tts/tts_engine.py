"""
Text-to-Speech Module
Supports local TTS (gTTS, pyttsx3) and custom TTS models
"""
import logging
import os
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class TTSEngine:
    """Base class for TTS engines"""
    
    def synthesize(self, text: str, output_path: str) -> bool:
        """Synthesize speech from text"""
        raise NotImplementedError


class GTTSEngine(TTSEngine):
    """Google Text-to-Speech engine"""
    
    def __init__(self, lang: str = 'ko'):
        self.lang = lang
        try:
            from gtts import gTTS
            self.gTTS = gTTS
            logger.info("gTTS engine initialized")
        except ImportError:
            logger.error("gTTS not installed. Run: pip install gTTS")
            self.gTTS = None
    
    def synthesize(self, text: str, output_path: str) -> bool:
        """Synthesize speech using gTTS"""
        if not self.gTTS:
            logger.error("gTTS not available")
            return False
        
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            tts = self.gTTS(text=text, lang=self.lang, slow=False)
            tts.save(output_path)
            
            logger.info(f"Speech synthesized successfully: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error synthesizing speech with gTTS: {e}")
            return False


class Pyttsx3Engine(TTSEngine):
    """Pyttsx3 offline TTS engine"""
    
    def __init__(self, rate: int = 150, volume: float = 1.0):
        self.rate = rate
        self.volume = volume
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            logger.info("Pyttsx3 engine initialized")
        except ImportError:
            logger.error("pyttsx3 not installed. Run: pip install pyttsx3")
            self.engine = None
        except Exception as e:
            logger.error(f"Error initializing pyttsx3: {e}")
            self.engine = None
    
    def synthesize(self, text: str, output_path: str) -> bool:
        """Synthesize speech using pyttsx3"""
        if not self.engine:
            logger.error("Pyttsx3 engine not available")
            return False
        
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
            logger.info(f"Speech synthesized successfully: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error synthesizing speech with pyttsx3: {e}")
            return False


class CustomTTSEngine(TTSEngine):
    """Custom TTS engine supporting trained models (Tortoise TTS, Coqui TTS, etc.)"""
    
    def __init__(self, model_path: Optional[str] = None, engine_type: str = 'coqui'):
        self.model_path = model_path
        self.engine_type = engine_type
        self.model = None
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def load_model(self, model_path: str) -> bool:
        """Load a custom TTS model"""
        try:
            if self.engine_type == 'coqui':
                # Coqui TTS implementation
                try:
                    from TTS.api import TTS
                    self.model = TTS(model_path=model_path)
                    logger.info(f"Coqui TTS model loaded from {model_path}")
                    return True
                except ImportError:
                    logger.error("Coqui TTS not installed. Run: pip install TTS")
                    return False
            else:
                logger.warning(f"Unsupported engine type: {self.engine_type}")
                return False
                
        except Exception as e:
            logger.error(f"Error loading custom TTS model: {e}")
            return False
    
    def synthesize(self, text: str, output_path: str) -> bool:
        """Synthesize speech using custom model"""
        if not self.model:
            logger.error("No custom TTS model loaded")
            return False
        
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            if self.engine_type == 'coqui':
                self.model.tts_to_file(text=text, file_path=output_path)
            
            logger.info(f"Speech synthesized with custom model: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error synthesizing with custom TTS: {e}")
            return False


class TTSManager:
    """Manager class for TTS operations"""
    
    def __init__(self, engine_type: str = 'gtts', **kwargs):
        """
        Initialize TTS manager with specified engine
        
        Args:
            engine_type: 'gtts', 'pyttsx3', or 'custom'
            **kwargs: Additional arguments for the engine
        """
        self.engine_type = engine_type
        self.engine = self._create_engine(engine_type, **kwargs)
    
    def _create_engine(self, engine_type: str, **kwargs) -> TTSEngine:
        """Create TTS engine based on type"""
        if engine_type == 'gtts':
            lang = kwargs.get('lang', 'ko')
            return GTTSEngine(lang=lang)
        
        elif engine_type == 'pyttsx3':
            rate = kwargs.get('rate', 150)
            volume = kwargs.get('volume', 1.0)
            return Pyttsx3Engine(rate=rate, volume=volume)
        
        elif engine_type == 'custom':
            model_path = kwargs.get('model_path')
            custom_engine_type = kwargs.get('custom_engine_type', 'coqui')
            return CustomTTSEngine(model_path=model_path, engine_type=custom_engine_type)
        
        else:
            logger.warning(f"Unknown engine type: {engine_type}. Using gTTS.")
            return GTTSEngine()
    
    def text_to_speech(self, text: str, output_path: str) -> bool:
        """Convert text to speech"""
        if not self.engine:
            logger.error("TTS engine not initialized")
            return False
        
        logger.info(f"Generating speech with {self.engine_type} engine")
        return self.engine.synthesize(text, output_path)
    
    def split_and_synthesize(self, text: str, output_dir: str, 
                            max_length: int = 500) -> list:
        """
        Split long text into chunks and synthesize each
        
        Returns:
            List of output file paths
        """
        # Split text into sentences
        sentences = text.replace('.\n', '.|').replace('. ', '.|').split('|')
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_length:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Synthesize each chunk
        output_files = []
        os.makedirs(output_dir, exist_ok=True)
        
        for i, chunk in enumerate(chunks):
            output_file = os.path.join(output_dir, f"speech_part_{i+1}.mp3")
            if self.text_to_speech(chunk, output_file):
                output_files.append(output_file)
            else:
                logger.warning(f"Failed to synthesize chunk {i+1}")
        
        logger.info(f"Created {len(output_files)} speech files")
        return output_files
