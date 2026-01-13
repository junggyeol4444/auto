"""Real-time subtitle translation tab"""
import customtkinter as ctk
from tkinter import messagebox
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from modules.translation.translation_engine import TranslationEngine
from modules.subtitle.realtime_subtitle import RealtimeSubtitle


class RealtimeTab:
    """Real-time subtitle translation tab"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.realtime_subtitle = None
        self.is_running = False
        
        self._create_ui()
    
    def _create_ui(self):
        """Create UI elements"""
        # Options frame
        options_frame = ctk.CTkFrame(self.parent)
        options_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(options_frame, text="From:").grid(row=0, column=0, padx=10, pady=10)
        self.source_lang = ctk.CTkComboBox(
            options_frame,
            values=["ko", "en", "ja", "zh-CN", "es", "fr", "de"],
            width=100
        )
        self.source_lang.set(self.config.get('default_source_lang', 'ko'))
        self.source_lang.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(options_frame, text="To:").grid(row=0, column=2, padx=10, pady=10)
        self.target_lang = ctk.CTkComboBox(
            options_frame,
            values=["en", "ko", "ja", "zh-CN", "es", "fr", "de"],
            width=100
        )
        self.target_lang.set(self.config.get('default_target_lang', 'en'))
        self.target_lang.grid(row=0, column=3, padx=10, pady=10)
        
        ctk.CTkLabel(options_frame, text="Engine:").grid(row=0, column=4, padx=10, pady=10)
        self.engine = ctk.CTkComboBox(
            options_frame,
            values=["auto", "deepl", "google", "papago", "gpt4"],
            width=100
        )
        self.engine.set(self.config.get('default_engine', 'google'))
        self.engine.grid(row=0, column=5, padx=10, pady=10)
        
        # Audio source frame
        audio_frame = ctk.CTkFrame(self.parent)
        audio_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(audio_frame, text="Audio Source:", font=("Arial", 14)).pack(side="left", padx=10)
        
        self.audio_source = ctk.CTkSegmentedButton(
            audio_frame,
            values=["Microphone", "System Audio", "Text Input (Demo)"]
        )
        self.audio_source.set("Text Input (Demo)")
        self.audio_source.pack(side="left", padx=20)
        
        # Control buttons
        control_frame = ctk.CTkFrame(self.parent)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        self.start_button = ctk.CTkButton(
            control_frame,
            text="▶ Start",
            command=self._start_translation,
            width=150,
            height=40,
            fg_color="green"
        )
        self.start_button.pack(side="left", padx=10)
        
        self.stop_button = ctk.CTkButton(
            control_frame,
            text="⬛ Stop",
            command=self._stop_translation,
            width=150,
            height=40,
            fg_color="red",
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=10)
        
        # Demo input (for text input mode)
        self.demo_frame = ctk.CTkFrame(self.parent)
        self.demo_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.demo_frame, text="Demo Input:").pack(side="left", padx=10)
        
        self.demo_input = ctk.CTkEntry(self.demo_frame, placeholder_text="Enter text to translate...")
        self.demo_input.pack(side="left", fill="x", expand=True, padx=10)
        
        ctk.CTkButton(
            self.demo_frame,
            text="Translate",
            command=self._demo_translate,
            width=100
        ).pack(side="right", padx=10)
        
        # Display frame
        display_frame = ctk.CTkFrame(self.parent)
        display_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Original text
        orig_frame = ctk.CTkFrame(display_frame)
        orig_frame.pack(fill="both", expand=True, pady=5)
        
        ctk.CTkLabel(orig_frame, text="Original", font=("Arial", 14, "bold")).pack(pady=5)
        
        self.original_text = ctk.CTkTextbox(orig_frame, height=150, font=("Arial", 16))
        self.original_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Translated text
        trans_frame = ctk.CTkFrame(display_frame)
        trans_frame.pack(fill="both", expand=True, pady=5)
        
        ctk.CTkLabel(trans_frame, text="Translated", font=("Arial", 14, "bold")).pack(pady=5)
        
        self.translated_text = ctk.CTkTextbox(trans_frame, height=150, font=("Arial", 16))
        self.translated_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Info label
        info_text = """
        Real-time translation demo mode:
        • Text Input: Enter text manually to see translation
        • Microphone/System Audio: Requires Whisper STT (advanced setup)
        
        Note: Full audio capture requires additional setup and dependencies.
        """
        
        ctk.CTkLabel(
            self.parent,
            text=info_text,
            justify="left",
            text_color="gray",
            font=("Arial", 10)
        ).pack(pady=10)
        
        # Status label
        self.status_label = ctk.CTkLabel(self.parent, text="Ready", text_color="gray")
        self.status_label.pack(pady=5)
    
    def _start_translation(self):
        """Start real-time translation"""
        try:
            engine = TranslationEngine(self.config)
            engine_type = self.engine.get()
            
            if engine_type == "auto":
                translator = engine.auto_select_engine(
                    self.source_lang.get(),
                    self.target_lang.get(),
                    "general"
                )
            else:
                translator = engine.get_translator(engine_type)
            
            if not translator:
                raise ValueError("Translation engine not available")
            
            # Initialize real-time subtitle
            self.realtime_subtitle = RealtimeSubtitle(
                translator,
                self.source_lang.get(),
                self.target_lang.get()
            )
            
            # Start translation worker
            self.realtime_subtitle.start(self._display_translation)
            
            self.is_running = True
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.status_label.configure(text="Running...", text_color="green")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _stop_translation(self):
        """Stop real-time translation"""
        if self.realtime_subtitle:
            self.realtime_subtitle.stop()
        
        self.is_running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="Stopped", text_color="gray")
    
    def _demo_translate(self):
        """Translate demo input"""
        if not self.is_running:
            messagebox.showwarning("Warning", "Please start translation first")
            return
        
        text = self.demo_input.get().strip()
        if text:
            self.realtime_subtitle.add_text(text)
            self.demo_input.delete(0, "end")
    
    def _display_translation(self, original: str, translated: str):
        """Display translation result"""
        # Update display in GUI thread
        self.original_text.delete("1.0", "end")
        self.original_text.insert("1.0", original)
        
        self.translated_text.delete("1.0", "end")
        self.translated_text.insert("1.0", translated)
