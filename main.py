"""
Bot Development Framework Suite
메인 프로그램 진입점

사용법:
    python main.py

Windows EXE 빌드:
    pyinstaller --onefile --windowed --name BotFramework main.py
"""
import tkinter as tk
from tkinter import messagebox
import sys
import os
import logging
from datetime import datetime

# 로깅 설정
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log'),
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('main')

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui.main_window import MainWindow
except ImportError as e:
    logger.error(f'GUI 모듈 임포트 실패: {str(e)}')
    sys.exit(1)


def main():
    """메인 함수"""
    try:
        logger.info('Bot Development Framework Suite 시작')
        
        # Tkinter 루트 윈도우 생성
        root = tk.Tk()
        
        # 아이콘 설정 (선택사항)
        # root.iconbitmap('icon.ico')
        
        # 메인 윈도우 생성
        app = MainWindow(root)
        
        # 종료 핸들러
        def on_closing():
            if messagebox.askokcancel("종료", "프로그램을 종료하시겠습니까?"):
                logger.info('프로그램 종료')
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # 메인 루프 실행
        root.mainloop()
    
    except Exception as e:
        logger.error(f'프로그램 실행 오류: {str(e)}', exc_info=True)
        messagebox.showerror('오류', f'프로그램 실행 중 오류가 발생했습니다:\n{str(e)}')
        sys.exit(1)


if __name__ == '__main__':
    main()
