"""
Text editor window for advanced editing
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog


class EditorWindow:
    """Standalone text editor window"""
    
    def __init__(self, parent, initial_text="", title="편집기"):
        self.parent = parent
        self.initial_text = initial_text
        
        # Create window
        self.window = ctk.CTkToplevel(parent)
        self.window.title(title)
        self.window.geometry("800x600")
        self.window.transient(parent)
        
        self._create_widgets()
        
        # Load initial text
        if initial_text:
            self.text_widget.insert("1.0", initial_text)
    
    def _create_widgets(self):
        """Create editor widgets"""
        # Toolbar
        toolbar = ctk.CTkFrame(self.window, height=40)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        # Save button
        save_btn = ctk.CTkButton(
            toolbar,
            text="💾 저장",
            width=80,
            command=self._save_file
        )
        save_btn.pack(side="left", padx=5)
        
        # Font size
        ctk.CTkLabel(toolbar, text="글자 크기:").pack(side="left", padx=5)
        self.font_size_var = ctk.StringVar(value="12")
        font_menu = ctk.CTkOptionMenu(
            toolbar,
            values=["10", "12", "14", "16", "18"],
            variable=self.font_size_var,
            command=self._change_font_size,
            width=80
        )
        font_menu.pack(side="left", padx=5)
        
        # Word count
        self.word_count_label = ctk.CTkLabel(toolbar, text="글자 수: 0")
        self.word_count_label.pack(side="right", padx=10)
        
        # Text widget
        text_frame = ctk.CTkFrame(self.window)
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.text_widget = ctk.CTkTextbox(text_frame, font=("맑은 고딕", 12))
        self.text_widget.pack(fill="both", expand=True)
        
        # Bind events
        self.text_widget.bind("<KeyRelease>", self._update_word_count)
        
        # Bottom buttons
        button_frame = ctk.CTkFrame(self.window)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ok_btn = ctk.CTkButton(
            button_frame,
            text="확인",
            command=self._on_ok
        )
        ok_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="취소",
            command=self.window.destroy
        )
        cancel_btn.pack(side="left", padx=5, expand=True, fill="x")
    
    def _change_font_size(self, size):
        """Change font size"""
        try:
            font_size = int(size)
            self.text_widget.configure(font=("맑은 고딕", font_size))
        except:
            pass
    
    def _update_word_count(self, event=None):
        """Update word count"""
        text = self.text_widget.get("1.0", "end-1c")
        count = len(text.replace(" ", "").replace("\n", ""))
        self.word_count_label.configure(text=f"글자 수: {count:,}")
    
    def _save_file(self):
        """Save to file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")]
        )
        
        if file_path:
            try:
                text = self.text_widget.get("1.0", "end-1c")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("저장 완료", "파일이 저장되었습니다.")
            except Exception as e:
                messagebox.showerror("저장 오류", f"파일 저장 실패:\n{str(e)}")
    
    def _on_ok(self):
        """Handle OK button"""
        self.result_text = self.text_widget.get("1.0", "end-1c")
        self.window.destroy()
    
    def get_text(self):
        """Get edited text"""
        return getattr(self, 'result_text', self.initial_text)
