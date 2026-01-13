"""
쇼츠 생성 모듈
하이라이트 클립을 쇼츠 형식(9:16)으로 변환
"""

import json
import os
from datetime import datetime
import subprocess


class ShortsGenerator:
    """쇼츠 생성 클래스"""
    
    def __init__(self, config_path="config.json"):
        """
        초기화
        Args:
            config_path: 설정 파일 경로
        """
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.paths = self.config.get('paths', {})
        
        # 쇼츠 저장 디렉토리
        self.output_dir = self.paths.get('shorts', './output/shorts')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 생성된 쇼츠 목록
        self.shorts = []
        
        # 쇼츠 설정
        self.shorts_width = 1080
        self.shorts_height = 1920
        self.shorts_duration_max = 60  # 최대 60초
        
        print("[ShortsGenerator] 초기화 완료")
    
    def create_shorts(self, clip_path, title=None, add_captions=False):
        """
        클립을 쇼츠로 변환
        Args:
            clip_path: 클립 파일 경로
            title: 쇼츠 제목
            add_captions: 자막 추가 여부
        Returns:
            dict: 생성된 쇼츠 정보
        """
        if not os.path.exists(clip_path):
            print(f"[ShortsGenerator] 클립 파일을 찾을 수 없습니다: {clip_path}")
            return None
        
        # 쇼츠 파일명 생성
        shorts_filename = self._generate_shorts_filename(title)
        shorts_path = os.path.join(self.output_dir, shorts_filename)
        
        # 쇼츠 변환 (9:16 비율)
        success = self._convert_to_shorts(clip_path, shorts_path, add_captions)
        
        if success:
            shorts_info = {
                'filename': shorts_filename,
                'path': shorts_path,
                'title': title or 'Untitled Shorts',
                'source_clip': clip_path,
                'created_at': datetime.now().isoformat()
            }
            
            self.shorts.append(shorts_info)
            print(f"[ShortsGenerator] 쇼츠 생성 완료: {shorts_filename}")
            
            return shorts_info
        
        return None
    
    def _generate_shorts_filename(self, title=None):
        """
        쇼츠 파일명 생성
        Args:
            title: 제목
        Returns:
            str: 파일명
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if title:
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')[:50]
            return f"shorts_{timestamp}_{safe_title}.mp4"
        
        return f"shorts_{timestamp}.mp4"
    
    def _convert_to_shorts(self, input_path, output_path, add_captions=False):
        """
        영상을 쇼츠 형식으로 변환
        Args:
            input_path: 입력 파일 경로
            output_path: 출력 파일 경로
            add_captions: 자막 추가 여부
        Returns:
            bool: 성공 여부
        """
        try:
            # FFmpeg 명령어 구성 (9:16 비율로 크롭 및 스케일)
            # 중앙 크롭 후 스케일
            filter_complex = (
                f"[0:v]scale={self.shorts_width}:{self.shorts_height}:force_original_aspect_ratio=increase,"
                f"crop={self.shorts_width}:{self.shorts_height}[v]"
            )
            
            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-filter_complex', filter_complex,
                '-map', '[v]',
                '-map', '0:a?',
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', 'fast',
                '-crf', '23',
                '-t', str(self.shorts_duration_max),  # 최대 60초
                '-y',
                output_path
            ]
            
            # FFmpeg 실행
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = process.communicate(timeout=120)
            
            if process.returncode == 0:
                # 자막 추가 (옵션)
                if add_captions:
                    self._add_auto_captions(output_path)
                
                return True
            else:
                print(f"[ShortsGenerator] FFmpeg 오류: {stderr.decode()}")
                return False
                
        except subprocess.TimeoutExpired:
            print("[ShortsGenerator] 쇼츠 생성 타임아웃")
            process.kill()
            return False
        except FileNotFoundError:
            print("[ShortsGenerator] FFmpeg를 찾을 수 없습니다.")
            return False
        except Exception as e:
            print(f"[ShortsGenerator] 쇼츠 생성 오류: {e}")
            return False
    
    def _add_auto_captions(self, video_path):
        """
        자동 자막 추가 (Whisper 사용)
        Args:
            video_path: 영상 파일 경로
        """
        # Whisper를 사용한 자동 자막 생성
        # 실제 구현은 Whisper API 연동 및 자막 삽입 필요
        print("[ShortsGenerator] 자동 자막 추가 기능은 추후 구현 예정")
        pass
    
    def create_thumbnail(self, shorts_path, timestamp=0):
        """
        쇼츠 썸네일 생성
        Args:
            shorts_path: 쇼츠 파일 경로
            timestamp: 썸네일 추출 시간 (초)
        Returns:
            str: 썸네일 파일 경로
        """
        try:
            thumbnail_filename = os.path.splitext(os.path.basename(shorts_path))[0] + '.jpg'
            thumbnail_path = os.path.join(self.output_dir, thumbnail_filename)
            
            cmd = [
                'ffmpeg',
                '-ss', str(timestamp),
                '-i', shorts_path,
                '-vframes', '1',
                '-vf', f'scale={self.shorts_width}:{self.shorts_height}',
                '-y',
                thumbnail_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if result.returncode == 0:
                print(f"[ShortsGenerator] 썸네일 생성 완료: {thumbnail_filename}")
                return thumbnail_path
            
        except Exception as e:
            print(f"[ShortsGenerator] 썸네일 생성 오류: {e}")
        
        return None
    
    def batch_create_shorts(self, clip_list, add_captions=False):
        """
        여러 클립을 한번에 쇼츠로 변환
        Args:
            clip_list: 클립 정보 리스트
            add_captions: 자막 추가 여부
        Returns:
            list: 생성된 쇼츠 정보 리스트
        """
        created_shorts = []
        
        for clip_info in clip_list:
            clip_path = clip_info.get('path')
            title = clip_info.get('title')
            
            shorts_info = self.create_shorts(clip_path, title, add_captions)
            
            if shorts_info:
                created_shorts.append(shorts_info)
        
        print(f"[ShortsGenerator] {len(created_shorts)}개 쇼츠 생성 완료")
        return created_shorts
    
    def get_shorts(self):
        """생성된 쇼츠 목록 조회"""
        return self.shorts
    
    def delete_shorts(self, shorts_info):
        """
        쇼츠 삭제
        Args:
            shorts_info: 쇼츠 정보
        Returns:
            bool: 성공 여부
        """
        try:
            if os.path.exists(shorts_info['path']):
                os.remove(shorts_info['path'])
                self.shorts.remove(shorts_info)
                print(f"[ShortsGenerator] 쇼츠 삭제됨: {shorts_info['filename']}")
                return True
        except Exception as e:
            print(f"[ShortsGenerator] 쇼츠 삭제 오류: {e}")
        
        return False
    
    def export_shorts_list(self, filepath):
        """
        쇼츠 목록 내보내기
        Args:
            filepath: 저장할 파일 경로
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.shorts, f, ensure_ascii=False, indent=2)
        
        print(f"[ShortsGenerator] 쇼츠 목록 저장됨: {filepath}")
