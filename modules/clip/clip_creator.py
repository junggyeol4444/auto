"""
클립 생성 모듈
하이라이트 순간 자동 클립 생성
"""

import json
import os
from datetime import datetime
import subprocess


class ClipCreator:
    """클립 생성 클래스"""
    
    def __init__(self, config_path="config.json"):
        """
        초기화
        Args:
            config_path: 설정 파일 경로
        """
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.clip_config = self.config.get('clip', {})
        self.paths = self.config.get('paths', {})
        
        # 클립 저장 디렉토리
        self.output_dir = self.paths.get('clips', './output/clips')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 생성된 클립 목록
        self.clips = []
        
        print("[ClipCreator] 초기화 완료")
    
    def create_clip(self, video_source, timestamp, duration=None, title=None):
        """
        클립 생성
        Args:
            video_source: 영상 소스 파일 경로 또는 스트림 URL
            timestamp: 클립 시작 시간 (초)
            duration: 클립 길이 (초, None이면 설정값 사용)
            title: 클립 제목
        Returns:
            dict: 생성된 클립 정보
        """
        if not self.clip_config.get('auto_create', True):
            return None
        
        # 클립 길이 계산
        before_seconds = self.clip_config.get('before_seconds', 10)
        after_seconds = self.clip_config.get('after_seconds', 10)
        
        if duration is None:
            duration = before_seconds + after_seconds
        
        start_time = max(0, timestamp - before_seconds)
        
        # 클립 파일명 생성
        clip_filename = self._generate_clip_filename(title)
        clip_path = os.path.join(self.output_dir, clip_filename)
        
        # FFmpeg로 클립 추출
        success = self._extract_clip_ffmpeg(
            video_source,
            start_time,
            duration,
            clip_path
        )
        
        if success:
            clip_info = {
                'filename': clip_filename,
                'path': clip_path,
                'title': title or 'Untitled Clip',
                'timestamp': timestamp,
                'start_time': start_time,
                'duration': duration,
                'created_at': datetime.now().isoformat()
            }
            
            self.clips.append(clip_info)
            print(f"[ClipCreator] 클립 생성 완료: {clip_filename}")
            
            return clip_info
        
        return None
    
    def _generate_clip_filename(self, title=None):
        """
        클립 파일명 생성
        Args:
            title: 클립 제목
        Returns:
            str: 파일명
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if title:
            # 파일명에 사용할 수 없는 문자 제거
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')[:50]  # 최대 50자
            return f"clip_{timestamp}_{safe_title}.mp4"
        
        return f"clip_{timestamp}.mp4"
    
    def _extract_clip_ffmpeg(self, source, start_time, duration, output_path):
        """
        FFmpeg를 사용한 클립 추출
        Args:
            source: 소스 파일/URL
            start_time: 시작 시간 (초)
            duration: 길이 (초)
            output_path: 출력 파일 경로
        Returns:
            bool: 성공 여부
        """
        try:
            # FFmpeg 명령어 구성
            cmd = [
                'ffmpeg',
                '-ss', str(start_time),
                '-i', source,
                '-t', str(duration),
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', 'fast',
                '-crf', '23',
                '-y',  # 덮어쓰기
                output_path
            ]
            
            # FFmpeg 실행 (백그라운드)
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 완료 대기 (타임아웃 60초)
            stdout, stderr = process.communicate(timeout=60)
            
            if process.returncode == 0:
                return True
            else:
                print(f"[ClipCreator] FFmpeg 오류: {stderr.decode()}")
                return False
                
        except subprocess.TimeoutExpired:
            print("[ClipCreator] 클립 생성 타임아웃")
            process.kill()
            return False
        except FileNotFoundError:
            print("[ClipCreator] FFmpeg를 찾을 수 없습니다. FFmpeg를 설치해주세요.")
            return False
        except Exception as e:
            print(f"[ClipCreator] 클립 생성 오류: {e}")
            return False
    
    def create_clip_from_highlight(self, video_source, highlight):
        """
        하이라이트에서 클립 생성
        Args:
            video_source: 영상 소스
            highlight: 하이라이트 정보 (dict)
        Returns:
            dict: 생성된 클립 정보
        """
        timestamp = highlight.get('unix_time', 0)
        title = highlight.get('description', 'Highlight')
        
        return self.create_clip(video_source, timestamp, title=title)
    
    def create_twitch_clip(self, broadcaster_id=None):
        """
        Twitch API로 클립 생성
        Args:
            broadcaster_id: 방송자 ID
        Returns:
            dict: 클립 정보
        """
        # Twitch API 클립 생성 로직
        # 실제 구현은 Twitch API 연동 필요
        print("[ClipCreator] Twitch 클립 생성 요청됨 (API 연동 필요)")
        return None
    
    def get_clips(self):
        """생성된 클립 목록 조회"""
        return self.clips
    
    def get_clip_by_index(self, index):
        """
        인덱스로 클립 조회
        Args:
            index: 클립 인덱스
        Returns:
            dict: 클립 정보
        """
        if 0 <= index < len(self.clips):
            return self.clips[index]
        return None
    
    def delete_clip(self, clip_info):
        """
        클립 삭제
        Args:
            clip_info: 클립 정보
        Returns:
            bool: 성공 여부
        """
        try:
            if os.path.exists(clip_info['path']):
                os.remove(clip_info['path'])
                self.clips.remove(clip_info)
                print(f"[ClipCreator] 클립 삭제됨: {clip_info['filename']}")
                return True
        except Exception as e:
            print(f"[ClipCreator] 클립 삭제 오류: {e}")
        
        return False
    
    def get_total_clips(self):
        """총 클립 수 조회"""
        return len(self.clips)
    
    def get_total_duration(self):
        """총 클립 길이 조회 (초)"""
        return sum(clip.get('duration', 0) for clip in self.clips)
    
    def export_clip_list(self, filepath):
        """
        클립 목록 내보내기
        Args:
            filepath: 저장할 파일 경로
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.clips, f, ensure_ascii=False, indent=2)
        
        print(f"[ClipCreator] 클립 목록 저장됨: {filepath}")
    
    def clear_clips(self):
        """클립 목록 초기화 (파일은 삭제하지 않음)"""
        self.clips.clear()
        print("[ClipCreator] 클립 목록 초기화됨")
