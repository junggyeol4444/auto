"""
Test script to verify Voice Service Integrated Suite installation
"""
import sys
import os

def test_imports():
    """Test all module imports."""
    print("=" * 60)
    print("Voice Service Integrated Suite - Installation Test")
    print("=" * 60)
    print()
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Utilities
    print("[ 1/10 ] Testing utility modules...")
    try:
        from utils.logger import setup_logger, get_logger
        from utils.config_manager import ConfigManager, get_config_manager
        from utils.file_handler import FileHandler
        print("         ✓ Utilities imported successfully")
        tests_passed += 1
    except Exception as e:
        print(f"         ✗ Failed to import utilities: {e}")
        tests_failed += 1
    
    # Test 2: TTS Modules
    print("[ 2/10 ] Testing TTS modules...")
    try:
        from modules.tts.gtts_engine import GTTSEngine
        from modules.tts.pyttsx3_engine import Pyttsx3Engine
        from modules.tts.azure_tts import AzureTTSEngine
        from modules.tts.google_cloud_tts import GoogleCloudTTSEngine
        from modules.tts.emotion_tts import EmotionTTS
        print("         ✓ TTS modules imported successfully")
        tests_passed += 1
    except Exception as e:
        print(f"         ✗ Failed to import TTS modules: {e}")
        tests_failed += 1
    
    # Test 3: STT Modules
    print("[ 3/10 ] Testing STT modules...")
    try:
        from modules.stt.whisper_stt import WhisperSTT
        from modules.stt.google_cloud_stt import GoogleCloudSTT
        from modules.stt.realtime_stt import RealtimeSTT
        print("         ✓ STT modules imported successfully")
        tests_passed += 1
    except Exception as e:
        print(f"         ✗ Failed to import STT modules: {e}")
        tests_failed += 1
    
    # Test 4: Dubbing Modules
    print("[ 4/10 ] Testing dubbing modules...")
    try:
        from modules.dubbing.video_dubbing import VideoDubbing
        from modules.dubbing.translation import TranslationService
        from modules.dubbing.lipsync import LipSync
        print("         ✓ Dubbing modules imported successfully")
        tests_passed += 1
    except Exception as e:
        print(f"         ✗ Failed to import dubbing modules: {e}")
        tests_failed += 1
    
    # Test 5: Voice Cloning Modules
    print("[ 5/10 ] Testing voice cloning modules...")
    try:
        from modules.voice_cloning.rvc_trainer import RVCTrainer
        from modules.voice_cloning.voice_converter import VoiceConverter
        from modules.voice_cloning.data_processor import DataProcessor
        print("         ✓ Voice cloning modules imported successfully")
        tests_passed += 1
    except Exception as e:
        print(f"         ✗ Failed to import voice cloning modules: {e}")
        tests_failed += 1
    
    # Test 6: Audio Processing Modules
    print("[ 6/10 ] Testing audio processing modules...")
    try:
        from modules.audio_processing.noise_remover import NoiseRemover
        from modules.audio_processing.source_separator import SourceSeparator
        from modules.audio_processing.normalizer import Normalizer
        from modules.audio_processing.volume_controller import VolumeController
        print("         ✓ Audio processing modules imported successfully")
        tests_passed += 1
    except Exception as e:
        print(f"         ✗ Failed to import audio processing modules: {e}")
        tests_failed += 1
    
    # Test 7: GUI Modules
    print("[ 7/10 ] Testing GUI modules...")
    try:
        from gui.main_window import MainWindow
        from gui.tts_tab import TTSTab
        from gui.stt_tab import STTTab
        from gui.dubbing_tab import DubbingTab
        from gui.voice_cloning_tab import VoiceCloningTab
        from gui.audio_processing_tab import AudioProcessingTab
        from gui.settings_window import SettingsWindow
        print("         ✓ GUI modules imported successfully")
        tests_passed += 1
    except Exception as e:
        print(f"         ✗ Failed to import GUI modules: {e}")
        tests_failed += 1
    
    # Test 8: Directory Structure
    print("[ 8/10 ] Testing directory structure...")
    required_dirs = [
        'modules', 'gui', 'utils', 'models', 'output', 'cache',
        'modules/tts', 'modules/stt', 'modules/dubbing',
        'modules/voice_cloning', 'modules/audio_processing',
        'output/tts', 'output/stt', 'output/dubbed_videos', 'output/processed_audio'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.isdir(dir_path):
            missing_dirs.append(dir_path)
    
    if not missing_dirs:
        print("         ✓ All directories exist")
        tests_passed += 1
    else:
        print(f"         ✗ Missing directories: {', '.join(missing_dirs)}")
        tests_failed += 1
    
    # Test 9: Configuration
    print("[ 9/10 ] Testing configuration...")
    try:
        if os.path.exists('config.json'):
            from utils.config_manager import get_config_manager
            config = get_config_manager()
            print("         ✓ Configuration loaded successfully")
            tests_passed += 1
        else:
            print("         ✗ config.json not found")
            tests_failed += 1
    except Exception as e:
        print(f"         ✗ Failed to load configuration: {e}")
        tests_failed += 1
    
    # Test 10: Main Entry Point
    print("[10/10 ] Testing main entry point...")
    try:
        if os.path.exists('main.py'):
            print("         ✓ main.py exists")
            tests_passed += 1
        else:
            print("         ✗ main.py not found")
            tests_failed += 1
    except Exception as e:
        print(f"         ✗ Failed to check main.py: {e}")
        tests_failed += 1
    
    # Summary
    print()
    print("=" * 60)
    print(f"Test Results: {tests_passed}/10 passed, {tests_failed}/10 failed")
    print("=" * 60)
    
    if tests_passed == 10:
        print("✓ All tests passed! Installation is complete.")
        print()
        print("To run the application:")
        print("  python main.py")
        print()
        print("Note: Some features require additional dependencies:")
        print("  - Whisper STT: pip install openai-whisper")
        print("  - Azure TTS: Configure API key in Settings")
        print("  - Google Cloud: Configure credentials in Settings")
        print("  - FFmpeg: Install system package for video processing")
        return 0
    else:
        print("✗ Some tests failed. Please check error messages above.")
        return 1


if __name__ == "__main__":
    sys.exit(test_imports())
