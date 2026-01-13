"""Video dubbing implementation."""
import os
import subprocess
from typing import Optional, List, Dict
from utils.logger import get_logger

logger = get_logger()


class VideoDubbing:
    """Video dubbing with translation and TTS."""
    
    def __init__(self, stt_engine, tts_engine, translator):
        """
        Initialize video dubbing.
        
        Args:
            stt_engine: Speech-to-text engine
            tts_engine: Text-to-speech engine
            translator: Translation service
        """
        self.stt_engine = stt_engine
        self.tts_engine = tts_engine
        self.translator = translator
        self.name = "Video Dubbing"
        logger.info("Video dubbing initialized")
    
    def dub_video(
        self,
        video_path: str,
        output_path: str,
        source_lang: str,
        target_lang: str,
        original_volume: float = 0.1,
        progress_callback=None
    ) -> bool:
        """
        Dub video with translation.
        
        Args:
            video_path: Path to input video
            output_path: Path to output video
            source_lang: Source language code
            target_lang: Target language code
            original_volume: Volume level for original audio (0.0-1.0)
            progress_callback: Callback for progress updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(video_path):
                logger.error(f"Video file not found: {video_path}")
                return False
            
            logger.info(f"Starting video dubbing: {video_path}")
            
            # Step 1: Extract audio
            if progress_callback:
                progress_callback("Extracting audio...", 20)
            
            audio_path = video_path.replace('.mp4', '_audio.wav')
            if not self._extract_audio(video_path, audio_path):
                return False
            
            # Step 2: Transcribe audio
            if progress_callback:
                progress_callback("Transcribing audio...", 40)
            
            transcript = self.stt_engine.transcribe(audio_path, language=source_lang)
            if not transcript:
                logger.error("Transcription failed")
                return False
            
            # Step 3: Translate text
            if progress_callback:
                progress_callback("Translating...", 60)
            
            translated_text = self.translator.translate(
                transcript.get('text', ''),
                source_lang,
                target_lang
            )
            
            if not translated_text:
                logger.error("Translation failed")
                return False
            
            # Step 4: Generate dubbed audio
            if progress_callback:
                progress_callback("Generating dubbed audio...", 80)
            
            dubbed_audio_path = video_path.replace('.mp4', '_dubbed.wav')
            if not self.tts_engine.synthesize(translated_text, dubbed_audio_path, language=target_lang):
                logger.error("TTS generation failed")
                return False
            
            # Step 5: Mix audio and combine with video
            if progress_callback:
                progress_callback("Combining audio and video...", 90)
            
            if not self._combine_audio_video(video_path, dubbed_audio_path, output_path, original_volume):
                return False
            
            # Cleanup
            for temp_file in [audio_path, dubbed_audio_path]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            if progress_callback:
                progress_callback("Dubbing completed!", 100)
            
            logger.info(f"Video dubbing completed: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error in video dubbing: {e}")
            return False
    
    def _extract_audio(self, video_path: str, audio_path: str) -> bool:
        """Extract audio from video using FFmpeg."""
        try:
            cmd = [
                'ffmpeg', '-i', video_path,
                '-vn', '-acodec', 'pcm_s16le',
                '-ar', '44100', '-ac', '2',
                audio_path, '-y'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info("Audio extracted successfully")
                return True
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error extracting audio: {e}")
            return False
    
    def _combine_audio_video(
        self,
        video_path: str,
        audio_path: str,
        output_path: str,
        original_volume: float
    ) -> bool:
        """Combine audio and video using FFmpeg."""
        try:
            # Mix original and dubbed audio
            cmd = [
                'ffmpeg', '-i', video_path, '-i', audio_path,
                '-filter_complex',
                f'[0:a]volume={original_volume}[a1];[1:a]volume=1.0[a2];[a1][a2]amix=inputs=2:duration=longest',
                '-c:v', 'copy', '-c:a', 'aac',
                output_path, '-y'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                logger.info("Audio and video combined successfully")
                return True
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error combining audio and video: {e}")
            return False
