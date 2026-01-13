"""
기능 시연 스크립트
각 모듈의 기본 기능을 테스트
"""

import sys
import os

# 모듈 임포트를 위한 경로 추가
sys.path.insert(0, os.path.dirname(__file__))


def demo_chat_moderator():
    """채팅 모더레이터 시연"""
    print("\n" + "=" * 60)
    print("📝 채팅 모더레이터 시연")
    print("=" * 60)
    
    from modules.chat.moderator import ChatModerator
    
    moderator = ChatModerator()
    
    # 테스트 메시지들
    test_messages = [
        ("user1", "안녕하세요!"),
        ("user2", "멋진 플레이네요 ㅋㅋㅋ"),
        ("user3", "http://spam.com http://spam2.com http://spam3.com"),
        ("spammer", "똑같은 메시지"),
        ("spammer", "똑같은 메시지"),
        ("spammer", "똑같은 메시지"),
    ]
    
    for username, message in test_messages:
        result = moderator.moderate_message(f"user_{username}", username, message)
        
        if result['allowed']:
            print(f"✓ {username}: {message}")
        else:
            print(f"✗ {username}: {message}")
            print(f"  → 차단 사유: {result['reason']}")
            if result['action']:
                print(f"  → 조치: {result['action']}")
    
    # 통계 출력
    stats = moderator.get_stats()
    print(f"\n📊 통계:")
    print(f"  - 총 경고: {stats['total_warnings']}")
    print(f"  - 차단된 메시지: {stats['blocked_messages']}")


def demo_title_optimizer():
    """제목 최적화 시연"""
    print("\n" + "=" * 60)
    print("📝 제목 최적화 시연")
    print("=" * 60)
    
    from modules.optimization.title_optimizer import TitleOptimizer
    
    optimizer = TitleOptimizer()
    
    # 제목 생성
    game_name = "리그 오브 레전드"
    titles = optimizer.generate_title(game_name, 'highlight')
    
    print(f"\n🎮 게임: {game_name}")
    print("\n생성된 제목 후보:")
    for i, title in enumerate(titles[:5], 1):
        print(f"{i}. {title}")
    
    # 쇼츠용 제목
    shorts_titles = optimizer.generate_shorts_title(game_name, 'kill')
    print("\n📱 쇼츠용 제목:")
    for i, title in enumerate(shorts_titles[:3], 1):
        print(f"{i}. {title}")


def demo_minigame():
    """미니게임 시연"""
    print("\n" + "=" * 60)
    print("🎮 미니게임 봇 시연")
    print("=" * 60)
    
    from modules.bot.minigame import MinigameBot
    
    bot = MinigameBot()
    
    # 가위바위보
    print("\n✊ 가위바위보 게임:")
    result = bot.play_rps("TestUser", "가위")
    print(f"  결과: {result['message']}")
    
    # 주사위
    print("\n🎲 주사위 게임:")
    result = bot.roll_dice("TestUser", 3)
    print(f"  결과: {result['message']}")
    
    # 랜덤 뽑기
    print("\n🎰 랜덤 뽑기:")
    items = ["아이템1", "아이템2", "아이템3", "아이템4"]
    result = bot.random_pick("TestUser", items)
    print(f"  결과: {result['message']}")


def demo_highlight_detector():
    """하이라이트 감지 시연"""
    print("\n" + "=" * 60)
    print("🎬 하이라이트 감지 시연")
    print("=" * 60)
    
    from modules.clip.highlight_detector import HighlightDetector
    
    detector = HighlightDetector()
    
    # 킬 감지 테스트
    print("\n⚔️ 킬 감지 테스트:")
    test_texts = [
        "Double Kill!",
        "You are legendary!",
        "Victory!",
        "일반적인 대화"
    ]
    
    for text in test_texts:
        detected = detector.detect_kill(text)
        status = "✓ 감지됨" if detected else "✗ 감지 안됨"
        print(f"  '{text}' → {status}")
    
    # 채팅 폭발 감지
    print("\n💬 채팅 폭발 감지:")
    for rate in [5, 15, 25]:
        detected = detector.detect_chat_burst(rate)
        status = "✓ 감지됨" if detected else "✗ 감지 안됨"
        print(f"  초당 {rate}개 메시지 → {status}")
    
    # 통계
    stats = detector.get_stats()
    print(f"\n📊 감지된 하이라이트: {stats['total_highlights']}개")


def demo_tag_generator():
    """태그 생성 시연"""
    print("\n" + "=" * 60)
    print("🏷️ 태그 생성 시연")
    print("=" * 60)
    
    from modules.optimization.tag_generator import TagGenerator
    
    generator = TagGenerator()
    
    # 태그 생성
    game_name = "Valorant"
    tags = generator.generate_tags(game_name, 'highlight', keywords=['헤드샷', '클러치'])
    
    print(f"\n🎮 게임: {game_name}")
    print(f"🏷️ 생성된 태그 ({len(tags)}개):")
    print(f"   {', '.join(tags[:20])}")
    
    # 해시태그
    hashtags = generator.generate_hashtags(tags)
    print(f"\n#️⃣ 해시태그:")
    print(f"   {hashtags}")


def demo_points_system():
    """포인트 시스템 시연"""
    print("\n" + "=" * 60)
    print("💰 포인트 시스템 시연")
    print("=" * 60)
    
    from modules.bot.points import PointsSystem
    
    points = PointsSystem(db_path=":memory:")  # 메모리 DB 사용
    
    # 포인트 지급
    print("\n💵 포인트 지급:")
    users = [
        ("user1", "Alice", 10, False, False),
        ("user2", "Bob", 10, True, False),   # 구독자
        ("user3", "Charlie", 10, False, True),  # 팔로워
    ]
    
    for user_id, username, minutes, is_sub, is_follower in users:
        awarded = points.award_watch_time_points(user_id, username, minutes, is_sub, is_follower)
        total = points.get_user_points(user_id)
        print(f"  {username}: +{awarded} 포인트 (총 {total})")
    
    # 리더보드
    print("\n🏆 리더보드:")
    leaderboard = points.get_leaderboard(3)
    for entry in leaderboard:
        print(f"  {entry['rank']}. {entry['username']}: {entry['points']} 포인트")


def demo_chat_translator():
    """채팅 번역 시연"""
    print("\n" + "=" * 60)
    print("🌐 채팅 번역 시연")
    print("=" * 60)
    
    from modules.chat.translator import ChatTranslator
    
    translator = ChatTranslator()
    
    # 번역 테스트
    test_messages = [
        ("JohnDoe", "Hello, how are you?"),
        ("Yuki", "こんにちは、元気ですか？"),
        ("Alice", "안녕하세요!"),
    ]
    
    print("\n🔄 채팅 번역:")
    for username, message in test_messages:
        detected_lang = translator.detect_language(message)
        print(f"\n  {username}: {message}")
        print(f"  감지된 언어: {detected_lang}")
        
        # 한국어로 번역
        if detected_lang != 'ko':
            translated = translator.translate_to_korean(message)
            print(f"  → 한국어: {translated}")


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("Streamer Automation Suite - 기능 시연")
    print("=" * 60)
    
    demos = [
        ("채팅 모더레이터", demo_chat_moderator),
        ("제목 최적화", demo_title_optimizer),
        ("미니게임", demo_minigame),
        ("하이라이트 감지", demo_highlight_detector),
        ("태그 생성", demo_tag_generator),
        ("포인트 시스템", demo_points_system),
        ("채팅 번역", demo_chat_translator),
    ]
    
    print("\n사용 가능한 시연:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"{i}. {name}")
    print("0. 모두 실행")
    
    try:
        choice = input("\n선택 (0-7): ").strip()
        
        if choice == '0':
            # 모두 실행
            for name, demo_func in demos:
                try:
                    demo_func()
                except Exception as e:
                    print(f"\n❌ {name} 시연 중 오류: {e}")
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            # 선택된 시연 실행
            name, demo_func = demos[int(choice) - 1]
            demo_func()
        else:
            print("❌ 잘못된 선택입니다.")
    
    except KeyboardInterrupt:
        print("\n\n프로그램 종료")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("시연 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()
