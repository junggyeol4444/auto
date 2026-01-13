#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
설치 및 설정 도우미
Auto Blog Master의 초기 설정을 도와줍니다.
"""

import os
import sys
import json
import subprocess


def print_banner():
    """배너 출력"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "Auto Blog Master 설정 도우미" + " " * 14 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")


def check_python_version():
    """Python 버전 확인"""
    print("🔍 Python 버전 확인 중...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8 이상이 필요합니다. (현재: {version.major}.{version.minor})")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def install_dependencies():
    """의존성 설치"""
    print("\n📦 의존성 설치 중...")
    print("이 작업은 몇 분 정도 걸릴 수 있습니다.\n")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("\n✅ 의존성 설치 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 의존성 설치 실패: {e}")
        return False


def download_nltk_data():
    """NLTK 데이터 다운로드"""
    print("\n📚 NLTK 데이터 다운로드 중...")
    
    try:
        import nltk
        
        downloads = ['punkt', 'stopwords', 'averaged_perceptron_tagger']
        for item in downloads:
            try:
                nltk.download(item, quiet=True)
                print(f"  ✓ {item}")
            except:
                print(f"  ✗ {item} (건너뛰기)")
        
        print("✅ NLTK 데이터 다운로드 완료!")
        return True
    except ImportError:
        print("⚠️  NLTK가 설치되지 않았습니다. 의존성 설치를 먼저 진행해주세요.")
        return False


def create_directories():
    """필수 디렉토리 생성"""
    print("\n📁 디렉토리 생성 중...")
    
    directories = [
        'output/drafts',
        'output/images',
        'cache/crawled_data',
        'database'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ {directory}")
    
    print("✅ 디렉토리 생성 완료!")
    return True


def check_config():
    """설정 파일 확인"""
    print("\n⚙️  설정 파일 확인 중...")
    
    if not os.path.exists('config.json'):
        print("❌ config.json 파일이 없습니다.")
        return False
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("✅ config.json 파일 존재")
        
        # API 키 확인
        has_keys = False
        
        if config.get('tistory', {}).get('access_token'):
            print("  ✓ 티스토리 API 키 설정됨")
            has_keys = True
        else:
            print("  ⚠️  티스토리 API 키 미설정")
        
        if config.get('unsplash', {}).get('access_key'):
            print("  ✓ Unsplash API 키 설정됨")
            has_keys = True
        else:
            print("  ⚠️  Unsplash API 키 미설정")
        
        if config.get('pexels', {}).get('api_key'):
            print("  ✓ Pexels API 키 설정됨")
            has_keys = True
        else:
            print("  ⚠️  Pexels API 키 미설정")
        
        if not has_keys:
            print("\n💡 API 키를 설정하면 더 많은 기능을 사용할 수 있습니다.")
            print("   config.json 파일을 편집하여 API 키를 입력해주세요.")
        
        return True
        
    except Exception as e:
        print(f"❌ config.json 파일 읽기 실패: {e}")
        return False


def run_tests():
    """기본 테스트 실행"""
    print("\n🧪 기본 테스트 실행 중...")
    
    try:
        result = subprocess.call([sys.executable, 'test_basic.py'])
        return result == 0
    except Exception as e:
        print(f"❌ 테스트 실행 실패: {e}")
        return False


def print_next_steps():
    """다음 단계 안내"""
    print("\n" + "=" * 60)
    print("🎉 설정 완료!")
    print("=" * 60)
    print("\n다음 단계:")
    print("  1. config.json 파일을 편집하여 API 키를 입력하세요")
    print("  2. python main.py 명령으로 프로그램을 실행하세요")
    print("  3. GUI에서 주제를 입력하고 블로그 글을 생성하세요")
    print("\n문서:")
    print("  - README.md: 상세한 사용 방법")
    print("  - config.json: API 키 및 설정")
    print("\n문제가 발생하면 GitHub Issues에 문의해주세요.")
    print()


def main():
    """메인 함수"""
    print_banner()
    
    # 1. Python 버전 확인
    if not check_python_version():
        return 1
    
    # 2. 사용자 선택
    print("\n설치 옵션:")
    print("  1. 전체 설치 (권장)")
    print("  2. 디렉토리만 생성")
    print("  3. 테스트만 실행")
    print("  4. 종료")
    
    choice = input("\n선택 (1-4): ").strip()
    
    if choice == '1':
        # 전체 설치
        create_directories()
        if install_dependencies():
            download_nltk_data()
        check_config()
        run_tests()
        print_next_steps()
        
    elif choice == '2':
        # 디렉토리만 생성
        create_directories()
        check_config()
        print_next_steps()
        
    elif choice == '3':
        # 테스트만 실행
        run_tests()
        
    elif choice == '4':
        print("\n설정을 취소했습니다.")
        return 0
        
    else:
        print("\n잘못된 선택입니다.")
        return 1
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n설정이 중단되었습니다.")
        sys.exit(1)
