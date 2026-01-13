"""
Main Window GUI
Main interface for Social Media Automation Suite
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import json
from datetime import datetime
import threading
from typing import Dict, List

# Import modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.converter.video_converter import VideoConverter
from modules.converter.image_processor import ImageProcessor
from modules.generator.hashtag_generator import HashtagGenerator
from modules.generator.caption_generator import CaptionGenerator
from modules.generator.trend_analyzer import TrendAnalyzer
from modules.publishing_coordinator import PublishingCoordinator
from gui.preview_window import PreviewWindow
from gui.settings_window import SettingsWindow


class MainWindow:
    """Main GUI Window"""
    
    def __init__(self):
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Social Media Automation Suite")
        self.root.geometry("1200x800")
        
        # Initialize modules
        self.video_converter = VideoConverter()
        self.image_processor = ImageProcessor()
        self.hashtag_generator = HashtagGenerator()
        self.caption_generator = CaptionGenerator()
        self.trend_analyzer = TrendAnalyzer()
        self.publishing_coordinator = PublishingCoordinator()
        
        # State variables
        self.selected_file = None
        self.selected_platforms = {}
        self.config = self.load_config()
        
        # Create UI
        self.create_ui()
    
    def load_config(self) -> Dict:
        """Load configuration"""
        config_path = 'config.json'
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def create_ui(self):
        """Create user interface"""
        # Create main layout
        self.create_header()
        self.create_content_area()
        self.create_platform_selection()
        self.create_caption_area()
        self.create_hashtag_area()
        self.create_schedule_area()
        self.create_action_buttons()
        self.create_log_area()
    
    def create_header(self):
        """Create header section"""
        header_frame = ctk.CTkFrame(self.root)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title = ctk.CTkLabel(
            header_frame,
            text="📱 Social Media Automation Suite",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=10)
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Automate Your Content Across 7 Platforms",
            font=ctk.CTkFont(size=14)
        )
        subtitle.pack()
    
    def create_content_area(self):
        """Create content upload area"""
        content_frame = ctk.CTkFrame(self.root)
        content_frame.pack(fill="x", padx=10, pady=10)
        
        label = ctk.CTkLabel(
            content_frame,
            text="📁 Content Upload",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # File selection
        file_frame = ctk.CTkFrame(content_frame)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        self.file_label = ctk.CTkLabel(
            file_frame,
            text="No file selected",
            font=ctk.CTkFont(size=12)
        )
        self.file_label.pack(side="left", padx=10)
        
        select_btn = ctk.CTkButton(
            file_frame,
            text="Select File",
            command=self.select_file
        )
        select_btn.pack(side="right", padx=10, pady=10)
    
    def create_platform_selection(self):
        """Create platform selection area"""
        platform_frame = ctk.CTkFrame(self.root)
        platform_frame.pack(fill="x", padx=10, pady=10)
        
        label = ctk.CTkLabel(
            platform_frame,
            text="🌐 Select Platforms",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Platform checkboxes
        checkbox_frame = ctk.CTkFrame(platform_frame)
        checkbox_frame.pack(fill="x", padx=10, pady=10)
        
        platforms = [
            ("Instagram", "instagram"),
            ("TikTok", "tiktok"),
            ("YouTube", "youtube"),
            ("Twitter", "twitter"),
            ("Facebook", "facebook"),
            ("Pinterest", "pinterest"),
            ("Discord", "discord")
        ]
        
        for i, (name, key) in enumerate(platforms):
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(
                checkbox_frame,
                text=name,
                variable=var
            )
            checkbox.grid(row=i//4, column=i%4, padx=10, pady=5, sticky="w")
            self.selected_platforms[key] = var
    
    def create_caption_area(self):
        """Create caption input area"""
        caption_frame = ctk.CTkFrame(self.root)
        caption_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        label_frame = ctk.CTkFrame(caption_frame)
        label_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        label = ctk.CTkLabel(
            label_frame,
            text="✍️ Caption",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(side="left")
        
        auto_btn = ctk.CTkButton(
            label_frame,
            text="Auto Generate",
            command=self.auto_generate_caption,
            width=120
        )
        auto_btn.pack(side="right", padx=10)
        
        self.caption_text = ctk.CTkTextbox(
            caption_frame,
            height=100,
            font=ctk.CTkFont(size=12)
        )
        self.caption_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_hashtag_area(self):
        """Create hashtag input area"""
        hashtag_frame = ctk.CTkFrame(self.root)
        hashtag_frame.pack(fill="x", padx=10, pady=10)
        
        label_frame = ctk.CTkFrame(hashtag_frame)
        label_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        label = ctk.CTkLabel(
            label_frame,
            text="#️⃣ Hashtags",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(side="left")
        
        auto_btn = ctk.CTkButton(
            label_frame,
            text="Auto Generate",
            command=self.auto_generate_hashtags,
            width=120
        )
        auto_btn.pack(side="right", padx=10)
        
        self.hashtag_text = ctk.CTkTextbox(
            hashtag_frame,
            height=60,
            font=ctk.CTkFont(size=12)
        )
        self.hashtag_text.pack(fill="x", padx=10, pady=10)
    
    def create_schedule_area(self):
        """Create schedule settings area"""
        schedule_frame = ctk.CTkFrame(self.root)
        schedule_frame.pack(fill="x", padx=10, pady=10)
        
        label = ctk.CTkLabel(
            schedule_frame,
            text="⏰ Schedule (Optional)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(anchor="w", padx=10, pady=(10, 5))
        
        settings_frame = ctk.CTkFrame(schedule_frame)
        settings_frame.pack(fill="x", padx=10, pady=10)
        
        self.schedule_enabled = ctk.BooleanVar()
        schedule_check = ctk.CTkCheckBox(
            settings_frame,
            text="Enable Scheduling",
            variable=self.schedule_enabled
        )
        schedule_check.pack(side="left", padx=10)
        
        ctk.CTkLabel(settings_frame, text="Date/Time:").pack(side="left", padx=10)
        
        self.schedule_entry = ctk.CTkEntry(settings_frame, placeholder_text="YYYY-MM-DD HH:MM")
        self.schedule_entry.pack(side="left", padx=10)
    
    def create_action_buttons(self):
        """Create action buttons"""
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        preview_btn = ctk.CTkButton(
            button_frame,
            text="👁️ Preview",
            command=self.preview_content,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        preview_btn.pack(side="left", padx=10)
        
        publish_btn = ctk.CTkButton(
            button_frame,
            text="🚀 Publish",
            command=self.publish_content,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        publish_btn.pack(side="left", padx=10)
        
        settings_btn = ctk.CTkButton(
            button_frame,
            text="⚙️ Settings",
            command=self.open_settings,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        settings_btn.pack(side="right", padx=10)
    
    def create_log_area(self):
        """Create log output area"""
        log_frame = ctk.CTkFrame(self.root)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        label = ctk.CTkLabel(
            log_frame,
            text="📋 Activity Log",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.log_text = ctk.CTkTextbox(
            log_frame,
            height=150,
            font=ctk.CTkFont(size=11, family="Courier")
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def select_file(self):
        """Open file dialog to select content"""
        filetypes = [
            ("All Files", "*.*"),
            ("Images", "*.jpg *.jpeg *.png *.gif"),
            ("Videos", "*.mp4 *.mov *.avi *.mkv")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Content File",
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file = filename
            self.file_label.configure(text=os.path.basename(filename))
            self.log(f"Selected file: {os.path.basename(filename)}")
    
    def auto_generate_caption(self):
        """Auto-generate caption"""
        caption_text = self.caption_text.get("1.0", "end-1c")
        
        if not caption_text.strip():
            caption_text = "Check out this amazing content!"
        
        # Generate caption
        caption = self.caption_generator.generate_caption(
            content=caption_text,
            platform='instagram'
        )
        
        self.caption_text.delete("1.0", "end")
        self.caption_text.insert("1.0", caption)
        self.log("Caption auto-generated")
    
    def auto_generate_hashtags(self):
        """Auto-generate hashtags"""
        caption_text = self.caption_text.get("1.0", "end-1c")
        
        if not caption_text.strip():
            caption_text = "content social media"
        
        # Generate hashtags
        hashtags = self.hashtag_generator.generate_hashtags(
            content=caption_text,
            platform='instagram',
            category='general'
        )
        
        hashtag_str = self.hashtag_generator.format_hashtags(hashtags, 'instagram')
        
        self.hashtag_text.delete("1.0", "end")
        self.hashtag_text.insert("1.0", hashtag_str)
        self.log(f"Generated {len(hashtags)} hashtags")
    
    def preview_content(self):
        """Preview content before publishing"""
        if not self.selected_file:
            messagebox.showwarning("No File", "Please select a file first")
            return
        
        selected = [name for name, var in self.selected_platforms.items() if var.get()]
        if not selected:
            messagebox.showwarning("No Platform", "Please select at least one platform")
            return
        
        caption = self.caption_text.get("1.0", "end-1c")
        hashtags = self.hashtag_text.get("1.0", "end-1c")
        
        self.log("Opening preview window...")
        PreviewWindow(self.root, self.selected_file, caption, hashtags, selected)
    
    def publish_content(self):
        """Publish content to selected platforms"""
        if not self.selected_file:
            messagebox.showwarning("No File", "Please select a file first")
            return
        
        selected = [name for name, var in self.selected_platforms.items() if var.get()]
        if not selected:
            messagebox.showwarning("No Platform", "Please select at least one platform")
            return
        
        caption = self.caption_text.get("1.0", "end-1c")
        hashtags = self.hashtag_text.get("1.0", "end-1c")
        
        self.log(f"Publishing to: {', '.join(selected)}")
        self.log(f"Caption: {caption[:50]}...")
        self.log(f"Hashtags: {hashtags[:50]}...")
        
        # Start publishing in background thread
        thread = threading.Thread(target=self.publish_worker, args=(selected, caption, hashtags))
        thread.daemon = True
        thread.start()
    
    def publish_worker(self, platforms: List[str], caption: str, hashtags: str):
        """Worker thread for publishing"""
        results = self.publishing_coordinator.publish_to_multiple(
            platforms=platforms,
            content_path=self.selected_file,
            caption=caption,
            hashtags=hashtags,
            callback=self.log
        )
        
        # Summary
        success_count = sum(1 for r in results.values() if r.get('success'))
        self.log(f"\n=== Publishing Complete ===")
        self.log(f"Successful: {success_count}/{len(platforms)}")
        
        if success_count == len(platforms):
            self.log("🎉 All posts published successfully!")
        elif success_count > 0:
            self.log("⚠️ Some posts failed. Check logs above.")
        else:
            self.log("❌ All posts failed.")
    
    def open_settings(self):
        """Open settings window"""
        self.log("Opening settings window...")
        SettingsWindow(self.root)
    
    def log(self, message: str):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert("end", log_message)
        self.log_text.see("end")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
