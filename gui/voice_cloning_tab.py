"""Voice cloning tab."""
import customtkinter as ctk
from tkinter import messagebox
from utils.logger import get_logger

logger = get_logger()


class VoiceCloningTab:
    """Voice cloning tab UI."""
    
    def __init__(self, parent):
        """Initialize voice cloning tab."""
        self.parent = parent
        self._create_ui()
        logger.info("Voice cloning tab initialized")
    
    def _create_ui(self):
        """Create UI elements."""
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Info label
        info_label = ctk.CTkLabel(
            main_frame,
            text="Voice Cloning (RVC)\n\nThis feature requires additional setup and dependencies.\n"
                 "Please refer to the documentation for RVC installation instructions.",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        info_label.pack(expand=True, pady=50)
        
        # Placeholder button
        placeholder_btn = ctk.CTkButton(
            main_frame,
            text="ℹ️ Feature Coming Soon",
            command=self.show_info,
            state="disabled"
        )
        placeholder_btn.pack(pady=10)
    
    def show_info(self):
        """Show information about voice cloning."""
        messagebox.showinfo(
            "Voice Cloning",
            "Voice cloning using RVC (Retrieval-based Voice Conversion) requires:\n\n"
            "1. Training audio samples (5-10 minutes)\n"
            "2. GPU for training (recommended)\n"
            "3. Additional RVC dependencies\n\n"
            "This feature is a placeholder and requires full RVC implementation."
        )
