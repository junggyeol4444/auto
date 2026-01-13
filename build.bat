@echo off
echo Building AI Design Automation Suite...
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

REM Build executable
echo Building executable...
pyinstaller --name "AI_Design_Automation" ^
    --windowed ^
    --onefile ^
    --add-data "config.json;." ^
    --add-data "assets;assets" ^
    --hidden-import "cv2" ^
    --hidden-import "PIL" ^
    --hidden-import "rembg" ^
    --hidden-import "customtkinter" ^
    main.py

echo.
echo Build complete! Check the 'dist' folder.
pause
