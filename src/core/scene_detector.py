"""
Scene change detection using OpenCV
"""
import cv2
import numpy as np
from typing import List, Tuple


class SceneDetector:
    """Detects scene changes in videos"""
    
    def __init__(self, threshold=30.0):
        """
        Initialize scene detector
        
        Args:
            threshold: Threshold for detecting scene changes (higher = less sensitive)
        """
        self.threshold = threshold
    
    def detect_scenes(self, video_path, progress_callback=None) -> List[Tuple[float, float]]:
        """
        Detect scene changes in a video
        
        Args:
            video_path: Path to video file
            progress_callback: Optional callback function(current_frame, total_frames)
        
        Returns:
            List of tuples (start_time, end_time) for each scene in seconds
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception(f"Could not open video: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        scenes = []
        scene_start_frame = 0
        prev_frame = None
        frame_idx = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert to grayscale for comparison
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                # Calculate frame difference
                diff = cv2.absdiff(prev_frame, gray)
                mean_diff = np.mean(diff)
                
                # Detect scene change
                if mean_diff > self.threshold:
                    scene_start_time = scene_start_frame / fps
                    scene_end_time = frame_idx / fps
                    scenes.append((scene_start_time, scene_end_time))
                    scene_start_frame = frame_idx
            
            prev_frame = gray
            frame_idx += 1
            
            if progress_callback and frame_idx % 30 == 0:
                progress_callback(frame_idx, total_frames)
        
        # Add final scene
        if scene_start_frame < frame_idx:
            scene_start_time = scene_start_frame / fps
            scene_end_time = frame_idx / fps
            scenes.append((scene_start_time, scene_end_time))
        
        cap.release()
        return scenes
    
    def calculate_scene_statistics(self, scenes: List[Tuple[float, float]]) -> dict:
        """
        Calculate statistics about scene durations
        
        Args:
            scenes: List of scene tuples (start_time, end_time)
        
        Returns:
            Dictionary with scene statistics
        """
        if not scenes:
            return {
                'avg_duration': 0,
                'min_duration': 0,
                'max_duration': 0,
                'total_scenes': 0,
            }
        
        durations = [end - start for start, end in scenes]
        
        return {
            'avg_duration': np.mean(durations),
            'min_duration': np.min(durations),
            'max_duration': np.max(durations),
            'total_scenes': len(scenes),
        }
