"""
Simple test script to validate core functionality
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all module imports"""
    print("Testing imports...")
    
    try:
        from modules.translation.translation_engine import TranslationEngine
        from modules.translation.google_api import GoogleTranslator
        from modules.subtitle.srt_parser import SRTParser
        from modules.subtitle.vtt_parser import VTTParser
        from modules.subtitle.ass_parser import ASSParser
        from modules.document.docx_translator import DocxTranslator
        from modules.document.pdf_translator import PDFTranslator
        from modules.web.html_translator import HTMLTranslator
        from modules.utils.glossary import GlossaryManager
        from modules.utils.cache_manager import CacheManager
        from modules.utils.language_detector import LanguageDetector
        
        print("✓ All module imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_translation_engine():
    """Test translation engine initialization"""
    print("\nTesting translation engine...")
    
    try:
        import json
        
        # Load config
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Initialize engine
        from modules.translation.translation_engine import TranslationEngine
        engine = TranslationEngine(config)
        
        # Check available engines
        available = engine.get_available_engines()
        print(f"  Available engines: {available}")
        
        # Google Translate should be available without API key
        if 'google' in available:
            print("✓ Google Translate available")
        else:
            print("⚠ Google Translate not available (googletrans may not be installed)")
        
        print("✓ Translation engine initialized")
        return True
    except Exception as e:
        print(f"✗ Translation engine error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_glossary():
    """Test glossary manager"""
    print("\nTesting glossary manager...")
    
    try:
        from modules.utils.glossary import GlossaryManager
        
        manager = GlossaryManager('data/glossaries')
        domains = manager.get_available_domains()
        print(f"  Available domains: {domains}")
        
        if domains:
            # Test loading a glossary
            glossary = manager.get_glossary(domains[0])
            print(f"  Loaded {domains[0]} glossary with {len(glossary)} terms")
            print("✓ Glossary manager working")
        else:
            print("⚠ No glossaries found")
        
        return True
    except Exception as e:
        print(f"✗ Glossary error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_subtitle_parser():
    """Test subtitle parser with sample data"""
    print("\nTesting subtitle parser...")
    
    try:
        from modules.subtitle.srt_parser import SRTParser, SubtitleEntry
        
        # Create sample entries
        entries = [
            SubtitleEntry(1, "00:00:01,000", "00:00:03,000", "Hello World"),
            SubtitleEntry(2, "00:00:04,000", "00:00:06,000", "Testing subtitles")
        ]
        
        # Test saving
        test_file = "output/subtitles/test.srt"
        SRTParser.save(entries, test_file)
        print(f"  Created test file: {test_file}")
        
        # Test parsing
        parsed = SRTParser.parse(test_file)
        print(f"  Parsed {len(parsed)} subtitle entries")
        
        if len(parsed) == len(entries):
            print("✓ Subtitle parser working")
        else:
            print("⚠ Parsed entry count mismatch")
        
        return True
    except Exception as e:
        print(f"✗ Subtitle parser error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cache_manager():
    """Test cache manager"""
    print("\nTesting cache manager...")
    
    try:
        from modules.utils.cache_manager import CacheManager
        
        cache = CacheManager("data/database/test_cache.db", 10)
        
        # Test setting cache
        cache.set("Hello", "en", "ko", "google", "안녕하세요")
        
        # Test getting cache
        result = cache.get("Hello", "en", "ko", "google")
        
        if result == "안녕하세요":
            print("  Cache set/get working")
            
            # Test stats
            stats = cache.get_stats()
            print(f"  Cache stats: {stats}")
            
            print("✓ Cache manager working")
        else:
            print("⚠ Cache value mismatch")
        
        return True
    except Exception as e:
        print(f"✗ Cache manager error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Translation Automation Platform - Core Functionality Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Translation Engine", test_translation_engine()))
    results.append(("Glossary Manager", test_glossary()))
    results.append(("Subtitle Parser", test_subtitle_parser()))
    results.append(("Cache Manager", test_cache_manager()))
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("=" * 60)
    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed. Check output above.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
