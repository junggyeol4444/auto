@echo off
REM Build Script for Translation Automation Platform - Windows
REM This script builds the standalone executable using PyInstaller

setlocal enabledelayedexpansion

echo ========================================================================
echo.
echo         TRANSLATION AUTOMATION PLATFORM - BUILD SCRIPT
echo.
echo ========================================================================
echo.

REM Get the directory where the batch file is located
cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    exit /b 1
)

echo [OK] Python found
python --version

REM Check/Create virtual environment
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/Update dependencies
echo Installing build dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q pyinstaller

echo [OK] Dependencies installed

REM Clean previous builds
echo Cleaning previous builds...
if exist "build\" rmdir /s /q build
if exist "dist\" rmdir /s /q dist

REM Build the executable
echo.
echo Building executable with PyInstaller...
echo This may take several minutes...
echo.

pyinstaller build.spec --clean

REM Check if build was successful
if exist "dist\" (
    echo.
    echo ========================================================================
    echo.
    echo                    BUILD SUCCESSFUL!
    echo.
    echo ========================================================================
    echo.
    echo Executable created in: dist\
    echo.
    dir dist\
    echo.
    
    REM Create a README in dist
    (
        echo Translation Automation Platform - Standalone Executable
        echo.
        echo This is a standalone version of the Translation Automation Platform.
        echo.
        echo USAGE:
        echo ------
        echo Windows: Run TranslationPlatform.exe
        echo.
        echo CONFIGURATION:
        echo --------------
        echo On first run, go to Settings to configure your API keys:
        echo - DeepL API key (optional, for best Korean-English quality^)
        echo - Papago credentials (optional, for Korean-Japanese^)
        echo - OpenAI API key (optional, for GPT-4 translation^)
        echo.
        echo Google Translate works without any API key configuration.
        echo.
        echo FILES:
        echo ------
        echo The executable will create these files/folders:
        echo - config.json - Your settings and API keys
        echo - data/ - Glossaries and translation cache
        echo - output/ - Translated files
        echo.
        echo SUPPORT:
        echo --------
        echo For issues or questions, visit:
        echo https://github.com/junggyeol4444/auto
        echo.
        echo Version: 1.0.0
        echo Built with PyInstaller
    ) > dist\README.txt
    
    echo [OK] README.txt created in dist\
    echo.
    echo To distribute the application:
    echo   1. Copy the entire 'dist' folder
    echo   2. Run TranslationPlatform.exe
    echo.
) else (
    echo.
    echo ========================================================================
    echo.
    echo                    BUILD FAILED!
    echo.
    echo ========================================================================
    echo.
    echo Check the output above for errors
    exit /b 1
)

pause
