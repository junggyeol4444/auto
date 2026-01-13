"""
Image Processor Module
Handles image editing, resizing, and format conversion
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
from typing import Tuple, List


class ImageProcessor:
    """Process images for social media platforms"""
    
    def __init__(self):
        self.supported_formats = ['jpg', 'jpeg', 'png', 'webp']
    
    def resize_image(self, input_path: str, output_path: str,
                    size: Tuple[int, int], maintain_aspect: bool = True) -> str:
        """
        Resize image to target size
        
        Args:
            input_path: Path to input image
            output_path: Path to save resized image
            size: Target size (width, height)
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            Path to resized image
        """
        try:
            img = Image.open(input_path)
            
            if maintain_aspect:
                img.thumbnail(size, Image.Resampling.LANCZOS)
            else:
                img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Convert RGBA to RGB if saving as JPEG
            if output_path.lower().endswith(('.jpg', '.jpeg')):
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
            
            img.save(output_path, quality=95)
            return output_path
            
        except Exception as e:
            raise Exception(f"Error resizing image: {str(e)}")
    
    def crop_to_aspect_ratio(self, input_path: str, output_path: str,
                            aspect_ratio: str = '1:1') -> str:
        """
        Crop image to specific aspect ratio
        
        Args:
            input_path: Path to input image
            output_path: Path to save cropped image
            aspect_ratio: Target aspect ratio ('1:1', '9:16', '16:9', '4:5')
            
        Returns:
            Path to cropped image
        """
        try:
            img = Image.open(input_path)
            width, height = img.size
            
            # Parse aspect ratio
            ratio_map = {
                '1:1': 1.0,
                '9:16': 9/16,
                '16:9': 16/9,
                '4:5': 4/5
            }
            
            target_ratio = ratio_map.get(aspect_ratio, 1.0)
            current_ratio = width / height
            
            if current_ratio > target_ratio:
                # Image is wider, crop sides
                new_width = int(height * target_ratio)
                left = (width - new_width) // 2
                img = img.crop((left, 0, left + new_width, height))
            else:
                # Image is taller, crop top/bottom
                new_height = int(width / target_ratio)
                top = (height - new_height) // 2
                img = img.crop((0, top, width, top + new_height))
            
            # Convert RGBA to RGB if saving as JPEG
            if output_path.lower().endswith(('.jpg', '.jpeg')):
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
            
            img.save(output_path, quality=95)
            return output_path
            
        except Exception as e:
            raise Exception(f"Error cropping image: {str(e)}")
    
    def create_carousel_images(self, image_paths: List[str], output_dir: str,
                              size: Tuple[int, int] = (1080, 1080)) -> List[str]:
        """
        Process multiple images for carousel post
        
        Args:
            image_paths: List of input image paths
            output_dir: Directory to save processed images
            size: Target size for all images
            
        Returns:
            List of processed image paths
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            output_paths = []
            
            for i, img_path in enumerate(image_paths):
                output_path = os.path.join(output_dir, f"carousel_{i+1}.jpg")
                self.resize_image(img_path, output_path, size, maintain_aspect=False)
                output_paths.append(output_path)
            
            return output_paths
            
        except Exception as e:
            raise Exception(f"Error creating carousel images: {str(e)}")
    
    def add_text_overlay(self, input_path: str, output_path: str,
                        text: str, position: str = 'bottom',
                        font_size: int = 40) -> str:
        """
        Add text overlay to image
        
        Args:
            input_path: Path to input image
            output_path: Path to save image with text
            text: Text to overlay
            position: Text position ('top', 'center', 'bottom')
            font_size: Font size
            
        Returns:
            Path to image with text
        """
        try:
            img = Image.open(input_path)
            draw = ImageDraw.Draw(img)
            
            # Try to use a default font
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Get text size
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate position
            img_width, img_height = img.size
            x = (img_width - text_width) // 2
            
            if position == 'top':
                y = 50
            elif position == 'center':
                y = (img_height - text_height) // 2
            else:  # bottom
                y = img_height - text_height - 50
            
            # Draw text with outline for better visibility
            outline_range = 2
            for adj_x in range(-outline_range, outline_range + 1):
                for adj_y in range(-outline_range, outline_range + 1):
                    draw.text((x + adj_x, y + adj_y), text, font=font, fill='black')
            
            draw.text((x, y), text, font=font, fill='white')
            
            # Convert RGBA to RGB if saving as JPEG
            if output_path.lower().endswith(('.jpg', '.jpeg')):
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
            
            img.save(output_path, quality=95)
            return output_path
            
        except Exception as e:
            raise Exception(f"Error adding text overlay: {str(e)}")
    
    def enhance_image(self, input_path: str, output_path: str,
                     brightness: float = 1.0, contrast: float = 1.0,
                     saturation: float = 1.0, sharpness: float = 1.0) -> str:
        """
        Enhance image with various adjustments
        
        Args:
            input_path: Path to input image
            output_path: Path to save enhanced image
            brightness: Brightness factor (1.0 = no change)
            contrast: Contrast factor (1.0 = no change)
            saturation: Saturation factor (1.0 = no change)
            sharpness: Sharpness factor (1.0 = no change)
            
        Returns:
            Path to enhanced image
        """
        try:
            img = Image.open(input_path)
            
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)
            
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)
            
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(saturation)
            
            if sharpness != 1.0:
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(sharpness)
            
            # Convert RGBA to RGB if saving as JPEG
            if output_path.lower().endswith(('.jpg', '.jpeg')):
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
            
            img.save(output_path, quality=95)
            return output_path
            
        except Exception as e:
            raise Exception(f"Error enhancing image: {str(e)}")
    
    def get_image_info(self, image_path: str) -> dict:
        """Get image information"""
        try:
            img = Image.open(image_path)
            info = {
                'size': img.size,
                'mode': img.mode,
                'format': img.format,
                'aspect_ratio': img.size[0] / img.size[1]
            }
            return info
        except Exception as e:
            raise Exception(f"Error getting image info: {str(e)}")
