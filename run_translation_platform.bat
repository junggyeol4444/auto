@echo off
REM Translation Automation Platform - Windows Launcher
REM This batch file launches the Translation Automation Platform on Windows

echo ========================================================================
echo.
echo         TRANSLATION AUTOMATION PLATFORM - LAUNCHER
echo.
echo ========================================================================
echo.

REM Get the directory where the batch file is located
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\.requirements_installed" (
    echo Installing dependencies (this may take a few minutes)...
    pip install -q -r requirements.txt
    
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        echo Try running manually: pip install -r requirements.txt
        pause
        exit /b 1
    )
    
    REM Mark requirements as installed
    type nul > venv\.requirements_installed
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

REM Launch the application
echo.
echo Launching Translation Automation Platform...
echo.

python main.py

REM Check exit status
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application exited with error
    pause
    exit /b 1
)

echo.
echo [OK] Application closed successfully
pause
