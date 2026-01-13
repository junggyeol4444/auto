"""
Example usage of the Translation Platform (headless mode)
Demonstrates core functionality without GUI
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from modules.translation.translation_engine import TranslationEngine
from modules.translation.google_api import GoogleTranslator
from modules.subtitle.srt_parser import SRTParser, SubtitleEntry
from modules.utils.glossary import GlossaryManager
import json


def example_google_translate():
    """Example: Direct Google Translate usage"""
    print("=" * 60)
    print("Example 1: Google Translate (no API key needed)")
    print("=" * 60)
    
    try:
        translator = GoogleTranslator()
        
        if translator.is_configured():
            # Simple translation
            text = "안녕하세요, 세계!"
            result = translator.translate(text, "ko", "en")
            print(f"Korean: {text}")
            print(f"English: {result}")
            print("✓ Translation successful\n")
        else:
            print("⚠ Google Translate not available (install: pip install googletrans==4.0.0rc1)")
            print("  Continuing with other examples...\n")
    except Exception as e:
        print(f"⚠ Google Translate error: {e}")
        print("  This is expected if googletrans is not installed.")
        print("  Continuing with other examples...\n")


def example_subtitle_translation():
    """Example: Subtitle file handling"""
    print("=" * 60)
    print("Example 2: Subtitle File Processing")
    print("=" * 60)
    
    # Create sample subtitle file
    sample_entries = [
        SubtitleEntry(1, "00:00:01,000", "00:00:03,000", "안녕하세요"),
        SubtitleEntry(2, "00:00:04,000", "00:00:06,000", "번역 플랫폼입니다"),
        SubtitleEntry(3, "00:00:07,000", "00:00:09,000", "자막 파일을 번역합니다")
    ]
    
    sample_file = "output/subtitles/sample_korean.srt"
    SRTParser.save(sample_entries, sample_file)
    print(f"Created sample subtitle file: {sample_file}")
    
    # Parse it back
    parsed = SRTParser.parse(sample_file)
    print(f"Parsed {len(parsed)} subtitle entries:")
    for entry in parsed:
        print(f"  [{entry.index}] {entry.start_time} --> {entry.end_time}")
        print(f"      {entry.text}")
    
    print("✓ Subtitle processing successful\n")


def example_glossary():
    """Example: Glossary usage"""
    print("=" * 60)
    print("Example 3: Domain-Specific Glossary")
    print("=" * 60)
    
    manager = GlossaryManager('data/glossaries')
    
    # Show available domains
    domains = manager.get_available_domains()
    print(f"Available domains: {', '.join(domains)}")
    
    # Load IT glossary
    it_glossary = manager.get_glossary('it')
    if it_glossary:
        print(f"\nIT Glossary ({len(it_glossary)} terms):")
        for i, (source, target) in enumerate(list(it_glossary.items())[:5]):
            print(f"  {source} → {target}")
        print("  ...")
        
        # Apply glossary to text
        text = "머신러닝과 인공지능은 중요한 기술입니다"
        result = manager.apply_glossary(text, 'it')
        print(f"\nApplying glossary:")
        print(f"  Original: {text}")
        print(f"  With glossary: {result}")
    
    print("✓ Glossary working\n")


def example_config():
    """Example: Configuration file"""
    print("=" * 60)
    print("Example 4: Configuration Management")
    print("=" * 60)
    
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    print("Configuration structure:")
    print(f"  Default source language: {config.get('default_source_lang')}")
    print(f"  Default target language: {config.get('default_target_lang')}")
    print(f"  Default engine: {config.get('default_engine')}")
    print(f"  Cache enabled: {config.get('cache_enabled')}")
    print(f"  Max cache size: {config.get('max_cache_size_mb')} MB")
    
    print("\nAPI Keys (configure in GUI Settings):")
    api_keys = config.get('api_keys', {})
    for key in api_keys:
        status = "Configured" if api_keys[key] else "Not set"
        print(f"  {key}: {status}")
    
    print("✓ Configuration loaded\n")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Translation Automation Platform - Usage Examples")
    print("=" * 60 + "\n")
    
    example_google_translate()
    example_subtitle_translation()
    example_glossary()
    example_config()
    
    print("=" * 60)
    print("Examples Complete!")
    print("=" * 60)
    print("\nTo use the full GUI application, run:")
    print("  python main.py")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()
