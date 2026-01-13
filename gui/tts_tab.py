"""TTS (Text-to-Speech) tab."""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from modules.tts.gtts_engine import GTTSEngine
from modules.tts.pyttsx3_engine import Pyttsx3Engine
from modules.tts.azure_tts import AzureTTSEngine
from modules.tts.google_cloud_tts import GoogleCloudTTSEngine
from utils.config_manager import get_config_manager
from utils.logger import get_logger

logger = get_logger()


class TTSTab:
    """TTS tab UI."""
    
    def __init__(self, parent):
        """Initialize TTS tab."""
        self.parent = parent
        self.config = get_config_manager()
        
        # Initialize engines
        self.engines = {
            'gTTS': GTTSEngine(),
            'pyttsx3': Pyttsx3Engine(),
            'Azure TTS': AzureTTSEngine(),
            'Google Cloud TTS': GoogleCloudTTSEngine()
        }
        
        self._create_ui()
        logger.info("TTS tab initialized")
    
    def _create_ui(self):
        """Create UI elements."""
        # Main container
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Input
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Text input
        ctk.CTkLabel(left_frame, text="Text Input:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        self.text_input = ctk.CTkTextbox(left_frame, height=200)
        self.text_input.pack(fill="both", expand=True, padx=10, pady=5)
        
        # File upload button
        upload_btn = ctk.CTkButton(left_frame, text="📁 Load from File", command=self.load_file)
        upload_btn.pack(pady=5)
        
        # Right panel - Settings
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="right", fill="both", padx=(10, 0))
        
        ctk.CTkLabel(right_frame, text="Settings", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        # Engine selection
        ctk.CTkLabel(right_frame, text="Engine:").pack(pady=(10, 0))
        self.engine_var = ctk.StringVar(value="gTTS")
        engine_menu = ctk.CTkOptionMenu(right_frame, variable=self.engine_var, 
                                        values=list(self.engines.keys()))
        engine_menu.pack(pady=5, padx=10, fill="x")
        
        # Language selection
        ctk.CTkLabel(right_frame, text="Language:").pack(pady=(10, 0))
        self.language_var = ctk.StringVar(value="en")
        languages = ["en", "ko", "ja", "zh-cn", "es", "fr", "de", "it", "pt", "ru"]
        language_menu = ctk.CTkOptionMenu(right_frame, variable=self.language_var, values=languages)
        language_menu.pack(pady=5, padx=10, fill="x")
        
        # Gender selection
        ctk.CTkLabel(right_frame, text="Voice Gender:").pack(pady=(10, 0))
        self.gender_var = ctk.StringVar(value="female")
        gender_menu = ctk.CTkOptionMenu(right_frame, variable=self.gender_var, 
                                        values=["female", "male"])
        gender_menu.pack(pady=5, padx=10, fill="x")
        
        # Speed slider
        ctk.CTkLabel(right_frame, text="Speed:").pack(pady=(10, 0))
        self.speed_var = ctk.DoubleVar(value=1.0)
        speed_slider = ctk.CTkSlider(right_frame, from_=0.5, to=2.0, variable=self.speed_var)
        speed_slider.pack(pady=5, padx=10, fill="x")
        self.speed_label = ctk.CTkLabel(right_frame, text="1.0x")
        self.speed_label.pack()
        speed_slider.configure(command=lambda v: self.speed_label.configure(text=f"{v:.1f}x"))
        
        # Pitch slider
        ctk.CTkLabel(right_frame, text="Pitch:").pack(pady=(10, 0))
        self.pitch_var = ctk.DoubleVar(value=1.0)
        pitch_slider = ctk.CTkSlider(right_frame, from_=0.5, to=2.0, variable=self.pitch_var)
        pitch_slider.pack(pady=5, padx=10, fill="x")
        self.pitch_label = ctk.CTkLabel(right_frame, text="1.0x")
        self.pitch_label.pack()
        pitch_slider.configure(command=lambda v: self.pitch_label.configure(text=f"{v:.1f}x"))
        
        # Buttons
        button_frame = ctk.CTkFrame(right_frame)
        button_frame.pack(pady=20, padx=10, fill="x")
        
        self.generate_btn = ctk.CTkButton(button_frame, text="🎤 Generate Speech", 
                                          command=self.generate_speech)
        self.generate_btn.pack(pady=5, fill="x")
        
        self.save_btn = ctk.CTkButton(button_frame, text="💾 Save Audio", 
                                      command=self.save_audio, state="disabled")
        self.save_btn.pack(pady=5, fill="x")
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(right_frame)
        self.progress.pack(pady=10, padx=10, fill="x")
        self.progress.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(right_frame, text="Ready")
        self.status_label.pack(pady=5)
        
        self.output_file = None
    
    def load_file(self):
        """Load text from file."""
        filename = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    text = f.read()
                self.text_input.delete("1.0", "end")
                self.text_input.insert("1.0", text)
                logger.info(f"Loaded text from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
                logger.error(f"Error loading file: {e}")
    
    def generate_speech(self):
        """Generate speech from text."""
        text = self.text_input.get("1.0", "end").strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter text to synthesize")
            return
        
        # Disable button during generation
        self.generate_btn.configure(state="disabled")
        self.status_label.configure(text="Generating...")
        self.progress.set(0.5)
        
        # Run in thread
        thread = threading.Thread(target=self._generate_thread, args=(text,))
        thread.start()
    
    def _generate_thread(self, text):
        """Generate speech in background thread."""
        try:
            engine_name = self.engine_var.get()
            engine = self.engines[engine_name]
            
            # Create output path
            output_dir = self.config.get_output_path('tts')
            self.output_file = os.path.join(output_dir, 'tts_output.mp3')
            
            # Generate speech
            success = engine.synthesize(
                text=text,
                output_path=self.output_file,
                language=self.language_var.get(),
                gender=self.gender_var.get(),
                rate=self.speed_var.get(),
                pitch=self.pitch_var.get()
            )
            
            if success:
                self.status_label.configure(text="✓ Speech generated successfully!")
                self.save_btn.configure(state="normal")
                self.progress.set(1.0)
            else:
                self.status_label.configure(text="✗ Generation failed")
                self.progress.set(0)
                
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            self.status_label.configure(text=f"✗ Error: {str(e)}")
            self.progress.set(0)
        finally:
            self.generate_btn.configure(state="normal")
    
    def save_audio(self):
        """Save generated audio to custom location."""
        if not self.output_file or not os.path.exists(self.output_file):
            messagebox.showwarning("Warning", "No audio to save")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Audio File",
            defaultextension=".mp3",
            filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                import shutil
                shutil.copy2(self.output_file, filename)
                messagebox.showinfo("Success", f"Audio saved to {filename}")
                logger.info(f"Audio saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
                logger.error(f"Error saving file: {e}")
