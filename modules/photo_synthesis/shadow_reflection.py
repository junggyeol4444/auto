"""
Shadow and reflection effects
"""
from PIL import Image, ImageFilter, ImageDraw
import numpy as np


class ShadowReflection:
    """Generate shadow and reflection effects"""
    
    @staticmethod
    def add_drop_shadow(image: Image.Image, offset: tuple = (10, 10),
                       blur: int = 15, opacity: int = 128) -> Image.Image:
        """
        Add drop shadow to image
        
        Args:
            image: PIL Image (should have transparency)
            offset: Shadow offset (x, y)
            blur: Shadow blur radius
            opacity: Shadow opacity (0-255)
        
        Returns:
            PIL Image with shadow
        """
        # Calculate new size
        new_width = image.width + abs(offset[0]) + blur * 2
        new_height = image.height + abs(offset[1]) + blur * 2
        
        # Create shadow layer
        shadow_layer = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
        
        # Create shadow
        if image.mode == 'RGBA':
            shadow = Image.new('RGBA', image.size, (0, 0, 0, opacity))
            shadow.putalpha(image.split()[3])  # Use alpha from original
        else:
            shadow = Image.new('RGBA', image.size, (0, 0, 0, opacity))
        
        # Position shadow
        shadow_x = blur + max(0, offset[0])
        shadow_y = blur + max(0, offset[1])
        shadow_layer.paste(shadow, (shadow_x, shadow_y), shadow)
        
        # Blur shadow
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(blur))
        
        # Paste original image
        img_x = blur - min(0, offset[0])
        img_y = blur - min(0, offset[1])
        if image.mode == 'RGBA':
            shadow_layer.paste(image, (img_x, img_y), image)
        else:
            shadow_layer.paste(image, (img_x, img_y))
        
        return shadow_layer
    
    @staticmethod
    def add_reflection(image: Image.Image, opacity: float = 0.5,
                      gradient: bool = True) -> Image.Image:
        """
        Add reflection effect below image
        
        Args:
            image: PIL Image
            opacity: Reflection opacity (0.0 to 1.0)
            gradient: Use gradient for fade effect
        
        Returns:
            PIL Image with reflection
        """
        # Create reflection
        reflection = image.copy()
        reflection = reflection.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        
        # Apply opacity
        if reflection.mode != 'RGBA':
            reflection = reflection.convert('RGBA')
        
        # Create gradient mask if requested
        if gradient:
            mask = Image.new('L', reflection.size)
            draw = ImageDraw.Draw(mask)
            
            for y in range(reflection.height):
                alpha = int(255 * opacity * (1 - y / reflection.height))
                draw.line([(0, y), (reflection.width, y)], fill=alpha)
            
            reflection.putalpha(mask)
        else:
            # Uniform opacity
            alpha = reflection.split()[3] if reflection.mode == 'RGBA' else Image.new('L', reflection.size, 255)
            alpha = alpha.point(lambda p: int(p * opacity))
            reflection.putalpha(alpha)
        
        # Create combined image
        total_height = image.height + reflection.height
        combined = Image.new('RGBA', (image.width, total_height), (255, 255, 255, 0))
        
        # Paste original
        combined.paste(image, (0, 0))
        
        # Paste reflection
        combined.paste(reflection, (0, image.height), reflection)
        
        return combined
    
    @staticmethod
    def add_perspective_shadow(image: Image.Image, angle: float = 45,
                              distance: int = 20, blur: int = 10) -> Image.Image:
        """
        Add perspective shadow (like object on ground)
        
        Args:
            image: PIL Image (should have transparency)
            angle: Shadow angle in degrees
            distance: Shadow distance
            blur: Shadow blur
        
        Returns:
            PIL Image with perspective shadow
        """
        import math
        
        # Calculate shadow dimensions
        angle_rad = math.radians(angle)
        shadow_width = image.width + int(distance * abs(math.cos(angle_rad)))
        shadow_height = image.height + int(distance * abs(math.sin(angle_rad)))
        
        # Create canvas
        canvas = Image.new('RGBA', (shadow_width, shadow_height + blur * 2), (0, 0, 0, 0))
        
        # Create shadow
        if image.mode == 'RGBA':
            shadow = Image.new('RGBA', image.size, (0, 0, 0, 100))
            shadow.putalpha(image.split()[3])
        else:
            shadow = Image.new('RGBA', image.size, (0, 0, 0, 100))
        
        # Transform shadow for perspective
        shadow_offset_x = int(distance * math.cos(angle_rad))
        shadow_offset_y = int(distance * math.sin(angle_rad))
        
        # Paste and blur shadow
        canvas.paste(shadow, (shadow_offset_x, shadow_offset_y + blur), shadow)
        canvas = canvas.filter(ImageFilter.GaussianBlur(blur))
        
        # Paste original image
        if image.mode == 'RGBA':
            canvas.paste(image, (0, blur), image)
        else:
            canvas.paste(image, (0, blur))
        
        return canvas
    
    @staticmethod
    def add_cast_shadow(image: Image.Image, light_angle: float = 45,
                       shadow_length: float = 0.5, blur: int = 10) -> Image.Image:
        """
        Add cast shadow based on light direction
        
        Args:
            image: PIL Image
            light_angle: Light angle in degrees (0 = right, 90 = top, etc.)
            shadow_length: Shadow length as ratio of image size
            blur: Shadow blur radius
        
        Returns:
            PIL Image with cast shadow
        """
        import math
        
        angle_rad = math.radians(light_angle)
        
        # Calculate shadow offset
        max_shadow = int(max(image.width, image.height) * shadow_length)
        offset_x = int(max_shadow * math.cos(angle_rad))
        offset_y = int(max_shadow * math.sin(angle_rad))
        
        # Create expanded canvas
        canvas_width = image.width + abs(offset_x) + blur * 2
        canvas_height = image.height + abs(offset_y) + blur * 2
        canvas = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        
        # Create shadow
        if image.mode == 'RGBA':
            shadow = Image.new('RGBA', image.size, (0, 0, 0, 80))
            shadow.putalpha(image.split()[3])
        else:
            shadow = Image.new('RGBA', image.size, (0, 0, 0, 80))
        
        # Position shadow
        shadow_x = blur + max(0, offset_x)
        shadow_y = blur + max(0, offset_y)
        canvas.paste(shadow, (shadow_x, shadow_y), shadow)
        
        # Blur shadow
        canvas = canvas.filter(ImageFilter.GaussianBlur(blur))
        
        # Paste original image
        img_x = blur - min(0, offset_x)
        img_y = blur - min(0, offset_y)
        if image.mode == 'RGBA':
            canvas.paste(image, (img_x, img_y), image)
        else:
            canvas.paste(image, (img_x, img_y))
        
        return canvas
