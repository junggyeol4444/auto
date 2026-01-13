"""
설치 및 설정 스크립트
Streamer Automation Suite 초기 설정
"""

import os
import sys
import json
import subprocess


def check_python_version():
    """Python 버전 확인"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 이상이 필요합니다.")
        print(f"   현재 버전: {sys.version}")
        sys.exit(1)
    print(f"✓ Python 버전: {sys.version.split()[0]}")


def check_ffmpeg():
    """FFmpeg 설치 확인"""
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ FFmpeg 설치됨")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ FFmpeg가 설치되지 않았습니다.")
    print("   설치 방법:")
    print("   - Windows: https://ffmpeg.org/download.html")
    print("   - Linux: sudo apt-get install ffmpeg")
    return False


def install_dependencies():
    """Python 패키지 설치"""
    print("\n📦 Python 패키지 설치 중...")
    
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            check=True
        )
        print("✓ 패키지 설치 완료")
        return True
    except subprocess.CalledProcessError:
        print("❌ 패키지 설치 실패")
        return False


def create_directories():
    """필요한 디렉토리 생성"""
    print("\n📁 디렉토리 생성 중...")
    
    directories = [
        'output/clips',
        'output/shorts',
        'output/stats',
        'cache',
        'data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ {directory}")
    
    print("✓ 디렉토리 생성 완료")


def setup_config():
    """설정 파일 확인"""
    print("\n⚙️  설정 파일 확인 중...")
    
    if os.path.exists('config.json'):
        print("✓ config.json 존재함")
        
        # 설정 가이드 출력
        print("\n📝 다음 정보를 config.json에 입력해주세요:")
        print("   1. Twitch API 키 (https://dev.twitch.tv/console/apps)")
        print("   2. YouTube API 키 (https://console.cloud.google.com/)")
        print("   3. Discord 웹훅 URL (선택사항)")
        print("   4. Twitter API 키 (선택사항)")
    else:
        print("❌ config.json이 없습니다")


def main():
    """메인 설정 함수"""
    print("=" * 60)
    print("Streamer Automation Suite - 설치 스크립트")
    print("=" * 60)
    print()
    
    # 1. Python 버전 확인
    check_python_version()
    
    # 2. FFmpeg 확인
    ffmpeg_ok = check_ffmpeg()
    
    # 3. 디렉토리 생성
    create_directories()
    
    # 4. 패키지 설치
    deps_ok = install_dependencies()
    
    # 5. 설정 파일 확인
    setup_config()
    
    # 결과 출력
    print("\n" + "=" * 60)
    if ffmpeg_ok and deps_ok:
        print("✅ 설치가 완료되었습니다!")
        print("\n다음 단계:")
        print("1. config.json에 API 키 입력")
        print("2. python main.py 실행")
    else:
        print("⚠️  일부 설치가 완료되지 않았습니다.")
        if not ffmpeg_ok:
            print("   - FFmpeg를 설치해주세요")
        if not deps_ok:
            print("   - Python 패키지를 수동으로 설치해주세요")
    print("=" * 60)


if __name__ == "__main__":
    main()
