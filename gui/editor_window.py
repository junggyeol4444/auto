# -*- coding: utf-8 -*-
"""
편집 윈도우
생성된 콘텐츠를 미리보기하고 편집합니다.
"""

import customtkinter as ctk
from tkinter import messagebox


class EditorWindow(ctk.CTkToplevel):
    """편집 윈도우 클래스"""
    
    def __init__(self, parent, content_data):
        super().__init__(parent)
        
        self.title("콘텐츠 편집")
        self.geometry("800x600")
        
        self.content_data = content_data
        
        self.create_widgets()
    
    def create_widgets(self):
        """UI 위젯 생성"""
        
        # 제목 입력
        title_frame = ctk.CTkFrame(self)
        title_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(title_frame, text="제목:", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.title_entry = ctk.CTkEntry(title_frame, width=700)
        self.title_entry.pack(fill="x", pady=5)
        self.title_entry.insert(0, self.content_data.get('title', ''))
        
        # 본문 편집
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(content_frame, text="본문:", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.content_text = ctk.CTkTextbox(content_frame, height=400)
        self.content_text.pack(fill="both", expand=True, pady=5)
        self.content_text.insert("1.0", self.content_data.get('content', ''))
        
        # 버튼
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        save_button = ctk.CTkButton(
            button_frame,
            text="저장",
            command=self.save_content
        )
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="취소",
            command=self.destroy
        )
        cancel_button.pack(side="left", padx=10)
    
    def save_content(self):
        """콘텐츠 저장"""
        self.content_data['title'] = self.title_entry.get()
        self.content_data['content'] = self.content_text.get("1.0", "end-1c")
        
        messagebox.showinfo("저장", "콘텐츠가 저장되었습니다.")
        self.destroy()
