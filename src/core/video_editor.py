"""
Video editor - applies learned patterns to edit videos
"""
from moviepy.editor import VideoFileClip, concatenate_videoclips
from .audio_analyzer import AudioAnalyzer
import os
import random


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
        if audio_patterns:
            # audio_patterns is a list of dicts from get_profile_patterns
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
    
    def generate_subtitles(self, voice_segments, output_path):
        """
        Generate SRT subtitle file from voice segments
        
        Args:
            voice_segments: List of (start_time, end_time) tuples in seconds
            output_path: Path for output SRT file
        
        Returns:
            Path to subtitle file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, (start, end) in enumerate(voice_segments, 1):
                # Convert to SRT time format (HH:MM:SS,mmm)
                start_time = self._format_srt_time(start)
                end_time = self._format_srt_time(end)
                
                # Write subtitle entry
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"[Speech segment {i}]\n")
                f.write("\n")
        
        return output_path
    
    def _format_srt_time(self, seconds):
        """Format time in seconds to SRT format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def edit_video_multiple(self, video_path, output_path, patterns, num_versions=3,
                           remove_silence_enabled=True, export_subtitles=True,
                           progress_callback=None):
        """
        Create multiple edited versions with varying parameters
        
        Args:
            video_path: Path to input video
            output_path: Base path for output videos
            patterns: Dictionary with scene and audio patterns
            num_versions: Number of versions to create
            remove_silence_enabled: Whether to remove silence
            export_subtitles: Whether to export subtitle files
            progress_callback: Optional callback for progress
        
        Returns:
            Dictionary with lists of video and subtitle paths
        """
        if not patterns:
            raise Exception("No patterns provided")
        
        # Prepare output paths
        base_name = os.path.splitext(output_path)[0]
        ext = os.path.splitext(output_path)[1] or '.mp4'
        
        results = {
            'videos': [],
            'subtitles': []
        }
        
        # Extract audio once for all versions
        if progress_callback:
            progress_callback(f"Preparing to create {num_versions} version(s)...", 0.0)
        
        # Load video
        video = VideoFileClip(video_path)
        
        # Get voice segments
        audio = self.audio_analyzer.extract_audio_from_video(video_path)
        
        # Create multiple versions with varying parameters
        for version_num in range(1, num_versions + 1):
            version_progress_start = (version_num - 1) / num_versions
            version_progress_end = version_num / num_versions
            
            if progress_callback:
                progress_callback(f"Creating version {version_num}/{num_versions}...", 
                                version_progress_start)
            
            # Vary parameters for different versions
            if version_num == 1:
                # Standard version - use learned patterns as-is
                silence_thresh = patterns['audio_patterns'][0]['silence_threshold'] if patterns.get('audio_patterns') else -40
                min_silence_len = patterns['audio_patterns'][0]['min_silence_duration'] * 1000 if patterns.get('audio_patterns') else 500
                padding = patterns['audio_patterns'][0].get('speech_padding_before', 0.1) if patterns.get('audio_patterns') else 0.1
            elif version_num == 2:
                # More aggressive silence removal
                silence_thresh = (patterns['audio_patterns'][0]['silence_threshold'] + 5) if patterns.get('audio_patterns') else -35
                min_silence_len = (patterns['audio_patterns'][0]['min_silence_duration'] * 1000 * 0.7) if patterns.get('audio_patterns') else 350
                padding = 0.05
            else:
                # More conservative - keep more content
                silence_thresh = (patterns['audio_patterns'][0]['silence_threshold'] - 5) if patterns.get('audio_patterns') else -45
                min_silence_len = (patterns['audio_patterns'][0]['min_silence_duration'] * 1000 * 1.3) if patterns.get('audio_patterns') else 650
                padding = 0.15
            
            # Apply settings to audio analyzer
            self.audio_analyzer.silence_thresh = silence_thresh
            self.audio_analyzer.min_silence_len = int(min_silence_len)
            
            # Detect voice segments
            voice_segments = self.audio_analyzer.detect_voice_segments(audio)
            
            if not voice_segments:
                continue
            
            # Create clips
            clips = []
            for start, end in voice_segments:
                clip_start = max(0, start - padding)
                clip_end = min(video.duration, end + padding)
                clip = video.subclip(clip_start, clip_end)
                clips.append(clip)
            
            # Concatenate clips
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Save video
            version_output = f"{base_name}_v{version_num}{ext}"
            final_clip.write_videofile(
                version_output,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            results['videos'].append(version_output)
            
            # Export subtitles if requested
            if export_subtitles:
                subtitle_output = f"{base_name}_v{version_num}.srt"
                self.generate_subtitles(voice_segments, subtitle_output)
                results['subtitles'].append(subtitle_output)
            
            # Clean up
            final_clip.close()
            for clip in clips:
                clip.close()
            
            if progress_callback:
                progress_callback(f"Version {version_num} complete!", version_progress_end)
        
        # Clean up
        video.close()
        
        if progress_callback:
            progress_callback(f"All {num_versions} version(s) complete!", 1.0)
        
        return results
