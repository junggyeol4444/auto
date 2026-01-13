@echo off
REM Windows EXE 빌드 스크립트
REM PyInstaller를 사용하여 단일 실행 파일 생성

echo ================================================
echo 금융 데이터 분석 시스템 빌드
echo ================================================
echo.

REM 의존성 확인
echo [1/3] 의존성 설치 확인...
pip install -r requirements.txt
echo.

REM 이전 빌드 정리
echo [2/3] 이전 빌드 정리...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo.

REM PyInstaller 빌드
echo [3/3] EXE 파일 빌드 중...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "금융분석시스템" ^
    --icon=NONE ^
    --add-data "config.example.json;." ^
    main.py

echo.
echo ================================================
echo 빌드 완료!
echo 생성된 파일: dist\금융분석시스템.exe
echo ================================================
echo.
echo 주의: config.json 파일을 EXE와 같은 폴더에 배치하세요.
echo.

pause
