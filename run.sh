#!/bin/bash
# Bot Development Framework Suite - Linux/Mac 실행 스크립트

echo "======================================"
echo "Bot Development Framework Suite"
echo "======================================"
echo ""

# 스크립트 디렉토리로 이동
cd "$(dirname "$0")"

# Python 버전 체크
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3가 설치되어 있지 않습니다."
    echo "Python 3을 설치한 후 다시 실행해주세요."
    exit 1
fi

echo "✓ Python 버전: $(python3 --version)"
echo ""

# 가상환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo "📦 가상환경 생성 중..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ 가상환경 생성 실패"
        exit 1
    fi
    echo "✓ 가상환경 생성 완료"
    echo ""
fi

# 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source venv/bin/activate

# 의존성 설치 확인
if [ ! -f "venv/.dependencies_installed" ]; then
    echo "📥 의존성 패키지 설치 중..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        touch venv/.dependencies_installed
        echo "✓ 의존성 설치 완료"
    else
        echo "❌ 의존성 설치 실패"
        echo "수동으로 설치하려면 다음 명령어를 실행하세요:"
        echo "  source venv/bin/activate"
        echo "  pip install -r requirements.txt"
        exit 1
    fi
    echo ""
fi

# 프로그램 실행
echo "🚀 Bot Framework 실행 중..."
echo ""
python3 main.py

# 종료 처리
deactivate
