#!/bin/bash

# Social Media Automation Suite - Launch Script
# This script launches the Social Media Automation Suite

echo "=========================================="
echo "Social Media Automation Suite"
echo "Version 1.0.1"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed
    echo "Dependencies installed successfully."
fi

# Launch the application
echo ""
echo "Starting Social Media Automation Suite..."
echo ""
python main.py

# Deactivate virtual environment on exit
deactivate
