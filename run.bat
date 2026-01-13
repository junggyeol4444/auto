@echo off
REM Smart Video Editor Pro - Windows Launcher
REM Double-click this file to run the application

echo ========================================
echo Smart Video Editor Pro
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo First time setup - Creating virtual environment...
    echo This may take a few minutes...
    echo.
    python -m venv venv
    
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo.
    echo Setup complete!
    echo.
) else (
    REM Activate existing virtual environment
    call venv\Scripts\activate.bat
)

REM Check if dependencies are installed
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo Installing/updating dependencies...
    pip install -r requirements.txt
    echo.
)

REM Run the application
echo Starting Smart Video Editor Pro...
echo.
python main.py

REM If the application exits with an error, show it
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    echo.
    pause
)
