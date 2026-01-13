"""
Windows EXE 빌드 스크립트
PyInstaller를 사용하여 실행 파일 생성
"""

import os
import subprocess
import sys
import shutil


def check_pyinstaller():
    """PyInstaller 설치 확인"""
    try:
        import PyInstaller
        print("✓ PyInstaller 설치됨")
        return True
    except ImportError:
        print("❌ PyInstaller가 설치되지 않았습니다.")
        print("   설치: pip install pyinstaller")
        return False


def build_exe():
    """EXE 파일 빌드"""
    print("\n🔨 EXE 파일 빌드 중...")
    
    # PyInstaller 명령어
    cmd = [
        'pyinstaller',
        '--name=StreamerAutomationSuite',
        '--windowed',
        '--onefile',
        '--add-data=config.json;.',
        '--add-data=data;data',
        '--add-data=modules;modules',
        '--add-data=gui;gui',
        '--hidden-import=customtkinter',
        '--hidden-import=PIL',
        '--hidden-import=sqlite3',
        '--collect-all=customtkinter',
        'main.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ 빌드 완료")
        return True
    except subprocess.CalledProcessError:
        print("❌ 빌드 실패")
        return False


def create_portable_package():
    """포터블 패키지 생성"""
    print("\n📦 포터블 패키지 생성 중...")
    
    # 패키지 디렉토리 생성
    package_dir = "StreamerAutomationSuite_Portable"
    os.makedirs(package_dir, exist_ok=True)
    
    # 파일 복사
    files_to_copy = [
        ('dist/StreamerAutomationSuite.exe', 'StreamerAutomationSuite.exe'),
        ('config.json', 'config.json'),
        ('README.md', 'README.md'),
        ('data', 'data')
    ]
    
    for src, dst in files_to_copy:
        dst_path = os.path.join(package_dir, dst)
        
        if os.path.isdir(src):
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path)
            shutil.copytree(src, dst_path)
        elif os.path.exists(src):
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src, dst_path)
    
    # 디렉토리 생성
    for directory in ['output/clips', 'output/shorts', 'output/stats', 'cache']:
        os.makedirs(os.path.join(package_dir, directory), exist_ok=True)
    
    # 사용 설명서 생성
    with open(os.path.join(package_dir, 'USAGE.txt'), 'w', encoding='utf-8') as f:
        f.write("""
Streamer Automation Suite - 사용 방법

1. FFmpeg 설치 (필수)
   https://ffmpeg.org/download.html
   환경 변수 PATH에 추가

2. config.json 수정
   - Twitch API 키 입력
   - YouTube API 키 입력

3. StreamerAutomationSuite.exe 실행

문제가 발생하면 README.md를 참고하세요.
        """)
    
    print(f"✓ 포터블 패키지 생성 완료: {package_dir}/")


def main():
    """메인 빌드 함수"""
    print("=" * 60)
    print("Streamer Automation Suite - 빌드 스크립트")
    print("=" * 60)
    print()
    
    # PyInstaller 확인
    if not check_pyinstaller():
        sys.exit(1)
    
    # EXE 빌드
    if not build_exe():
        sys.exit(1)
    
    # 포터블 패키지 생성
    create_portable_package()
    
    print("\n" + "=" * 60)
    print("✅ 빌드 완료!")
    print("\n생성된 파일:")
    print("  - dist/StreamerAutomationSuite.exe")
    print("  - StreamerAutomationSuite_Portable/ (포터블 패키지)")
    print("=" * 60)


if __name__ == "__main__":
    main()
