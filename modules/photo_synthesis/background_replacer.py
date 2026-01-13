"""
Background replacement functionality
"""
from PIL import Image, ImageDraw
from typing import Tuple, Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.image_utils import create_gradient


class BackgroundReplacer:
    """Replace image backgrounds"""
    
    def replace_with_color(self, foreground: Image.Image, color: str) -> Image.Image:
        """
        Replace transparent background with solid color
        
        Args:
            foreground: PIL Image with transparent background
            color: Background color (hex or name)
        
        Returns:
            PIL Image with colored background
        """
        # Create background
        background = Image.new('RGB', foreground.size, color)
        
        # Paste foreground
        if foreground.mode == 'RGBA':
            background.paste(foreground, (0, 0), foreground)
        else:
            background.paste(foreground, (0, 0))
        
        return background
    
    def replace_with_gradient(self, foreground: Image.Image, color1: str, color2: str,
                             direction: str = 'vertical') -> Image.Image:
        """
        Replace transparent background with gradient
        
        Args:
            foreground: PIL Image with transparent background
            color1: Start color
            color2: End color
            direction: Gradient direction ('horizontal', 'vertical', 'diagonal')
        
        Returns:
            PIL Image with gradient background
        """
        # Create gradient background
        background = create_gradient(foreground.size, color1, color2, direction)
        
        # Paste foreground
        if foreground.mode == 'RGBA':
            background.paste(foreground, (0, 0), foreground)
        else:
            background.paste(foreground, (0, 0))
        
        return background
    
    def replace_with_image(self, foreground: Image.Image, background_image: Image.Image,
                          scale: str = 'fit') -> Image.Image:
        """
        Replace transparent background with another image
        
        Args:
            foreground: PIL Image with transparent background
            background_image: Background PIL Image
            scale: How to scale background ('fit', 'fill', 'stretch')
        
        Returns:
            PIL Image with custom background
        """
        # Prepare background
        if scale == 'stretch':
            background = background_image.resize(foreground.size, Image.Resampling.LANCZOS)
        elif scale == 'fit':
            background = Image.new('RGB', foreground.size, 'white')
            background_image.thumbnail(foreground.size, Image.Resampling.LANCZOS)
            # Center the background
            x = (foreground.width - background_image.width) // 2
            y = (foreground.height - background_image.height) // 2
            background.paste(background_image, (x, y))
        else:  # fill
            # Scale to fill and crop
            bg_aspect = background_image.width / background_image.height
            fg_aspect = foreground.width / foreground.height
            
            if bg_aspect > fg_aspect:
                # Background is wider
                new_height = foreground.height
                new_width = int(new_height * bg_aspect)
            else:
                # Background is taller
                new_width = foreground.width
                new_height = int(new_width / bg_aspect)
            
            background_image = background_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Center crop
            x = (new_width - foreground.width) // 2
            y = (new_height - foreground.height) // 2
            background = background_image.crop((x, y, x + foreground.width, y + foreground.height))
        
        # Paste foreground
        if foreground.mode == 'RGBA':
            background.paste(foreground, (0, 0), foreground)
        else:
            background.paste(foreground, (0, 0))
        
        return background
    
    def replace_with_blur(self, original: Image.Image, foreground: Image.Image,
                         blur_radius: int = 20) -> Image.Image:
        """
        Replace background with blurred version of original
        
        Args:
            original: Original PIL Image (before background removal)
            foreground: PIL Image with transparent background
            blur_radius: Blur intensity
        
        Returns:
            PIL Image with blurred background
        """
        from PIL import ImageFilter
        
        # Create blurred background
        background = original.copy()
        background = background.filter(ImageFilter.GaussianBlur(blur_radius))
        background = background.resize(foreground.size, Image.Resampling.LANCZOS)
        
        # Paste foreground
        if foreground.mode == 'RGBA':
            background.paste(foreground, (0, 0), foreground)
        else:
            background.paste(foreground, (0, 0))
        
        return background
