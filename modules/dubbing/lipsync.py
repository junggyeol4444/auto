"""Lip sync timing adjustment."""
from typing import List, Dict
from utils.logger import get_logger

logger = get_logger()


class LipSync:
    """Lip sync timing adjustment for dubbed videos."""
    
    def __init__(self):
        """Initialize lip sync."""
        self.name = "Lip Sync"
        logger.info("Lip sync initialized")
    
    def adjust_timing(
        self,
        segments: List[Dict],
        speed_factor: float = 1.0
    ) -> List[Dict]:
        """
        Adjust segment timings for lip sync.
        
        Args:
            segments: List of subtitle segments with start/end times
            speed_factor: Speed adjustment factor
            
        Returns:
            Adjusted segments
        """
        try:
            adjusted_segments = []
            
            for segment in segments:
                adjusted_segment = segment.copy()
                adjusted_segment['start'] = segment['start'] * speed_factor
                adjusted_segment['end'] = segment['end'] * speed_factor
                adjusted_segments.append(adjusted_segment)
            
            logger.info(f"Adjusted {len(segments)} segments with factor {speed_factor}")
            return adjusted_segments
            
        except Exception as e:
            logger.error(f"Error adjusting timing: {e}")
            return segments
