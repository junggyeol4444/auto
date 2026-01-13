"""
YouTube thumbnail creation tab
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.thumbnail.template_manager import TemplateManager
from modules.thumbnail.text_overlay import TextOverlay
from modules.thumbnail.face_detect import FaceDetector
from modules.thumbnail.effects import EffectsGenerator
from modules.utils.font_manager import FontManager
from modules.utils.image_utils import resize_image


class ThumbnailTab:
    """YouTube thumbnail creation tab"""
    
    def __init__(self, parent):
        self.parent = parent
        self.uploaded_image = None
        self.current_thumbnails = []
        self.current_version = 0
        
        # Load config
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # Initialize modules
        self.template_manager = TemplateManager()
        self.font_manager = FontManager(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'fonts'))
        self.text_overlay = TextOverlay(self.font_manager)
        self.face_detector = FaceDetector()
        self.effects = EffectsGenerator()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Create main containers
        left_frame = ctk.CTkFrame(self.parent)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        right_frame = ctk.CTkFrame(self.parent)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Left side - Input controls
        self.setup_input_controls(left_frame)
        
        # Right side - Preview
        self.setup_preview(right_frame)
    
    def setup_input_controls(self, parent):
        """Setup input control widgets"""
        # Title
        title_label = ctk.CTkLabel(parent, text="썸네일 제작", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Text input
        ctk.CTkLabel(parent, text="제목:").pack(pady=(10, 0))
        self.title_entry = ctk.CTkEntry(parent, width=400, placeholder_text="썸네일 제목을 입력하세요")
        self.title_entry.pack(pady=5)
        
        # Keyword input
        ctk.CTkLabel(parent, text="강조 단어 (쉼표로 구분):").pack(pady=(10, 0))
        self.keyword_entry = ctk.CTkEntry(parent, width=400, placeholder_text="예: 초간단, 꿀팁, 대박")
        self.keyword_entry.pack(pady=5)
        
        # Image upload button
        self.upload_btn = ctk.CTkButton(parent, text="이미지 업로드", command=self.upload_image, width=400)
        self.upload_btn.pack(pady=10)
        
        # Image preview label
        self.image_label = ctk.CTkLabel(parent, text="이미지가 업로드되지 않음")
        self.image_label.pack(pady=5)
        
        # Genre selection
        ctk.CTkLabel(parent, text="장르:").pack(pady=(10, 0))
        self.genre_var = ctk.StringVar(value="게임")
        self.genre_menu = ctk.CTkOptionMenu(parent, variable=self.genre_var, 
                                           values=self.config['thumbnail']['genres'],
                                           width=400)
        self.genre_menu.pack(pady=5)
        
        # Color scheme selection
        ctk.CTkLabel(parent, text="색상 조합:").pack(pady=(10, 0))
        color_schemes = list(self.config['thumbnail']['color_schemes'].keys())
        self.color_var = ctk.StringVar(value=color_schemes[0])
        self.color_menu = ctk.CTkOptionMenu(parent, variable=self.color_var,
                                           values=color_schemes,
                                           width=400)
        self.color_menu.pack(pady=5)
        
        # Generate button
        self.generate_btn = ctk.CTkButton(parent, text="생성 시작", command=self.generate_thumbnails,
                                         width=400, height=40, font=("Arial", 16, "bold"))
        self.generate_btn.pack(pady=20)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(parent, text="")
        self.progress_label.pack(pady=5)
    
    def setup_preview(self, parent):
        """Setup preview area"""
        # Title
        title_label = ctk.CTkLabel(parent, text="미리보기", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Preview canvas
        self.preview_canvas = ctk.CTkLabel(parent, text="썸네일이 생성되지 않음")
        self.preview_canvas.pack(pady=20, fill="both", expand=True)
        
        # Version control
        version_frame = ctk.CTkFrame(parent)
        version_frame.pack(pady=10)
        
        self.prev_btn = ctk.CTkButton(version_frame, text="◀ 이전", command=self.show_previous,
                                     width=100, state="disabled")
        self.prev_btn.pack(side="left", padx=5)
        
        self.version_label = ctk.CTkLabel(version_frame, text="0 / 0")
        self.version_label.pack(side="left", padx=10)
        
        self.next_btn = ctk.CTkButton(version_frame, text="다음 ▶", command=self.show_next,
                                     width=100, state="disabled")
        self.next_btn.pack(side="left", padx=5)
        
        # Action buttons
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(pady=10)
        
        self.save_btn = ctk.CTkButton(button_frame, text="저장", command=self.save_current,
                                     width=150, state="disabled")
        self.save_btn.pack(side="left", padx=5)
        
        self.save_all_btn = ctk.CTkButton(button_frame, text="모두 저장", command=self.save_all,
                                         width=150, state="disabled")
        self.save_all_btn.pack(side="left", padx=5)
    
    def upload_image(self):
        """Handle image upload"""
        file_path = filedialog.askopenfilename(
            title="이미지 선택",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if file_path:
            try:
                self.uploaded_image = Image.open(file_path)
                self.image_label.configure(text=f"업로드됨: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("오류", f"이미지를 불러올 수 없습니다: {e}")
    
    def generate_thumbnails(self):
        """Generate thumbnail variations"""
        title = self.title_entry.get().strip()
        
        if not title:
            messagebox.showwarning("경고", "제목을 입력해주세요")
            return
        
        if not self.uploaded_image:
            messagebox.showwarning("경고", "이미지를 업로드해주세요")
            return
        
        self.progress_label.configure(text="썸네일 생성 중...")
        self.generate_btn.configure(state="disabled")
        self.parent.update()
        
        try:
            genre = self.genre_var.get()
            color_scheme = self.color_var.get()
            keywords = [k.strip() for k in self.keyword_entry.get().split(',') if k.strip()]
            
            # Generate A/B test versions
            versions = self.template_manager.generate_ab_test_versions(genre)
            self.current_thumbnails = []
            
            for i, version in enumerate(versions[:9]):  # Limit to 9 versions
                self.progress_label.configure(text=f"생성 중... {i+1}/9")
                self.parent.update()
                
                # Create template
                template = self.template_manager.create_template(
                    version['genre'], 
                    version['color_scheme']
                )
                
                # Process uploaded image
                processed_image = self.face_detector.smart_crop_for_thumbnail(
                    self.uploaded_image, 
                    (1280, 720)
                )
                
                # Paste processed image onto template
                template.paste(processed_image, (0, 0))
                
                # Add text
                if keywords:
                    template = self.text_overlay.highlight_keywords(
                        template, title, keywords, 
                        position=version['text_position'],
                        font_size=80
                    )
                else:
                    template = self.text_overlay.add_text(
                        template, title,
                        position=version['text_position'],
                        font_size=80
                    )
                
                # Add effects based on genre
                if i % 3 == 0:
                    template = self.effects.add_multiple_effects(template, "stars")
                elif i % 3 == 1:
                    template = self.effects.add_multiple_effects(template, "circles")
                else:
                    template = self.effects.add_multiple_effects(template, "sparkles")
                
                self.current_thumbnails.append(template)
            
            # Show first thumbnail
            self.current_version = 0
            self.show_current_thumbnail()
            
            # Enable buttons
            self.prev_btn.configure(state="normal")
            self.next_btn.configure(state="normal")
            self.save_btn.configure(state="normal")
            self.save_all_btn.configure(state="normal")
            
            self.progress_label.configure(text="생성 완료!")
            
        except Exception as e:
            messagebox.showerror("오류", f"썸네일 생성 실패: {e}")
            self.progress_label.configure(text="")
        finally:
            self.generate_btn.configure(state="normal")
    
    def show_current_thumbnail(self):
        """Display current thumbnail"""
        if not self.current_thumbnails:
            return
        
        thumbnail = self.current_thumbnails[self.current_version]
        
        # Resize for preview
        preview_size = (640, 360)
        preview_img = thumbnail.copy()
        preview_img.thumbnail(preview_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(preview_img)
        self.preview_canvas.configure(image=photo, text="")
        self.preview_canvas.image = photo
        
        # Update version label
        self.version_label.configure(text=f"{self.current_version + 1} / {len(self.current_thumbnails)}")
    
    def show_previous(self):
        """Show previous thumbnail"""
        if self.current_version > 0:
            self.current_version -= 1
            self.show_current_thumbnail()
    
    def show_next(self):
        """Show next thumbnail"""
        if self.current_version < len(self.current_thumbnails) - 1:
            self.current_version += 1
            self.show_current_thumbnail()
    
    def save_current(self):
        """Save current thumbnail"""
        if not self.current_thumbnails:
            return
        
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 'output', 'thumbnails')
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"thumbnail_{timestamp}_v{self.current_version + 1}.png"
        filepath = os.path.join(output_dir, filename)
        
        self.current_thumbnails[self.current_version].save(filepath)
        messagebox.showinfo("저장 완료", f"저장됨: {filename}")
    
    def save_all(self):
        """Save all thumbnails"""
        if not self.current_thumbnails:
            return
        
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 'output', 'thumbnails')
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i, thumbnail in enumerate(self.current_thumbnails):
            filename = f"thumbnail_{timestamp}_v{i + 1}.png"
            filepath = os.path.join(output_dir, filename)
            thumbnail.save(filepath)
        
        messagebox.showinfo("저장 완료", f"{len(self.current_thumbnails)}개 파일 저장됨")
