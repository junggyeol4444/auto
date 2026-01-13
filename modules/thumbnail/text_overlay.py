"""
Text overlay functionality for thumbnails
"""
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, List, Optional
import re


class TextOverlay:
    """Handle text overlay on thumbnails"""
    
    def __init__(self, font_manager):
        self.font_manager = font_manager
    
    def add_text(self, image: Image.Image, text: str, position: str = "center", 
                 font_size: int = 60, color: str = "#FFFFFF", 
                 outline: bool = True, outline_color: str = "#000000",
                 outline_width: int = 3, shadow: bool = True) -> Image.Image:
        """
        Add text to image
        
        Args:
            image: PIL Image object
            text: Text to add
            position: Position ("top", "center", "bottom")
            font_size: Font size in pixels
            color: Text color
            outline: Whether to add outline
            outline_color: Outline color
            outline_width: Outline width in pixels
            shadow: Whether to add shadow
        
        Returns:
            PIL Image with text
        """
        draw = ImageDraw.Draw(image)
        font = self.font_manager.get_korean_font(font_size)
        
        # Calculate text position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (image.width - text_width) // 2
        
        if position == "top":
            y = image.height // 6
        elif position == "bottom":
            y = image.height - image.height // 4
        else:  # center
            y = (image.height - text_height) // 2
        
        # Draw shadow
        if shadow:
            shadow_offset = 5
            draw.text((x + shadow_offset, y + shadow_offset), text, 
                     font=font, fill=(0, 0, 0, 128))
        
        # Draw outline
        if outline:
            for adj_x in range(-outline_width, outline_width + 1):
                for adj_y in range(-outline_width, outline_width + 1):
                    if adj_x != 0 or adj_y != 0:
                        draw.text((x + adj_x, y + adj_y), text, 
                                font=font, fill=outline_color)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=color)
        
        return image
    
    def add_multi_line_text(self, image: Image.Image, text: str, position: str = "center",
                           font_size: int = 60, color: str = "#FFFFFF",
                           line_spacing: int = 10, max_width: int = None) -> Image.Image:
        """
        Add multi-line text to image
        
        Args:
            image: PIL Image object
            text: Text to add (use \n for line breaks)
            position: Position ("top", "center", "bottom")
            font_size: Font size in pixels
            color: Text color
            line_spacing: Spacing between lines
            max_width: Maximum width for text wrapping
        
        Returns:
            PIL Image with text
        """
        draw = ImageDraw.Draw(image)
        font = self.font_manager.get_korean_font(font_size)
        
        if max_width:
            # Wrap text
            lines = self._wrap_text(text, font, max_width, draw)
        else:
            lines = text.split('\n')
        
        # Calculate total height
        total_height = 0
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            total_height += (bbox[3] - bbox[1]) + line_spacing
        
        # Starting y position
        if position == "top":
            y = image.height // 6
        elif position == "bottom":
            y = image.height - image.height // 4 - total_height
        else:  # center
            y = (image.height - total_height) // 2
        
        # Draw each line
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (image.width - text_width) // 2
            
            # Draw outline
            for adj_x in range(-3, 4):
                for adj_y in range(-3, 4):
                    if adj_x != 0 or adj_y != 0:
                        draw.text((x + adj_x, y + adj_y), line, 
                                font=font, fill="#000000")
            
            # Draw main text
            draw.text((x, y), line, font=font, fill=color)
            
            y += text_height + line_spacing
        
        return image
    
    def highlight_keywords(self, image: Image.Image, text: str, keywords: List[str],
                          position: str = "center", font_size: int = 60,
                          normal_color: str = "#FFFFFF", highlight_color: str = "#FF0000") -> Image.Image:
        """
        Add text with highlighted keywords
        
        Args:
            image: PIL Image object
            text: Full text
            keywords: List of keywords to highlight
            position: Position ("top", "center", "bottom")
            font_size: Font size in pixels
            normal_color: Normal text color
            highlight_color: Highlight color for keywords
        
        Returns:
            PIL Image with text
        """
        draw = ImageDraw.Draw(image)
        font = self.font_manager.get_korean_font(font_size)
        
        # Split text into segments
        segments = []
        current_pos = 0
        text_lower = text.lower()
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            idx = text_lower.find(keyword_lower, current_pos)
            if idx != -1:
                # Add text before keyword
                if idx > current_pos:
                    segments.append((text[current_pos:idx], normal_color))
                # Add keyword
                segments.append((text[idx:idx + len(keyword)], highlight_color))
                current_pos = idx + len(keyword)
        
        # Add remaining text
        if current_pos < len(text):
            segments.append((text[current_pos:], normal_color))
        
        # Calculate total width
        total_width = sum(draw.textbbox((0, 0), seg[0], font=font)[2] - 
                         draw.textbbox((0, 0), seg[0], font=font)[0] for seg in segments)
        
        # Calculate position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_height = bbox[3] - bbox[1]
        
        x = (image.width - total_width) // 2
        
        if position == "top":
            y = image.height // 6
        elif position == "bottom":
            y = image.height - image.height // 4
        else:  # center
            y = (image.height - text_height) // 2
        
        # Draw each segment
        current_x = x
        for segment_text, segment_color in segments:
            # Draw outline
            for adj_x in range(-3, 4):
                for adj_y in range(-3, 4):
                    if adj_x != 0 or adj_y != 0:
                        draw.text((current_x + adj_x, y + adj_y), segment_text,
                                font=font, fill="#000000")
            
            # Draw text
            draw.text((current_x, y), segment_text, font=font, fill=segment_color)
            
            bbox = draw.textbbox((0, 0), segment_text, font=font)
            current_x += bbox[2] - bbox[0]
        
        return image
    
    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, 
                   max_width: int, draw: ImageDraw.ImageDraw) -> List[str]:
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
