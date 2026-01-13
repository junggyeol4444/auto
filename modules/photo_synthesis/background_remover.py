"""
Background removal using rembg
"""
from PIL import Image
import io


class BackgroundRemover:
    """Remove background from images"""
    
    def __init__(self):
        self.rembg_available = False
        try:
            from rembg import remove
            self.remove_func = remove
            self.rembg_available = True
        except ImportError:
            print("Warning: rembg not available. Background removal will use fallback method.")
    
    def remove_background(self, image: Image.Image) -> Image.Image:
        """
        Remove background from image
        
        Args:
            image: PIL Image object
        
        Returns:
            PIL Image with transparent background
        """
        if self.rembg_available:
            return self._remove_with_rembg(image)
        else:
            return self._remove_fallback(image)
    
    def _remove_with_rembg(self, image: Image.Image) -> Image.Image:
        """Remove background using rembg library"""
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Remove background
        output = self.remove_func(img_byte_arr)
        
        # Convert back to PIL Image
        return Image.open(io.BytesIO(output))
    
    def _remove_fallback(self, image: Image.Image) -> Image.Image:
        """
        Fallback background removal using simple color threshold
        (Not as accurate as rembg but works without dependencies)
        """
        import numpy as np
        
        # Convert to RGBA
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Get image data
        data = np.array(image)
        
        # Simple background detection (assumes corners are background)
        # Get corner colors
        corners = [
            data[0, 0],
            data[0, -1],
            data[-1, 0],
            data[-1, -1]
        ]
        
        # Find most common corner color
        from collections import Counter
        corner_colors = [tuple(c[:3]) for c in corners]
        bg_color = Counter(corner_colors).most_common(1)[0][0]
        
        # Create mask based on color similarity
        threshold = 30
        r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
        
        mask = (
            (np.abs(r.astype(int) - bg_color[0]) < threshold) &
            (np.abs(g.astype(int) - bg_color[1]) < threshold) &
            (np.abs(b.astype(int) - bg_color[2]) < threshold)
        )
        
        # Set alpha to 0 for background
        data[mask, 3] = 0
        
        return Image.fromarray(data)
    
    def remove_background_batch(self, images: list) -> list:
        """
        Remove background from multiple images
        
        Args:
            images: List of PIL Image objects
        
        Returns:
            List of PIL Images with transparent backgrounds
        """
        return [self.remove_background(img) for img in images]
    
    def save_with_transparency(self, image: Image.Image, output_path: str):
        """
        Save image with transparency
        
        Args:
            image: PIL Image object
            output_path: Output file path (should be .png)
        """
        image.save(output_path, 'PNG')
