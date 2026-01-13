"""
GUI Module
Provides intuitive user interface using CustomTkinter
"""
import logging
import os
import sys
import threading
from typing import Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import core modules
from crawler import ContentCrawler
from content import ContentRestructurer
from tts import TTSManager
from video import VideoCreator
from youtube import YouTubeUploader

logger = logging.getLogger(__name__)


class AutoContentGeneratorGUI:
    """Main GUI application for YouTube Auto Content Generator"""
    
    def __init__(self):
        try:
            import customtkinter as ctk
            self.ctk = ctk
            
            # Set appearance and theme
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            
            # Create main window
            self.root = ctk.CTk()
            self.root.title("YouTube Auto Content Generator")
            self.root.geometry("900x700")
            
            # Variables
            self.topic_var = None
            self.channel_type_var = None
            self.tts_engine_var = None
            self.status_var = None
            
            # Create UI
            self._create_ui()
            
            logger.info("GUI initialized successfully")
            
        except ImportError as e:
            logger.error(f"CustomTkinter not installed: {e}. Run: pip install customtkinter")
            raise
    
    def _create_ui(self):
        """Create UI components"""
        
        # Title
        title = self.ctk.CTkLabel(
            self.root, 
            text="YouTube Auto Content Generator",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        # Main frame
        main_frame = self.ctk.CTkFrame(self.root)
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Topic section
        topic_label = self.ctk.CTkLabel(
            main_frame, 
            text="콘텐츠 주제:",
            font=("Arial", 14)
        )
        topic_label.pack(pady=(20, 5))
        
        self.topic_var = self.ctk.StringVar()
        topic_entry = self.ctk.CTkEntry(
            main_frame,
            textvariable=self.topic_var,
            width=400,
            height=40,
            placeholder_text="예: 인공지능, 기후변화, K-POP 등"
        )
        topic_entry.pack(pady=5)
        
        # Channel type section
        channel_label = self.ctk.CTkLabel(
            main_frame,
            text="채널 유형:",
            font=("Arial", 14)
        )
        channel_label.pack(pady=(20, 5))
        
        self.channel_type_var = self.ctk.StringVar(value="informational")
        channel_frame = self.ctk.CTkFrame(main_frame)
        channel_frame.pack(pady=5)
        
        channel_types = [
            ("뉴스 리포트", "news"),
            ("정보/교육", "informational"),
            ("스토리텔링", "storytelling")
        ]
        
        for text, value in channel_types:
            radio = self.ctk.CTkRadioButton(
                channel_frame,
                text=text,
                variable=self.channel_type_var,
                value=value
            )
            radio.pack(side="left", padx=10)
        
        # TTS engine section
        tts_label = self.ctk.CTkLabel(
            main_frame,
            text="TTS 엔진:",
            font=("Arial", 14)
        )
        tts_label.pack(pady=(20, 5))
        
        self.tts_engine_var = self.ctk.StringVar(value="gtts")
        tts_frame = self.ctk.CTkFrame(main_frame)
        tts_frame.pack(pady=5)
        
        tts_engines = [
            ("Google TTS", "gtts"),
            ("Pyttsx3 (오프라인)", "pyttsx3"),
            ("맞춤형 TTS", "custom")
        ]
        
        for text, value in tts_engines:
            radio = self.ctk.CTkRadioButton(
                tts_frame,
                text=text,
                variable=self.tts_engine_var,
                value=value
            )
            radio.pack(side="left", padx=10)
        
        # Options section
        options_frame = self.ctk.CTkFrame(main_frame)
        options_frame.pack(pady=20, fill="x", padx=20)
        
        self.crawl_news_var = self.ctk.BooleanVar(value=True)
        news_check = self.ctk.CTkCheckBox(
            options_frame,
            text="뉴스 크롤링",
            variable=self.crawl_news_var
        )
        news_check.pack(side="left", padx=10)
        
        self.crawl_wiki_var = self.ctk.BooleanVar(value=True)
        wiki_check = self.ctk.CTkCheckBox(
            options_frame,
            text="위키 크롤링",
            variable=self.crawl_wiki_var
        )
        wiki_check.pack(side="left", padx=10)
        
        self.upload_youtube_var = self.ctk.BooleanVar(value=False)
        upload_check = self.ctk.CTkCheckBox(
            options_frame,
            text="YouTube 자동 업로드",
            variable=self.upload_youtube_var
        )
        upload_check.pack(side="left", padx=10)
        
        # Generate button
        self.generate_btn = self.ctk.CTkButton(
            main_frame,
            text="콘텐츠 생성 시작",
            command=self._on_generate_click,
            width=300,
            height=50,
            font=("Arial", 16, "bold")
        )
        self.generate_btn.pack(pady=20)
        
        # Progress/Status section
        status_label = self.ctk.CTkLabel(
            main_frame,
            text="상태:",
            font=("Arial", 14)
        )
        status_label.pack(pady=(10, 5))
        
        self.status_text = self.ctk.CTkTextbox(
            main_frame,
            width=500,
            height=150
        )
        self.status_text.pack(pady=5)
        self.status_text.configure(state="disabled")
        
        # Progress bar
        self.progress_bar = self.ctk.CTkProgressBar(main_frame, width=500)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
    
    def _on_generate_click(self):
        """Handle generate button click"""
        topic = self.topic_var.get().strip()
        
        if not topic:
            self._update_status("❌ 주제를 입력해주세요!")
            return
        
        # Disable button during generation
        self.generate_btn.configure(state="disabled")
        
        # Run generation in separate thread
        thread = threading.Thread(target=self._generate_content, args=(topic,))
        thread.daemon = True
        thread.start()
    
    def _generate_content(self, topic: str):
        """Generate content (runs in separate thread)"""
        try:
            # Get options
            channel_type = self.channel_type_var.get()
            tts_engine = self.tts_engine_var.get()
            crawl_news = self.crawl_news_var.get()
            crawl_wiki = self.crawl_wiki_var.get()
            upload_youtube = self.upload_youtube_var.get()
            
            # Create output directory
            output_dir = os.path.join("output", topic.replace(' ', '_'))
            os.makedirs(output_dir, exist_ok=True)
            
            # Step 1: Crawl content
            self._update_status(f"🔍 '{topic}' 콘텐츠 수집 중...")
            self._update_progress(0.1)
            
            crawler = ContentCrawler()
            content_data = crawler.crawl_content(topic, include_news=crawl_news, 
                                                include_wiki=crawl_wiki)
            
            # Step 2: Generate script
            self._update_status("📝 스크립트 생성 중...")
            self._update_progress(0.3)
            
            restructurer = ContentRestructurer()
            script = restructurer.generate_script(content_data, template_type=channel_type)
            metadata = restructurer.generate_metadata(content_data, script)
            
            # Save script
            script_path = os.path.join(output_dir, "script.txt")
            restructurer.save_script(script, script_path)
            
            # Step 3: Generate TTS
            self._update_status("🎤 음성 생성 중...")
            self._update_progress(0.5)
            
            tts_manager = TTSManager(engine_type=tts_engine)
            audio_path = os.path.join(output_dir, "audio.mp3")
            tts_manager.text_to_speech(script, audio_path)
            
            # Step 4: Create video
            self._update_status("🎬 비디오 생성 중...")
            self._update_progress(0.7)
            
            video_creator = VideoCreator()
            video_path = os.path.join(output_dir, "video.mp4")
            video_creator.create_simple_video(audio_path, video_path)
            
            # Step 5: Upload to YouTube (if enabled)
            if upload_youtube:
                self._update_status("📤 YouTube 업로드 중...")
                self._update_progress(0.9)
                
                uploader = YouTubeUploader()
                if uploader.is_authenticated():
                    video_id = uploader.upload_video(video_path, metadata)
                    if video_id:
                        self._update_status(f"✅ 완료! YouTube Video ID: {video_id}")
                    else:
                        self._update_status("⚠️ 비디오는 생성되었으나 업로드 실패")
                else:
                    self._update_status("⚠️ YouTube 인증 필요. 비디오는 로컬에 저장됨")
            else:
                self._update_status(f"✅ 완료! 비디오 저장 위치: {video_path}")
            
            self._update_progress(1.0)
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            self._update_status(f"❌ 오류 발생: {str(e)}")
        finally:
            # Re-enable button
            self.root.after(0, lambda: self.generate_btn.configure(state="normal"))
    
    def _update_status(self, message: str):
        """Update status text"""
        def update():
            self.status_text.configure(state="normal")
            self.status_text.insert("end", message + "\n")
            self.status_text.see("end")
            self.status_text.configure(state="disabled")
        
        self.root.after(0, update)
        logger.info(message)
    
    def _update_progress(self, value: float):
        """Update progress bar"""
        self.root.after(0, lambda: self.progress_bar.set(value))
    
    def run(self):
        """Run the GUI application"""
        logger.info("Starting GUI application")
        self.root.mainloop()


def launch_gui():
    """Launch the GUI application"""
    try:
        app = AutoContentGeneratorGUI()
        app.run()
    except Exception as e:
        logger.error(f"Failed to launch GUI: {e}")
        raise
