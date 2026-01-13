"""Settings window"""
import customtkinter as ctk
from tkinter import messagebox


class SettingsWindow:
    """Settings configuration window"""
    
    def __init__(self, parent, config, save_callback):
        self.config = config
        self.save_callback = save_callback
        
        # Create new window
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Settings")
        self.window.geometry("600x700")
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self._create_ui()
    
    def _create_ui(self):
        """Create UI elements"""
        # Title
        title_label = ctk.CTkLabel(
            self.window,
            text="API Configuration",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=20)
        
        # Scrollable frame for settings
        scroll_frame = ctk.CTkScrollableFrame(self.window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        api_keys = self.config.get('api_keys', {})
        
        # DeepL API Key
        self._create_api_field(
            scroll_frame,
            "DeepL API Key:",
            "deepl",
            api_keys.get('deepl', ''),
            "For Korean-English translation (best quality)"
        )
        
        # Google API (note about googletrans)
        info_frame = ctk.CTkFrame(scroll_frame)
        info_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text="Google Translate:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkLabel(
            info_frame,
            text="Uses googletrans library (no API key needed)",
            text_color="gray",
            font=("Arial", 10)
        ).pack(anchor="w", padx=10)
        
        # Papago API
        self._create_api_field(
            scroll_frame,
            "Papago Client ID:",
            "papago_client_id",
            api_keys.get('papago_client_id', ''),
            "For Korean-Japanese translation"
        )
        
        self._create_api_field(
            scroll_frame,
            "Papago Client Secret:",
            "papago_client_secret",
            api_keys.get('papago_client_secret', ''),
            ""
        )
        
        # OpenAI API Key
        self._create_api_field(
            scroll_frame,
            "OpenAI API Key:",
            "openai",
            api_keys.get('openai', ''),
            "For GPT-4 translation (context-aware)"
        )
        
        # Default settings
        defaults_frame = ctk.CTkFrame(scroll_frame)
        defaults_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            defaults_frame,
            text="Default Settings",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        # Default source language
        lang_frame = ctk.CTkFrame(defaults_frame)
        lang_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(lang_frame, text="Default Source Language:").pack(side="left", padx=5)
        self.default_source = ctk.CTkComboBox(
            lang_frame,
            values=["ko", "en", "ja", "zh-CN", "es", "fr", "de"],
            width=100
        )
        self.default_source.set(self.config.get('default_source_lang', 'ko'))
        self.default_source.pack(side="left", padx=5)
        
        # Default target language
        lang_frame2 = ctk.CTkFrame(defaults_frame)
        lang_frame2.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(lang_frame2, text="Default Target Language:").pack(side="left", padx=5)
        self.default_target = ctk.CTkComboBox(
            lang_frame2,
            values=["en", "ko", "ja", "zh-CN", "es", "fr", "de"],
            width=100
        )
        self.default_target.set(self.config.get('default_target_lang', 'en'))
        self.default_target.pack(side="left", padx=5)
        
        # Default engine
        engine_frame = ctk.CTkFrame(defaults_frame)
        engine_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(engine_frame, text="Default Engine:").pack(side="left", padx=5)
        self.default_engine = ctk.CTkComboBox(
            engine_frame,
            values=["auto", "deepl", "google", "papago", "gpt4"],
            width=100
        )
        self.default_engine.set(self.config.get('default_engine', 'google'))
        self.default_engine.pack(side="left", padx=5)
        
        # Cache settings
        cache_frame = ctk.CTkFrame(scroll_frame)
        cache_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            cache_frame,
            text="Cache Settings",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.cache_enabled = ctk.CTkCheckBox(
            cache_frame,
            text="Enable translation cache"
        )
        self.cache_enabled.pack(anchor="w", padx=10, pady=5)
        if self.config.get('cache_enabled', True):
            self.cache_enabled.select()
        
        # Buttons
        button_frame = ctk.CTkFrame(self.window)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Save",
            command=self._save_settings,
            width=150,
            height=40,
            fg_color="green"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.window.destroy,
            width=150,
            height=40
        ).pack(side="right", padx=10)
    
    def _create_api_field(self, parent, label, key, value, description):
        """Create API key input field"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            frame,
            text=label,
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        entry = ctk.CTkEntry(frame, placeholder_text="Enter API key", show="*")
        entry.pack(fill="x", padx=10, pady=5)
        entry.insert(0, value)
        
        if description:
            ctk.CTkLabel(
                frame,
                text=description,
                text_color="gray",
                font=("Arial", 10)
            ).pack(anchor="w", padx=10)
        
        # Store reference
        setattr(self, f"entry_{key}", entry)
    
    def _save_settings(self):
        """Save settings"""
        try:
            # Update API keys
            api_keys = self.config.setdefault('api_keys', {})
            
            api_keys['deepl'] = self.entry_deepl.get()
            api_keys['papago_client_id'] = self.entry_papago_client_id.get()
            api_keys['papago_client_secret'] = self.entry_papago_client_secret.get()
            api_keys['openai'] = self.entry_openai.get()
            
            # Update defaults
            self.config['default_source_lang'] = self.default_source.get()
            self.config['default_target_lang'] = self.default_target.get()
            self.config['default_engine'] = self.default_engine.get()
            self.config['cache_enabled'] = self.cache_enabled.get() == 1
            
            # Save to file
            self.save_callback()
            
            messagebox.showinfo("Success", "Settings saved successfully")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings:\n{e}")
