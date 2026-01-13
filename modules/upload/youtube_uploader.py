"""
YouTube 업로드 모듈
영상 자동 업로드
"""

import json
import os


class YouTubeUploader:
    """YouTube 업로더 클래스"""
    
    def __init__(self, config_path="config.json"):
        """초기화"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.youtube_config = self.config.get('youtube', {})
        self.upload_config = self.config.get('upload', {})
        
        # 업로드 큐
        self.upload_queue = []
        
        print("[YouTubeUploader] 초기화 완료")
    
    def upload_video(self, video_path, title, description, tags, privacy='public'):
        """
        영상 업로드
        Args:
            video_path: 영상 파일 경로
            title: 제목
            description: 설명
            tags: 태그 목록
            privacy: 공개 설정 (public/private/unlisted)
        Returns:
            dict: 업로드 결과
        """
        if not os.path.exists(video_path):
            return {'success': False, 'message': '영상 파일을 찾을 수 없습니다.'}
        
        # YouTube API 업로드 로직 (실제 구현 필요)
        print(f"[YouTubeUploader] 업로드 요청: {title}")
        print(f"  - 파일: {video_path}")
        print(f"  - 태그: {', '.join(tags[:5])}")
        print(f"  - 공개 설정: {privacy}")
        
        # 큐에 추가
        upload_item = {
            'video_path': video_path,
            'title': title,
            'description': description,
            'tags': tags,
            'privacy': privacy,
            'status': 'pending'
        }
        
        self.upload_queue.append(upload_item)
        
        return {
            'success': True,
            'message': '업로드 큐에 추가됨',
            'video_id': None  # 실제 업로드 후 video_id 반환
        }
    
    def schedule_upload(self, video_path, title, description, tags, schedule_time):
        """예약 업로드"""
        print(f"[YouTubeUploader] 예약 업로드: {title} (예정: {schedule_time})")
        return {'success': True, 'scheduled': True}
    
    def get_upload_queue(self):
        """업로드 큐 조회"""
        return self.upload_queue
