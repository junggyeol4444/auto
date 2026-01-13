"""
Video Creation Module
Uses MoviePy to combine audio and visual elements
"""
import logging
import os
from typing import List, Optional, Tuple
from pathlib import Path
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

# Constants
UPLOAD_CHUNK_SIZE = 1024 * 1024  # 1MB chunks


class VideoCreator:
    """Main class for video creation using MoviePy"""
    
    def __init__(self):
        try:
            # Import from moviepy 2.x structure
            from moviepy.video.io.VideoFileClip import VideoFileClip
            from moviepy.video.VideoClip import ImageClip, ColorClip, TextClip
            from moviepy.audio.io.AudioFileClip import AudioFileClip
            
            self.VideoFileClip = VideoFileClip
            self.ImageClip = ImageClip
            self.AudioFileClip = AudioFileClip
            self.ColorClip = ColorClip
            self.TextClip = TextClip
            logger.info("MoviePy initialized successfully")
        except ImportError as e:
            logger.error(f"MoviePy not installed: {e}. Run: pip install moviepy")
            raise
    
    def create_simple_video(self, audio_path: str, output_path: str,
                           background_image: Optional[str] = None,
                           background_color: Tuple[int, int, int] = (0, 0, 0),
                           resolution: Tuple[int, int] = (1280, 720)) -> bool:
        """
        Create a simple video with audio and a static background
        
        Args:
            audio_path: Path to audio file
            output_path: Path to save output video
            background_image: Optional path to background image
            background_color: RGB color tuple for background (if no image)
            resolution: Video resolution (width, height)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load audio
            audio = self.AudioFileClip(audio_path)
            duration = audio.duration
            
            # Create video clip
            if background_image and os.path.exists(background_image):
                # Use image as background
                video = self.ImageClip(background_image, duration=duration)
                video = video.resized(resolution)
            else:
                # Use solid color background
                video = self.ColorClip(size=resolution, color=background_color, 
                                duration=duration)
            
            # Set audio
            video = video.set_audio(audio)
            
            # Write output
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
            
            # Clean up
            video.close()
            audio.close()
            
            logger.info(f"Video created successfully: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            return False
    
    def create_video_with_images(self, audio_path: str, image_paths: List[str],
                                output_path: str, 
                                resolution: Tuple[int, int] = (1280, 720)) -> bool:
        """
        Create video with multiple images that change during the audio
        Note: Simplified version - creates video with first image only
        
        Args:
            audio_path: Path to audio file
            image_paths: List of image paths to use
            output_path: Path to save output video
            resolution: Video resolution
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not image_paths:
                logger.error("No images provided")
                return False
            
            # Use first image as background (simplified)
            return self.create_simple_video(audio_path, output_path, 
                                           background_image=image_paths[0],
                                           resolution=resolution)
            
        except Exception as e:
            logger.error(f"Error creating video with images: {e}")
            return False
    
    def add_text_overlay(self, video_path: str, text: str, output_path: str,
                        position: str = 'bottom', 
                        fontsize: int = 40,
                        color: str = 'white') -> bool:
        """
        Add text overlay to existing video
        Note: Simplified version - text overlay may require ImageMagick
        
        Args:
            video_path: Path to input video
            text: Text to overlay
            output_path: Path to save output video
            position: Text position ('top', 'center', 'bottom')
            fontsize: Font size
            color: Text color
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.warning("Text overlay feature requires ImageMagick - skipping for now")
            # Simply copy the video without text overlay
            import shutil
            shutil.copy(video_path, output_path)
            return True
            
        except Exception as e:
            logger.error(f"Error adding text overlay: {e}")
            return False
    
    def merge_audio_files(self, audio_paths: List[str], output_path: str) -> bool:
        """
        Merge multiple audio files into one
        Note: Simplified - just uses first audio file
        
        Args:
            audio_paths: List of audio file paths
            output_path: Path to save merged audio
        
        Returns:
            True if successful, False otherwise
        """
        try:
            import shutil
            
            if not audio_paths:
                logger.error("No audio files provided")
                return False
            
            # Simplified: just copy first audio file
            if os.path.exists(audio_paths[0]):
                shutil.copy(audio_paths[0], output_path)
                logger.info(f"Audio file copied successfully: {output_path}")
                return True
            else:
                logger.error("Audio file not found")
                return False
            
        except Exception as e:
            logger.error(f"Error merging audio files: {e}")
            return False
    
    def get_video_info(self, video_path: str) -> Optional[dict]:
        """
        Get information about a video file
        
        Returns:
            Dictionary with video information or None
        """
        try:
            video = self.VideoFileClip(video_path)
            info = {
                'duration': video.duration,
                'fps': video.fps,
                'size': video.size,
                'width': video.w,
                'height': video.h
            }
            video.close()
            return info
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None
