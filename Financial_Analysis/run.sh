#!/bin/bash
# 금융 데이터 분석 시스템 실행 프로그램
# Unix/Linux/Mac용 간편 실행 스크립트

echo "================================================"
echo "금융 데이터 분석 시스템 시작"
echo "================================================"
echo

# Python 설치 확인
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "[오류] Python이 설치되어 있지 않습니다."
        echo "Python 3.8 이상을 설치해주세요."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "[확인] Python 버전: $($PYTHON_CMD --version)"
echo

# 의존성 확인 (requirements.txt가 있는 경우)
if [ -f requirements.txt ]; then
    echo "[확인] 필요한 패키지가 설치되어 있는지 확인 중..."
    if ! $PYTHON_CMD -c "import customtkinter" &> /dev/null; then
        echo "[설치] 필요한 패키지를 설치합니다..."
        $PYTHON_CMD -m pip install -r requirements.txt
        echo
    fi
fi

# 프로그램 실행
echo "[실행] 금융 데이터 분석 시스템을 시작합니다..."
echo
$PYTHON_CMD main.py

# 프로그램 종료 후
echo
echo "================================================"
echo "프로그램이 종료되었습니다."
echo "================================================"
