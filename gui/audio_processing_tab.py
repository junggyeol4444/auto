"""Audio processing tab."""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from modules.audio_processing.noise_remover import NoiseRemover
from modules.audio_processing.source_separator import SourceSeparator
from modules.audio_processing.normalizer import Normalizer
from modules.audio_processing.volume_controller import VolumeController
from utils.config_manager import get_config_manager
from utils.logger import get_logger

logger = get_logger()


class AudioProcessingTab:
    """Audio processing tab UI."""
    
    def __init__(self, parent):
        """Initialize audio processing tab."""
        self.parent = parent
        self.config = get_config_manager()
        
        # Initialize processors
        self.noise_remover = NoiseRemover()
        self.source_separator = SourceSeparator()
        self.normalizer = Normalizer()
        self.volume_controller = VolumeController()
        
        self.audio_file = None
        
        self._create_ui()
        logger.info("Audio processing tab initialized")
    
    def _create_ui(self):
        """Create UI elements."""
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # File selection
        ctk.CTkLabel(main_frame, text="Audio Processing", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", padx=20, pady=10)
        
        self.file_label = ctk.CTkLabel(file_frame, text="No audio file selected")
        self.file_label.pack(side="left", padx=10)
        
        select_btn = ctk.CTkButton(file_frame, text="📁 Select Audio", command=self.select_audio)
        select_btn.pack(side="right", padx=10)
        
        # Processing options
        options_frame = ctk.CTkFrame(main_frame)
        options_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left column - Processing types
        left_col = ctk.CTkFrame(options_frame)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(left_col, text="Processing Options", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        self.process_var = ctk.StringVar(value="noise_removal")
        
        ctk.CTkRadioButton(left_col, text="Noise Removal", variable=self.process_var, 
                          value="noise_removal").pack(pady=5, padx=10, anchor="w")
        ctk.CTkRadioButton(left_col, text="Vocal/Accompaniment Separation", variable=self.process_var,
                          value="source_separation").pack(pady=5, padx=10, anchor="w")
        ctk.CTkRadioButton(left_col, text="Volume Normalization (LUFS)", variable=self.process_var,
                          value="normalization").pack(pady=5, padx=10, anchor="w")
        ctk.CTkRadioButton(left_col, text="Volume Adjustment", variable=self.process_var,
                          value="volume_adjustment").pack(pady=5, padx=10, anchor="w")
        
        # Right column - Settings
        right_col = ctk.CTkFrame(options_frame)
        right_col.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(right_col, text="Settings", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Target LUFS for normalization
        ctk.CTkLabel(right_col, text="Target LUFS:").pack(pady=(10, 0))
        self.lufs_var = ctk.DoubleVar(value=-16.0)
        lufs_slider = ctk.CTkSlider(right_col, from_=-30.0, to=-6.0, variable=self.lufs_var)
        lufs_slider.pack(pady=5, padx=10, fill="x")
        self.lufs_label = ctk.CTkLabel(right_col, text="-16.0 LUFS")
        self.lufs_label.pack()
        lufs_slider.configure(command=lambda v: self.lufs_label.configure(text=f"{v:.1f} LUFS"))
        
        # Volume gain
        ctk.CTkLabel(right_col, text="Volume Gain (dB):").pack(pady=(10, 0))
        self.gain_var = ctk.DoubleVar(value=0.0)
        gain_slider = ctk.CTkSlider(right_col, from_=-20.0, to=20.0, variable=self.gain_var)
        gain_slider.pack(pady=5, padx=10, fill="x")
        self.gain_label = ctk.CTkLabel(right_col, text="0.0 dB")
        self.gain_label.pack()
        gain_slider.configure(command=lambda v: self.gain_label.configure(text=f"{v:.1f} dB"))
        
        # Progress
        self.progress = ctk.CTkProgressBar(main_frame)
        self.progress.pack(fill="x", padx=20, pady=10)
        self.progress.set(0)
        
        self.status_label = ctk.CTkLabel(main_frame, text="Ready")
        self.status_label.pack(pady=5)
        
        # Process button
        self.process_btn = ctk.CTkButton(main_frame, text="⚙️ Process Audio", 
                                        command=self.process_audio, state="disabled", width=200)
        self.process_btn.pack(pady=20)
    
    def select_audio(self):
        """Select audio file."""
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.flac"), ("All Files", "*.*")]
        )
        
        if filename:
            self.audio_file = filename
            self.file_label.configure(text=os.path.basename(filename))
            self.process_btn.configure(state="normal")
            logger.info(f"Selected audio: {filename}")
    
    def process_audio(self):
        """Process audio file."""
        if not self.audio_file:
            messagebox.showwarning("Warning", "Please select an audio file")
            return
        
        process_type = self.process_var.get()
        
        # Get output filename
        output_file = filedialog.asksaveasfilename(
            title="Save Processed Audio",
            defaultextension=".wav",
            filetypes=[("WAV Files", "*.wav"), ("MP3 Files", "*.mp3"), ("All Files", "*.*")]
        )
        
        if not output_file:
            return
        
        self.process_btn.configure(state="disabled")
        self.status_label.configure(text="Processing...")
        self.progress.set(0.5)
        
        thread = threading.Thread(target=self._process_thread, args=(process_type, output_file))
        thread.start()
    
    def _process_thread(self, process_type, output_file):
        """Process audio in background thread."""
        try:
            success = False
            
            if process_type == "noise_removal":
                success = self.noise_remover.remove_noise(self.audio_file, output_file)
            
            elif process_type == "source_separation":
                output_dir = os.path.dirname(output_file)
                success = self.source_separator.separate_vocals(self.audio_file, output_dir, stems=2)
            
            elif process_type == "normalization":
                target_lufs = self.lufs_var.get()
                success = self.normalizer.normalize(self.audio_file, output_file, target_lufs=target_lufs)
            
            elif process_type == "volume_adjustment":
                gain_db = self.gain_var.get()
                success = self.volume_controller.adjust_volume(self.audio_file, output_file, gain_db=gain_db)
            
            if success:
                self.status_label.configure(text="✓ Processing completed!")
                self.progress.set(1.0)
                messagebox.showinfo("Success", f"Processed audio saved to {output_file}")
            else:
                self.status_label.configure(text="✗ Processing failed")
                self.progress.set(0)
                messagebox.showerror("Error", "Audio processing failed")
                
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            self.status_label.configure(text=f"✗ Error: {str(e)}")
            self.progress.set(0)
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
        finally:
            self.process_btn.configure(state="normal")
