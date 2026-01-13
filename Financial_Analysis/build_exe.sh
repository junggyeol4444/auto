#!/bin/bash
# Unix/Linux/Mac용 빌드 스크립트

echo "================================================"
echo "금융 데이터 분석 시스템 빌드"
echo "================================================"
echo

# 의존성 확인
echo "[1/3] 의존성 설치 확인..."
pip install -r requirements.txt
echo

# 이전 빌드 정리
echo "[2/3] 이전 빌드 정리..."
rm -rf build dist *.spec
echo

# PyInstaller 빌드
echo "[3/3] 실행 파일 빌드 중..."
pyinstaller \
    --onefile \
    --windowed \
    --name "금융분석시스템" \
    --add-data "config.example.json:." \
    main.py

echo
echo "================================================"
echo "빌드 완료!"
echo "생성된 파일: dist/금융분석시스템"
echo "================================================"
echo
echo "주의: config.json 파일을 실행 파일과 같은 폴더에 배치하세요."
echo
