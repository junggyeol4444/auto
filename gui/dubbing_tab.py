"""Dubbing tab."""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from modules.dubbing.video_dubbing import VideoDubbing
from modules.dubbing.translation import TranslationService
from modules.stt.whisper_stt import WhisperSTT
from modules.tts.gtts_engine import GTTSEngine
from utils.config_manager import get_config_manager
from utils.logger import get_logger

logger = get_logger()


class DubbingTab:
    """Dubbing tab UI."""
    
    def __init__(self, parent):
        """Initialize dubbing tab."""
        self.parent = parent
        self.config = get_config_manager()
        
        # Initialize components
        self.stt_engine = WhisperSTT('base')
        self.tts_engine = GTTSEngine()
        self.translator = TranslationService()
        self.dubbing = VideoDubbing(self.stt_engine, self.tts_engine, self.translator)
        
        self.video_file = None
        
        self._create_ui()
        logger.info("Dubbing tab initialized")
    
    def _create_ui(self):
        """Create UI elements."""
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Video file selection
        ctk.CTkLabel(main_frame, text="Video Dubbing", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", padx=20, pady=10)
        
        self.file_label = ctk.CTkLabel(file_frame, text="No video selected")
        self.file_label.pack(side="left", padx=10)
        
        select_btn = ctk.CTkButton(file_frame, text="📁 Select Video", command=self.select_video)
        select_btn.pack(side="right", padx=10)
        
        # Settings frame
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        # Source language
        ctk.CTkLabel(settings_frame, text="Source Language:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.source_lang_var = ctk.StringVar(value="en")
        source_lang_menu = ctk.CTkOptionMenu(settings_frame, variable=self.source_lang_var,
                                             values=["en", "ko", "ja", "zh", "es", "fr", "de"])
        source_lang_menu.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # Target language
        ctk.CTkLabel(settings_frame, text="Target Language:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.target_lang_var = ctk.StringVar(value="ko")
        target_lang_menu = ctk.CTkOptionMenu(settings_frame, variable=self.target_lang_var,
                                             values=["ko", "en", "ja", "zh", "es", "fr", "de"])
        target_lang_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Original audio volume
        ctk.CTkLabel(settings_frame, text="Original Audio Volume:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.volume_var = ctk.DoubleVar(value=0.1)
        volume_slider = ctk.CTkSlider(settings_frame, from_=0.0, to=1.0, variable=self.volume_var)
        volume_slider.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.volume_label = ctk.CTkLabel(settings_frame, text="10%")
        self.volume_label.grid(row=2, column=2, padx=10, pady=5)
        volume_slider.configure(command=lambda v: self.volume_label.configure(text=f"{int(v*100)}%"))
        
        settings_frame.columnconfigure(1, weight=1)
        
        # Progress
        self.progress_label = ctk.CTkLabel(main_frame, text="Ready")
        self.progress_label.pack(pady=10)
        
        self.progress = ctk.CTkProgressBar(main_frame)
        self.progress.pack(fill="x", padx=20, pady=10)
        self.progress.set(0)
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=20)
        
        self.dub_btn = ctk.CTkButton(button_frame, text="🎬 Start Dubbing", 
                                     command=self.start_dubbing, state="disabled", width=200)
        self.dub_btn.pack()
    
    def select_video(self):
        """Select video file."""
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video Files", "*.mp4 *.mkv *.avi *.mov"), ("All Files", "*.*")]
        )
        
        if filename:
            self.video_file = filename
            self.file_label.configure(text=os.path.basename(filename))
            self.dub_btn.configure(state="normal")
            logger.info(f"Selected video: {filename}")
    
    def start_dubbing(self):
        """Start video dubbing process."""
        if not self.video_file:
            messagebox.showwarning("Warning", "Please select a video file")
            return
        
        output_file = filedialog.asksaveasfilename(
            title="Save Dubbed Video",
            defaultextension=".mp4",
            filetypes=[("MP4 Files", "*.mp4"), ("All Files", "*.*")]
        )
        
        if not output_file:
            return
        
        self.dub_btn.configure(state="disabled")
        
        thread = threading.Thread(target=self._dubbing_thread, args=(output_file,))
        thread.start()
    
    def _dubbing_thread(self, output_file):
        """Dubbing process in background thread."""
        try:
            def progress_callback(message, percent):
                self.progress_label.configure(text=message)
                self.progress.set(percent / 100)
            
            success = self.dubbing.dub_video(
                video_path=self.video_file,
                output_path=output_file,
                source_lang=self.source_lang_var.get(),
                target_lang=self.target_lang_var.get(),
                original_volume=self.volume_var.get(),
                progress_callback=progress_callback
            )
            
            if success:
                messagebox.showinfo("Success", f"Dubbed video saved to {output_file}")
                logger.info(f"Dubbed video saved to {output_file}")
            else:
                messagebox.showerror("Error", "Dubbing failed")
                
        except Exception as e:
            logger.error(f"Error in dubbing: {e}")
            messagebox.showerror("Error", f"Dubbing failed: {str(e)}")
        finally:
            self.dub_btn.configure(state="normal")
            self.progress.set(0)
            self.progress_label.configure(text="Ready")
