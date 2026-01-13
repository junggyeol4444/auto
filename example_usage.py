"""
Example script showing how to use the AI Design Automation Suite programmatically
"""
import sys
import os
from PIL import Image

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.thumbnail.template_manager import TemplateManager
from modules.thumbnail.text_overlay import TextOverlay
from modules.thumbnail.effects import EffectsGenerator
from modules.utils.font_manager import FontManager


def example_create_thumbnail():
    """Example: Create a YouTube thumbnail"""
    print("Creating YouTube thumbnail...")
    
    # Initialize managers
    template_manager = TemplateManager((1280, 720))
    font_manager = FontManager()
    text_overlay = TextOverlay(font_manager)
    
    # Create template
    template = template_manager.create_template("게임", "빨강+노랑")
    
    # Add text
    title = "완전 초간단 꿀팁 대공개!"
    keywords = ["초간단", "꿀팁", "대공개"]
    
    thumbnail = text_overlay.highlight_keywords(
        template, 
        title, 
        keywords,
        position="center",
        font_size=80,
        normal_color="#FFFFFF",
        highlight_color="#FFFF00"
    )
    
    # Add effects
    thumbnail = EffectsGenerator.add_multiple_effects(thumbnail, "stars", color="#FFFF00")
    thumbnail = EffectsGenerator.draw_circle(thumbnail, (200, 200), 80, "#FF0000", 12)
    thumbnail = EffectsGenerator.add_exclamation(thumbnail, (1100, 200), 80, "#FF0000")
    
    # Save
    output_dir = os.path.join(os.path.dirname(__file__), 'output', 'thumbnails')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'example_thumbnail.png')
    thumbnail.save(output_path)
    
    print(f"Thumbnail saved to: {output_path}")
    return thumbnail


def example_create_gradient_background():
    """Example: Create a gradient background"""
    print("\nCreating gradient background...")
    
    from modules.utils.image_utils import create_gradient
    
    # Create gradient
    gradient = create_gradient((1280, 720), "#FF6B6B", "#4ECDC4", "diagonal")
    
    # Save
    output_dir = os.path.join(os.path.dirname(__file__), 'output', 'synthesis')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'example_gradient.png')
    gradient.save(output_path)
    
    print(f"Gradient saved to: {output_path}")
    return gradient


def example_create_collage():
    """Example: Create a collage"""
    print("\nCreating collage...")
    
    from modules.photo_synthesis.collage import CollageCreator
    
    # Create some sample images
    images = []
    colors = ["#FF6B6B", "#4ECDC4", "#95E1D3", "#F38181"]
    
    for i, color in enumerate(colors):
        img = Image.new('RGB', (400, 300), color)
        images.append(img)
    
    # Create collage
    collage_creator = CollageCreator()
    collage = collage_creator.create_grid_collage(
        images, 
        grid_size=(2, 2),
        output_size=(1920, 1080),
        spacing=20,
        border_width=5,
        border_color="#FFFFFF"
    )
    
    # Save
    output_dir = os.path.join(os.path.dirname(__file__), 'output', 'synthesis')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'example_collage.png')
    collage.save(output_path)
    
    print(f"Collage saved to: {output_path}")
    return collage


def example_apply_filters():
    """Example: Apply color filters"""
    print("\nApplying color filters...")
    
    from modules.photo_synthesis.color_grading import ColorGrading
    
    # Create sample image
    original = Image.new('RGB', (640, 480), '#FF6B6B')
    
    # Apply filters
    filters = ['vintage', 'vivid', 'warm', 'cool']
    
    output_dir = os.path.join(os.path.dirname(__file__), 'output', 'synthesis')
    os.makedirs(output_dir, exist_ok=True)
    
    for filter_name in filters:
        filtered = ColorGrading.apply_filter(original, filter_name)
        output_path = os.path.join(output_dir, f'example_filter_{filter_name}.png')
        filtered.save(output_path)
        print(f"  - {filter_name} filter saved to: {output_path}")


def main():
    """Run all examples"""
    print("="*60)
    print("AI Design Automation Suite - Example Usage")
    print("="*60)
    
    try:
        # Example 1: Create thumbnail
        example_create_thumbnail()
        
        # Example 2: Create gradient
        example_create_gradient_background()
        
        # Example 3: Create collage
        example_create_collage()
        
        # Example 4: Apply filters
        example_apply_filters()
        
        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("Check the 'output' folder for generated files.")
        print("="*60)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
