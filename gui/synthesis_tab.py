"""
Photo synthesis tab
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

from modules.photo_synthesis.background_remover import BackgroundRemover
from modules.photo_synthesis.background_replacer import BackgroundReplacer
from modules.photo_synthesis.face_swap import FaceSwapper
from modules.photo_synthesis.collage import CollageCreator
from modules.photo_synthesis.color_grading import ColorGrading
from modules.photo_synthesis.shadow_reflection import ShadowReflection


class SynthesisTab:
    """Photo synthesis tab"""
    
    def __init__(self, parent):
        self.parent = parent
        self.uploaded_images = []
        self.result_image = None
        
        # Load config
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # Initialize modules
        self.bg_remover = BackgroundRemover()
        self.bg_replacer = BackgroundReplacer()
        self.face_swapper = FaceSwapper()
        self.collage_creator = CollageCreator()
        self.color_grading = ColorGrading()
        self.shadow_reflection = ShadowReflection()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Create main containers
        left_frame = ctk.CTkFrame(self.parent)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        right_frame = ctk.CTkFrame(self.parent)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Left side - Controls
        self.setup_controls(left_frame)
        
        # Right side - Preview
        self.setup_preview(right_frame)
    
    def setup_controls(self, parent):
        """Setup control widgets"""
        # Title
        title_label = ctk.CTkLabel(parent, text="사진 합성", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Function selector
        ctk.CTkLabel(parent, text="기능 선택:").pack(pady=(10, 0))
        self.function_var = ctk.StringVar(value="배경 제거")
        functions = ["배경 제거", "배경 교체", "얼굴 합성", "콜라주", "색감 통일"]
        self.function_menu = ctk.CTkOptionMenu(parent, variable=self.function_var,
                                              values=functions,
                                              command=self.on_function_change,
                                              width=400)
        self.function_menu.pack(pady=5)
        
        # Upload buttons
        self.upload_single_btn = ctk.CTkButton(parent, text="이미지 업로드", 
                                              command=self.upload_single_image, width=400)
        self.upload_single_btn.pack(pady=10)
        
        self.upload_multiple_btn = ctk.CTkButton(parent, text="여러 이미지 업로드",
                                                command=self.upload_multiple_images, width=400)
        self.upload_multiple_btn.pack(pady=5)
        self.upload_multiple_btn.pack_forget()  # Hide initially
        
        # Image info label
        self.image_info_label = ctk.CTkLabel(parent, text="이미지가 업로드되지 않음")
        self.image_info_label.pack(pady=5)
        
        # Options frame (dynamic based on function)
        self.options_frame = ctk.CTkFrame(parent)
        self.options_frame.pack(pady=10, fill="both", expand=True)
        
        self.update_options_ui()
        
        # Process button
        self.process_btn = ctk.CTkButton(parent, text="처리 시작", command=self.process_image,
                                        width=400, height=40, font=("Arial", 16, "bold"))
        self.process_btn.pack(pady=20)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(parent, text="")
        self.progress_label.pack(pady=5)
    
    def setup_preview(self, parent):
        """Setup preview area"""
        # Title
        title_label = ctk.CTkLabel(parent, text="결과 미리보기", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Preview canvas
        self.preview_canvas = ctk.CTkLabel(parent, text="처리된 이미지가 없음")
        self.preview_canvas.pack(pady=20, fill="both", expand=True)
        
        # Save button
        self.save_btn = ctk.CTkButton(parent, text="저장", command=self.save_result,
                                     width=300, state="disabled")
        self.save_btn.pack(pady=10)
    
    def on_function_change(self, choice):
        """Handle function selection change"""
        self.update_options_ui()
        
        # Show/hide multiple upload button
        if choice in ["콜라주", "색감 통일"]:
            self.upload_multiple_btn.pack(pady=5)
        else:
            self.upload_multiple_btn.pack_forget()
    
    def update_options_ui(self):
        """Update options UI based on selected function"""
        # Clear existing widgets
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        function = self.function_var.get()
        
        if function == "배경 제거":
            ctk.CTkLabel(self.options_frame, text="배경을 자동으로 제거합니다").pack(pady=10)
        
        elif function == "배경 교체":
            ctk.CTkLabel(self.options_frame, text="배경 종류:").pack(pady=(10, 0))
            self.bg_type_var = ctk.StringVar(value="단색")
            ctk.CTkOptionMenu(self.options_frame, variable=self.bg_type_var,
                            values=["단색", "그라데이션"],
                            width=300).pack(pady=5)
            
            ctk.CTkLabel(self.options_frame, text="배경 색상:").pack(pady=(10, 0))
            colors = list(self.config['synthesis']['background_colors'].keys())
            self.bg_color_var = ctk.StringVar(value=colors[0])
            ctk.CTkOptionMenu(self.options_frame, variable=self.bg_color_var,
                            values=colors, width=300).pack(pady=5)
        
        elif function == "얼굴 합성":
            ctk.CTkLabel(self.options_frame, 
                        text="소스 이미지(얼굴을 가져올)를 먼저 업로드하고\n타겟 이미지를 두번째로 업로드하세요").pack(pady=10)
        
        elif function == "콜라주":
            ctk.CTkLabel(self.options_frame, text="그리드 크기:").pack(pady=(10, 0))
            self.grid_var = ctk.StringVar(value="2x2")
            ctk.CTkOptionMenu(self.options_frame, variable=self.grid_var,
                            values=["2x2", "3x3", "2x3", "3x2"],
                            width=300).pack(pady=5)
            
            ctk.CTkLabel(self.options_frame, text="간격 (픽셀):").pack(pady=(10, 0))
            self.spacing_var = ctk.StringVar(value="10")
            ctk.CTkEntry(self.options_frame, textvariable=self.spacing_var,
                        width=300).pack(pady=5)
        
        elif function == "색감 통일":
            ctk.CTkLabel(self.options_frame, text="필터:").pack(pady=(10, 0))
            filters = self.config['synthesis']['filters']
            self.filter_var = ctk.StringVar(value=filters[0])
            ctk.CTkOptionMenu(self.options_frame, variable=self.filter_var,
                            values=filters, width=300).pack(pady=5)
    
    def upload_single_image(self):
        """Upload single image"""
        file_path = filedialog.askopenfilename(
            title="이미지 선택",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if file_path:
            try:
                image = Image.open(file_path)
                self.uploaded_images = [image]
                self.image_info_label.configure(text=f"업로드됨: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("오류", f"이미지를 불러올 수 없습니다: {e}")
    
    def upload_multiple_images(self):
        """Upload multiple images"""
        file_paths = filedialog.askopenfilenames(
            title="이미지 선택 (여러 개)",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if file_paths:
            try:
                self.uploaded_images = [Image.open(fp) for fp in file_paths]
                self.image_info_label.configure(text=f"{len(self.uploaded_images)}개 이미지 업로드됨")
            except Exception as e:
                messagebox.showerror("오류", f"이미지를 불러올 수 없습니다: {e}")
    
    def process_image(self):
        """Process image based on selected function"""
        if not self.uploaded_images:
            messagebox.showwarning("경고", "이미지를 업로드해주세요")
            return
        
        function = self.function_var.get()
        self.progress_label.configure(text="처리 중...")
        self.process_btn.configure(state="disabled")
        self.parent.update()
        
        try:
            if function == "배경 제거":
                self.result_image = self.bg_remover.remove_background(self.uploaded_images[0])
            
            elif function == "배경 교체":
                # First remove background
                fg_image = self.bg_remover.remove_background(self.uploaded_images[0])
                
                # Then replace
                bg_type = self.bg_type_var.get()
                bg_color = self.config['synthesis']['background_colors'][self.bg_color_var.get()]
                
                if bg_type == "단색":
                    self.result_image = self.bg_replacer.replace_with_color(fg_image, bg_color)
                else:  # 그라데이션
                    self.result_image = self.bg_replacer.replace_with_gradient(
                        fg_image, bg_color, "#FFFFFF"
                    )
            
            elif function == "얼굴 합성":
                if len(self.uploaded_images) < 2:
                    messagebox.showwarning("경고", "두 개의 이미지를 업로드해주세요")
                    return
                
                self.result_image = self.face_swapper.swap_faces(
                    self.uploaded_images[0], self.uploaded_images[1]
                )
                
                if self.result_image is None:
                    messagebox.showerror("오류", "얼굴을 찾을 수 없습니다")
                    return
            
            elif function == "콜라주":
                if not self.uploaded_images:
                    messagebox.showwarning("경고", "이미지를 업로드해주세요")
                    return
                
                grid_str = self.grid_var.get()
                rows, cols = map(int, grid_str.split('x'))
                spacing = int(self.spacing_var.get())
                
                self.result_image = self.collage_creator.create_grid_collage(
                    self.uploaded_images, (rows, cols), spacing=spacing
                )
            
            elif function == "색감 통일":
                if not self.uploaded_images:
                    messagebox.showwarning("경고", "이미지를 업로드해주세요")
                    return
                
                filter_name = self.filter_var.get()
                
                if filter_name == "original":
                    # Just create collage
                    self.result_image = self.collage_creator.create_grid_collage(
                        self.uploaded_images, (2, 2)
                    )
                else:
                    # Apply filter to all
                    filtered = [self.color_grading.apply_filter(img, filter_name) 
                              for img in self.uploaded_images]
                    self.result_image = self.collage_creator.create_grid_collage(
                        filtered, (2, 2)
                    )
            
            # Show result
            self.show_result()
            self.progress_label.configure(text="처리 완료!")
            self.save_btn.configure(state="normal")
            
        except Exception as e:
            messagebox.showerror("오류", f"처리 실패: {e}")
            self.progress_label.configure(text="")
        finally:
            self.process_btn.configure(state="normal")
    
    def show_result(self):
        """Display result image"""
        if not self.result_image:
            return
        
        # Resize for preview
        preview_img = self.result_image.copy()
        preview_img.thumbnail((640, 480), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(preview_img)
        self.preview_canvas.configure(image=photo, text="")
        self.preview_canvas.image = photo
    
    def save_result(self):
        """Save result image"""
        if not self.result_image:
            return
        
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 'output', 'synthesis')
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        function = self.function_var.get().replace(" ", "_")
        filename = f"{function}_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        
        self.result_image.save(filepath)
        messagebox.showinfo("저장 완료", f"저장됨: {filename}")
