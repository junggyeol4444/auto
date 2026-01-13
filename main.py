#!/usr/bin/env python3
"""
AI Writing Assistant Suite
Main application entry point
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from utils.file_handler import FileHandler
from utils.api_manager import APIManager


def main():
    """Main application entry point"""
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    
    try:
        file_handler = FileHandler()
        config = file_handler.load_json(config_path)
    except Exception as e:
        print(f"설정 파일 로드 오류: {str(e)}")
        print("기본 설정으로 시작합니다.")
        config = {
            "api": {
                "openai_key": "",
                "anthropic_key": "",
                "use_ai": False
            },
            "output": {
                "default_path": "./output",
                "default_format": "docx"
            },
            "webnovel": {
                "default_chapter_length": 4000,
                "default_genre": "fantasy"
            },
            "proofreading": {
                "spell_check": True,
                "grammar_check": True,
                "consistency_check": True
            }
        }
    
    # Initialize managers
    api_manager = APIManager(config)
    
    # Create and run main window
    app = MainWindow(config, file_handler, api_manager)
    app.run()


if __name__ == "__main__":
    main()
