#!/bin/bash
# Smart Video Editor Pro - Linux/macOS Launcher
# Run this file to start the application

echo "========================================"
echo "Smart Video Editor Pro"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  macOS: brew install python3"
    echo "  Linux: sudo apt-get install python3 python3-pip python3-venv"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Python found: $(python3 --version)"
echo ""

# Check if FFmpeg is installed (optional but recommended)
if ! command -v ffmpeg &> /dev/null; then
    echo "WARNING: FFmpeg is not installed!"
    echo "The application will not work without FFmpeg."
    echo ""
    echo "Please install FFmpeg:"
    echo "  macOS: brew install ffmpeg"
    echo "  Linux: sudo apt-get install ffmpeg"
    echo ""
    read -p "Press Enter to continue anyway..."
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "First time setup - Creating virtual environment..."
    echo "This may take a few minutes..."
    echo ""
    python3 -m venv venv
    
    # Activate and install dependencies
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo ""
    echo "Setup complete!"
    echo ""
else
    # Activate existing virtual environment
    source venv/bin/activate
fi

# Check if dependencies are installed
python -c "import PyQt5" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing/updating dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Run the application
echo "Starting Smart Video Editor Pro..."
echo ""
python main.py

# Keep terminal open if there was an error
if [ $? -ne 0 ]; then
    echo ""
    echo "Application exited with an error."
    echo ""
    read -p "Press Enter to exit..."
fi
