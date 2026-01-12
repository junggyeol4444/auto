"""
Video editor - applies learned patterns to edit videos
"""
from moviepy.editor import VideoFileClip, concatenate_videoclips
from .audio_analyzer import AudioAnalyzer
import os


class VideoEditor:
    """Edits videos based on learned patterns"""
    
    def __init__(self):
        self.audio_analyzer = AudioAnalyzer()
    
    def remove_silence(self, video_path, output_path, audio_patterns, progress_callback=None):
        """
        Remove silence from video based on learned patterns
        
        Args:
            video_path: Path to input video
            output_path: Path for output video
            audio_patterns: Audio pattern dictionary
            progress_callback: Optional callback for progress
        
        Returns:
            Path to edited video
        """
        if progress_callback:
            progress_callback("Loading video...", 0.1)
        
        video = VideoFileClip(video_path)
        
        # Update audio analyzer settings based on patterns
        if audio_patterns:
            pattern = audio_patterns[0]
            self.audio_analyzer.silence_thresh = pattern['silence_threshold']
            self.audio_analyzer.min_silence_len = int(pattern['min_silence_duration'] * 1000)
        
        if progress_callback:
            progress_callback("Detecting voice segments...", 0.3)
        
        # Detect voice segments
        audio = self.audio_analyzer.extract_audio_from_video(video_path)
        voice_segments = self.audio_analyzer.detect_voice_segments(audio)
        
        if not voice_segments:
            video.close()
            raise Exception("No voice segments detected")
        
        if progress_callback:
            progress_callback("Creating edited clips...", 0.5)
        
        # Create clips for each voice segment with padding
        padding = 0.1  # default padding
        if audio_patterns and audio_patterns[0]:
            padding = audio_patterns[0].get('speech_padding_before', 0.1)
        
        clips = []
        for start, end in voice_segments:
            # Add padding
            clip_start = max(0, start - padding)
            clip_end = min(video.duration, end + padding)
            
            clip = video.subclip(clip_start, clip_end)
            clips.append(clip)
        
        if progress_callback:
            progress_callback("Concatenating clips...", 0.7)
        
        # Concatenate all clips
        final_clip = concatenate_videoclips(clips, method="compose")
        
        if progress_callback:
            progress_callback("Writing output file...", 0.9)
        
        # Write output
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        # Clean up
        video.close()
        final_clip.close()
        for clip in clips:
            clip.close()
        
        if progress_callback:
            progress_callback("Complete!", 1.0)
        
        return output_path
    
    def apply_scene_patterns(self, video_path, output_path, scene_patterns, progress_callback=None):
        """
        Apply scene-based editing patterns
        
        Args:
            video_path: Path to input video
            output_path: Path for output video
            scene_patterns: Scene pattern dictionary
            progress_callback: Optional callback for progress
        
        Returns:
            Path to edited video
        """
        # This is a placeholder for future scene-based editing
        # For MVP, we'll focus on silence removal
        if progress_callback:
            progress_callback("Scene pattern editing not yet implemented", 1.0)
        
        return video_path
    
    def edit_video(self, video_path, output_path, patterns, remove_silence_enabled=True, 
                   progress_callback=None):
        """
        Edit video using learned patterns
        
        Args:
            video_path: Path to input video
            output_path: Path for output video
            patterns: Dictionary with scene and audio patterns
            remove_silence_enabled: Whether to remove silence
            progress_callback: Optional callback for progress
        
        Returns:
            Path to edited video
        """
        if not patterns:
            raise Exception("No patterns provided")
        
        current_path = video_path
        
        # Apply silence removal
        if remove_silence_enabled and patterns.get('audio_patterns'):
            if progress_callback:
                progress_callback("Removing silence...", 0.0)
            
            current_path = self.remove_silence(
                current_path, 
                output_path, 
                patterns['audio_patterns'],
                progress_callback
            )
        
        return current_path
