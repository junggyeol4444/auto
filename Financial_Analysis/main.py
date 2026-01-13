"""
금융 데이터 분석 & 알림 시스템
메인 진입점
"""
import sys
import os

# 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import FinancialAnalysisApp


def main():
    """메인 함수"""
    print("=" * 50)
    print("금융 데이터 분석 & 알림 시스템")
    print("Financial Data Analysis & Alert System")
    print("=" * 50)
    print()
    
    # GUI 실행
    try:
        app = FinancialAnalysisApp()
        app.mainloop()
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        input("Enter 키를 눌러 종료하세요...")


if __name__ == "__main__":
    main()
