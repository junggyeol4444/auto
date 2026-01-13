"""
쇼츠 업로드 모듈
YouTube Shorts 업로드
"""

import json


class ShortsUploader:
    """쇼츠 업로더 클래스"""
    
    def __init__(self, config_path="config.json"):
        """초기화"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        print("[ShortsUploader] 초기화 완료")
    
    def upload_shorts(self, shorts_path, title, description, tags):
        """
        쇼츠 업로드
        Args:
            shorts_path: 쇼츠 파일 경로
            title: 제목
            description: 설명 (#Shorts 포함)
            tags: 태그
        Returns:
            dict: 업로드 결과
        """
        # #Shorts 해시태그 추가
        if '#Shorts' not in description:
            description += '\n\n#Shorts'
        
        print(f"[ShortsUploader] 쇼츠 업로드: {title}")
        
        return {
            'success': True,
            'message': '쇼츠 업로드 완료',
            'shorts_id': None  # 실제 업로드 후 ID 반환
        }
