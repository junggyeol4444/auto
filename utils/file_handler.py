"""File handler utilities for Voice Service Integrated Suite."""
import os
import shutil
from typing import List, Optional
from pathlib import Path
from utils.logger import get_logger

logger = get_logger()


class FileHandler:
    """Handles file operations."""
    
    AUDIO_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac', '.wma']
    VIDEO_EXTENSIONS = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm']
    TEXT_EXTENSIONS = ['.txt', '.srt', '.vtt']
    
    @staticmethod
    def ensure_directory(path: str) -> str:
        """
        Ensure directory exists, create if not.
        
        Args:
            path: Directory path
            
        Returns:
            Absolute path to directory
        """
        os.makedirs(path, exist_ok=True)
        return os.path.abspath(path)
    
    @staticmethod
    def is_audio_file(filepath: str) -> bool:
        """Check if file is an audio file."""
        return Path(filepath).suffix.lower() in FileHandler.AUDIO_EXTENSIONS
    
    @staticmethod
    def is_video_file(filepath: str) -> bool:
        """Check if file is a video file."""
        return Path(filepath).suffix.lower() in FileHandler.VIDEO_EXTENSIONS
    
    @staticmethod
    def is_text_file(filepath: str) -> bool:
        """Check if file is a text file."""
        return Path(filepath).suffix.lower() in FileHandler.TEXT_EXTENSIONS
    
    @staticmethod
    def get_unique_filename(directory: str, basename: str, extension: str) -> str:
        """
        Get unique filename by appending number if file exists.
        
        Args:
            directory: Directory path
            basename: Base filename without extension
            extension: File extension (with or without dot)
            
        Returns:
            Unique filepath
        """
        if not extension.startswith('.'):
            extension = f'.{extension}'
        
        filepath = os.path.join(directory, f"{basename}{extension}")
        counter = 1
        
        while os.path.exists(filepath):
            filepath = os.path.join(directory, f"{basename}_{counter}{extension}")
            counter += 1
        
        return filepath
    
    @staticmethod
    def get_file_size_mb(filepath: str) -> float:
        """Get file size in megabytes."""
        try:
            size_bytes = os.path.getsize(filepath)
            return size_bytes / (1024 * 1024)
        except Exception as e:
            logger.error(f"Error getting file size: {e}")
            return 0.0
    
    @staticmethod
    def clean_directory(directory: str, extensions: Optional[List[str]] = None) -> int:
        """
        Clean files from directory.
        
        Args:
            directory: Directory to clean
            extensions: List of extensions to remove (None = all files)
            
        Returns:
            Number of files removed
        """
        if not os.path.exists(directory):
            return 0
        
        count = 0
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            
            if os.path.isfile(filepath):
                if extensions is None or Path(filepath).suffix.lower() in extensions:
                    try:
                        os.remove(filepath)
                        count += 1
                    except Exception as e:
                        logger.error(f"Error removing file {filepath}: {e}")
        
        logger.info(f"Cleaned {count} files from {directory}")
        return count
    
    @staticmethod
    def copy_file(src: str, dst: str) -> bool:
        """
        Copy file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            shutil.copy2(src, dst)
            logger.debug(f"Copied {src} to {dst}")
            return True
        except Exception as e:
            logger.error(f"Error copying file: {e}")
            return False
    
    @staticmethod
    def read_text_file(filepath: str, encoding: str = 'utf-8') -> Optional[str]:
        """
        Read text from file.
        
        Args:
            filepath: Path to text file
            encoding: Text encoding
            
        Returns:
            File content or None if error
        """
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
            return content
        except Exception as e:
            logger.error(f"Error reading file {filepath}: {e}")
            return None
    
    @staticmethod
    def write_text_file(filepath: str, content: str, encoding: str = 'utf-8') -> bool:
        """
        Write text to file.
        
        Args:
            filepath: Path to text file
            content: Text content
            encoding: Text encoding
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding=encoding) as f:
                f.write(content)
            logger.debug(f"Written to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error writing file {filepath}: {e}")
            return False
