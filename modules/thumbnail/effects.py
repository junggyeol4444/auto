"""
Visual effects for thumbnails (arrows, circles, stars, etc.)
"""
from PIL import Image, ImageDraw
from typing import Tuple, List
import math


class EffectsGenerator:
    """Generate visual effects for thumbnails"""
    
    @staticmethod
    def draw_arrow(image: Image.Image, start: Tuple[int, int], end: Tuple[int, int],
                   color: str = "#FF0000", width: int = 15) -> Image.Image:
        """
        Draw an arrow on the image
        
        Args:
            image: PIL Image object
            start: Starting point (x, y)
            end: Ending point (x, y)
            color: Arrow color
            width: Arrow width
        
        Returns:
            PIL Image with arrow
        """
        draw = ImageDraw.Draw(image)
        
        # Draw line
        draw.line([start, end], fill=color, width=width)
        
        # Calculate arrowhead
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        arrow_length = width * 2
        
        # Arrowhead points
        point1 = (
            end[0] - arrow_length * math.cos(angle - math.pi / 6),
            end[1] - arrow_length * math.sin(angle - math.pi / 6)
        )
        point2 = (
            end[0] - arrow_length * math.cos(angle + math.pi / 6),
            end[1] - arrow_length * math.sin(angle + math.pi / 6)
        )
        
        # Draw arrowhead
        draw.polygon([end, point1, point2], fill=color)
        
        return image
    
    @staticmethod
    def draw_circle(image: Image.Image, center: Tuple[int, int], radius: int = 50,
                   color: str = "#FF0000", width: int = 10) -> Image.Image:
        """
        Draw a circle on the image
        
        Args:
            image: PIL Image object
            center: Center point (x, y)
            radius: Circle radius
            color: Circle color
            width: Line width
        
        Returns:
            PIL Image with circle
        """
        draw = ImageDraw.Draw(image)
        
        bbox = [
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius
        ]
        
        draw.ellipse(bbox, outline=color, width=width)
        
        return image
    
    @staticmethod
    def draw_star(image: Image.Image, center: Tuple[int, int], size: int = 50,
                 color: str = "#FFFF00") -> Image.Image:
        """
        Draw a star on the image
        
        Args:
            image: PIL Image object
            center: Center point (x, y)
            size: Star size
            color: Star color
        
        Returns:
            PIL Image with star
        """
        draw = ImageDraw.Draw(image)
        
        # Calculate star points (5-pointed star)
        points = []
        for i in range(10):
            angle = (i * math.pi / 5) - math.pi / 2
            if i % 2 == 0:
                # Outer point
                r = size
            else:
                # Inner point
                r = size * 0.4
            
            x = center[0] + r * math.cos(angle)
            y = center[1] + r * math.sin(angle)
            points.append((x, y))
        
        # Draw star
        draw.polygon(points, fill=color, outline=color)
        
        return image
    
    @staticmethod
    def draw_sparkle(image: Image.Image, center: Tuple[int, int], size: int = 30,
                    color: str = "#FFFFFF") -> Image.Image:
        """
        Draw a sparkle effect
        
        Args:
            image: PIL Image object
            center: Center point (x, y)
            size: Sparkle size
            color: Sparkle color
        
        Returns:
            PIL Image with sparkle
        """
        draw = ImageDraw.Draw(image)
        
        # Draw cross
        draw.line([
            (center[0] - size, center[1]),
            (center[0] + size, center[1])
        ], fill=color, width=4)
        
        draw.line([
            (center[0], center[1] - size),
            (center[0], center[1] + size)
        ], fill=color, width=4)
        
        # Draw diagonal cross
        draw.line([
            (center[0] - size * 0.7, center[1] - size * 0.7),
            (center[0] + size * 0.7, center[1] + size * 0.7)
        ], fill=color, width=3)
        
        draw.line([
            (center[0] - size * 0.7, center[1] + size * 0.7),
            (center[0] + size * 0.7, center[1] - size * 0.7)
        ], fill=color, width=3)
        
        return image
    
    @staticmethod
    def add_multiple_effects(image: Image.Image, effect_type: str, 
                            positions: List[Tuple[int, int]] = None,
                            color: str = "#FF0000") -> Image.Image:
        """
        Add multiple effects to image
        
        Args:
            image: PIL Image object
            effect_type: Type of effect ("stars", "circles", "sparkles")
            positions: List of positions or None for random
            color: Effect color
        
        Returns:
            PIL Image with effects
        """
        import random
        
        if positions is None:
            # Generate random positions
            positions = []
            for _ in range(random.randint(3, 6)):
                x = random.randint(50, image.width - 50)
                y = random.randint(50, image.height - 50)
                positions.append((x, y))
        
        for pos in positions:
            if effect_type == "stars":
                image = EffectsGenerator.draw_star(image, pos, 
                                                   random.randint(20, 40), color)
            elif effect_type == "circles":
                image = EffectsGenerator.draw_circle(image, pos,
                                                     random.randint(30, 60), color, 8)
            elif effect_type == "sparkles":
                image = EffectsGenerator.draw_sparkle(image, pos,
                                                      random.randint(15, 30), color)
        
        return image
    
    @staticmethod
    def add_exclamation(image: Image.Image, position: Tuple[int, int],
                       size: int = 60, color: str = "#FF0000") -> Image.Image:
        """
        Add exclamation mark
        
        Args:
            image: PIL Image object
            position: Position (x, y)
            size: Size
            color: Color
        
        Returns:
            PIL Image with exclamation
        """
        draw = ImageDraw.Draw(image)
        
        # Draw exclamation body
        body_width = size // 5
        body_height = size * 2 // 3
        
        draw.rectangle([
            position[0] - body_width // 2,
            position[1],
            position[0] + body_width // 2,
            position[1] + body_height
        ], fill=color)
        
        # Draw exclamation dot
        dot_radius = size // 4
        dot_y = position[1] + body_height + size // 6
        
        draw.ellipse([
            position[0] - dot_radius,
            dot_y - dot_radius,
            position[0] + dot_radius,
            dot_y + dot_radius
        ], fill=color)
        
        return image
