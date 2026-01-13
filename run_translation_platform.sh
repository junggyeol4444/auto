#!/bin/bash
# Translation Automation Platform - Linux/Mac Launcher
# This script launches the Translation Automation Platform

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║         TRANSLATION AUTOMATION PLATFORM - LAUNCHER                   ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}Error: Python is not installed!${NC}"
        echo "Please install Python 3.8 or higher from https://www.python.org/"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo -e "${GREEN}✓${NC} Python found: $($PYTHON_CMD --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    $PYTHON_CMD -m venv venv
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to create virtual environment${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓${NC} Virtual environment created"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Check if requirements are installed
if [ ! -f "venv/.requirements_installed" ]; then
    echo -e "${YELLOW}Installing dependencies (this may take a few minutes)...${NC}"
    pip install -q -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to install dependencies${NC}"
        echo "Try running manually: pip install -r requirements.txt"
        exit 1
    fi
    
    # Mark requirements as installed
    touch venv/.requirements_installed
    echo -e "${GREEN}✓${NC} Dependencies installed"
else
    echo -e "${GREEN}✓${NC} Dependencies already installed"
fi

# Launch the application
echo ""
echo -e "${GREEN}Launching Translation Automation Platform...${NC}"
echo ""

$PYTHON_CMD main.py

# Check exit status
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}Application exited with error${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Application closed successfully${NC}"
