"""
Preview Window GUI
Shows platform-specific previews of content
"""

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os


class PreviewWindow:
    """Preview Window for Content"""
    
    def __init__(self, parent, content_file: str, caption: str, hashtags: str, platforms: list):
        self.parent = parent
        self.content_file = content_file
        self.caption = caption
        self.hashtags = hashtags
        self.platforms = platforms
        
        # Create window
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Content Preview")
        self.window.geometry("900x700")
        
        self.create_ui()
    
    def create_ui(self):
        """Create user interface"""
        # Header
        header = ctk.CTkLabel(
            self.window,
            text="👁️ Content Preview",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.pack(pady=20)
        
        # Tabview for platforms
        self.tabview = ctk.CTkTabview(self.window)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create tabs for each platform
        for platform in self.platforms:
            self.tabview.add(platform.capitalize())
            self.create_platform_preview(platform)
        
        # Close button
        close_btn = ctk.CTkButton(
            self.window,
            text="Close",
            command=self.window.destroy,
            width=150
        )
        close_btn.pack(pady=20)
    
    def create_platform_preview(self, platform: str):
        """Create preview for specific platform"""
        tab = self.tabview.tab(platform.capitalize())
        
        # Content preview frame
        content_frame = ctk.CTkFrame(tab)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # File info
        file_label = ctk.CTkLabel(
            content_frame,
            text=f"File: {os.path.basename(self.content_file)}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        file_label.pack(pady=10)
        
        # Content type
        is_video = self.content_file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))
        content_type = "Video" if is_video else "Image"
        
        type_label = ctk.CTkLabel(
            content_frame,
            text=f"Type: {content_type}",
            font=ctk.CTkFont(size=12)
        )
        type_label.pack()
        
        # Platform-specific info
        format_info = self.get_platform_format(platform, is_video)
        format_label = ctk.CTkLabel(
            content_frame,
            text=f"Format: {format_info}",
            font=ctk.CTkFont(size=12)
        )
        format_label.pack(pady=5)
        
        # Caption preview
        caption_frame = ctk.CTkFrame(content_frame)
        caption_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            caption_frame,
            text="Caption:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        caption_text = ctk.CTkTextbox(caption_frame, height=100)
        caption_text.pack(fill="x", padx=10, pady=5)
        caption_text.insert("1.0", self.caption)
        caption_text.configure(state="disabled")
        
        # Hashtags preview
        hashtag_frame = ctk.CTkFrame(content_frame)
        hashtag_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            hashtag_frame,
            text="Hashtags:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        hashtag_text = ctk.CTkTextbox(hashtag_frame, height=60)
        hashtag_text.pack(fill="x", padx=10, pady=5)
        hashtag_text.insert("1.0", self.hashtags)
        hashtag_text.configure(state="disabled")
    
    def get_platform_format(self, platform: str, is_video: bool) -> str:
        """Get recommended format for platform"""
        if platform == 'instagram':
            return "9:16 (Reels) or 1:1 (Feed)" if is_video else "1:1 or 4:5"
        elif platform == 'tiktok':
            return "9:16 (Vertical)" if is_video else "9:16"
        elif platform == 'youtube':
            return "9:16 (Shorts)" if is_video else "16:9"
        elif platform == 'twitter':
            return "16:9 or 1:1" if is_video else "Any"
        elif platform == 'facebook':
            return "9:16 (Reels) or 16:9" if is_video else "Any"
        elif platform == 'pinterest':
            return "2:3 (Vertical)" if is_video else "2:3 or 1:1"
        elif platform == 'discord':
            return "Any" if is_video else "Any"
        return "Standard"
