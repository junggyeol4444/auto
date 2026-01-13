"""
썸네일 생성 모듈
자동 썸네일 생성
"""

import os
from PIL import Image, ImageDraw, ImageFont
import subprocess


class ThumbnailCreator:
    """썸네일 생성 클래스"""
    
    def __init__(self):
        """초기화"""
        self.thumbnail_width = 1280
        self.thumbnail_height = 720
        print("[ThumbnailCreator] 초기화 완료")
    
    def create_from_video(self, video_path, timestamp=0, output_path=None):
        """
        영상에서 썸네일 추출
        Args:
            video_path: 영상 파일 경로
            timestamp: 추출 시간 (초)
            output_path: 출력 경로
        Returns:
            str: 썸네일 경로
        """
        if output_path is None:
            output_path = video_path.replace('.mp4', '_thumbnail.jpg')
        
        try:
            cmd = [
                'ffmpeg',
                '-ss', str(timestamp),
                '-i', video_path,
                '-vframes', '1',
                '-vf', f'scale={self.thumbnail_width}:{self.thumbnail_height}',
                '-y',
                output_path
            ]
            
            subprocess.run(cmd, capture_output=True, timeout=30)
            print(f"[ThumbnailCreator] 썸네일 생성: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"[ThumbnailCreator] 썸네일 생성 실패: {e}")
            return None
    
    def add_text_overlay(self, image_path, text, output_path=None):
        """
        썸네일에 텍스트 추가
        Args:
            image_path: 이미지 경로
            text: 추가할 텍스트
            output_path: 출력 경로
        Returns:
            str: 썸네일 경로
        """
        try:
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            
            # 텍스트 추가 (중앙 하단)
            # 폰트가 없으면 기본 폰트 사용
            text_position = (self.thumbnail_width // 2, self.thumbnail_height - 100)
            draw.text(text_position, text, fill='white', anchor='mm')
            
            if output_path is None:
                output_path = image_path
            
            img.save(output_path)
            return output_path
            
        except Exception as e:
            print(f"[ThumbnailCreator] 텍스트 추가 실패: {e}")
            return None
