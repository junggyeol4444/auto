"""
Settings Window GUI
Configuration interface for platform credentials and settings
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import os


class SettingsWindow:
    """Settings Window for Configuration"""
    
    def __init__(self, parent):
        self.parent = parent
        self.config_path = 'config.json'
        self.config = self.load_config()
        
        # Create window
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Settings")
        self.window.geometry("800x600")
        
        self.create_ui()
    
    def load_config(self) -> dict:
        """Load configuration file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save_config(self):
        """Save configuration file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def create_ui(self):
        """Create user interface"""
        # Header
        header = ctk.CTkLabel(
            self.window,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.pack(pady=20)
        
        # Tabview for different settings
        self.tabview = ctk.CTkTabview(self.window)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create tabs
        self.tabview.add("Instagram")
        self.tabview.add("TikTok")
        self.tabview.add("YouTube")
        self.tabview.add("Twitter")
        self.tabview.add("Facebook")
        self.tabview.add("Pinterest")
        self.tabview.add("Discord")
        self.tabview.add("General")
        
        # Create settings for each platform
        self.create_instagram_settings()
        self.create_tiktok_settings()
        self.create_youtube_settings()
        self.create_twitter_settings()
        self.create_facebook_settings()
        self.create_pinterest_settings()
        self.create_discord_settings()
        self.create_general_settings()
        
        # Save button
        save_btn = ctk.CTkButton(
            self.window,
            text="💾 Save Settings",
            command=self.save_all_settings,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        save_btn.pack(pady=20)
    
    def create_instagram_settings(self):
        """Create Instagram settings"""
        tab = self.tabview.tab("Instagram")
        
        ig_config = self.config.get('platforms', {}).get('instagram', {})
        
        self.ig_enabled = self.create_checkbox(tab, "Enable Instagram", ig_config.get('enabled', False))
        self.ig_username = self.create_entry(tab, "Username:", ig_config.get('username', ''))
        self.ig_password = self.create_entry(tab, "Password:", ig_config.get('password', ''), show="*")
    
    def create_tiktok_settings(self):
        """Create TikTok settings"""
        tab = self.tabview.tab("TikTok")
        
        tt_config = self.config.get('platforms', {}).get('tiktok', {})
        
        self.tt_enabled = self.create_checkbox(tab, "Enable TikTok", tt_config.get('enabled', False))
        self.tt_username = self.create_entry(tab, "Username:", tt_config.get('username', ''))
        self.tt_password = self.create_entry(tab, "Password:", tt_config.get('password', ''), show="*")
        self.tt_headless = self.create_checkbox(tab, "Headless Mode", tt_config.get('headless', False))
    
    def create_youtube_settings(self):
        """Create YouTube settings"""
        tab = self.tabview.tab("YouTube")
        
        yt_config = self.config.get('platforms', {}).get('youtube', {})
        
        self.yt_enabled = self.create_checkbox(tab, "Enable YouTube", yt_config.get('enabled', False))
        
        ctk.CTkLabel(tab, text="Client Secrets File:").pack(anchor="w", padx=20, pady=5)
        file_frame = ctk.CTkFrame(tab)
        file_frame.pack(fill="x", padx=20, pady=5)
        
        self.yt_secrets = ctk.CTkEntry(file_frame, placeholder_text="client_secrets.json")
        self.yt_secrets.pack(side="left", fill="x", expand=True, padx=5)
        self.yt_secrets.insert(0, yt_config.get('client_secrets_file', ''))
        
        browse_btn = ctk.CTkButton(file_frame, text="Browse", width=80, command=self.browse_client_secrets)
        browse_btn.pack(side="right", padx=5)
    
    def create_twitter_settings(self):
        """Create Twitter settings"""
        tab = self.tabview.tab("Twitter")
        
        tw_config = self.config.get('platforms', {}).get('twitter', {})
        
        self.tw_enabled = self.create_checkbox(tab, "Enable Twitter", tw_config.get('enabled', False))
        self.tw_api_key = self.create_entry(tab, "API Key:", tw_config.get('api_key', ''))
        self.tw_api_secret = self.create_entry(tab, "API Secret:", tw_config.get('api_secret', ''), show="*")
        self.tw_access_token = self.create_entry(tab, "Access Token:", tw_config.get('access_token', ''))
        self.tw_access_secret = self.create_entry(tab, "Access Token Secret:", tw_config.get('access_token_secret', ''), show="*")
        self.tw_bearer = self.create_entry(tab, "Bearer Token:", tw_config.get('bearer_token', ''))
    
    def create_facebook_settings(self):
        """Create Facebook settings"""
        tab = self.tabview.tab("Facebook")
        
        fb_config = self.config.get('platforms', {}).get('facebook', {})
        
        self.fb_enabled = self.create_checkbox(tab, "Enable Facebook", fb_config.get('enabled', False))
        self.fb_access_token = self.create_entry(tab, "Access Token:", fb_config.get('access_token', ''))
        self.fb_page_id = self.create_entry(tab, "Page ID:", fb_config.get('page_id', ''))
    
    def create_pinterest_settings(self):
        """Create Pinterest settings"""
        tab = self.tabview.tab("Pinterest")
        
        pin_config = self.config.get('platforms', {}).get('pinterest', {})
        
        self.pin_enabled = self.create_checkbox(tab, "Enable Pinterest", pin_config.get('enabled', False))
        self.pin_access_token = self.create_entry(tab, "Access Token:", pin_config.get('access_token', ''))
        self.pin_board_id = self.create_entry(tab, "Board ID:", pin_config.get('board_id', ''))
    
    def create_discord_settings(self):
        """Create Discord settings"""
        tab = self.tabview.tab("Discord")
        
        dc_config = self.config.get('platforms', {}).get('discord', {})
        
        self.dc_enabled = self.create_checkbox(tab, "Enable Discord", dc_config.get('enabled', False))
        self.dc_webhook = self.create_entry(tab, "Webhook URL:", dc_config.get('webhook_url', ''))
    
    def create_general_settings(self):
        """Create general settings"""
        tab = self.tabview.tab("General")
        
        caption_config = self.config.get('caption_settings', {})
        
        self.use_emoji = self.create_checkbox(tab, "Use Emojis in Captions", caption_config.get('use_emoji', True))
        self.add_cta = self.create_checkbox(tab, "Add Call-to-Action", caption_config.get('add_cta', True))
        
        ctk.CTkLabel(tab, text="Default Caption Template:").pack(anchor="w", padx=20, pady=5)
        self.caption_template = ctk.CTkOptionMenu(
            tab,
            values=["simple", "engaging", "promotional", "informative", "motivational"]
        )
        self.caption_template.pack(fill="x", padx=20, pady=5)
        self.caption_template.set(caption_config.get('default_template', 'simple'))
    
    def create_checkbox(self, parent, text: str, default: bool):
        """Helper to create checkbox"""
        var = ctk.BooleanVar(value=default)
        checkbox = ctk.CTkCheckBox(parent, text=text, variable=var)
        checkbox.pack(anchor="w", padx=20, pady=10)
        return var
    
    def create_entry(self, parent, label: str, default: str, show: str = None):
        """Helper to create labeled entry"""
        ctk.CTkLabel(parent, text=label).pack(anchor="w", padx=20, pady=5)
        entry = ctk.CTkEntry(parent, placeholder_text=label, show=show)
        entry.pack(fill="x", padx=20, pady=5)
        if default:
            entry.insert(0, default)
        return entry
    
    def browse_client_secrets(self):
        """Browse for client secrets file"""
        filename = filedialog.askopenfilename(
            title="Select Client Secrets File",
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            self.yt_secrets.delete(0, "end")
            self.yt_secrets.insert(0, filename)
    
    def save_all_settings(self):
        """Save all settings to config"""
        # Update config
        if 'platforms' not in self.config:
            self.config['platforms'] = {}
        
        # Instagram
        self.config['platforms']['instagram'] = {
            'enabled': self.ig_enabled.get(),
            'username': self.ig_username.get(),
            'password': self.ig_password.get(),
            'session_file': 'cache/sessions/instagram_session.json'
        }
        
        # TikTok
        self.config['platforms']['tiktok'] = {
            'enabled': self.tt_enabled.get(),
            'username': self.tt_username.get(),
            'password': self.tt_password.get(),
            'headless': self.tt_headless.get()
        }
        
        # YouTube
        self.config['platforms']['youtube'] = {
            'enabled': self.yt_enabled.get(),
            'client_secrets_file': self.yt_secrets.get(),
            'credentials_file': 'cache/sessions/youtube_credentials.json'
        }
        
        # Twitter
        self.config['platforms']['twitter'] = {
            'enabled': self.tw_enabled.get(),
            'api_key': self.tw_api_key.get(),
            'api_secret': self.tw_api_secret.get(),
            'access_token': self.tw_access_token.get(),
            'access_token_secret': self.tw_access_secret.get(),
            'bearer_token': self.tw_bearer.get()
        }
        
        # Facebook
        self.config['platforms']['facebook'] = {
            'enabled': self.fb_enabled.get(),
            'access_token': self.fb_access_token.get(),
            'page_id': self.fb_page_id.get()
        }
        
        # Pinterest
        self.config['platforms']['pinterest'] = {
            'enabled': self.pin_enabled.get(),
            'access_token': self.pin_access_token.get(),
            'board_id': self.pin_board_id.get()
        }
        
        # Discord
        self.config['platforms']['discord'] = {
            'enabled': self.dc_enabled.get(),
            'webhook_url': self.dc_webhook.get()
        }
        
        # General settings
        self.config['caption_settings'] = {
            'use_emoji': self.use_emoji.get(),
            'add_cta': self.add_cta.get(),
            'default_template': self.caption_template.get()
        }
        
        # Save to file
        self.save_config()
