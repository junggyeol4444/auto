"""Audio source separation using Spleeter/Demucs."""
import os
import subprocess
from typing import Optional, List
from utils.logger import get_logger

logger = get_logger()


class SourceSeparator:
    """Separate audio sources (vocals, accompaniment, etc.)."""
    
    def __init__(self):
        """Initialize source separator."""
        self.name = "Audio Source Separator"
        logger.info("Source separator initialized")
    
    def separate_vocals(
        self,
        input_path: str,
        output_dir: str,
        stems: int = 2,
        engine: str = 'spleeter'
    ) -> bool:
        """
        Separate vocals and accompaniment.
        
        Args:
            input_path: Path to input audio file
            output_dir: Directory for output files
            stems: Number of stems (2, 4, or 5 for spleeter; any for demucs)
            engine: 'spleeter' or 'demucs'
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(input_path):
                logger.error(f"Input file not found: {input_path}")
                return False
            
            os.makedirs(output_dir, exist_ok=True)
            
            logger.info(f"Separating audio sources from {input_path} (engine={engine}, stems={stems})")
            
            if engine == 'spleeter':
                return self._separate_with_spleeter(input_path, output_dir, stems)
            elif engine == 'demucs':
                return self._separate_with_demucs(input_path, output_dir)
            else:
                logger.error(f"Unknown engine: {engine}")
                return False
                
        except Exception as e:
            logger.error(f"Error in source separation: {e}")
            return False
    
    def _separate_with_spleeter(
        self,
        input_path: str,
        output_dir: str,
        stems: int
    ) -> bool:
        """Separate using Spleeter."""
        try:
            # Validate stems
            if stems not in [2, 4, 5]:
                logger.warning(f"Invalid stems {stems} for Spleeter, using 2")
                stems = 2
            
            model_name = f"spleeter:{stems}stems"
            
            cmd = [
                'spleeter',
                'separate',
                '-i', input_path,
                '-p', model_name,
                '-o', output_dir
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                logger.info(f"Spleeter separation completed, output in {output_dir}")
                return True
            else:
                logger.error(f"Spleeter failed: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.error("Spleeter not found. Please install: pip install spleeter")
            return False
        except Exception as e:
            logger.error(f"Spleeter error: {e}")
            return False
    
    def _separate_with_demucs(self, input_path: str, output_dir: str) -> bool:
        """Separate using Demucs."""
        try:
            cmd = [
                'demucs',
                '--out', output_dir,
                input_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                logger.info(f"Demucs separation completed, output in {output_dir}")
                return True
            else:
                logger.error(f"Demucs failed: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.error("Demucs not found. Please install: pip install demucs")
            return False
        except Exception as e:
            logger.error(f"Demucs error: {e}")
            return False
