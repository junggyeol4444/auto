"""
Streamer Automation Suite - 메인 애플리케이션
모든 모듈을 통합하여 실행
"""

import json
import threading
import time
from datetime import datetime

# 모듈 임포트
from modules.chat.moderator import ChatModerator
from modules.chat.translator import ChatTranslator
from modules.chat.stats import ChatStats
from modules.clip.highlight_detector import HighlightDetector
from modules.clip.clip_creator import ClipCreator
from modules.clip.shorts_generator import ShortsGenerator
from modules.bot.minigame import MinigameBot
from modules.bot.points import PointsSystem
from modules.bot.music_player import MusicPlayer
from modules.optimization.title_optimizer import TitleOptimizer
from modules.optimization.tag_generator import TagGenerator
from modules.optimization.thumbnail_creator import ThumbnailCreator
from modules.upload.youtube_uploader import YouTubeUploader
from modules.upload.shorts_uploader import ShortsUploader
from modules.upload.social_share import SocialShare
from gui.main_window import MainWindow


class StreamerAutomationApp:
    """스트리머 자동화 앱 메인 클래스"""
    
    def __init__(self, config_path="config.json"):
        """
        초기화
        Args:
            config_path: 설정 파일 경로
        """
        print("=" * 60)
        print("Streamer Automation Suite 초기화 중...")
        print("=" * 60)
        
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 모듈 초기화
        print("\n[1/13] 채팅 모더레이터 초기화...")
        self.moderator = ChatModerator(config_path)
        
        print("[2/13] 채팅 번역기 초기화...")
        self.translator = ChatTranslator(config_path)
        
        print("[3/13] 채팅 통계 초기화...")
        self.chat_stats = ChatStats(config_path)
        
        print("[4/13] 하이라이트 감지기 초기화...")
        self.highlight_detector = HighlightDetector(config_path)
        
        print("[5/13] 클립 생성기 초기화...")
        self.clip_creator = ClipCreator(config_path)
        
        print("[6/13] 쇼츠 생성기 초기화...")
        self.shorts_generator = ShortsGenerator(config_path)
        
        print("[7/13] 미니게임 봇 초기화...")
        self.minigame_bot = MinigameBot(config_path)
        
        print("[8/13] 포인트 시스템 초기화...")
        self.points_system = PointsSystem(config_path)
        
        print("[9/13] 음악 플레이어 초기화...")
        self.music_player = MusicPlayer(config_path)
        
        print("[10/13] 제목 최적화 초기화...")
        self.title_optimizer = TitleOptimizer(config_path)
        
        print("[11/13] 태그 생성기 초기화...")
        self.tag_generator = TagGenerator(config_path)
        
        print("[12/13] YouTube 업로더 초기화...")
        self.youtube_uploader = YouTubeUploader(config_path)
        
        print("[13/13] 소셜 미디어 공유 초기화...")
        self.social_share = SocialShare(config_path)
        
        # 실행 상태
        self.running = False
        self.monitoring_thread = None
        
        # GUI 초기화
        print("\n[GUI] 메인 윈도우 초기화...")
        self.gui = MainWindow(self)
        
        print("\n" + "=" * 60)
        print("초기화 완료! 프로그램을 시작할 준비가 되었습니다.")
        print("=" * 60)
    
    def start(self):
        """애플리케이션 시작"""
        print("\n[App] 모니터링 시작...")
        self.running = True
        
        # 알림 전송
        self.social_share.notify_stream_start("라이브 방송", "게임")
        
        # 병렬 실행 스레드 시작
        threads = [
            threading.Thread(target=self._monitor_chat, daemon=True),
            threading.Thread(target=self._monitor_highlights, daemon=True),
            threading.Thread(target=self._update_stats, daemon=True)
        ]
        
        for thread in threads:
            thread.start()
    
    def stop(self):
        """애플리케이션 중지"""
        print("\n[App] 모니터링 중지...")
        self.running = False
        
        # 통계 저장
        self._save_session_data()
    
    def _monitor_chat(self):
        """채팅 모니터링 (시뮬레이션)"""
        print("[Chat] 채팅 모니터링 시작")
        
        # 실제로는 Twitch/YouTube 채팅 API 연동
        # 여기서는 시뮬레이션
        test_messages = [
            ("user1", "안녕하세요!"),
            ("user2", "ㅋㅋㅋㅋ"),
            ("user3", "!가위바위보 가위"),
            ("user4", "!sr Dynamite"),
        ]
        
        while self.running:
            for username, message in test_messages:
                if not self.running:
                    break
                
                # 모더레이션 체크
                result = self.moderator.moderate_message(
                    f"user_{username}",
                    username,
                    message
                )
                
                if not result['allowed']:
                    log_msg = f"{username}: {message} - 차단 ({result['reason']})"
                    self.gui.add_blocked_message_log(log_msg)
                    continue
                
                # 통계 기록
                self.chat_stats.record_message(username, message)
                
                # 번역 (외국어인 경우)
                if self.translator.should_translate(message):
                    translation = self.translator.translate_message(username, message)
                    print(f"[번역] {username}: {translation.get('translations', {}).get('ko', message)}")
                
                # 명령어 처리
                if message.startswith('!'):
                    self._handle_command(username, message)
                
                time.sleep(0.5)
            
            time.sleep(2)
    
    def _monitor_highlights(self):
        """하이라이트 모니터링"""
        print("[Highlight] 하이라이트 모니터링 시작")
        
        while self.running:
            # 채팅 폭발 감지
            chat_rate = self.chat_stats.get_chat_burst_rate(10)
            if self.highlight_detector.detect_chat_burst(chat_rate):
                self.gui.add_highlight_log(f"채팅 폭발 감지! (초당 {chat_rate:.1f}개)")
            
            time.sleep(5)
    
    def _update_stats(self):
        """통계 업데이트"""
        print("[Stats] 통계 업데이트 시작")
        
        viewer_count = 0
        while self.running:
            # 시청자 수 시뮬레이션
            import random
            viewer_count = random.randint(50, 200)
            
            self.chat_stats.record_viewer_count(viewer_count)
            self.gui.update_viewer_count(viewer_count)
            
            time.sleep(10)
    
    def _handle_command(self, username, message):
        """채팅 명령어 처리"""
        parts = message.split()
        command = parts[0].lower()
        
        if command == '!가위바위보' or command == '!rps':
            if len(parts) > 1:
                result = self.minigame_bot.play_rps(username, parts[1])
                if result['success']:
                    print(f"[Bot] {username}: {result['message']}")
        
        elif command == '!주사위' or command == '!dice':
            num_dice = int(parts[1]) if len(parts) > 1 else 1
            result = self.minigame_bot.roll_dice(username, num_dice)
            if result['success']:
                print(f"[Bot] {username}: {result['message']}")
        
        elif command == '!sr' or command == '!songrequest':
            if len(parts) > 1:
                query = ' '.join(parts[1:])
                result = self.music_player.request_song(username, query)
                if result['success']:
                    print(f"[Bot] {username}: {result['message']}")
        
        elif command == '!포인트' or command == '!points':
            user_id = f"user_{username}"
            points = self.points_system.get_user_points(user_id)
            print(f"[Bot] {username}님의 포인트: {points}")
    
    def _save_session_data(self):
        """세션 데이터 저장"""
        print("\n[App] 세션 데이터 저장 중...")
        
        # 통계 저장
        stats_path = f"output/stats/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.chat_stats.export_stats(stats_path)
        
        # 하이라이트 저장
        highlight_path = f"output/stats/highlights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.highlight_detector.export_highlights(highlight_path)
        
        print("[App] 세션 데이터 저장 완료")
    
    def process_vod(self, video_path, game_name):
        """
        VOD 후처리 (스트림 종료 후)
        Args:
            video_path: VOD 파일 경로
            game_name: 게임명
        """
        print("\n[App] VOD 후처리 시작...")
        
        # 1. 하이라이트 클립 생성
        highlights = self.highlight_detector.get_all_highlights()
        print(f"[App] {len(highlights)}개 하이라이트 감지됨")
        
        for highlight in highlights[:5]:  # 상위 5개만
            clip_info = self.clip_creator.create_clip_from_highlight(
                video_path,
                highlight
            )
            
            if clip_info:
                # 쇼츠 생성
                shorts_info = self.shorts_generator.create_shorts(
                    clip_info['path'],
                    clip_info['title']
                )
        
        # 2. 제목 및 태그 생성
        titles = self.title_optimizer.generate_title(game_name, 'highlight')
        tags = self.tag_generator.generate_tags(game_name, 'highlight')
        
        print(f"[App] 생성된 제목 후보: {len(titles)}개")
        print(f"[App] 제목 예시: {titles[0] if titles else 'N/A'}")
        print(f"[App] 태그: {', '.join(tags[:10])}")
        
        # 3. 소셜 미디어 공유
        if self.clip_creator.get_clips():
            clip = self.clip_creator.get_clips()[0]
            self.social_share.share_clip("https://clip-url", clip['title'])
        
        print("[App] VOD 후처리 완료")
    
    def run(self):
        """애플리케이션 실행"""
        # GUI 실행 (메인 루프)
        self.gui.run()


def main():
    """메인 함수"""
    try:
        # 애플리케이션 생성 및 실행
        app = StreamerAutomationApp()
        app.run()
        
    except KeyboardInterrupt:
        print("\n\n프로그램이 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
