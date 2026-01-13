"""
Template manager for YouTube thumbnails
"""
from PIL import Image, ImageDraw
from typing import Tuple, Dict, List
import random


class TemplateManager:
    """Generate templates for different genres"""
    
    GENRES = {
        "게임": {
            "colors": ["#FF0000", "#00FF00", "#0000FF", "#FFFF00"],
            "style": "bold",
            "effects": ["arrows", "circles"]
        },
        "브이로그": {
            "colors": ["#FFB6C1", "#87CEEB", "#98FB98", "#FAFAD2"],
            "style": "casual",
            "effects": ["stars"]
        },
        "리뷰": {
            "colors": ["#4169E1", "#FFFFFF", "#FFD700", "#000000"],
            "style": "professional",
            "effects": ["circles", "stars"]
        },
        "먹방": {
            "colors": ["#FF6347", "#FFA500", "#FFD700", "#FF69B4"],
            "style": "vibrant",
            "effects": ["sparkles", "circles"]
        },
        "교육": {
            "colors": ["#4169E1", "#FFFFFF", "#32CD32", "#FFD700"],
            "style": "clean",
            "effects": ["arrows"]
        }
    }
    
    COLOR_SCHEMES = {
        "빨강+노랑": {"primary": "#FF0000", "secondary": "#FFFF00", "text": "#FFFFFF"},
        "파랑+흰색": {"primary": "#0066FF", "secondary": "#FFFFFF", "text": "#000000"},
        "검정+금색": {"primary": "#000000", "secondary": "#FFD700", "text": "#FFFFFF"},
        "형광": {"primary": "#00FF00", "secondary": "#FF00FF", "text": "#FFFFFF"}
    }
    
    def __init__(self, size: Tuple[int, int] = (1280, 720)):
        self.size = size
    
    def create_template(self, genre: str, color_scheme: str = None) -> Image.Image:
        """
        Create a template for the specified genre
        
        Args:
            genre: Genre name (게임, 브이로그, 리뷰, 먹방, 교육)
            color_scheme: Optional color scheme name
        
        Returns:
            PIL Image template
        """
        if genre not in self.GENRES:
            genre = "게임"
        
        template = Image.new('RGB', self.size, 'white')
        draw = ImageDraw.Draw(template)
        
        if color_scheme and color_scheme in self.COLOR_SCHEMES:
            colors = self.COLOR_SCHEMES[color_scheme]
            primary = colors["primary"]
            secondary = colors["secondary"]
        else:
            genre_colors = self.GENRES[genre]["colors"]
            primary = genre_colors[0]
            secondary = genre_colors[1] if len(genre_colors) > 1 else genre_colors[0]
        
        # Create gradient background
        r1, g1, b1 = self._hex_to_rgb(primary)
        r2, g2, b2 = self._hex_to_rgb(secondary)
        
        # Use numpy for efficient gradient generation
        import numpy as np
        y_range = np.linspace(0, 1, self.size[1])
        
        for y in range(self.size[1]):
            # Linear interpolation
            ratio = y_range[y]
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            draw.line([(0, y), (self.size[0], y)], fill=(r, g, b))
        
        return template
    
    def create_split_template(self, genre: str, color_scheme: str = None) -> Image.Image:
        """
        Create a split-screen template
        
        Args:
            genre: Genre name
            color_scheme: Optional color scheme name
        
        Returns:
            PIL Image template
        """
        template = Image.new('RGB', self.size, 'white')
        draw = ImageDraw.Draw(template)
        
        if color_scheme and color_scheme in self.COLOR_SCHEMES:
            colors = self.COLOR_SCHEMES[color_scheme]
            primary = colors["primary"]
            secondary = colors["secondary"]
        else:
            genre_colors = self.GENRES[genre]["colors"]
            primary = genre_colors[0]
            secondary = genre_colors[1] if len(genre_colors) > 1 else genre_colors[0]
        
        # Left side
        draw.rectangle([(0, 0), (self.size[0] // 2, self.size[1])], fill=primary)
        
        # Right side
        draw.rectangle([(self.size[0] // 2, 0), (self.size[0], self.size[1])], fill=secondary)
        
        return template
    
    def create_border_template(self, genre: str, border_width: int = 20) -> Image.Image:
        """
        Create template with border
        
        Args:
            genre: Genre name
            border_width: Border width in pixels
        
        Returns:
            PIL Image template
        """
        template = Image.new('RGB', self.size, 'white')
        draw = ImageDraw.Draw(template)
        
        genre_colors = self.GENRES.get(genre, self.GENRES["게임"])["colors"]
        border_color = genre_colors[0]
        bg_color = genre_colors[1] if len(genre_colors) > 1 else "#FFFFFF"
        
        # Draw border
        draw.rectangle([(0, 0), (self.size[0], self.size[1])], fill=border_color)
        
        # Draw inner rectangle
        draw.rectangle([
            (border_width, border_width),
            (self.size[0] - border_width, self.size[1] - border_width)
        ], fill=bg_color)
        
        return template
    
    def generate_ab_test_versions(self, genre: str) -> List[Dict]:
        """
        Generate multiple versions for A/B testing
        
        Args:
            genre: Genre name
        
        Returns:
            List of dictionaries with template configurations
        """
        versions = []
        
        # 3 color schemes
        color_schemes = list(self.COLOR_SCHEMES.keys())[:3]
        
        # 3 text positions
        text_positions = ["top", "center", "bottom"]
        
        for color_scheme in color_schemes:
            for position in text_positions:
                versions.append({
                    "genre": genre,
                    "color_scheme": color_scheme,
                    "text_position": position,
                    "template_type": "gradient"
                })
        
        return versions
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
