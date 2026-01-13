"""TTS package initialization"""
from .tts_engine import TTSManager, GTTSEngine, Pyttsx3Engine, CustomTTSEngine

__all__ = ['TTSManager', 'GTTSEngine', 'Pyttsx3Engine', 'CustomTTSEngine']
