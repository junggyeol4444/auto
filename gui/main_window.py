"""Main window for Voice Service Integrated Suite."""
import customtkinter as ctk
from gui.tts_tab import TTSTab
from gui.stt_tab import STTTab
from gui.dubbing_tab import DubbingTab
from gui.voice_cloning_tab import VoiceCloningTab
from gui.audio_processing_tab import AudioProcessingTab
from gui.settings_window import SettingsWindow
from utils.logger import get_logger

logger = get_logger()


class MainWindow:
    """Main application window."""
    
    def __init__(self):
        """Initialize main window."""
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Voice Service Integrated Suite")
        self.root.geometry("1200x800")
        
        # Create menu bar
        self._create_menu()
        
        # Create tab view
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self._create_tabs()
        
        logger.info("Main window initialized")
    
    def _create_menu(self):
        """Create menu bar."""
        menu_frame = ctk.CTkFrame(self.root, height=40)
        menu_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        # Settings button
        settings_btn = ctk.CTkButton(
            menu_frame,
            text="⚙ Settings",
            width=100,
            command=self.open_settings
        )
        settings_btn.pack(side="right", padx=5, pady=5)
        
        # Title label
        title_label = ctk.CTkLabel(
            menu_frame,
            text="Voice Service Integrated Suite",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=10, pady=5)
    
    def _create_tabs(self):
        """Create all tabs."""
        # TTS Tab
        self.tabview.add("TTS")
        self.tts_tab = TTSTab(self.tabview.tab("TTS"))
        
        # STT Tab
        self.tabview.add("STT")
        self.stt_tab = STTTab(self.tabview.tab("STT"))
        
        # Dubbing Tab
        self.tabview.add("Dubbing")
        self.dubbing_tab = DubbingTab(self.tabview.tab("Dubbing"))
        
        # Voice Cloning Tab
        self.tabview.add("Voice Cloning")
        self.voice_cloning_tab = VoiceCloningTab(self.tabview.tab("Voice Cloning"))
        
        # Audio Processing Tab
        self.tabview.add("Audio Processing")
        self.audio_processing_tab = AudioProcessingTab(self.tabview.tab("Audio Processing"))
    
    def open_settings(self):
        """Open settings window."""
        SettingsWindow(self.root)
    
    def run(self):
        """Run the application."""
        logger.info("Starting application")
        self.root.mainloop()


def main():
    """Main entry point for GUI."""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
