@echo off
REM 금융 데이터 분석 시스템 실행 프로그램
REM Windows용 간편 실행 스크립트

echo ================================================
echo 금융 데이터 분석 시스템 시작
echo ================================================
echo.

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo Python 3.8 이상을 설치해주세요: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM 의존성 확인 (requirements.txt가 있는 경우)
if exist requirements.txt (
    echo [확인] 필요한 패키지가 설치되어 있는지 확인 중...
    python -c "import customtkinter" >nul 2>&1
    if errorlevel 1 (
        echo [설치] 필요한 패키지를 설치합니다...
        pip install -r requirements.txt
        echo.
    )
)

REM 프로그램 실행
echo [실행] 금융 데이터 분석 시스템을 시작합니다...
echo.
python main.py

REM 프로그램 종료 후
echo.
echo ================================================
echo 프로그램이 종료되었습니다.
echo ================================================
pause
