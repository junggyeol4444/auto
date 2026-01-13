"""Audio volume control and dynamics processing."""
import os
from typing import Optional
from utils.logger import get_logger

logger = get_logger()


class VolumeController:
    """Control and adjust audio volume."""
    
    def __init__(self):
        """Initialize volume controller."""
        self.name = "Volume Controller"
        logger.info("Volume controller initialized")
    
    def adjust_volume(
        self,
        input_path: str,
        output_path: str,
        gain_db: float = 0.0,
        fade_in: float = 0.0,
        fade_out: float = 0.0
    ) -> bool:
        """
        Adjust audio volume.
        
        Args:
            input_path: Path to input audio file
            output_path: Path to output audio file
            gain_db: Volume gain in decibels
            fade_in: Fade in duration in seconds
            fade_out: Fade out duration in seconds
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(input_path):
                logger.error(f"Input file not found: {input_path}")
                return False
            
            from pydub import AudioSegment
            
            logger.info(f"Adjusting volume (gain={gain_db}dB, fade_in={fade_in}s, fade_out={fade_out}s)")
            
            # Load audio
            audio = AudioSegment.from_file(input_path)
            
            # Apply gain
            if gain_db != 0.0:
                audio = audio + gain_db
            
            # Apply fades
            if fade_in > 0:
                fade_in_ms = int(fade_in * 1000)
                audio = audio.fade_in(fade_in_ms)
            
            if fade_out > 0:
                fade_out_ms = int(fade_out * 1000)
                audio = audio.fade_out(fade_out_ms)
            
            # Create output directory
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            # Export
            audio.export(output_path, format=os.path.splitext(output_path)[1][1:])
            
            logger.info(f"Volume adjusted, saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error adjusting volume: {e}")
            return False
    
    def mix_audio(
        self,
        audio1_path: str,
        audio2_path: str,
        output_path: str,
        audio1_gain: float = 0.0,
        audio2_gain: float = 0.0
    ) -> bool:
        """
        Mix two audio files.
        
        Args:
            audio1_path: Path to first audio file
            audio2_path: Path to second audio file
            output_path: Path to output audio file
            audio1_gain: Gain for first audio in dB
            audio2_gain: Gain for second audio in dB
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from pydub import AudioSegment
            
            logger.info(f"Mixing {audio1_path} and {audio2_path}")
            
            # Load audio files
            audio1 = AudioSegment.from_file(audio1_path)
            audio2 = AudioSegment.from_file(audio2_path)
            
            # Apply gains
            if audio1_gain != 0.0:
                audio1 = audio1 + audio1_gain
            if audio2_gain != 0.0:
                audio2 = audio2 + audio2_gain
            
            # Mix (overlay)
            mixed = audio1.overlay(audio2)
            
            # Create output directory
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            # Export
            mixed.export(output_path, format=os.path.splitext(output_path)[1][1:])
            
            logger.info(f"Mixed audio saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error mixing audio: {e}")
            return False
    
    def compress_dynamics(
        self,
        input_path: str,
        output_path: str,
        threshold: float = -20.0,
        ratio: float = 4.0
    ) -> bool:
        """
        Apply dynamic range compression.
        
        Args:
            input_path: Path to input audio file
            output_path: Path to output audio file
            threshold: Compression threshold in dB
            ratio: Compression ratio
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from pydub import AudioSegment
            from pydub.effects import compress_dynamic_range
            
            logger.info(f"Compressing dynamics (threshold={threshold}dB, ratio={ratio})")
            
            # Load audio
            audio = AudioSegment.from_file(input_path)
            
            # Apply compression
            compressed = compress_dynamic_range(audio, threshold=threshold, ratio=ratio)
            
            # Create output directory
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            # Export
            compressed.export(output_path, format=os.path.splitext(output_path)[1][1:])
            
            logger.info(f"Compressed audio saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error compressing dynamics: {e}")
            return False
