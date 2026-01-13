#!/bin/bash
# Bot Development Framework Suite - EXE 빌드 스크립트 (Windows용)

echo "======================================"
echo "Bot Framework - Windows EXE 빌드"
echo "======================================"
echo ""

# 스크립트 디렉토리로 이동
cd "$(dirname "$0")"

# Python 및 PyInstaller 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3가 설치되어 있지 않습니다."
    exit 1
fi

echo "✓ Python 버전: $(python3 --version)"
echo ""

# 가상환경 활성화 (있는 경우)
if [ -d "venv" ]; then
    echo "🔧 가상환경 활성화 중..."
    source venv/bin/activate
fi

# PyInstaller 설치 확인
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "📥 PyInstaller 설치 중..."
    pip install pyinstaller
fi

# 빌드 디렉토리 정리
echo "🧹 이전 빌드 파일 정리 중..."
rm -rf build/ dist/

# EXE 빌드
echo "🔨 EXE 파일 빌드 중..."
echo ""
pyinstaller BotFramework.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✅ 빌드 완료!"
    echo "======================================"
    echo ""
    echo "생성된 파일: dist/BotFramework.exe"
    echo ""
    echo "배포 방법:"
    echo "1. dist/ 폴더의 모든 파일을 복사"
    echo "2. config.json 파일을 함께 배포"
    echo "3. BotFramework.exe를 실행"
    echo ""
else
    echo ""
    echo "❌ 빌드 실패"
    echo "오류 메시지를 확인하고 다시 시도해주세요."
    exit 1
fi
