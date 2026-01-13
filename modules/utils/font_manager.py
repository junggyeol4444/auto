"""
Font management for the AI Design Automation Suite
"""
import os
import platform
from PIL import ImageFont
from typing import List, Optional


class FontManager:
    """Manage fonts for text rendering"""
    
    def __init__(self, custom_fonts_dir: Optional[str] = None):
        self.custom_fonts_dir = custom_fonts_dir
        self.system_fonts = self._get_system_fonts()
    
    def _get_system_fonts(self) -> List[str]:
        """Get list of system font paths"""
        fonts = []
        system = platform.system()
        
        if system == "Windows":
            font_dirs = [
                "C:\\Windows\\Fonts",
                os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\Fonts")
            ]
        elif system == "Darwin":  # macOS
            font_dirs = [
                "/Library/Fonts",
                "/System/Library/Fonts",
                os.path.expanduser("~/Library/Fonts")
            ]
        else:  # Linux
            font_dirs = [
                "/usr/share/fonts",
                "/usr/local/share/fonts",
                os.path.expanduser("~/.fonts")
            ]
        
        for font_dir in font_dirs:
            if os.path.exists(font_dir):
                for root, dirs, files in os.walk(font_dir):
                    for file in files:
                        if file.lower().endswith(('.ttf', '.otf', '.ttc')):
                            fonts.append(os.path.join(root, file))
        
        return fonts
    
    def get_font(self, font_name: Optional[str] = None, size: int = 40, bold: bool = False) -> ImageFont.FreeTypeFont:
        """
        Get a font object
        
        Args:
            font_name: Font name or None for default
            size: Font size in pixels
            bold: Whether to use bold variant
        
        Returns:
            PIL ImageFont object
        """
        # Try custom fonts first
        if self.custom_fonts_dir and os.path.exists(self.custom_fonts_dir):
            custom_fonts = [f for f in os.listdir(self.custom_fonts_dir) 
                          if f.lower().endswith(('.ttf', '.otf'))]
            if custom_fonts:
                font_path = os.path.join(self.custom_fonts_dir, custom_fonts[0])
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    pass
        
        # Try to find requested font
        if font_name:
            for font_path in self.system_fonts:
                if font_name.lower() in os.path.basename(font_path).lower():
                    if bold and 'bold' in os.path.basename(font_path).lower():
                        try:
                            return ImageFont.truetype(font_path, size)
                        except:
                            pass
                    elif not bold and 'bold' not in os.path.basename(font_path).lower():
                        try:
                            return ImageFont.truetype(font_path, size)
                        except:
                            pass
        
        # Try common Korean fonts
        korean_fonts = ['malgun', 'gulim', 'batang', 'dotum', 'nanum', 'nanumgothic']
        for korean_font in korean_fonts:
            for font_path in self.system_fonts:
                if korean_font in os.path.basename(font_path).lower():
                    try:
                        return ImageFont.truetype(font_path, size)
                    except:
                        pass
        
        # Try common fonts
        common_fonts = ['arial', 'verdana', 'helvetica', 'times', 'courier']
        for common_font in common_fonts:
            for font_path in self.system_fonts:
                if common_font in os.path.basename(font_path).lower():
                    if bold and 'bold' in os.path.basename(font_path).lower():
                        try:
                            return ImageFont.truetype(font_path, size)
                        except:
                            pass
                    elif not bold:
                        try:
                            return ImageFont.truetype(font_path, size)
                        except:
                            pass
        
        # Fall back to any available font
        if self.system_fonts:
            for font_path in self.system_fonts:
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    pass
        
        # Last resort: default font
        try:
            return ImageFont.load_default()
        except:
            return ImageFont.truetype("arial.ttf", size)
    
    def get_bold_font(self, size: int = 40) -> ImageFont.FreeTypeFont:
        """Get a bold font"""
        return self.get_font(None, size, bold=True)
    
    def get_korean_font(self, size: int = 40) -> ImageFont.FreeTypeFont:
        """Get a Korean-compatible font"""
        korean_fonts = ['malgun', 'gulim', 'nanum', 'nanumgothic', 'batang', 'dotum']
        
        for korean_font in korean_fonts:
            for font_path in self.system_fonts:
                if korean_font in os.path.basename(font_path).lower():
                    try:
                        return ImageFont.truetype(font_path, size)
                    except:
                        pass
        
        # Fallback to any available font
        return self.get_font(None, size)
