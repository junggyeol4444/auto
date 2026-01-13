"""
Voice Service Integrated Suite
Main application entry point
"""
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from utils.logger import setup_logger
from gui.main_window import MainWindow


def main():
    """Main entry point."""
    # Setup logger
    setup_logger()
    
    # Create and run application
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
