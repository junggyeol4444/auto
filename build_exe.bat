@echo off
REM Bot Development Framework Suite - EXE 빌드 스크립트 (Windows)
chcp 65001 > nul

echo ======================================
echo Bot Framework - Windows EXE 빌드
echo ======================================
echo.

REM 현재 디렉토리를 스크립트 위치로 변경
cd /d "%~dp0"

REM Python 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되어 있지 않습니다.
    pause
    exit /b 1
)

echo ✓ Python 설치 확인됨
echo.

REM 가상환경 활성화 (있는 경우)
if exist "venv\Scripts\activate.bat" (
    echo 🔧 가상환경 활성화 중...
    call venv\Scripts\activate.bat
)

REM PyInstaller 설치 확인
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 PyInstaller 설치 중...
    pip install pyinstaller
)

REM 빌드 디렉토리 정리
echo 🧹 이전 빌드 파일 정리 중...
if exist "build\" rmdir /s /q build
if exist "dist\" rmdir /s /q dist

REM EXE 빌드
echo 🔨 EXE 파일 빌드 중...
echo 이 작업은 몇 분 정도 소요될 수 있습니다...
echo.
pyinstaller BotFramework.spec

if %errorlevel% equ 0 (
    echo.
    echo ======================================
    echo ✅ 빌드 완료!
    echo ======================================
    echo.
    echo 생성된 파일: dist\BotFramework.exe
    echo.
    echo 배포 방법:
    echo 1. dist\ 폴더의 모든 파일을 복사
    echo 2. config.json 파일을 함께 배포
    echo 3. BotFramework.exe를 실행
    echo.
    pause
) else (
    echo.
    echo ❌ 빌드 실패
    echo 오류 메시지를 확인하고 다시 시도해주세요.
    pause
    exit /b 1
)
