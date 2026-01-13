"""Settings window."""
import customtkinter as ctk
from tkinter import messagebox
from utils.config_manager import get_config_manager
from utils.logger import get_logger

logger = get_logger()


class SettingsWindow:
    """Settings window for API keys and configuration."""
    
    def __init__(self, parent):
        """Initialize settings window."""
        self.config = get_config_manager()
        
        # Create window
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Settings")
        self.window.geometry("600x500")
        self.window.grab_set()  # Make modal
        
        self._create_ui()
        logger.info("Settings window opened")
    
    def _create_ui(self):
        """Create UI elements."""
        # Main frame
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="Settings", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # API Keys section
        api_frame = ctk.CTkFrame(main_frame)
        api_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(api_frame, text="API Keys", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5, anchor="w", padx=10)
        
        # Azure Speech Key
        ctk.CTkLabel(api_frame, text="Azure Speech Key:").pack(pady=(10, 0), anchor="w", padx=10)
        self.azure_key_entry = ctk.CTkEntry(api_frame, placeholder_text="Enter Azure Speech API Key")
        self.azure_key_entry.pack(fill="x", padx=10, pady=5)
        current_azure_key = self.config.get_api_key('azure_speech_key')
        if current_azure_key:
            self.azure_key_entry.insert(0, current_azure_key)
        
        # Azure Region
        ctk.CTkLabel(api_frame, text="Azure Region:").pack(pady=(10, 0), anchor="w", padx=10)
        self.azure_region_entry = ctk.CTkEntry(api_frame, placeholder_text="e.g., eastus")
        self.azure_region_entry.pack(fill="x", padx=10, pady=5)
        current_region = self.config.get('api_keys.azure_speech_region', 'eastus')
        self.azure_region_entry.insert(0, current_region)
        
        # Google Cloud Credentials
        ctk.CTkLabel(api_frame, text="Google Cloud Credentials Path:").pack(pady=(10, 0), anchor="w", padx=10)
        self.google_creds_entry = ctk.CTkEntry(api_frame, placeholder_text="Path to credentials JSON file")
        self.google_creds_entry.pack(fill="x", padx=10, pady=5)
        current_google_creds = self.config.get_api_key('google_cloud_credentials_path')
        if current_google_creds:
            self.google_creds_entry.insert(0, current_google_creds)
        
        # DeepL API Key
        ctk.CTkLabel(api_frame, text="DeepL API Key (optional):").pack(pady=(10, 0), anchor="w", padx=10)
        self.deepl_key_entry = ctk.CTkEntry(api_frame, placeholder_text="Enter DeepL API Key")
        self.deepl_key_entry.pack(fill="x", padx=10, pady=5)
        current_deepl_key = self.config.get_api_key('deepl_api_key')
        if current_deepl_key:
            self.deepl_key_entry.insert(0, current_deepl_key)
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=20)
        
        save_btn = ctk.CTkButton(button_frame, text="💾 Save Settings", command=self.save_settings)
        save_btn.pack(side="left", padx=5)
        
        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", command=self.window.destroy)
        cancel_btn.pack(side="left", padx=5)
    
    def save_settings(self):
        """Save settings to config file."""
        try:
            # Update config
            self.config.set('api_keys.azure_speech_key', self.azure_key_entry.get())
            self.config.set('api_keys.azure_speech_region', self.azure_region_entry.get())
            self.config.set('api_keys.google_cloud_credentials_path', self.google_creds_entry.get())
            self.config.set('api_keys.deepl_api_key', self.deepl_key_entry.get())
            
            # Save to file
            if self.config.save_config():
                messagebox.showinfo("Success", "Settings saved successfully!")
                logger.info("Settings saved")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Failed to save settings")
                
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
