"""
Video Converter Module
Handles video format conversions for different social media platforms
"""

from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.fx.resize import resize
from moviepy.video.fx.crop import crop
import os
from typing import Tuple, Literal


class VideoConverter:
    """Convert videos to different aspect ratios for social media platforms"""
    
    def __init__(self):
        self.supported_formats = ['mp4', 'mov', 'avi', 'mkv']
        
    def convert_to_vertical(self, input_path: str, output_path: str, 
                           resolution: Tuple[int, int] = (1080, 1920)) -> str:
        """
        Convert 16:9 video to 9:16 (vertical) for Reels/Shorts/TikTok
        
        Args:
            input_path: Path to input video
            output_path: Path to save converted video
            resolution: Target resolution (width, height)
            
        Returns:
            Path to converted video
        """
        try:
            clip = VideoFileClip(input_path)
            
            # Get current dimensions
            current_width, current_height = clip.size
            target_width, target_height = resolution
            
            # Calculate aspect ratios
            current_ratio = current_width / current_height
            target_ratio = target_width / target_height
            
            if current_ratio > target_ratio:
                # Video is wider, crop sides
                new_width = int(current_height * target_ratio)
                x_center = current_width / 2
                x1 = int(x_center - new_width / 2)
                cropped = crop(clip, x1=x1, width=new_width)
            else:
                # Video is taller, crop top/bottom
                new_height = int(current_width / target_ratio)
                y_center = current_height / 2
                y1 = int(y_center - new_height / 2)
                cropped = crop(clip, y1=y1, height=new_height)
            
            # Resize to target resolution
            final = cropped.resize(resolution)
            
            # Export
            final.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                fps=30
            )
            
            clip.close()
            final.close()
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error converting to vertical: {str(e)}")
    
    def convert_to_square(self, input_path: str, output_path: str,
                         resolution: Tuple[int, int] = (1080, 1080)) -> str:
        """
        Convert video to 1:1 (square) for Instagram feed
        
        Args:
            input_path: Path to input video
            output_path: Path to save converted video
            resolution: Target resolution (width, height)
            
        Returns:
            Path to converted video
        """
        try:
            clip = VideoFileClip(input_path)
            
            # Get current dimensions
            current_width, current_height = clip.size
            target_size = resolution[0]
            
            # Crop to square (center crop)
            min_dim = min(current_width, current_height)
            
            if current_width > current_height:
                # Landscape: crop sides
                x_center = current_width / 2
                x1 = int(x_center - min_dim / 2)
                cropped = crop(clip, x1=x1, width=min_dim)
            else:
                # Portrait: crop top/bottom
                y_center = current_height / 2
                y1 = int(y_center - min_dim / 2)
                cropped = crop(clip, y1=y1, height=min_dim)
            
            # Resize to target resolution
            final = cropped.resize((target_size, target_size))
            
            # Export
            final.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                fps=30
            )
            
            clip.close()
            final.close()
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error converting to square: {str(e)}")
    
    def convert_format(self, input_path: str, output_path: str,
                      format: Literal['16:9', '9:16', '1:1']) -> str:
        """
        Convert video to specified format
        
        Args:
            input_path: Path to input video
            output_path: Path to save converted video
            format: Target format ('16:9', '9:16', '1:1')
            
        Returns:
            Path to converted video
        """
        if format == '9:16':
            return self.convert_to_vertical(input_path, output_path)
        elif format == '1:1':
            return self.convert_to_square(input_path, output_path)
        elif format == '16:9':
            # Just copy/transcode to standard format
            clip = VideoFileClip(input_path)
            clip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                fps=30
            )
            clip.close()
            return output_path
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_video_info(self, video_path: str) -> dict:
        """Get video information"""
        try:
            clip = VideoFileClip(video_path)
            info = {
                'duration': clip.duration,
                'fps': clip.fps,
                'size': clip.size,
                'aspect_ratio': clip.size[0] / clip.size[1]
            }
            clip.close()
            return info
        except Exception as e:
            raise Exception(f"Error getting video info: {str(e)}")
