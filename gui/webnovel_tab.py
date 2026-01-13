"""
Web novel generation tab
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.webnovel import WebNovelGenerator


class WebNovelTab:
    """Tab for web novel generation"""
    
    def __init__(self, parent, config, file_handler, api_manager):
        self.parent = parent
        self.config = config
        self.file_handler = file_handler
        self.api_manager = api_manager
        
        self.current_novel = None
        self.templates = {}
        self._load_templates()
        
        self._create_widgets()
    
    def _load_templates(self):
        """Load genre templates"""
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates', 'webnovel')
        
        genres = {
            'fantasy': '판타지',
            'romance': '로맨스',
            'martial_arts': '무협',
            'modern': '현대물'
        }
        
        for key, name in genres.items():
            template_path = os.path.join(template_dir, f'{key}.json')
            if os.path.exists(template_path):
                try:
                    self.templates[name] = self.file_handler.load_json(template_path)
                except:
                    pass
    
    def _create_widgets(self):
        """Create tab widgets"""
        # Main container with scrollbar
        main_container = ctk.CTkFrame(self.parent)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel for input
        left_panel = ctk.CTkFrame(main_container)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Title
        title_label = ctk.CTkLabel(left_panel, text="웹소설 생성", font=("맑은 고딕", 20, "bold"))
        title_label.pack(pady=10)
        
        # Genre selection
        genre_frame = ctk.CTkFrame(left_panel)
        genre_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(genre_frame, text="장르:").pack(side="left", padx=5)
        self.genre_var = ctk.StringVar(value="판타지")
        genre_menu = ctk.CTkOptionMenu(
            genre_frame,
            values=list(self.templates.keys()) if self.templates else ["판타지"],
            variable=self.genre_var
        )
        genre_menu.pack(side="left", padx=5, fill="x", expand=True)
        
        # Title input
        title_frame = ctk.CTkFrame(left_panel)
        title_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(title_frame, text="제목:").pack(side="left", padx=5)
        self.title_entry = ctk.CTkEntry(title_frame, placeholder_text="소설 제목을 입력하세요")
        self.title_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Protagonist name
        protag_frame = ctk.CTkFrame(left_panel)
        protag_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(protag_frame, text="주인공:").pack(side="left", padx=5)
        self.protag_entry = ctk.CTkEntry(protag_frame, placeholder_text="주인공 이름 (선택)")
        self.protag_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Number of chapters
        chapter_frame = ctk.CTkFrame(left_panel)
        chapter_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(chapter_frame, text="회차 수:").pack(side="left", padx=5)
        self.chapter_slider = ctk.CTkSlider(chapter_frame, from_=1, to=20, number_of_steps=19)
        self.chapter_slider.set(5)
        self.chapter_slider.pack(side="left", padx=5, fill="x", expand=True)
        
        self.chapter_label = ctk.CTkLabel(chapter_frame, text="5")
        self.chapter_label.pack(side="left", padx=5)
        self.chapter_slider.configure(command=lambda v: self.chapter_label.configure(text=f"{int(v)}"))
        
        # Chapter length
        length_frame = ctk.CTkFrame(left_panel)
        length_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(length_frame, text="회당 분량:").pack(side="left", padx=5)
        self.length_var = ctk.StringVar(value="4000")
        length_menu = ctk.CTkOptionMenu(
            length_frame,
            values=["3000", "4000", "5000"],
            variable=self.length_var
        )
        length_menu.pack(side="left", padx=5, fill="x", expand=True)
        ctk.CTkLabel(length_frame, text="자").pack(side="left", padx=5)
        
        # Plot summary
        plot_frame = ctk.CTkFrame(left_panel)
        plot_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(plot_frame, text="줄거리 개요 (선택):").pack(anchor="w", padx=5, pady=5)
        self.plot_text = ctk.CTkTextbox(plot_frame, height=100)
        self.plot_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            left_panel,
            text="📝 생성 시작",
            command=self._generate_novel,
            height=40,
            font=("맑은 고딕", 14, "bold")
        )
        self.generate_btn.pack(pady=10, padx=10, fill="x")
        
        # Progress label
        self.progress_label = ctk.CTkLabel(left_panel, text="")
        self.progress_label.pack(pady=5)
        
        # Right panel for output
        right_panel = ctk.CTkFrame(main_container)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Output title
        output_title = ctk.CTkLabel(right_panel, text="생성된 소설", font=("맑은 고딕", 20, "bold"))
        output_title.pack(pady=10)
        
        # Chapter selector
        selector_frame = ctk.CTkFrame(right_panel)
        selector_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(selector_frame, text="회차:").pack(side="left", padx=5)
        self.chapter_select_var = ctk.StringVar(value="1")
        self.chapter_select = ctk.CTkOptionMenu(
            selector_frame,
            values=["1"],
            variable=self.chapter_select_var,
            command=self._display_chapter
        )
        self.chapter_select.pack(side="left", padx=5, fill="x", expand=True)
        
        # Output text
        self.output_text = ctk.CTkTextbox(right_panel)
        self.output_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Action buttons
        button_frame = ctk.CTkFrame(right_panel)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 저장",
            command=self._save_novel
        )
        save_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        regenerate_btn = ctk.CTkButton(
            button_frame,
            text="🔄 다시 생성",
            command=self._generate_novel
        )
        regenerate_btn.pack(side="left", padx=5, expand=True, fill="x")
    
    def _generate_novel(self):
        """Generate web novel"""
        # Get inputs
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("입력 오류", "제목을 입력해주세요.")
            return
        
        genre = self.genre_var.get()
        protagonist = self.protag_entry.get().strip() or None
        num_chapters = int(self.chapter_slider.get())
        chapter_length = int(self.length_var.get())
        plot_summary = self.plot_text.get("1.0", "end-1c").strip() or None
        
        # Get template
        template = self.templates.get(genre)
        if not template:
            messagebox.showerror("오류", "선택한 장르의 템플릿을 찾을 수 없습니다.")
            return
        
        # Update UI
        self.generate_btn.configure(state="disabled")
        self.progress_label.configure(text="소설 생성 중...")
        self.parent.update()
        
        try:
            # Create generator
            generator = WebNovelGenerator(template, self.api_manager)
            
            # Generate novel
            self.current_novel = generator.generate_novel(
                title=title,
                protagonist_name=protagonist,
                num_chapters=num_chapters,
                chapter_length=chapter_length,
                plot_summary=plot_summary
            )
            
            # Update chapter selector
            chapter_numbers = [str(i) for i in range(1, num_chapters + 1)]
            self.chapter_select.configure(values=chapter_numbers)
            self.chapter_select_var.set("1")
            
            # Display first chapter
            self._display_chapter("1")
            
            self.progress_label.configure(text="✅ 생성 완료!")
            messagebox.showinfo("완료", "소설이 성공적으로 생성되었습니다!")
            
        except Exception as e:
            messagebox.showerror("오류", f"소설 생성 중 오류가 발생했습니다:\n{str(e)}")
            self.progress_label.configure(text="❌ 생성 실패")
        
        finally:
            self.generate_btn.configure(state="normal")
    
    def _display_chapter(self, chapter_num):
        """Display selected chapter"""
        if not self.current_novel:
            return
        
        chapter_idx = int(chapter_num) - 1
        if 0 <= chapter_idx < len(self.current_novel['chapters']):
            chapter = self.current_novel['chapters'][chapter_idx]
            
            # Clear and display
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", f"{chapter['title']}\n\n{chapter['content']}")
    
    def _save_novel(self):
        """Save generated novel"""
        if not self.current_novel:
            messagebox.showwarning("경고", "저장할 소설이 없습니다.")
            return
        
        # Ask for file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word 문서", "*.docx"), ("텍스트 파일", "*.txt")],
            initialfile=f"{self.current_novel['title']}.docx"
        )
        
        if not file_path:
            return
        
        try:
            # Prepare chapters
            chapters = [ch['content'] for ch in self.current_novel['chapters']]
            
            if file_path.endswith('.docx'):
                self.file_handler.write_docx(
                    file_path,
                    "",
                    title=self.current_novel['title'],
                    chapters=chapters
                )
            else:
                # Save as text
                full_text = f"{self.current_novel['title']}\n\n"
                for ch in self.current_novel['chapters']:
                    full_text += f"\n\n{ch['title']}\n\n{ch['content']}\n"
                self.file_handler.write_text(file_path, full_text)
            
            messagebox.showinfo("저장 완료", f"소설이 저장되었습니다:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("저장 오류", f"파일 저장 중 오류가 발생했습니다:\n{str(e)}")
