"""
Social Media Automation Suite
Main entry point for the application
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow


def main():
    """Main application entry point"""
    print("=" * 50)
    print("Social Media Automation Suite")
    print("Version 1.0.0")
    print("=" * 50)
    print()
    
    # Create and run GUI
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
