"""Main GUI window"""
import customtkinter as ctk
from pathlib import Path
import json
from .subtitle_tab import SubtitleTab
from .document_tab import DocumentTab
from .web_tab import WebTab
from .text_tab import TextTab
from .realtime_tab import RealtimeTab
from .settings_window import SettingsWindow


class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Translation Automation Platform")
        self.root.geometry("1200x800")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Load config
        self.config = self._load_config()
        
        # Create UI
        self._create_menu()
        self._create_tabs()
        
    def _load_config(self) -> dict:
        """Load configuration from file"""
        config_path = Path("config.json")
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        # Default config
        return {
            "api_keys": {
                "deepl": "",
                "google": "",
                "papago_client_id": "",
                "papago_client_secret": "",
                "openai": ""
            },
            "default_source_lang": "ko",
            "default_target_lang": "en",
            "default_engine": "google",
            "cache_enabled": True,
            "max_cache_size_mb": 100
        }
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def _create_menu(self):
        """Create menu bar"""
        # Header frame
        header_frame = ctk.CTkFrame(self.root, height=60)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Translation Automation Platform",
            font=("Arial", 24, "bold")
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        settings_button = ctk.CTkButton(
            header_frame,
            text="⚙ Settings",
            width=100,
            command=self._open_settings
        )
        settings_button.pack(side="right", padx=20, pady=15)
    
    def _create_tabs(self):
        """Create tab view"""
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("📄 Subtitles")
        self.tabview.add("📚 Documents")
        self.tabview.add("🌐 Web")
        self.tabview.add("✏️ Text")
        self.tabview.add("🎤 Real-time")
        
        # Initialize tab content
        self.subtitle_tab = SubtitleTab(self.tabview.tab("📄 Subtitles"), self.config)
        self.document_tab = DocumentTab(self.tabview.tab("📚 Documents"), self.config)
        self.web_tab = WebTab(self.tabview.tab("🌐 Web"), self.config)
        self.text_tab = TextTab(self.tabview.tab("✏️ Text"), self.config)
        self.realtime_tab = RealtimeTab(self.tabview.tab("🎤 Real-time"), self.config)
    
    def _open_settings(self):
        """Open settings window"""
        settings_window = SettingsWindow(self.root, self.config, self._save_config)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()
