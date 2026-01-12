"""
YouTube video downloader using yt-dlp
"""
import os
import yt_dlp


class VideoDownloader:
    """Downloads YouTube videos for style learning"""
    
    def __init__(self, output_dir='data/temp'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def download_video(self, url, output_filename=None, progress_callback=None):
        """
        Download a YouTube video
        
        Args:
            url: YouTube video URL
            output_filename: Optional custom filename
            progress_callback: Optional callback function for progress updates
        
        Returns:
            Path to downloaded video file
        """
        if output_filename is None:
            output_template = os.path.join(self.output_dir, '%(title)s.%(ext)s')
        else:
            output_template = os.path.join(self.output_dir, output_filename)
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_callback] if progress_callback else [],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                return filename
        except Exception as e:
            raise Exception(f"Failed to download video: {str(e)}")
    
    def get_video_info(self, url):
        """
        Get video information without downloading
        
        Args:
            url: YouTube video URL
        
        Returns:
            Dictionary with video information
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', ''),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', ''),
                    'description': info.get('description', ''),
                    'view_count': info.get('view_count', 0),
                }
        except Exception as e:
            raise Exception(f"Failed to get video info: {str(e)}")
