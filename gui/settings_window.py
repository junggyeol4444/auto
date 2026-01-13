"""
Settings window
"""
import customtkinter as ctk
from tkinter import messagebox


class SettingsWindow:
    """Settings configuration window"""
    
    def __init__(self, parent, config, file_handler):
        self.parent = parent
        self.config = config
        self.file_handler = file_handler
        
        # Create dialog
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("설정")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create settings widgets"""
        # Main frame
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(main_frame, text="설정", font=("맑은 고딕", 24, "bold"))
        title.pack(pady=10)
        
        # API Settings
        api_frame = ctk.CTkFrame(main_frame)
        api_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(api_frame, text="API 설정", font=("맑은 고딕", 16, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # Use AI checkbox
        self.use_ai_var = ctk.BooleanVar(value=self.config.get('api', {}).get('use_ai', False))
        use_ai_check = ctk.CTkCheckBox(
            api_frame,
            text="AI API 사용 (고품질 생성)",
            variable=self.use_ai_var
        )
        use_ai_check.pack(anchor="w", padx=20, pady=5)
        
        # OpenAI Key
        openai_frame = ctk.CTkFrame(api_frame)
        openai_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(openai_frame, text="OpenAI API Key:").pack(anchor="w")
        self.openai_entry = ctk.CTkEntry(openai_frame, placeholder_text="sk-...")
        self.openai_entry.insert(0, self.config.get('api', {}).get('openai_key', ''))
        self.openai_entry.pack(fill="x", pady=5)
        
        # Anthropic Key
        anthropic_frame = ctk.CTkFrame(api_frame)
        anthropic_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(anthropic_frame, text="Anthropic API Key:").pack(anchor="w")
        self.anthropic_entry = ctk.CTkEntry(anthropic_frame, placeholder_text="sk-ant-...")
        self.anthropic_entry.insert(0, self.config.get('api', {}).get('anthropic_key', ''))
        self.anthropic_entry.pack(fill="x", pady=5)
        
        # Output Settings
        output_frame = ctk.CTkFrame(main_frame)
        output_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(output_frame, text="출력 설정", font=("맑은 고딕", 16, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # Default format
        format_frame = ctk.CTkFrame(output_frame)
        format_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(format_frame, text="기본 저장 형식:").pack(side="left", padx=5)
        self.format_var = ctk.StringVar(value=self.config.get('output', {}).get('default_format', 'docx'))
        format_menu = ctk.CTkOptionMenu(
            format_frame,
            values=["docx", "txt"],
            variable=self.format_var
        )
        format_menu.pack(side="left", padx=5)
        
        # Webnovel Settings
        webnovel_frame = ctk.CTkFrame(main_frame)
        webnovel_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(webnovel_frame, text="웹소설 설정", font=("맑은 고딕", 16, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # Default chapter length
        length_frame = ctk.CTkFrame(webnovel_frame)
        length_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(length_frame, text="기본 회당 분량:").pack(side="left", padx=5)
        self.length_var = ctk.StringVar(
            value=str(self.config.get('webnovel', {}).get('default_chapter_length', 4000))
        )
        length_menu = ctk.CTkOptionMenu(
            length_frame,
            values=["3000", "4000", "5000"],
            variable=self.length_var
        )
        length_menu.pack(side="left", padx=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=20)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="저장",
            command=self._save_settings,
            fg_color="green"
        )
        save_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="취소",
            command=self.dialog.destroy
        )
        cancel_btn.pack(side="left", padx=5, expand=True, fill="x")
    
    def _save_settings(self):
        """Save settings to config file"""
        try:
            # Update config
            self.config['api']['use_ai'] = self.use_ai_var.get()
            self.config['api']['openai_key'] = self.openai_entry.get().strip()
            self.config['api']['anthropic_key'] = self.anthropic_entry.get().strip()
            self.config['output']['default_format'] = self.format_var.get()
            self.config['webnovel']['default_chapter_length'] = int(self.length_var.get())
            
            # Save to file
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
            self.file_handler.save_json(config_path, self.config)
            
            messagebox.showinfo("저장 완료", "설정이 저장되었습니다.")
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("저장 오류", f"설정 저장 중 오류가 발생했습니다:\n{str(e)}")


import os
