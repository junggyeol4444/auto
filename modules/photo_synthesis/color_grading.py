"""
Color grading and adjustment for photo synthesis
"""
from PIL import Image, ImageEnhance
import cv2
import numpy as np
from typing import Tuple


class ColorGrading:
    """Apply color grading and adjustments to images"""
    
    @staticmethod
    def apply_filter(image: Image.Image, filter_name: str) -> Image.Image:
        """
        Apply predefined filter to image
        
        Args:
            image: PIL Image object
            filter_name: Filter name ('vintage', 'vivid', 'warm', 'cool', 'bw')
        
        Returns:
            PIL Image with filter applied
        """
        if filter_name == 'vintage':
            return ColorGrading.vintage_filter(image)
        elif filter_name == 'vivid':
            return ColorGrading.vivid_filter(image)
        elif filter_name == 'warm':
            return ColorGrading.warm_filter(image)
        elif filter_name == 'cool':
            return ColorGrading.cool_filter(image)
        elif filter_name == 'bw':
            return ColorGrading.black_white_filter(image)
        else:
            return image
    
    @staticmethod
    def vintage_filter(image: Image.Image) -> Image.Image:
        """Apply vintage/retro filter"""
        # Reduce saturation
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(0.7)
        
        # Reduce contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(0.85)
        
        # Add warm tint
        img_array = np.array(image)
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.1, 0, 255)  # Red
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 0.9, 0, 255)  # Blue
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    @staticmethod
    def vivid_filter(image: Image.Image) -> Image.Image:
        """Apply vivid/saturated filter"""
        # Increase saturation
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.5)
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        # Increase sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.3)
        
        return image
    
    @staticmethod
    def warm_filter(image: Image.Image) -> Image.Image:
        """Apply warm filter"""
        img_array = np.array(image)
        
        # Increase red and decrease blue
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.15, 0, 255)  # Red
        img_array[:, :, 1] = np.clip(img_array[:, :, 1] * 1.05, 0, 255)  # Green
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 0.9, 0, 255)   # Blue
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    @staticmethod
    def cool_filter(image: Image.Image) -> Image.Image:
        """Apply cool filter"""
        img_array = np.array(image)
        
        # Increase blue and decrease red
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 0.9, 0, 255)   # Red
        img_array[:, :, 1] = np.clip(img_array[:, :, 1] * 1.0, 0, 255)   # Green
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 1.15, 0, 255)  # Blue
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    @staticmethod
    def black_white_filter(image: Image.Image) -> Image.Image:
        """Convert to black and white"""
        return image.convert('L').convert('RGB')
    
    @staticmethod
    def adjust_hsv(image: Image.Image, h_shift: int = 0, 
                   s_scale: float = 1.0, v_scale: float = 1.0) -> Image.Image:
        """
        Adjust HSV values
        
        Args:
            image: PIL Image object
            h_shift: Hue shift (-180 to 180)
            s_scale: Saturation scale (0.0 to 2.0)
            v_scale: Value/brightness scale (0.0 to 2.0)
        
        Returns:
            PIL Image with adjusted HSV
        """
        # Convert to OpenCV format
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        img_hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV).astype(np.float32)
        
        # Adjust hue
        img_hsv[:, :, 0] = (img_hsv[:, :, 0] + h_shift) % 180
        
        # Adjust saturation
        img_hsv[:, :, 1] = np.clip(img_hsv[:, :, 1] * s_scale, 0, 255)
        
        # Adjust value
        img_hsv[:, :, 2] = np.clip(img_hsv[:, :, 2] * v_scale, 0, 255)
        
        # Convert back
        img_hsv = img_hsv.astype(np.uint8)
        img_bgr = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        return Image.fromarray(img_rgb)
    
    @staticmethod
    def match_colors(source: Image.Image, reference: Image.Image) -> Image.Image:
        """
        Match colors of source image to reference image
        
        Args:
            source: Source PIL Image to adjust
            reference: Reference PIL Image with target colors
        
        Returns:
            PIL Image with matched colors
        """
        # Convert to LAB color space for better color matching
        source_cv = cv2.cvtColor(np.array(source), cv2.COLOR_RGB2BGR)
        reference_cv = cv2.cvtColor(np.array(reference), cv2.COLOR_RGB2BGR)
        
        source_lab = cv2.cvtColor(source_cv, cv2.COLOR_BGR2LAB).astype(np.float32)
        reference_lab = cv2.cvtColor(reference_cv, cv2.COLOR_BGR2LAB).astype(np.float32)
        
        # Calculate mean and std for each channel
        source_mean = source_lab.mean(axis=(0, 1))
        source_std = source_lab.std(axis=(0, 1))
        reference_mean = reference_lab.mean(axis=(0, 1))
        reference_std = reference_lab.std(axis=(0, 1))
        
        # Adjust colors
        result_lab = source_lab.copy()
        for i in range(3):
            result_lab[:, :, i] = ((source_lab[:, :, i] - source_mean[i]) * 
                                  (reference_std[i] / (source_std[i] + 1e-6)) + 
                                  reference_mean[i])
        
        result_lab = np.clip(result_lab, 0, 255).astype(np.uint8)
        
        # Convert back to RGB
        result_bgr = cv2.cvtColor(result_lab, cv2.COLOR_LAB2BGR)
        result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)
        
        return Image.fromarray(result_rgb)
    
    @staticmethod
    def unify_colors(images: list, reference_idx: int = 0) -> list:
        """
        Unify colors across multiple images
        
        Args:
            images: List of PIL Images
            reference_idx: Index of reference image
        
        Returns:
            List of PIL Images with unified colors
        """
        if not images:
            return []
        
        reference = images[reference_idx]
        result = []
        
        for i, img in enumerate(images):
            if i == reference_idx:
                result.append(img)
            else:
                result.append(ColorGrading.match_colors(img, reference))
        
        return result
