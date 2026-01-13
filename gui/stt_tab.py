"""STT (Speech-to-Text) tab."""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from modules.stt.whisper_stt import WhisperSTT
from utils.config_manager import get_config_manager
from utils.logger import get_logger

logger = get_logger()


class STTTab:
    """STT tab UI."""
    
    def __init__(self, parent):
        """Initialize STT tab."""
        self.parent = parent
        self.config = get_config_manager()
        self.whisper_engine = WhisperSTT()
        self.audio_file = None
        
        self._create_ui()
        logger.info("STT tab initialized")
    
    def _create_ui(self):
        """Create UI elements."""
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # File selection
        ctk.CTkLabel(left_frame, text="Audio File:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        file_frame = ctk.CTkFrame(left_frame)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        self.file_label = ctk.CTkLabel(file_frame, text="No file selected")
        self.file_label.pack(side="left", padx=10)
        
        select_btn = ctk.CTkButton(file_frame, text="📁 Select Audio", command=self.select_file)
        select_btn.pack(side="right", padx=10)
        
        # Output text
        ctk.CTkLabel(left_frame, text="Transcription:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))
        
        self.output_text = ctk.CTkTextbox(left_frame, height=400)
        self.output_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Right panel - Settings
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="right", fill="both", padx=(10, 0))
        
        ctk.CTkLabel(right_frame, text="Settings", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        # Model size
        ctk.CTkLabel(right_frame, text="Whisper Model:").pack(pady=(10, 0))
        self.model_var = ctk.StringVar(value="base")
        model_menu = ctk.CTkOptionMenu(right_frame, variable=self.model_var,
                                       values=["tiny", "base", "small", "medium", "large"])
        model_menu.pack(pady=5, padx=10, fill="x")
        
        # Language
        ctk.CTkLabel(right_frame, text="Language:").pack(pady=(10, 0))
        self.language_var = ctk.StringVar(value="auto")
        languages = ["auto", "en", "ko", "ja", "zh", "es", "fr", "de", "it", "pt", "ru"]
        language_menu = ctk.CTkOptionMenu(right_frame, variable=self.language_var, values=languages)
        language_menu.pack(pady=5, padx=10, fill="x")
        
        # Timestamps option
        self.timestamps_var = ctk.BooleanVar(value=True)
        timestamps_check = ctk.CTkCheckBox(right_frame, text="Include Timestamps", 
                                          variable=self.timestamps_var)
        timestamps_check.pack(pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(right_frame)
        button_frame.pack(pady=20, padx=10, fill="x")
        
        self.transcribe_btn = ctk.CTkButton(button_frame, text="🎙️ Transcribe", 
                                            command=self.transcribe, state="disabled")
        self.transcribe_btn.pack(pady=5, fill="x")
        
        self.save_txt_btn = ctk.CTkButton(button_frame, text="💾 Save Text", 
                                         command=self.save_text, state="disabled")
        self.save_txt_btn.pack(pady=5, fill="x")
        
        self.save_srt_btn = ctk.CTkButton(button_frame, text="💾 Save SRT", 
                                         command=self.save_srt, state="disabled")
        self.save_srt_btn.pack(pady=5, fill="x")
        
        # Progress
        self.progress = ctk.CTkProgressBar(right_frame)
        self.progress.pack(pady=10, padx=10, fill="x")
        self.progress.set(0)
        
        self.status_label = ctk.CTkLabel(right_frame, text="Ready")
        self.status_label.pack(pady=5)
        
        self.result = None
    
    def select_file(self):
        """Select audio file."""
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.flac *.ogg"), ("All Files", "*.*")]
        )
        
        if filename:
            self.audio_file = filename
            self.file_label.configure(text=os.path.basename(filename))
            self.transcribe_btn.configure(state="normal")
            logger.info(f"Selected audio file: {filename}")
    
    def transcribe(self):
        """Transcribe audio file."""
        if not self.audio_file:
            messagebox.showwarning("Warning", "Please select an audio file")
            return
        
        # Update Whisper model if changed
        model_size = self.model_var.get()
        if self.whisper_engine.model_size != model_size:
            self.whisper_engine = WhisperSTT(model_size)
        
        self.transcribe_btn.configure(state="disabled")
        self.status_label.configure(text="Transcribing...")
        self.progress.set(0.5)
        
        thread = threading.Thread(target=self._transcribe_thread)
        thread.start()
    
    def _transcribe_thread(self):
        """Transcribe in background thread."""
        try:
            language = self.language_var.get()
            if language == "auto":
                language = None
            
            self.result = self.whisper_engine.transcribe(self.audio_file, language=language)
            
            if self.result:
                text = self.result.get('text', '')
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", text)
                
                self.status_label.configure(text=f"✓ Transcription completed! Language: {self.result.get('language', 'unknown')}")
                self.save_txt_btn.configure(state="normal")
                
                if self.timestamps_var.get():
                    self.save_srt_btn.configure(state="normal")
                
                self.progress.set(1.0)
            else:
                self.status_label.configure(text="✗ Transcription failed")
                self.progress.set(0)
                
        except Exception as e:
            logger.error(f"Error transcribing: {e}")
            self.status_label.configure(text=f"✗ Error: {str(e)}")
            self.progress.set(0)
        finally:
            self.transcribe_btn.configure(state="normal")
    
    def save_text(self):
        """Save transcription as text file."""
        if not self.result:
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Transcription",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                text = self.result.get('text', '')
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("Success", f"Transcription saved to {filename}")
                logger.info(f"Transcription saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}")
    
    def save_srt(self):
        """Save transcription as SRT subtitle file."""
        if not self.audio_file:
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save SRT Subtitle",
            defaultextension=".srt",
            filetypes=[("SRT Files", "*.srt"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                language = self.language_var.get()
                if language == "auto":
                    language = None
                
                success = self.whisper_engine.generate_srt(self.audio_file, filename, language)
                
                if success:
                    messagebox.showinfo("Success", f"SRT saved to {filename}")
                    logger.info(f"SRT saved to {filename}")
                else:
                    messagebox.showerror("Error", "Failed to generate SRT")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save SRT: {e}")
