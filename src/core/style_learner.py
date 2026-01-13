"""
Style learner - analyzes videos to learn editing patterns
"""
from moviepy.editor import VideoFileClip
from .scene_detector import SceneDetector
from .audio_analyzer import AudioAnalyzer
from ..database.models import Database, ScenePattern, AudioPattern, EditingProfile


class StyleLearner:
    """Learns editing styles from videos"""
    
    def __init__(self, database: Database):
        self.database = database
        self.scene_detector = SceneDetector()
        self.audio_analyzer = AudioAnalyzer()
    
    def learn_from_video(self, video_path, profile_name, progress_callback=None):
        """
        Learn editing patterns from a video
        
        Args:
            video_path: Path to video file
            profile_name: Name of the profile to save patterns to
            progress_callback: Optional callback function for progress updates
        
        Returns:
            Dictionary with learned patterns
        """
        results = {}
        
        # Get or create profile
        session = self.database.get_session()
        try:
            profile = session.query(EditingProfile).filter_by(name=profile_name).first()
            
            if not profile:
                session.close()
                profile = self.database.create_profile(profile_name)
                session = self.database.get_session()
                profile = session.query(EditingProfile).filter_by(name=profile_name).first()
            
            # Detect scenes
            if progress_callback:
                progress_callback("Detecting scene changes...", 0.1)
            
            scenes = self.scene_detector.detect_scenes(video_path)
            scene_stats = self.scene_detector.calculate_scene_statistics(scenes)
            results['scenes'] = scenes
            results['scene_stats'] = scene_stats
            
            # Save scene patterns
            scene_pattern = ScenePattern(
                profile_id=profile.id,
                avg_scene_duration=scene_stats['avg_duration'],
                min_scene_duration=scene_stats['min_duration'],
                max_scene_duration=scene_stats['max_duration'],
                scene_change_threshold=self.scene_detector.threshold
            )
            session.add(scene_pattern)
            
            # Analyze audio
            if progress_callback:
                progress_callback("Analyzing audio...", 0.5)
            
            audio = self.audio_analyzer.extract_audio_from_video(video_path)
            voice_segments = self.audio_analyzer.detect_voice_segments(audio)
            
            # Get total duration
            video = VideoFileClip(video_path)
            total_duration = video.duration
            video.close()
            
            audio_stats = self.audio_analyzer.calculate_audio_statistics(
                voice_segments, total_duration
            )
            results['voice_segments'] = voice_segments
            results['audio_stats'] = audio_stats
            
            # Save audio patterns
            audio_pattern = AudioPattern(
                profile_id=profile.id,
                silence_threshold=self.audio_analyzer.silence_thresh,
                min_silence_duration=self.audio_analyzer.min_silence_len / 1000.0,
                speech_padding_before=0.1,  # Default 100ms
                speech_padding_after=0.1    # Default 100ms
            )
            session.add(audio_pattern)
            
            session.commit()
            
            if progress_callback:
                progress_callback("Learning complete!", 1.0)
            
            return results
        finally:
            session.close()
    
    def get_profile_patterns(self, profile_name):
        """
        Get learned patterns for a profile
        
        Args:
            profile_name: Name of the profile
        
        Returns:
            Dictionary with scene and audio patterns
        """
        session = self.database.get_session()
        try:
            profile = session.query(EditingProfile).filter_by(name=profile_name).first()
            
            if not profile:
                return None
            
            patterns = {
                'scene_patterns': [],
                'audio_patterns': []
            }
            
            for sp in profile.scene_patterns:
                patterns['scene_patterns'].append({
                    'avg_scene_duration': sp.avg_scene_duration,
                    'min_scene_duration': sp.min_scene_duration,
                    'max_scene_duration': sp.max_scene_duration,
                    'scene_change_threshold': sp.scene_change_threshold
                })
            
            for ap in profile.audio_patterns:
                patterns['audio_patterns'].append({
                    'silence_threshold': ap.silence_threshold,
                    'min_silence_duration': ap.min_silence_duration,
                    'speech_padding_before': ap.speech_padding_before,
                    'speech_padding_after': ap.speech_padding_after
                })
            
            return patterns
        finally:
            session.close()
