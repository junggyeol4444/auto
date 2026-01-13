"""
Collage creation functionality
"""
from PIL import Image, ImageDraw
from typing import List, Tuple


class CollageCreator:
    """Create photo collages"""
    
    def create_grid_collage(self, images: List[Image.Image], grid_size: Tuple[int, int],
                           output_size: Tuple[int, int] = (1920, 1080),
                           spacing: int = 10, border_width: int = 0,
                           border_color: str = "#FFFFFF") -> Image.Image:
        """
        Create a grid collage
        
        Args:
            images: List of PIL Images
            grid_size: (rows, cols) tuple
            output_size: Output image size
            spacing: Spacing between images
            border_width: Border width around each image
            border_color: Border color
        
        Returns:
            PIL Image collage
        """
        rows, cols = grid_size
        width, height = output_size
        
        # Calculate cell size
        cell_width = (width - spacing * (cols + 1)) // cols
        cell_height = (height - spacing * (rows + 1)) // rows
        
        # Create background
        collage = Image.new('RGB', output_size, 'white')
        
        # Place images
        img_idx = 0
        for row in range(rows):
            for col in range(cols):
                if img_idx >= len(images):
                    break
                
                # Get image and resize
                img = images[img_idx].copy()
                
                # Resize to fit cell
                img.thumbnail((cell_width - border_width * 2, 
                             cell_height - border_width * 2), 
                            Image.Resampling.LANCZOS)
                
                # Calculate position
                x = spacing + col * (cell_width + spacing) + border_width
                y = spacing + row * (cell_height + spacing) + border_width
                
                # Center image in cell
                x += (cell_width - border_width * 2 - img.width) // 2
                y += (cell_height - border_width * 2 - img.height) // 2
                
                # Draw border if needed
                if border_width > 0:
                    draw = ImageDraw.Draw(collage)
                    draw.rectangle([
                        x - border_width, y - border_width,
                        x + img.width + border_width, y + img.height + border_width
                    ], outline=border_color, width=border_width)
                
                # Paste image
                collage.paste(img, (x, y))
                
                img_idx += 1
        
        return collage
    
    def create_free_collage(self, images: List[Image.Image], 
                           positions: List[Tuple[int, int]],
                           sizes: List[Tuple[int, int]],
                           output_size: Tuple[int, int] = (1920, 1080),
                           background_color: str = "white") -> Image.Image:
        """
        Create a free-form collage with custom positions
        
        Args:
            images: List of PIL Images
            positions: List of (x, y) positions for each image
            sizes: List of (width, height) for each image
            output_size: Output image size
            background_color: Background color
        
        Returns:
            PIL Image collage
        """
        collage = Image.new('RGB', output_size, background_color)
        
        for img, pos, size in zip(images, positions, sizes):
            # Resize image
            resized = img.copy()
            resized.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Paste image
            if resized.mode == 'RGBA':
                collage.paste(resized, pos, resized)
            else:
                collage.paste(resized, pos)
        
        return collage
    
    def create_polaroid_collage(self, images: List[Image.Image],
                               output_size: Tuple[int, int] = (1920, 1080)) -> Image.Image:
        """
        Create a polaroid-style collage
        
        Args:
            images: List of PIL Images
            output_size: Output image size
        
        Returns:
            PIL Image collage
        """
        import random
        
        collage = Image.new('RGB', output_size, '#F5F5DC')  # Beige background
        
        # Polaroid dimensions
        polaroid_width = output_size[0] // 4
        polaroid_height = int(polaroid_width * 1.2)
        photo_margin = polaroid_width // 10
        
        for i, img in enumerate(images):
            # Create polaroid
            polaroid = Image.new('RGB', (polaroid_width, polaroid_height), 'white')
            
            # Resize and center photo
            photo = img.copy()
            photo.thumbnail((polaroid_width - photo_margin * 2,
                           polaroid_height - photo_margin * 3), 
                          Image.Resampling.LANCZOS)
            
            photo_x = (polaroid_width - photo.width) // 2
            photo_y = photo_margin
            
            polaroid.paste(photo, (photo_x, photo_y))
            
            # Rotate slightly
            angle = random.randint(-15, 15)
            polaroid = polaroid.rotate(angle, expand=True, fillcolor='white')
            
            # Position on collage
            x = random.randint(0, output_size[0] - polaroid.width)
            y = random.randint(0, output_size[1] - polaroid.height)
            
            collage.paste(polaroid, (x, y))
        
        return collage
    
    def create_mosaic(self, images: List[Image.Image],
                     output_size: Tuple[int, int] = (1920, 1080),
                     tile_size: int = 100) -> Image.Image:
        """
        Create a mosaic from multiple images
        
        Args:
            images: List of PIL Images
            output_size: Output image size
            tile_size: Size of each tile
        
        Returns:
            PIL Image mosaic
        """
        mosaic = Image.new('RGB', output_size, 'white')
        
        cols = output_size[0] // tile_size
        rows = output_size[1] // tile_size
        
        img_idx = 0
        for row in range(rows):
            for col in range(cols):
                if img_idx >= len(images):
                    img_idx = 0  # Wrap around
                
                # Get and resize image
                img = images[img_idx].copy()
                img = img.resize((tile_size, tile_size), Image.Resampling.LANCZOS)
                
                # Paste tile
                x = col * tile_size
                y = row * tile_size
                mosaic.paste(img, (x, y))
                
                img_idx += 1
        
        return mosaic
