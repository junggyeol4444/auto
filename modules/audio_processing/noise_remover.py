"""Audio noise removal using DeepFilterNet."""
import os
import subprocess
from typing import Optional
from utils.logger import get_logger

logger = get_logger()


class NoiseRemover:
    """Remove noise from audio using DeepFilterNet."""
    
    def __init__(self):
        """Initialize noise remover."""
        self.name = "DeepFilterNet Noise Remover"
        logger.info("Noise remover initialized")
    
    def remove_noise(
        self,
        input_path: str,
        output_path: str,
        level: str = 'medium'
    ) -> bool:
        """
        Remove noise from audio file.
        
        Args:
            input_path: Path to input audio file
            output_path: Path to output audio file
            level: Noise reduction level ('light', 'medium', 'heavy')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(input_path):
                logger.error(f"Input file not found: {input_path}")
                return False
            
            logger.info(f"Removing noise from {input_path} (level={level})")
            
            # Create output directory
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            # Use DeepFilterNet CLI if available
            try:
                cmd = ['deepFilter', input_path, '-o', output_path]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    logger.info(f"Noise removed, output saved to {output_path}")
                    return True
                else:
                    logger.error(f"DeepFilterNet failed: {result.stderr}")
                    return False
                    
            except FileNotFoundError:
                logger.warning("DeepFilterNet CLI not found, using fallback method")
                return self._fallback_noise_removal(input_path, output_path)
                
        except Exception as e:
            logger.error(f"Error removing noise: {e}")
            return False
    
    def _fallback_noise_removal(self, input_path: str, output_path: str) -> bool:
        """
        Fallback noise removal using librosa.
        
        Args:
            input_path: Path to input audio
            output_path: Path to output audio
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import librosa
            import soundfile as sf
            import numpy as np
            
            # Load audio
            y, sr = librosa.load(input_path, sr=None)
            
            # Simple noise reduction using spectral gating
            # Estimate noise from first 0.5 seconds
            noise_sample = y[:int(sr * 0.5)]
            noise_level = np.mean(np.abs(noise_sample))
            
            # Apply threshold
            y_denoised = np.where(np.abs(y) > noise_level * 2, y, 0)
            
            # Save
            sf.write(output_path, y_denoised, sr)
            
            logger.info(f"Fallback noise removal completed, saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Fallback noise removal failed: {e}")
            return False
