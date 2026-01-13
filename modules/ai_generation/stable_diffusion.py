"""
AI background generation using Stable Diffusion (optional)
"""
from PIL import Image
from typing import Tuple, Optional


class StableDiffusionGenerator:
    """Generate backgrounds using Stable Diffusion"""
    
    def __init__(self):
        self.available = False
        self.pipe = None
        
        try:
            from diffusers import StableDiffusionPipeline
            import torch
            
            self.StableDiffusionPipeline = StableDiffusionPipeline
            self.torch = torch
            self.available = True
            
            print("Stable Diffusion is available (will load on first use)")
        except ImportError:
            print("Note: Stable Diffusion not available. Install diffusers and torch to enable.")
    
    def _load_model(self):
        """Load Stable Diffusion model (lazy loading)"""
        if self.pipe is None and self.available:
            try:
                print("Loading Stable Diffusion model (this may take a while)...")
                
                # Use CPU by default, GPU if available
                device = "cuda" if self.torch.cuda.is_available() else "cpu"
                
                self.pipe = self.StableDiffusionPipeline.from_pretrained(
                    "runwayml/stable-diffusion-v1-5",
                    torch_dtype=self.torch.float16 if device == "cuda" else self.torch.float32
                )
                self.pipe = self.pipe.to(device)
                
                print(f"Stable Diffusion loaded on {device}")
            except Exception as e:
                print(f"Failed to load Stable Diffusion: {e}")
                self.available = False
    
    def generate_background(self, prompt: str, size: Tuple[int, int] = (1280, 720),
                           num_inference_steps: int = 20) -> Optional[Image.Image]:
        """
        Generate background image from text prompt
        
        Args:
            prompt: Text description of desired background
            size: Output size (width, height)
            num_inference_steps: Number of denoising steps (higher = better quality, slower)
        
        Returns:
            PIL Image or None if generation failed
        """
        if not self.available:
            print("Stable Diffusion is not available")
            return None
        
        self._load_model()
        
        if self.pipe is None:
            return None
        
        try:
            # Generate image
            result = self.pipe(
                prompt,
                height=size[1],
                width=size[0],
                num_inference_steps=num_inference_steps,
                guidance_scale=7.5
            )
            
            return result.images[0]
        except Exception as e:
            print(f"Failed to generate image: {e}")
            return None
    
    def generate_thumbnail_background(self, genre: str, 
                                     size: Tuple[int, int] = (1280, 720)) -> Optional[Image.Image]:
        """
        Generate background suitable for thumbnail based on genre
        
        Args:
            genre: Content genre
            size: Output size
        
        Returns:
            PIL Image or None
        """
        prompts = {
            "게임": "epic gaming background, colorful, energetic, digital art",
            "브이로그": "casual lifestyle background, soft colors, modern",
            "리뷰": "clean professional background, minimalist",
            "먹방": "appetizing food background, warm lighting, restaurant",
            "교육": "clean educational background, professional, organized"
        }
        
        prompt = prompts.get(genre, "colorful abstract background")
        return self.generate_background(prompt, size, num_inference_steps=15)
    
    def generate_simple_background(self, style: str = "gradient") -> Image.Image:
        """
        Generate simple background without AI (fallback)
        
        Args:
            style: Background style ('gradient', 'solid', 'pattern')
        
        Returns:
            PIL Image
        """
        from PIL import ImageDraw
        import random
        
        size = (1280, 720)
        
        if style == "gradient":
            # Random gradient
            colors = [
                ("#FF6B6B", "#4ECDC4"),
                ("#A8E6CF", "#FFD3B6"),
                ("#FFA8A8", "#B4AAFF"),
                ("#FFABAB", "#FFC3A0")
            ]
            color1, color2 = random.choice(colors)
            
            img = Image.new('RGB', size)
            draw = ImageDraw.Draw(img)
            
            for y in range(size[1]):
                r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
                r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
                
                ratio = y / size[1]
                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)
                
                draw.line([(0, y), (size[0], y)], fill=(r, g, b))
            
            return img
        
        elif style == "solid":
            # Random solid color
            colors = ["#FF6B6B", "#4ECDC4", "#FFD93D", "#6C5CE7", "#A8E6CF"]
            color = random.choice(colors)
            return Image.new('RGB', size, color)
        
        else:  # pattern
            # Simple pattern
            img = Image.new('RGB', size, '#F0F0F0')
            draw = ImageDraw.Draw(img)
            
            # Draw circles pattern
            for x in range(0, size[0], 100):
                for y in range(0, size[1], 100):
                    draw.ellipse([x, y, x + 50, y + 50], outline='#CCCCCC', width=2)
            
            return img
