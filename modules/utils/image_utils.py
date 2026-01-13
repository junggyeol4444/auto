"""
Image utility functions for the AI Design Automation Suite
"""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import cv2
from typing import Tuple, Optional


def resize_image(image: Image.Image, target_size: Tuple[int, int], keep_aspect: bool = True) -> Image.Image:
    """
    Resize image to target size
    
    Args:
        image: PIL Image object
        target_size: (width, height) tuple
        keep_aspect: Whether to keep aspect ratio
    
    Returns:
        Resized PIL Image
    """
    if keep_aspect:
        image.thumbnail(target_size, Image.Resampling.LANCZOS)
        return image
    else:
        return image.resize(target_size, Image.Resampling.LANCZOS)


def center_crop(image: Image.Image, crop_size: Tuple[int, int]) -> Image.Image:
    """
    Center crop an image
    
    Args:
        image: PIL Image object
        crop_size: (width, height) tuple
    
    Returns:
        Cropped PIL Image
    """
    width, height = image.size
    crop_width, crop_height = crop_size
    
    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = left + crop_width
    bottom = top + crop_height
    
    return image.crop((left, top, right, bottom))


def paste_with_transparency(background: Image.Image, foreground: Image.Image, position: Tuple[int, int]) -> Image.Image:
    """
    Paste image with transparency support
    
    Args:
        background: Background PIL Image
        foreground: Foreground PIL Image (can have alpha channel)
        position: (x, y) position to paste
    
    Returns:
        Combined PIL Image
    """
    if foreground.mode == 'RGBA':
        background.paste(foreground, position, foreground)
    else:
        background.paste(foreground, position)
    return background


def add_shadow(image: Image.Image, offset: Tuple[int, int] = (5, 5), blur: int = 10) -> Image.Image:
    """
    Add shadow effect to image
    
    Args:
        image: PIL Image object (should have transparency)
        offset: (x, y) offset for shadow
        blur: Blur radius for shadow
    
    Returns:
        PIL Image with shadow
    """
    # Create shadow layer
    shadow = Image.new('RGBA', (image.width + abs(offset[0]) + blur * 2, 
                                 image.height + abs(offset[1]) + blur * 2), (0, 0, 0, 0))
    
    # Create shadow mask
    shadow_mask = image.split()[3] if image.mode == 'RGBA' else Image.new('L', image.size, 255)
    shadow_img = Image.new('RGBA', image.size, (0, 0, 0, 128))
    shadow_img.putalpha(shadow_mask)
    
    # Paste shadow with offset
    shadow.paste(shadow_img, (blur + max(0, offset[0]), blur + max(0, offset[1])))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    
    # Paste original image on top
    shadow.paste(image, (blur, blur), image if image.mode == 'RGBA' else None)
    
    return shadow


def pil_to_cv2(pil_image: Image.Image) -> np.ndarray:
    """
    Convert PIL Image to OpenCV format
    
    Args:
        pil_image: PIL Image object
    
    Returns:
        OpenCV numpy array
    """
    if pil_image.mode == 'RGBA':
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGBA2BGRA)
    elif pil_image.mode == 'RGB':
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    else:
        return np.array(pil_image)


def cv2_to_pil(cv2_image: np.ndarray) -> Image.Image:
    """
    Convert OpenCV format to PIL Image
    
    Args:
        cv2_image: OpenCV numpy array
    
    Returns:
        PIL Image object
    """
    if len(cv2_image.shape) == 3:
        if cv2_image.shape[2] == 4:
            return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGRA2RGBA))
        else:
            return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))
    else:
        return Image.fromarray(cv2_image)


def create_gradient(size: Tuple[int, int], color1: str, color2: str, direction: str = 'horizontal') -> Image.Image:
    """
    Create gradient background
    
    Args:
        size: (width, height) tuple
        color1: Start color (hex or name)
        color2: End color (hex or name)
        direction: 'horizontal', 'vertical', or 'diagonal'
    
    Returns:
        PIL Image with gradient
    """
    width, height = size
    base = Image.new('RGB', size, color1)
    top = Image.new('RGB', size, color2)
    
    if direction == 'horizontal':
        mask = Image.new('L', size)
        for x in range(width):
            mask.paste(int(255 * x / width), (x, 0, x + 1, height))
    elif direction == 'vertical':
        mask = Image.new('L', size)
        for y in range(height):
            mask.paste(int(255 * y / height), (0, y, width, y + 1))
    else:  # diagonal
        mask = Image.new('L', size)
        for y in range(height):
            for x in range(width):
                distance = (x + y) / (width + height)
                mask.putpixel((x, y), int(255 * distance))
    
    base.paste(top, mask=mask)
    return base


def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
    """
    Adjust image brightness
    
    Args:
        image: PIL Image object
        factor: Brightness factor (1.0 = no change, < 1.0 = darker, > 1.0 = brighter)
    
    Returns:
        Adjusted PIL Image
    """
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
    """
    Adjust image contrast
    
    Args:
        image: PIL Image object
        factor: Contrast factor (1.0 = no change, < 1.0 = less contrast, > 1.0 = more contrast)
    
    Returns:
        Adjusted PIL Image
    """
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)
