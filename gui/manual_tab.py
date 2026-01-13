"""
Manual generation tab
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.manual import TemplateManager, StructureGenerator, FAQGenerator


class ManualTab:
    """Tab for manual generation"""
    
    def __init__(self, parent, config, file_handler):
        self.parent = parent
        self.config = config
        self.file_handler = file_handler
        
        self.current_manual = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create tab widgets"""
        # Main container
        main_container = ctk.CTkFrame(self.parent)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel for input
        left_panel = ctk.CTkFrame(main_container)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Title
        title_label = ctk.CTkLabel(left_panel, text="매뉴얼 생성", font=("맑은 고딕", 20, "bold"))
        title_label.pack(pady=10)
        
        # Manual type
        type_frame = ctk.CTkFrame(left_panel)
        type_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(type_frame, text="유형:").pack(side="left", padx=5)
        self.manual_type_var = ctk.StringVar(value="제품")
        type_menu = ctk.CTkOptionMenu(
            type_frame,
            values=["제품", "소프트웨어"],
            variable=self.manual_type_var
        )
        type_menu.pack(side="left", padx=5, fill="x", expand=True)
        
        # Product/Software name
        name_frame = ctk.CTkFrame(left_panel)
        name_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(name_frame, text="제품명:").pack(side="left", padx=5)
        self.name_entry = ctk.CTkEntry(name_frame, placeholder_text="제품/소프트웨어 이름")
        self.name_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Version (for software)
        version_frame = ctk.CTkFrame(left_panel)
        version_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(version_frame, text="버전:").pack(side="left", padx=5)
        self.version_entry = ctk.CTkEntry(version_frame, placeholder_text="예: 1.0.0 (소프트웨어만)")
        self.version_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Features
        features_frame = ctk.CTkFrame(left_panel)
        features_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(features_frame, text="주요 기능 (한 줄에 하나씩):").pack(anchor="w", padx=5, pady=5)
        self.features_text = ctk.CTkTextbox(features_frame, height=100)
        self.features_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Instructions/Functions
        instructions_frame = ctk.CTkFrame(left_panel)
        instructions_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(instructions_frame, text="사용 방법/기능 설명:").pack(anchor="w", padx=5, pady=5)
        self.instructions_text = ctk.CTkTextbox(instructions_frame, height=100)
        self.instructions_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            left_panel,
            text="📋 매뉴얼 생성",
            command=self._generate_manual,
            height=40,
            font=("맑은 고딕", 14, "bold")
        )
        self.generate_btn.pack(pady=10, padx=10, fill="x")
        
        # Progress label
        self.progress_label = ctk.CTkLabel(left_panel, text="")
        self.progress_label.pack(pady=5)
        
        # Right panel for preview
        right_panel = ctk.CTkFrame(main_container)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Preview title
        preview_title = ctk.CTkLabel(right_panel, text="매뉴얼 미리보기", font=("맑은 고딕", 20, "bold"))
        preview_title.pack(pady=10)
        
        # Preview text
        self.preview_text = ctk.CTkTextbox(right_panel)
        self.preview_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Save buttons
        button_frame = ctk.CTkFrame(right_panel)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        save_docx_btn = ctk.CTkButton(
            button_frame,
            text="💾 DOCX 저장",
            command=lambda: self._save_manual('docx')
        )
        save_docx_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        save_txt_btn = ctk.CTkButton(
            button_frame,
            text="💾 TXT 저장",
            command=lambda: self._save_manual('txt')
        )
        save_txt_btn.pack(side="left", padx=5, expand=True, fill="x")
    
    def _generate_manual(self):
        """Generate manual"""
        # Get inputs
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("입력 오류", "제품/소프트웨어 이름을 입력해주세요.")
            return
        
        manual_type = self.manual_type_var.get()
        version = self.version_entry.get().strip() or "1.0.0"
        features = self.features_text.get("1.0", "end-1c").strip()
        instructions = self.instructions_text.get("1.0", "end-1c").strip()
        
        # Update UI
        self.generate_btn.configure(state="disabled")
        self.progress_label.configure(text="매뉴얼 생성 중...")
        self.parent.update()
        
        try:
            # Get template
            if manual_type == "제품":
                template_path = os.path.join(
                    os.path.dirname(__file__), '..', 'templates', 'manual', 'product.json'
                )
            else:
                template_path = os.path.join(
                    os.path.dirname(__file__), '..', 'templates', 'manual', 'software.json'
                )
            
            template_manager = TemplateManager(template_path)
            structure_gen = StructureGenerator(template_manager)
            
            # Generate manual structure
            if manual_type == "제품":
                self.current_manual = structure_gen.generate_product_manual(
                    name, "제품", features, instructions
                )
            else:
                self.current_manual = structure_gen.generate_software_manual(
                    name, version, features, instructions
                )
            
            # Display preview
            preview = self._format_manual_preview(self.current_manual)
            self.preview_text.delete("1.0", "end")
            self.preview_text.insert("1.0", preview)
            
            self.progress_label.configure(text="✅ 생성 완료!")
            messagebox.showinfo("완료", "매뉴얼이 성공적으로 생성되었습니다!")
            
        except Exception as e:
            messagebox.showerror("오류", f"매뉴얼 생성 중 오류가 발생했습니다:\n{str(e)}")
            self.progress_label.configure(text="❌ 생성 실패")
        
        finally:
            self.generate_btn.configure(state="normal")
    
    def _format_manual_preview(self, manual):
        """Format manual for preview"""
        lines = []
        
        # Title
        lines.append(manual['title'])
        lines.append("=" * len(manual['title']))
        lines.append("")
        
        # Sections
        for section in manual['sections']:
            lines.append("")
            lines.append(section['title'])
            lines.append("-" * len(section['title']))
            lines.append("")
            
            # Section content
            if 'content' in section:
                lines.append(section['content'])
                lines.append("")
            
            # Subsections
            if 'subsections' in section:
                for subsection in section['subsections']:
                    if isinstance(subsection, dict):
                        lines.append("")
                        lines.append(f"  {subsection.get('title', '')}")
                        lines.append(f"  {subsection.get('content', '')}")
                    else:
                        lines.append(f"  • {subsection}")
                lines.append("")
        
        return '\n'.join(lines)
    
    def _save_manual(self, format_type):
        """Save generated manual"""
        if not self.current_manual:
            messagebox.showwarning("경고", "저장할 매뉴얼이 없습니다.")
            return
        
        # Ask for file location
        if format_type == 'docx':
            file_path = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word 문서", "*.docx")],
                initialfile=f"{self.current_manual['title']}.docx"
            )
        else:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("텍스트 파일", "*.txt")],
                initialfile=f"{self.current_manual['title']}.txt"
            )
        
        if not file_path:
            return
        
        try:
            if format_type == 'docx':
                self.file_handler.write_manual_docx(
                    file_path,
                    self.current_manual['title'],
                    self.current_manual['sections']
                )
            else:
                # Save as text
                preview = self._format_manual_preview(self.current_manual)
                self.file_handler.write_text(file_path, preview)
            
            messagebox.showinfo("저장 완료", f"매뉴얼이 저장되었습니다:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("저장 오류", f"파일 저장 중 오류가 발생했습니다:\n{str(e)}")
