"""
Video Creation Module
Uses MoviePy to combine audio and visual elements
"""
import logging
import os
from typing import List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class VideoCreator:
    """Main class for video creation using MoviePy"""
    
    def __init__(self):
        try:
            from moviepy.editor import (
                VideoFileClip, ImageClip, AudioFileClip,
                CompositeVideoClip, concatenate_videoclips,
                TextClip, CompositeAudioClip
            )
            self.VideoFileClip = VideoFileClip
            self.ImageClip = ImageClip
            self.AudioFileClip = AudioFileClip
            self.CompositeVideoClip = CompositeVideoClip
            self.concatenate_videoclips = concatenate_videoclips
            self.TextClip = TextClip
            self.CompositeAudioClip = CompositeAudioClip
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
                video = self.ImageClip(background_image).set_duration(duration)
                video = video.resize(resolution)
            else:
                # Use solid color background
                from moviepy.editor import ColorClip
                video = ColorClip(size=resolution, color=background_color, 
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
            
            # Load audio
            audio = self.AudioFileClip(audio_path)
            duration = audio.duration
            
            # Calculate duration per image
            duration_per_image = duration / len(image_paths)
            
            # Create clips for each image
            clips = []
            for img_path in image_paths:
                if os.path.exists(img_path):
                    clip = self.ImageClip(img_path).set_duration(duration_per_image)
                    clip = clip.resize(resolution)
                    clips.append(clip)
            
            if not clips:
                logger.error("No valid images found")
                return False
            
            # Concatenate clips
            video = self.concatenate_videoclips(clips, method="compose")
            
            # Set audio
            video = video.set_audio(audio)
            
            # Write output
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
            
            # Clean up
            video.close()
            audio.close()
            
            logger.info(f"Video with images created successfully: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating video with images: {e}")
            return False
    
    def add_text_overlay(self, video_path: str, text: str, output_path: str,
                        position: str = 'bottom', 
                        fontsize: int = 40,
                        color: str = 'white') -> bool:
        """
        Add text overlay to existing video
        
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
            # Load video
            video = self.VideoFileClip(video_path)
            
            # Create text clip
            txt_clip = self.TextClip(text, fontsize=fontsize, color=color,
                                    font='Arial', method='caption',
                                    size=(video.w * 0.8, None))
            
            # Set position
            if position == 'top':
                txt_clip = txt_clip.set_position(('center', 50))
            elif position == 'center':
                txt_clip = txt_clip.set_position('center')
            else:  # bottom
                txt_clip = txt_clip.set_position(('center', video.h - 100))
            
            txt_clip = txt_clip.set_duration(video.duration)
            
            # Composite video with text
            final_video = self.CompositeVideoClip([video, txt_clip])
            
            # Write output
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            final_video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
            
            # Clean up
            final_video.close()
            video.close()
            txt_clip.close()
            
            logger.info(f"Text overlay added successfully: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding text overlay: {e}")
            return False
    
    def merge_audio_files(self, audio_paths: List[str], output_path: str) -> bool:
        """
        Merge multiple audio files into one
        
        Args:
            audio_paths: List of audio file paths
            output_path: Path to save merged audio
        
        Returns:
            True if successful, False otherwise
        """
        try:
            from moviepy.editor import concatenate_audioclips
            
            if not audio_paths:
                logger.error("No audio files provided")
                return False
            
            # Load audio clips
            audio_clips = []
            for path in audio_paths:
                if os.path.exists(path):
                    audio_clips.append(self.AudioFileClip(path))
            
            if not audio_clips:
                logger.error("No valid audio files found")
                return False
            
            # Concatenate
            final_audio = concatenate_audioclips(audio_clips)
            
            # Write output
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            final_audio.write_audiofile(output_path)
            
            # Clean up
            final_audio.close()
            for clip in audio_clips:
                clip.close()
            
            logger.info(f"Audio files merged successfully: {output_path}")
            return True
            
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
