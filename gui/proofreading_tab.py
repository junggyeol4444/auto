"""
Proofreading tab
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.proofreading import GrammarChecker, StyleChecker, ConsistencyChecker


class ProofreadingTab:
    """Tab for proofreading"""
    
    def __init__(self, parent, config, file_handler):
        self.parent = parent
        self.config = config
        self.file_handler = file_handler
        
        self.original_text = ""
        self.errors = []
        
        self.grammar_checker = GrammarChecker()
        self.style_checker = StyleChecker()
        self.consistency_checker = ConsistencyChecker()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create tab widgets"""
        # Main container
        main_container = ctk.CTkFrame(self.parent)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top controls
        control_frame = ctk.CTkFrame(main_container)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        # File upload button
        upload_btn = ctk.CTkButton(
            control_frame,
            text="📁 파일 업로드",
            command=self._load_file
        )
        upload_btn.pack(side="left", padx=5)
        
        # Check options
        self.spell_check_var = ctk.BooleanVar(value=True)
        spell_check = ctk.CTkCheckBox(
            control_frame,
            text="맞춤법",
            variable=self.spell_check_var
        )
        spell_check.pack(side="left", padx=10)
        
        self.grammar_check_var = ctk.BooleanVar(value=True)
        grammar_check = ctk.CTkCheckBox(
            control_frame,
            text="문법",
            variable=self.grammar_check_var
        )
        grammar_check.pack(side="left", padx=10)
        
        self.style_check_var = ctk.BooleanVar(value=True)
        style_check = ctk.CTkCheckBox(
            control_frame,
            text="스타일",
            variable=self.style_check_var
        )
        style_check.pack(side="left", padx=10)
        
        self.consistency_check_var = ctk.BooleanVar(value=True)
        consistency_check = ctk.CTkCheckBox(
            control_frame,
            text="일관성",
            variable=self.consistency_check_var
        )
        consistency_check.pack(side="left", padx=10)
        
        # Check button
        check_btn = ctk.CTkButton(
            control_frame,
            text="✓ 교정 시작",
            command=self._run_proofreading,
            fg_color="green"
        )
        check_btn.pack(side="right", padx=5)
        
        # Text comparison frame
        text_frame = ctk.CTkFrame(main_container)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Original text (left)
        left_frame = ctk.CTkFrame(text_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(left_frame, text="원본", font=("맑은 고딕", 16, "bold")).pack(pady=5)
        self.original_textbox = ctk.CTkTextbox(left_frame)
        self.original_textbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Corrected text (right)
        right_frame = ctk.CTkFrame(text_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        ctk.CTkLabel(right_frame, text="수정본", font=("맑은 고딕", 16, "bold")).pack(pady=5)
        self.corrected_textbox = ctk.CTkTextbox(right_frame)
        self.corrected_textbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Error list (bottom)
        error_frame = ctk.CTkFrame(main_container)
        error_frame.pack(fill="both", padx=10, pady=10)
        
        ctk.CTkLabel(error_frame, text="오류 목록", font=("맑은 고딕", 14, "bold")).pack(pady=5)
        
        self.error_textbox = ctk.CTkTextbox(error_frame, height=150)
        self.error_textbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Save buttons
        button_frame = ctk.CTkFrame(main_container)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 저장",
            command=self._save_corrected
        )
        save_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        apply_btn = ctk.CTkButton(
            button_frame,
            text="✓ 수정 적용",
            command=self._apply_corrections
        )
        apply_btn.pack(side="left", padx=5, expand=True, fill="x")
    
    def _load_file(self):
        """Load file for proofreading"""
        file_path = filedialog.askopenfilename(
            filetypes=[("텍스트 파일", "*.txt"), ("Word 문서", "*.docx"), ("모든 파일", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            if file_path.endswith('.docx'):
                text = self.file_handler.read_docx(file_path)
            else:
                text = self.file_handler.read_text(file_path)
            
            self.original_text = text
            self.original_textbox.delete("1.0", "end")
            self.original_textbox.insert("1.0", text)
            
            messagebox.showinfo("로드 완료", "파일이 로드되었습니다.")
            
        except Exception as e:
            messagebox.showerror("로드 오류", f"파일을 읽는 중 오류가 발생했습니다:\n{str(e)}")
    
    def _run_proofreading(self):
        """Run proofreading checks"""
        text = self.original_textbox.get("1.0", "end-1c").strip()
        
        if not text:
            messagebox.showwarning("경고", "교정할 텍스트를 입력하거나 파일을 업로드하세요.")
            return
        
        self.original_text = text
        self.errors = []
        
        # Run selected checks
        try:
            if self.grammar_check_var.get():
                self.errors.extend(self.grammar_checker.check_all(text))
            
            if self.style_check_var.get():
                self.errors.extend(self.style_checker.check_all(text))
            
            if self.consistency_check_var.get():
                self.errors.extend(self.consistency_checker.check_all(text))
            
            # Display errors
            self._display_errors()
            
            # Generate corrected version
            corrected = self._generate_corrected_text(text)
            self.corrected_textbox.delete("1.0", "end")
            self.corrected_textbox.insert("1.0", corrected)
            
            messagebox.showinfo("완료", f"교정이 완료되었습니다.\n발견된 오류: {len(self.errors)}개")
            
        except Exception as e:
            messagebox.showerror("오류", f"교정 중 오류가 발생했습니다:\n{str(e)}")
    
    def _display_errors(self):
        """Display error list"""
        self.error_textbox.delete("1.0", "end")
        
        if not self.errors:
            self.error_textbox.insert("1.0", "발견된 오류가 없습니다.")
            return
        
        error_text = []
        for i, error in enumerate(self.errors[:50], 1):  # Limit to 50 errors
            error_type = error.get('type', 'unknown')
            message = error.get('message', '오류')
            
            if 'original' in error and 'corrected' in error:
                error_text.append(f"{i}. [{error_type}] {message}")
                error_text.append(f"   원본: {error['original']}")
                error_text.append(f"   수정: {error['corrected']}\n")
            else:
                error_text.append(f"{i}. [{error_type}] {message}\n")
        
        if len(self.errors) > 50:
            error_text.append(f"\n... 외 {len(self.errors) - 50}개의 오류")
        
        self.error_textbox.insert("1.0", '\n'.join(error_text))
    
    def _generate_corrected_text(self, text):
        """Generate corrected version of text"""
        corrected = text
        
        # Apply corrections
        for error in self.errors:
            if 'original' in error and 'corrected' in error:
                corrected = corrected.replace(error['original'], error['corrected'])
        
        return corrected
    
    def _apply_corrections(self):
        """Apply corrections to original text"""
        corrected = self.corrected_textbox.get("1.0", "end-1c")
        self.original_textbox.delete("1.0", "end")
        self.original_textbox.insert("1.0", corrected)
        messagebox.showinfo("적용 완료", "수정사항이 원본에 적용되었습니다.")
    
    def _save_corrected(self):
        """Save corrected text"""
        text = self.corrected_textbox.get("1.0", "end-1c")
        
        if not text.strip():
            messagebox.showwarning("경고", "저장할 내용이 없습니다.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("텍스트 파일", "*.txt"), ("Word 문서", "*.docx")]
        )
        
        if not file_path:
            return
        
        try:
            if file_path.endswith('.docx'):
                self.file_handler.write_docx(file_path, text)
            else:
                self.file_handler.write_text(file_path, text)
            
            messagebox.showinfo("저장 완료", f"파일이 저장되었습니다:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("저장 오류", f"파일 저장 중 오류가 발생했습니다:\n{str(e)}")
