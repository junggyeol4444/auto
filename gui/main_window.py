# -*- coding: utf-8 -*-
"""
메인 GUI 윈도우
Auto Blog Master의 메인 인터페이스
"""

import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import threading
import json
import os
import sys

# 모듈 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainWindow(ctk.CTk):
    """메인 윈도우 클래스"""
    
    def __init__(self):
        super().__init__()
        
        # 윈도우 설정
        self.title("Auto Blog Master - 블로그 자동화 시스템")
        self.geometry("900x700")
        
        # 테마 설정
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # 설정 로드
        self.config = self.load_config()
        
        # UI 생성
        self.create_widgets()
        
        logger.info("메인 윈도우 초기화 완료")
    
    def load_config(self):
        """설정 파일 로드"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning("설정 파일이 없습니다")
                return {}
        except Exception as e:
            logger.error(f"설정 파일 로드 실패: {e}")
            return {}
    
    def create_widgets(self):
        """UI 위젯 생성"""
        
        # 메인 프레임
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 제목
        title_label = ctk.CTkLabel(
            main_frame,
            text="🤖 Auto Blog Master",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=10)
        
        # 입력 프레임
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # 주제/키워드 입력
        ctk.CTkLabel(input_frame, text="주제/키워드:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.keyword_entry = ctk.CTkEntry(input_frame, width=400, placeholder_text="예: 인공지능, 머신러닝")
        self.keyword_entry.pack(padx=10, pady=5)
        
        # 블로그 유형 선택
        ctk.CTkLabel(input_frame, text="블로그 유형:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.blog_type = ctk.CTkComboBox(
            input_frame,
            values=[
                "SEO 최적화 블로그",
                "게임 공략 블로그",
                "웹툰/웹소설 리뷰",
                "만화 리뷰 블로그",
                "드라마/영화 리뷰",
                "IT/테크 뉴스 블로그",
                "쿠팡파트너스 블로그"
            ],
            width=400
        )
        self.blog_type.set("SEO 최적화 블로그")
        self.blog_type.pack(padx=10, pady=5)
        
        # 발행 플랫폼 선택
        platform_frame = ctk.CTkFrame(input_frame)
        platform_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(platform_frame, text="발행 플랫폼:", font=("Arial", 12)).pack(anchor="w")
        
        self.platform_tistory = ctk.CTkCheckBox(platform_frame, text="티스토리")
        self.platform_tistory.pack(side="left", padx=10)
        
        self.platform_naver = ctk.CTkCheckBox(platform_frame, text="네이버 블로그")
        self.platform_naver.pack(side="left", padx=10)
        
        self.platform_wordpress = ctk.CTkCheckBox(platform_frame, text="워드프레스")
        self.platform_wordpress.pack(side="left", padx=10)
        
        # 옵션 설정
        option_frame = ctk.CTkFrame(input_frame)
        option_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(option_frame, text="옵션:", font=("Arial", 12)).pack(anchor="w")
        
        self.option_images = ctk.CTkCheckBox(option_frame, text="이미지 자동 삽입")
        self.option_images.select()
        self.option_images.pack(side="left", padx=10)
        
        self.option_seo = ctk.CTkCheckBox(option_frame, text="SEO 최적화")
        self.option_seo.select()
        self.option_seo.pack(side="left", padx=10)
        
        self.option_coupang = ctk.CTkCheckBox(option_frame, text="쿠팡 제품 삽입")
        self.option_coupang.pack(side="left", padx=10)
        
        # 버튼 프레임
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        self.generate_button = ctk.CTkButton(
            button_frame,
            text="🚀 생성 시작",
            font=("Arial", 14, "bold"),
            height=40,
            command=self.start_generation
        )
        self.generate_button.pack(side="left", padx=10, expand=True, fill="x")
        
        settings_button = ctk.CTkButton(
            button_frame,
            text="⚙️ 설정",
            font=("Arial", 14),
            height=40,
            command=self.open_settings
        )
        settings_button.pack(side="left", padx=10, expand=True, fill="x")
        
        # 진행 상황
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(progress_frame, text="진행 상황:", font=("Arial", 12)).pack(anchor="w", padx=10)
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(progress_frame, text="대기 중...", font=("Arial", 10))
        self.status_label.pack(anchor="w", padx=10)
        
        # 로그 출력 창
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(log_frame, text="로그:", font=("Arial", 12)).pack(anchor="w", padx=10)
        
        self.log_text = ctk.CTkTextbox(log_frame, height=200)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=5)
    
    def log(self, message):
        """로그 메시지 추가"""
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        logger.info(message)
    
    def update_progress(self, value, status):
        """진행 상황 업데이트"""
        self.progress_bar.set(value)
        self.status_label.configure(text=status)
        self.log(status)
    
    def start_generation(self):
        """콘텐츠 생성 시작"""
        keyword = self.keyword_entry.get().strip()
        
        if not keyword:
            messagebox.showwarning("경고", "주제/키워드를 입력해주세요.")
            return
        
        # 버튼 비활성화
        self.generate_button.configure(state="disabled")
        
        # 로그 초기화
        self.log_text.delete("1.0", "end")
        
        # 생성 스레드 시작
        thread = threading.Thread(target=self.generate_content, args=(keyword,))
        thread.daemon = True
        thread.start()
    
    def generate_content(self, keyword):
        """콘텐츠 생성 프로세스"""
        try:
            self.update_progress(0.1, "크롤링 시작...")
            
            # 여기에 실제 생성 로직 구현
            # 데모를 위해 간단한 단계만 표시
            
            import time
            time.sleep(1)
            self.update_progress(0.2, "뉴스 크롤링 중...")
            
            time.sleep(1)
            self.update_progress(0.3, "위키피디아 검색 중...")
            
            time.sleep(1)
            self.update_progress(0.5, "콘텐츠 생성 중...")
            
            time.sleep(1)
            self.update_progress(0.7, "SEO 최적화 중...")
            
            time.sleep(1)
            self.update_progress(0.9, "이미지 처리 중...")
            
            time.sleep(1)
            self.update_progress(1.0, "완료!")
            
            self.log(f"\n✅ '{keyword}' 주제의 블로그 글 생성 완료!")
            
            # 버튼 활성화
            self.generate_button.configure(state="normal")
            
            messagebox.showinfo("완료", "블로그 콘텐츠 생성이 완료되었습니다!")
            
        except Exception as e:
            self.log(f"\n❌ 오류 발생: {e}")
            logger.error(f"콘텐츠 생성 실패: {e}")
            self.generate_button.configure(state="normal")
            messagebox.showerror("오류", f"콘텐츠 생성 중 오류가 발생했습니다:\n{e}")
    
    def open_settings(self):
        """설정 창 열기"""
        messagebox.showinfo("설정", "설정 창은 추후 구현 예정입니다.")


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
