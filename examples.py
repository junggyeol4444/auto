"""
Example usage of Voice Service Integrated Suite modules
This demonstrates how to use the core features programmatically.
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import setup_logger
from utils.config_manager import get_config_manager
from modules.tts.gtts_engine import GTTSEngine
from modules.tts.pyttsx3_engine import Pyttsx3Engine


def example_tts_gtts():
    """Example: Text-to-Speech with gTTS (requires internet)"""
    print("\n" + "="*60)
    print("Example 1: Text-to-Speech with gTTS")
    print("="*60)
    
    engine = GTTSEngine()
    
    text = "Hello! This is an example of text-to-speech using gTTS."
    output_file = "output/tts/example_gtts.mp3"
    
    print(f"Generating speech: '{text}'")
    success = engine.synthesize(
        text=text,
        output_path=output_file,
        language='en',
        slow=False
    )
    
    if success:
        print(f"✓ Audio saved to: {output_file}")
        print(f"  File size: {os.path.getsize(output_file)} bytes")
    else:
        print("✗ Failed (may need internet connection)")


def example_tts_pyttsx3():
    """Example: Text-to-Speech with pyttsx3 (offline)"""
    print("\n" + "="*60)
    print("Example 2: Text-to-Speech with pyttsx3 (offline)")
    print("="*60)
    
    engine = Pyttsx3Engine()
    
    if not engine.engine:
        print("✗ pyttsx3 not available (requires eSpeak)")
        return
    
    # Get available voices
    voices = engine.get_voices()
    print(f"Available voices: {len(voices)}")
    
    text = "This is an example of offline text-to-speech."
    output_file = "output/tts/example_pyttsx3.wav"
    
    print(f"Generating speech: '{text}'")
    success = engine.synthesize(
        text=text,
        output_path=output_file,
        rate=150,
        volume=1.0
    )
    
    if success:
        print(f"✓ Audio saved to: {output_file}")
        print(f"  File size: {os.path.getsize(output_file)} bytes")
    else:
        print("✗ Failed")


def example_config():
    """Example: Configuration management"""
    print("\n" + "="*60)
    print("Example 3: Configuration Management")
    print("="*60)
    
    config = get_config_manager()
    
    print("Default TTS settings:")
    engine = config.get('default_settings.tts.engine', 'unknown')
    language = config.get('default_settings.tts.language', 'unknown')
    speed = config.get('default_settings.tts.speed', 1.0)
    
    print(f"  Engine: {engine}")
    print(f"  Language: {language}")
    print(f"  Speed: {speed}x")
    
    print("\nOutput paths:")
    print(f"  TTS: {config.get_output_path('tts')}")
    print(f"  STT: {config.get_output_path('stt')}")
    print(f"  Dubbed videos: {config.get_output_path('dubbed_videos')}")


def example_multilingual_tts():
    """Example: Multi-language TTS"""
    print("\n" + "="*60)
    print("Example 4: Multi-language Text-to-Speech")
    print("="*60)
    
    engine = GTTSEngine()
    
    texts = {
        'en': 'Hello, how are you?',
        'ko': '안녕하세요, 어떻게 지내세요?',
        'ja': 'こんにちは、お元気ですか？',
        'es': '¡Hola! ¿Cómo estás?',
        'fr': 'Bonjour, comment allez-vous?',
    }
    
    for lang, text in texts.items():
        output_file = f"output/tts/example_{lang}.mp3"
        print(f"\n{lang.upper()}: {text}")
        
        success = engine.synthesize(
            text=text,
            output_path=output_file,
            language=lang
        )
        
        if success:
            print(f"  ✓ Saved to {output_file}")
        else:
            print(f"  ✗ Failed")


def example_audio_file_check():
    """Example: Check output directory"""
    print("\n" + "="*60)
    print("Example 5: Check Generated Files")
    print("="*60)
    
    output_dir = "output/tts"
    
    if not os.path.exists(output_dir):
        print(f"Directory {output_dir} does not exist")
        return
    
    files = [f for f in os.listdir(output_dir) if f.endswith(('.mp3', '.wav'))]
    
    if not files:
        print("No audio files found")
        return
    
    print(f"Found {len(files)} audio file(s):")
    for file in files:
        filepath = os.path.join(output_dir, file)
        size = os.path.getsize(filepath)
        print(f"  • {file} ({size:,} bytes)")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("Voice Service Integrated Suite - Example Usage")
    print("="*70)
    
    # Setup logger
    setup_logger()
    
    # Run examples
    try:
        example_config()
        example_tts_gtts()
        example_tts_pyttsx3()
        example_multilingual_tts()
        example_audio_file_check()
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
    except Exception as e:
        print(f"\n\nError running examples: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)
    print("Examples completed!")
    print("To use the GUI, run: python main.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
