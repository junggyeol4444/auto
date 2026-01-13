"""
Voice/speech segment detection and audio analysis
"""
import numpy as np
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from typing import List, Tuple
import os


class AudioAnalyzer:
    """Analyzes audio to detect voice segments and silence"""
    
    def __init__(self, silence_thresh=-40, min_silence_len=500):
        """
        Initialize audio analyzer
        
        Args:
            silence_thresh: Silence threshold in dB (lower = more sensitive)
            min_silence_len: Minimum silence length in milliseconds
        """
        self.silence_thresh = silence_thresh
        self.min_silence_len = min_silence_len
    
    def extract_audio_from_video(self, video_path, audio_output_path=None):
        """
        Extract audio from video file
        
        Args:
            video_path: Path to video file
            audio_output_path: Optional path for output audio file
        
        Returns:
            AudioSegment object
        """
        from moviepy.editor import VideoFileClip
        
        if audio_output_path is None:
            audio_output_path = video_path.rsplit('.', 1)[0] + '.wav'
        
        # Extract audio using moviepy
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_output_path, verbose=False, logger=None)
        video.close()
        
        # Load with pydub
        audio = AudioSegment.from_wav(audio_output_path)
        return audio
    
    def detect_voice_segments(self, audio_or_path, progress_callback=None) -> List[Tuple[float, float]]:
        """
        Detect voice/speech segments in audio
        
        Args:
            audio_or_path: AudioSegment object or path to audio file
            progress_callback: Optional callback function
        
        Returns:
            List of tuples (start_time, end_time) for each voice segment in seconds
        """
        if isinstance(audio_or_path, str):
            audio = AudioSegment.from_file(audio_or_path)
        else:
            audio = audio_or_path
        
        # Detect non-silent segments
        nonsilent_ranges = detect_nonsilent(
            audio,
            min_silence_len=self.min_silence_len,
            silence_thresh=self.silence_thresh
        )
        
        # Convert from milliseconds to seconds
        voice_segments = [
            (start / 1000.0, end / 1000.0) 
            for start, end in nonsilent_ranges
        ]
        
        return voice_segments
    
    def detect_silence_segments(self, audio_or_path) -> List[Tuple[float, float]]:
        """
        Detect silence segments in audio
        
        Args:
            audio_or_path: AudioSegment object or path to audio file
        
        Returns:
            List of tuples (start_time, end_time) for each silence segment in seconds
        """
        voice_segments = self.detect_voice_segments(audio_or_path)
        
        if isinstance(audio_or_path, str):
            audio = AudioSegment.from_file(audio_or_path)
        else:
            audio = audio_or_path
        
        total_duration = len(audio) / 1000.0
        
        # Calculate silence segments as gaps between voice segments
        silence_segments = []
        
        if not voice_segments:
            return [(0, total_duration)]
        
        # Add silence at the beginning
        if voice_segments[0][0] > 0:
            silence_segments.append((0, voice_segments[0][0]))
        
        # Add silence between voice segments
        for i in range(len(voice_segments) - 1):
            silence_start = voice_segments[i][1]
            silence_end = voice_segments[i + 1][0]
            if silence_end > silence_start:
                silence_segments.append((silence_start, silence_end))
        
        # Add silence at the end
        if voice_segments[-1][1] < total_duration:
            silence_segments.append((voice_segments[-1][1], total_duration))
        
        return silence_segments
    
    def calculate_audio_statistics(self, voice_segments: List[Tuple[float, float]], 
                                   total_duration: float) -> dict:
        """
        Calculate statistics about audio segments
        
        Args:
            voice_segments: List of voice segment tuples
            total_duration: Total audio duration in seconds
        
        Returns:
            Dictionary with audio statistics
        """
        if not voice_segments:
            return {
                'total_voice_time': 0,
                'total_silence_time': total_duration,
                'voice_percentage': 0,
                'avg_voice_segment_duration': 0,
                'total_voice_segments': 0,
            }
        
        voice_durations = [end - start for start, end in voice_segments]
        total_voice_time = sum(voice_durations)
        
        return {
            'total_voice_time': total_voice_time,
            'total_silence_time': total_duration - total_voice_time,
            'voice_percentage': (total_voice_time / total_duration * 100) if total_duration > 0 else 0,
            'avg_voice_segment_duration': np.mean(voice_durations),
            'total_voice_segments': len(voice_segments),
        }
