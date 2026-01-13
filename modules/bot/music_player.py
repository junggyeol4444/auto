"""
음악 재생 모듈
채팅 명령어로 YouTube 음악 요청 및 재생
"""

import json
import os
from collections import deque
import subprocess


class MusicPlayer:
    """음악 재생 클래스"""
    
    def __init__(self, config_path="config.json"):
        """
        초기화
        Args:
            config_path: 설정 파일 경로
        """
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.music_config = self.config.get('music', {})
        self.enabled = self.music_config.get('enabled', True)
        self.command = self.music_config.get('command', '!sr')
        self.max_duration = self.music_config.get('max_duration', 600)
        self.volume = self.music_config.get('volume', 0.5)
        
        # 재생 목록
        self.playlist = deque(maxlen=100)
        
        # 현재 재생 중인 곡
        self.current_track = None
        
        # 금지곡 목록
        self.banned_tracks = set()
        
        # 재생 히스토리
        self.play_history = deque(maxlen=50)
        
        # 캐시 디렉토리
        self.cache_dir = self.config.get('paths', {}).get('cache', './cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        
        print("[MusicPlayer] 초기화 완료")
    
    def request_song(self, username, query):
        """
        음악 요청
        Args:
            username: 요청자
            query: 검색 쿼리 또는 YouTube URL
        Returns:
            dict: 요청 결과
        """
        if not self.enabled:
            return {'success': False, 'message': '음악 요청 기능이 비활성화되어 있습니다.'}
        
        # YouTube에서 검색
        track_info = self._search_youtube(query)
        
        if not track_info:
            return {'success': False, 'message': f'"{query}"를 찾을 수 없습니다.'}
        
        # 금지곡 확인
        if track_info['video_id'] in self.banned_tracks:
            return {'success': False, 'message': '이 곡은 금지된 곡입니다.'}
        
        # 길이 확인
        if track_info['duration'] > self.max_duration:
            return {
                'success': False,
                'message': f'곡이 너무 깁니다. (최대 {self.max_duration}초)'
            }
        
        # 중복 확인
        for track in self.playlist:
            if track['video_id'] == track_info['video_id']:
                return {'success': False, 'message': '이미 재생 목록에 있는 곡입니다.'}
        
        # 재생 목록에 추가
        track_info['requester'] = username
        self.playlist.append(track_info)
        
        position = len(self.playlist)
        
        print(f"[MusicPlayer] {username}님이 '{track_info['title']}' 요청 (대기열 {position}번)")
        
        return {
            'success': True,
            'track': track_info,
            'position': position,
            'message': f'🎵 "{track_info["title"]}" 추가됨 (대기열 {position}번)'
        }
    
    def _search_youtube(self, query):
        """
        YouTube에서 음악 검색
        Args:
            query: 검색 쿼리
        Returns:
            dict: 곡 정보
        """
        try:
            # yt-dlp로 정보 추출
            cmd = [
                'yt-dlp',
                '--dump-json',
                '--no-playlist',
                '--default-search', 'ytsearch1:',
                query
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return None
            
            import json as json_lib
            info = json_lib.loads(result.stdout)
            
            return {
                'video_id': info.get('id'),
                'title': info.get('title'),
                'duration': info.get('duration', 0),
                'url': info.get('webpage_url'),
                'thumbnail': info.get('thumbnail')
            }
            
        except Exception as e:
            print(f"[MusicPlayer] YouTube 검색 오류: {e}")
            return None
    
    def play_next(self):
        """
        다음 곡 재생
        Returns:
            dict: 재생 정보
        """
        if not self.playlist:
            self.current_track = None
            return {'success': False, 'message': '재생 목록이 비어있습니다.'}
        
        # 다음 곡 가져오기
        track = self.playlist.popleft()
        self.current_track = track
        
        # 다운로드 및 재생
        success = self._download_and_play(track)
        
        if success:
            # 히스토리에 추가
            self.play_history.append(track)
            
            print(f"[MusicPlayer] 재생 중: {track['title']}")
            
            return {
                'success': True,
                'track': track,
                'message': f'🎵 재생 중: {track["title"]}'
            }
        else:
            return {'success': False, 'message': '재생 실패'}
    
    def _download_and_play(self, track):
        """
        음악 다운로드 및 재생
        Args:
            track: 곡 정보
        Returns:
            bool: 성공 여부
        """
        try:
            # 캐시 파일 경로
            cache_file = os.path.join(self.cache_dir, f"{track['video_id']}.m4a")
            
            # 이미 캐시에 있으면 다운로드 스킵
            if not os.path.exists(cache_file):
                # yt-dlp로 다운로드
                cmd = [
                    'yt-dlp',
                    '-f', 'bestaudio',
                    '-o', cache_file,
                    '--no-playlist',
                    track['url']
                ]
                
                result = subprocess.run(cmd, capture_output=True, timeout=60)
                
                if result.returncode != 0:
                    print(f"[MusicPlayer] 다운로드 실패: {track['title']}")
                    return False
            
            # 재생 로직 (실제로는 OBS 오디오 소스로 전송 필요)
            print(f"[MusicPlayer] 재생: {cache_file}")
            # pygame 또는 FFmpeg로 재생
            
            return True
            
        except Exception as e:
            print(f"[MusicPlayer] 재생 오류: {e}")
            return False
    
    def skip_current(self):
        """현재 곡 스킵"""
        if self.current_track:
            print(f"[MusicPlayer] 스킵: {self.current_track['title']}")
            self.current_track = None
            return self.play_next()
        
        return {'success': False, 'message': '재생 중인 곡이 없습니다.'}
    
    def get_playlist(self):
        """재생 목록 조회"""
        return list(self.playlist)
    
    def get_current_track(self):
        """현재 재생 중인 곡 조회"""
        return self.current_track
    
    def clear_playlist(self):
        """재생 목록 초기화"""
        self.playlist.clear()
        print("[MusicPlayer] 재생 목록 초기화됨")
    
    def ban_track(self, video_id):
        """
        곡 금지
        Args:
            video_id: YouTube 비디오 ID
        """
        self.banned_tracks.add(video_id)
        print(f"[MusicPlayer] 곡 금지: {video_id}")
    
    def unban_track(self, video_id):
        """
        곡 금지 해제
        Args:
            video_id: YouTube 비디오 ID
        """
        if video_id in self.banned_tracks:
            self.banned_tracks.remove(video_id)
            print(f"[MusicPlayer] 곡 금지 해제: {video_id}")
    
    def get_stats(self):
        """통계 조회"""
        return {
            'playlist_size': len(self.playlist),
            'current_track': self.current_track['title'] if self.current_track else None,
            'play_history_size': len(self.play_history),
            'banned_tracks': len(self.banned_tracks)
        }
