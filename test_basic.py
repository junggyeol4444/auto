"""
Test script to verify basic functionality without GUI
Run this to test if all modules work correctly
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing module imports...")
    
    try:
        from modules.thumbnail.template_manager import TemplateManager
        print("✓ TemplateManager imported")
    except Exception as e:
        print(f"✗ TemplateManager import failed: {e}")
    
    try:
        from modules.thumbnail.text_overlay import TextOverlay
        print("✓ TextOverlay imported")
    except Exception as e:
        print(f"✗ TextOverlay import failed: {e}")
    
    try:
        from modules.thumbnail.face_detect import FaceDetector
        print("✓ FaceDetector imported")
    except Exception as e:
        print(f"✗ FaceDetector import failed: {e}")
    
    try:
        from modules.thumbnail.effects import EffectsGenerator
        print("✓ EffectsGenerator imported")
    except Exception as e:
        print(f"✗ EffectsGenerator import failed: {e}")
    
    try:
        from modules.photo_synthesis.background_remover import BackgroundRemover
        print("✓ BackgroundRemover imported")
    except Exception as e:
        print(f"✗ BackgroundRemover import failed: {e}")
    
    try:
        from modules.photo_synthesis.background_replacer import BackgroundReplacer
        print("✓ BackgroundReplacer imported")
    except Exception as e:
        print(f"✗ BackgroundReplacer import failed: {e}")
    
    try:
        from modules.photo_synthesis.collage import CollageCreator
        print("✓ CollageCreator imported")
    except Exception as e:
        print(f"✗ CollageCreator import failed: {e}")
    
    try:
        from modules.photo_synthesis.color_grading import ColorGrading
        print("✓ ColorGrading imported")
    except Exception as e:
        print(f"✗ ColorGrading import failed: {e}")
    
    try:
        from modules.utils.font_manager import FontManager
        print("✓ FontManager imported")
    except Exception as e:
        print(f"✗ FontManager import failed: {e}")
    
    try:
        from modules.utils.image_utils import resize_image
        print("✓ image_utils imported")
    except Exception as e:
        print(f"✗ image_utils import failed: {e}")
    
    print("\nImport test complete!")


def test_basic_functionality():
    """Test basic functionality without requiring images"""
    print("\n" + "="*50)
    print("Testing basic functionality...")
    print("="*50)
    
    try:
        from modules.thumbnail.template_manager import TemplateManager
        from modules.utils.font_manager import FontManager
        from PIL import Image
        
        # Test template generation
        print("\n1. Testing template generation...")
        tm = TemplateManager((1280, 720))
        template = tm.create_template("게임", "빨강+노랑")
        print(f"   ✓ Created template: {template.size}")
        
        # Test font manager
        print("\n2. Testing font manager...")
        fm = FontManager()
        font = fm.get_font(size=40)
        print(f"   ✓ Font loaded: {type(font)}")
        
        # Test A/B versions
        print("\n3. Testing A/B test version generation...")
        versions = tm.generate_ab_test_versions("게임")
        print(f"   ✓ Generated {len(versions)} versions")
        
        # Test effects
        print("\n4. Testing effects...")
        from modules.thumbnail.effects import EffectsGenerator
        test_img = Image.new('RGB', (1280, 720), 'white')
        result = EffectsGenerator.draw_star(test_img, (640, 360), 50, "#FFFF00")
        print(f"   ✓ Effects applied: {result.size}")
        
        # Test color grading
        print("\n5. Testing color grading...")
        from modules.photo_synthesis.color_grading import ColorGrading
        test_img = Image.new('RGB', (640, 480), 'red')
        filtered = ColorGrading.apply_filter(test_img, 'vintage')
        print(f"   ✓ Filter applied: {filtered.size}")
        
        print("\n✓ All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("="*50)
    print("AI Design Automation Suite - Test Script")
    print("="*50)
    
    test_imports()
    
    try:
        success = test_basic_functionality()
        
        if success:
            print("\n" + "="*50)
            print("All tests passed! The application is ready to use.")
            print("Run 'python main.py' to start the GUI.")
            print("="*50)
        else:
            print("\n" + "="*50)
            print("Some tests failed. Check the error messages above.")
            print("="*50)
    except Exception as e:
        print(f"\nTest suite failed: {e}")


if __name__ == "__main__":
    main()
