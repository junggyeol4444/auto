@echo off
REM Social Media Automation Suite - Launch Script (Windows)
REM This script launches the Social Media Automation Suite

echo ==========================================
echo Social Media Automation Suite
echo Version 1.0.1
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed.
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
if not exist "venv\installed" (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo. > venv\installed
    echo Dependencies installed successfully.
)

REM Launch the application
echo.
echo Starting Social Media Automation Suite...
echo.
python main.py

REM Deactivate virtual environment on exit
call venv\Scripts\deactivate.bat

pause
