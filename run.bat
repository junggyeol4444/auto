@echo off
REM Bot Development Framework Suite - Windows 실행 스크립트
chcp 65001 > nul

echo ======================================
echo Bot Development Framework Suite
echo ======================================
echo.

REM 현재 디렉토리를 스크립트 위치로 변경
cd /d "%~dp0"

REM Python 설치 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되어 있지 않습니다.
    echo Python을 설치한 후 다시 실행해주세요.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python 설치 확인됨
echo.

REM 가상환경 확인 및 생성
if not exist "venv\" (
    echo 📦 가상환경 생성 중...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ 가상환경 생성 실패
        pause
        exit /b 1
    )
    echo ✓ 가상환경 생성 완료
    echo.
)

REM 가상환경 활성화
echo 🔧 가상환경 활성화 중...
call venv\Scripts\activate.bat

REM 의존성 설치 확인
if not exist "venv\.dependencies_installed" (
    echo 📥 의존성 패키지 설치 중...
    echo 이 작업은 몇 분 정도 소요될 수 있습니다...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    if %errorlevel% equ 0 (
        echo. > venv\.dependencies_installed
        echo ✓ 의존성 설치 완료
    ) else (
        echo ❌ 의존성 설치 실패
        echo 수동으로 설치하려면 다음 명령어를 실행하세요:
        echo   venv\Scripts\activate.bat
        echo   pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo.
)

REM 프로그램 실행
echo 🚀 Bot Framework 실행 중...
echo.
python main.py

REM 종료 처리
call venv\Scripts\deactivate.bat
if %errorlevel% neq 0 (
    echo.
    echo 프로그램이 종료되었습니다.
    pause
)
