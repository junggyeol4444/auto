#!/bin/bash
# Build Script for Translation Automation Platform
# This script builds the standalone executable using PyInstaller

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                      ║${NC}"
echo -e "${BLUE}║         TRANSLATION AUTOMATION PLATFORM - BUILD SCRIPT               ║${NC}"
echo -e "${BLUE}║                                                                      ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}Error: Python is not installed!${NC}"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo -e "${GREEN}✓${NC} Python found: $($PYTHON_CMD --version)"

# Check/Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Install/Update dependencies
echo -e "${YELLOW}Installing build dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q pyinstaller

echo -e "${GREEN}✓${NC} Dependencies installed"

# Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
rm -rf build dist *.spec.bak

# Build the executable
echo ""
echo -e "${BLUE}Building executable with PyInstaller...${NC}"
echo -e "${YELLOW}This may take several minutes...${NC}"
echo ""

pyinstaller build.spec --clean

# Check if build was successful
if [ -d "dist" ]; then
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                      ║${NC}"
    echo -e "${GREEN}║                    BUILD SUCCESSFUL!                                 ║${NC}"
    echo -e "${GREEN}║                                                                      ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}Executable created in:${NC} dist/"
    echo ""
    ls -lh dist/
    echo ""
    
    # Create a README in dist
    cat > dist/README.txt << 'EOF'
Translation Automation Platform - Standalone Executable

This is a standalone version of the Translation Automation Platform.

USAGE:
------
Windows: Run TranslationPlatform.exe
Linux/Mac: Run ./TranslationPlatform

CONFIGURATION:
--------------
On first run, go to Settings to configure your API keys:
- DeepL API key (optional, for best Korean-English quality)
- Papago credentials (optional, for Korean-Japanese)
- OpenAI API key (optional, for GPT-4 translation)

Google Translate works without any API key configuration.

FILES:
------
The executable will create these files/folders:
- config.json - Your settings and API keys
- data/ - Glossaries and translation cache
- output/ - Translated files

SUPPORT:
--------
For issues or questions, visit:
https://github.com/junggyeol4444/auto

Version: 1.0.0
Built with PyInstaller
EOF
    
    echo -e "${GREEN}✓${NC} README.txt created in dist/"
    echo ""
    echo -e "${YELLOW}To distribute the application:${NC}"
    echo "  1. Copy the entire 'dist' folder"
    echo "  2. Run TranslationPlatform executable"
    echo ""
else
    echo ""
    echo -e "${RED}╔══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                                                                      ║${NC}"
    echo -e "${RED}║                    BUILD FAILED!                                     ║${NC}"
    echo -e "${RED}║                                                                      ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${RED}Check the output above for errors${NC}"
    exit 1
fi
