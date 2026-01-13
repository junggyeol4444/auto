"""
Main GUI window
"""
import customtkinter as ctk
from .webnovel_tab import WebNovelTab
from .proofreading_tab import ProofreadingTab
from .manual_tab import ManualTab
from .settings_window import SettingsWindow


class MainWindow:
    """Main application window"""
    
    def __init__(self, config, file_handler, api_manager):
        self.config = config
        self.file_handler = file_handler
        self.api_manager = api_manager
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("AI Writing Assistant Suite")
        self.root.geometry("1200x800")
        
        # Create menu bar
        self._create_menu()
        
        # Create tab view
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self._create_tabs()
    
    def _create_menu(self):
        """Create menu bar"""
        # Create top frame for menu buttons
        menu_frame = ctk.CTkFrame(self.root, height=40)
        menu_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        # Settings button
        settings_btn = ctk.CTkButton(
            menu_frame,
            text="⚙️ 설정",
            width=100,
            command=self._open_settings
        )
        settings_btn.pack(side="right", padx=5, pady=5)
        
        # About button
        about_btn = ctk.CTkButton(
            menu_frame,
            text="ℹ️ 정보",
            width=100,
            command=self._show_about
        )
        about_btn.pack(side="right", padx=5, pady=5)
    
    def _create_tabs(self):
        """Create application tabs"""
        # Web Novel tab
        self.tabview.add("웹소설 대필")
        webnovel_frame = self.tabview.tab("웹소설 대필")
        self.webnovel_tab = WebNovelTab(
            webnovel_frame,
            self.config,
            self.file_handler,
            self.api_manager
        )
        
        # Proofreading tab
        self.tabview.add("소설 교정")
        proofreading_frame = self.tabview.tab("소설 교정")
        self.proofreading_tab = ProofreadingTab(
            proofreading_frame,
            self.config,
            self.file_handler
        )
        
        # Manual tab
        self.tabview.add("매뉴얼 작성")
        manual_frame = self.tabview.tab("매뉴얼 작성")
        self.manual_tab = ManualTab(
            manual_frame,
            self.config,
            self.file_handler
        )
    
    def _open_settings(self):
        """Open settings window"""
        SettingsWindow(self.root, self.config, self.file_handler)
    
    def _show_about(self):
        """Show about dialog"""
        about_text = """AI Writing Assistant Suite
버전: 1.0.0

웹소설 대필, 소설 교정, 매뉴얼 작성을 지원하는
올인원 AI 작문 도우미입니다.

© 2024 All rights reserved.
"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("프로그램 정보")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        label = ctk.CTkLabel(
            dialog,
            text=about_text,
            justify="left"
        )
        label.pack(padx=20, pady=20)
        
        ok_btn = ctk.CTkButton(
            dialog,
            text="확인",
            command=dialog.destroy
        )
        ok_btn.pack(pady=10)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()
