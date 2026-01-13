#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Auto Blog Master - 메인 실행 파일
블로그 자동화 시스템의 메인 진입점입니다.
"""

import sys
import os

# 경로 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# GUI 모듈 임포트
from gui.main_window import MainWindow

import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_blog_master.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """메인 함수"""
    try:
        logger.info("=" * 50)
        logger.info("Auto Blog Master 시작")
        logger.info("=" * 50)
        
        # 메인 윈도우 실행
        app = MainWindow()
        app.mainloop()
        
        logger.info("Auto Blog Master 종료")
        
    except Exception as e:
        logger.error(f"프로그램 실행 중 오류 발생: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
