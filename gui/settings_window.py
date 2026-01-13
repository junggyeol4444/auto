# -*- coding: utf-8 -*-
"""
설정 윈도우
API 키 및 계정 정보를 설정합니다.
"""

import customtkinter as ctk
from tkinter import messagebox
import json
import os


class SettingsWindow(ctk.CTkToplevel):
    """설정 윈도우 클래스"""
    
    def __init__(self, parent, config):
        super().__init__(parent)
        
        self.title("설정")
        self.geometry("700x600")
        
        self.config = config
        
        self.create_widgets()
    
    def create_widgets(self):
        """UI 위젯 생성"""
        
        # 탭뷰
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 티스토리 탭
        tab_tistory = tabview.add("티스토리")
        self.create_tistory_settings(tab_tistory)
        
        # 네이버 탭
        tab_naver = tabview.add("네이버")
        self.create_naver_settings(tab_naver)
        
        # 워드프레스 탭
        tab_wordpress = tabview.add("워드프레스")
        self.create_wordpress_settings(tab_wordpress)
        
        # 이미지 API 탭
        tab_image = tabview.add("이미지 API")
        self.create_image_settings(tab_image)
        
        # 쿠팡 탭
        tab_coupang = tabview.add("쿠팡")
        self.create_coupang_settings(tab_coupang)
        
        # 저장 버튼
        save_button = ctk.CTkButton(
            self,
            text="저장",
            command=self.save_settings
        )
        save_button.pack(pady=10)
    
    def create_tistory_settings(self, parent):
        """티스토리 설정"""
        ctk.CTkLabel(parent, text="Client ID:").pack(anchor="w", padx=10, pady=5)
        self.tistory_client_id = ctk.CTkEntry(parent, width=500)
        self.tistory_client_id.pack(padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="Client Secret:").pack(anchor="w", padx=10, pady=5)
        self.tistory_client_secret = ctk.CTkEntry(parent, width=500, show="*")
        self.tistory_client_secret.pack(padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="Access Token:").pack(anchor="w", padx=10, pady=5)
        self.tistory_access_token = ctk.CTkEntry(parent, width=500)
        self.tistory_access_token.pack(padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="Blog Name:").pack(anchor="w", padx=10, pady=5)
        self.tistory_blog_name = ctk.CTkEntry(parent, width=500)
        self.tistory_blog_name.pack(padx=10, pady=5)
    
    def create_naver_settings(self, parent):
        """네이버 설정"""
        ctk.CTkLabel(parent, text="ID:").pack(anchor="w", padx=10, pady=5)
        self.naver_id = ctk.CTkEntry(parent, width=500)
        self.naver_id.pack(padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="Password:").pack(anchor="w", padx=10, pady=5)
        self.naver_password = ctk.CTkEntry(parent, width=500, show="*")
        self.naver_password.pack(padx=10, pady=5)
    
    def create_wordpress_settings(self, parent):
        """워드프레스 설정"""
        ctk.CTkLabel(parent, text="URL:").pack(anchor="w", padx=10, pady=5)
        self.wordpress_url = ctk.CTkEntry(parent, width=500)
        self.wordpress_url.pack(padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="Username:").pack(anchor="w", padx=10, pady=5)
        self.wordpress_username = ctk.CTkEntry(parent, width=500)
        self.wordpress_username.pack(padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="Password:").pack(anchor="w", padx=10, pady=5)
        self.wordpress_password = ctk.CTkEntry(parent, width=500, show="*")
        self.wordpress_password.pack(padx=10, pady=5)
    
    def create_image_settings(self, parent):
        """이미지 API 설정"""
        ctk.CTkLabel(parent, text="Unsplash Access Key:").pack(anchor="w", padx=10, pady=5)
        self.unsplash_key = ctk.CTkEntry(parent, width=500)
        self.unsplash_key.pack(padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="Pexels API Key:").pack(anchor="w", padx=10, pady=5)
        self.pexels_key = ctk.CTkEntry(parent, width=500)
        self.pexels_key.pack(padx=10, pady=5)
    
    def create_coupang_settings(self, parent):
        """쿠팡 설정"""
        ctk.CTkLabel(parent, text="Partner ID:").pack(anchor="w", padx=10, pady=5)
        self.coupang_partner_id = ctk.CTkEntry(parent, width=500)
        self.coupang_partner_id.pack(padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="Access Key:").pack(anchor="w", padx=10, pady=5)
        self.coupang_access_key = ctk.CTkEntry(parent, width=500)
        self.coupang_access_key.pack(padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="Secret Key:").pack(anchor="w", padx=10, pady=5)
        self.coupang_secret_key = ctk.CTkEntry(parent, width=500, show="*")
        self.coupang_secret_key.pack(padx=10, pady=5)
    
    def save_settings(self):
        """설정 저장"""
        # 설정 업데이트
        self.config['tistory'] = {
            'client_id': self.tistory_client_id.get(),
            'client_secret': self.tistory_client_secret.get(),
            'access_token': self.tistory_access_token.get(),
            'blog_name': self.tistory_blog_name.get()
        }
        
        self.config['naver'] = {
            'id': self.naver_id.get(),
            'password': self.naver_password.get()
        }
        
        self.config['wordpress'] = {
            'url': self.wordpress_url.get(),
            'username': self.wordpress_username.get(),
            'password': self.wordpress_password.get()
        }
        
        self.config['unsplash'] = {
            'access_key': self.unsplash_key.get()
        }
        
        self.config['pexels'] = {
            'api_key': self.pexels_key.get()
        }
        
        self.config['coupang'] = {
            'partner_id': self.coupang_partner_id.get(),
            'access_key': self.coupang_access_key.get(),
            'secret_key': self.coupang_secret_key.get()
        }
        
        # 파일로 저장
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("저장", "설정이 저장되었습니다.")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("오류", f"설정 저장 실패:\n{e}")
