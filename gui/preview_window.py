"""
Preview window for viewing results
"""
import customtkinter as ctk
from PIL import Image, ImageTk


class PreviewWindow(ctk.CTkToplevel):
    """Standalone preview window"""
    
    def __init__(self, parent, image: Image.Image, title: str = "미리보기"):
        super().__init__(parent)
        
        self.title(title)
        self.image = image
        
        # Set window size based on image
        max_width = 1200
        max_height = 800
        
        img_width, img_height = image.size
        aspect_ratio = img_width / img_height
        
        if img_width > max_width or img_height > max_height:
            if aspect_ratio > max_width / max_height:
                width = max_width
                height = int(max_width / aspect_ratio)
            else:
                height = max_height
                width = int(max_height * aspect_ratio)
        else:
            width = img_width
            height = img_height
        
        self.geometry(f"{width + 40}x{height + 100}")
        
        # Display image
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        # Image display
        display_img = self.image.copy()
        display_img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(display_img)
        
        image_label = ctk.CTkLabel(self, image=photo, text="")
        image_label.image = photo
        image_label.pack(pady=20)
        
        # Close button
        close_btn = ctk.CTkButton(self, text="닫기", command=self.destroy,
                                 width=200)
        close_btn.pack(pady=10)
