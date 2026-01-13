"""Audio normalization with LUFS."""
import os
from typing import Optional
from utils.logger import get_logger

logger = get_logger()


class Normalizer:
    """Normalize audio levels using LUFS standards."""
    
    def __init__(self):
        """Initialize normalizer."""
        self.name = "Audio Normalizer"
        logger.info("Audio normalizer initialized")
    
    def normalize(
        self,
        input_path: str,
        output_path: str,
        target_lufs: float = -16.0,
        peak_limit: float = -1.0
    ) -> bool:
        """
        Normalize audio to target LUFS.
        
        Args:
            input_path: Path to input audio file
            output_path: Path to output audio file
            target_lufs: Target loudness in LUFS (default -16.0)
            peak_limit: Peak limiter threshold in dB (default -1.0)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(input_path):
                logger.error(f"Input file not found: {input_path}")
                return False
            
            import librosa
            import soundfile as sf
            import pyloudnorm as pyln
            
            logger.info(f"Normalizing {input_path} to {target_lufs} LUFS")
            
            # Load audio
            data, rate = librosa.load(input_path, sr=None, mono=False)
            
            # Transpose if stereo
            if len(data.shape) == 2:
                data = data.T
            
            # Measure loudness
            meter = pyln.Meter(rate)
            loudness = meter.integrated_loudness(data)
            
            logger.info(f"Current loudness: {loudness:.2f} LUFS")
            
            # Normalize
            normalized_data = pyln.normalize.loudness(data, loudness, target_lufs)
            
            # Apply peak limiting
            if peak_limit < 0:
                peak_db = 10 ** (peak_limit / 20)
                normalized_data = normalized_data / max(abs(normalized_data.max()), abs(normalized_data.min())) * peak_db
            
            # Create output directory
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            # Save
            if len(normalized_data.shape) == 2:
                normalized_data = normalized_data.T
            
            sf.write(output_path, normalized_data, rate)
            
            logger.info(f"Normalized audio saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error normalizing audio: {e}")
            return False
    
    def measure_loudness(self, input_path: str) -> Optional[float]:
        """
        Measure loudness of audio file.
        
        Args:
            input_path: Path to audio file
            
        Returns:
            Loudness in LUFS or None if error
        """
        try:
            import librosa
            import pyloudnorm as pyln
            
            # Load audio
            data, rate = librosa.load(input_path, sr=None, mono=False)
            
            if len(data.shape) == 2:
                data = data.T
            
            # Measure
            meter = pyln.Meter(rate)
            loudness = meter.integrated_loudness(data)
            
            logger.info(f"Measured loudness: {loudness:.2f} LUFS")
            return loudness
            
        except Exception as e:
            logger.error(f"Error measuring loudness: {e}")
            return None
