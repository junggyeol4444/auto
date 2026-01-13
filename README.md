# Voice Service Integrated Suite

A comprehensive voice service application integrating TTS (Text-to-Speech), STT (Speech-to-Text), video dubbing, voice cloning, and audio processing capabilities.

## 🌟 Features

### 1. Text-to-Speech (TTS)
- **Multiple Engines**: gTTS (free), pyttsx3 (offline), Azure TTS, Google Cloud TTS
- **40+ Languages**: Support for Korean, English, Japanese, Chinese, Spanish, French, German, and more
- **Voice Customization**: 
  - Male/Female voice selection
  - Speed, pitch, and volume control
  - Emotion-based speech (joy, sadness, anger, neutral)
- **SSML Support**: Advanced speech synthesis with emotion tags

### 2. Speech-to-Text (STT)
- **Whisper (OpenAI)**: High-quality local transcription
- **Google Cloud STT**: Cloud-based recognition (optional)
- **Real-time Recognition**: Live microphone input
- **Features**:
  - Automatic language detection (100+ languages)
  - Timestamp generation
  - SRT subtitle export
  - Speaker separation support

### 3. Video Dubbing
- **Complete Pipeline**:
  1. Audio extraction from video
  2. Speech-to-text transcription
  3. Translation to target language
  4. TTS generation
  5. Audio mixing with original
  6. Video synthesis
- **Features**:
  - Original audio volume control
  - Background music preservation
  - Lip sync timing adjustment

### 4. Voice Cloning (Placeholder)
- RVC (Retrieval-based Voice Conversion) framework
- Train custom voice models from samples
- Voice conversion and synthesis
- *Note: Requires additional RVC dependencies*

### 5. Audio Processing
- **Noise Removal**: DeepFilterNet AI-based noise reduction
- **Source Separation**: Spleeter/Demucs vocal/accompaniment separation
- **Volume Normalization**: LUFS-based loudness standardization (-16 LUFS)
- **Volume Control**: 
  - Gain adjustment
  - Fade in/out effects
  - Dynamic range compression
  - Audio mixing

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11, Linux, macOS
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended for Whisper large models)
- **Storage**: 5GB free space for models
- **GPU**: Optional but recommended for faster processing

### Dependencies
- FFmpeg (required for video/audio processing)
- See `requirements.txt` for Python packages

## 🚀 Installation

### 1. Clone Repository
```bash
git clone https://github.com/junggyeol4444/auto.git
cd auto
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

**Windows:**
- Download from https://ffmpeg.org/download.html
- Add to PATH environment variable

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### 4. Configure API Keys (Optional)

For premium features (Azure TTS, Google Cloud), configure API keys:

1. Run the application
2. Click "⚙ Settings" button
3. Enter your API keys:
   - Azure Speech API Key & Region
   - Google Cloud Credentials Path
   - DeepL API Key (for translation)

## 🎯 Usage

### Starting the Application

```bash
python main.py
```

### TTS (Text-to-Speech)

1. Navigate to the **TTS** tab
2. Enter or load text
3. Select engine, language, and voice settings
4. Adjust speed, pitch as needed
5. Click "🎤 Generate Speech"
6. Save the generated audio

### STT (Speech-to-Text)

1. Navigate to the **STT** tab
2. Click "📁 Select Audio" to choose an audio file
3. Select Whisper model size (tiny to large)
4. Choose language or use auto-detection
5. Click "🎙️ Transcribe"
6. Save as text or SRT subtitle file

### Video Dubbing

1. Navigate to the **Dubbing** tab
2. Click "📁 Select Video"
3. Set source and target languages
4. Adjust original audio volume (for background)
5. Click "🎬 Start Dubbing"
6. Wait for processing (progress shown)
7. Save the dubbed video

### Audio Processing

1. Navigate to the **Audio Processing** tab
2. Click "📁 Select Audio"
3. Choose processing type:
   - Noise Removal
   - Vocal/Accompaniment Separation
   - Volume Normalization
   - Volume Adjustment
4. Adjust settings (LUFS target, gain, etc.)
5. Click "⚙️ Process Audio"
6. Save the processed file

## 📁 Directory Structure

```
Voice_Service_Suite/
├── main.py                    # Application entry point
├── config.json                # Configuration file
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── modules/                   # Core functionality modules
│   ├── tts/                  # Text-to-Speech engines
│   ├── stt/                  # Speech-to-Text engines
│   ├── dubbing/              # Video dubbing
│   ├── voice_cloning/        # Voice cloning (placeholder)
│   └── audio_processing/     # Audio processing tools
│
├── gui/                       # GUI components
│   ├── main_window.py        # Main application window
│   ├── tts_tab.py           # TTS interface
│   ├── stt_tab.py           # STT interface
│   ├── dubbing_tab.py       # Dubbing interface
│   ├── voice_cloning_tab.py # Voice cloning interface
│   ├── audio_processing_tab.py # Audio processing interface
│   └── settings_window.py   # Settings dialog
│
├── utils/                     # Utility modules
│   ├── logger.py             # Logging utility
│   ├── config_manager.py     # Configuration management
│   └── file_handler.py       # File operations
│
├── models/                    # Model storage
│   ├── rvc/                  # RVC models
│   ├── whisper/              # Whisper models (auto-downloaded)
│   └── deepfilternet/        # DeepFilterNet models
│
├── output/                    # Output files
│   ├── tts/                  # TTS generated audio
│   ├── stt/                  # STT transcriptions
│   ├── dubbed_videos/        # Dubbed videos
│   └── processed_audio/      # Processed audio
│
├── cache/                     # Cache directory
└── logs/                      # Application logs
```

## ⚙️ Configuration

### config.json

```json
{
  "api_keys": {
    "azure_speech_key": "YOUR_KEY_HERE",
    "azure_speech_region": "eastus",
    "google_cloud_credentials_path": "/path/to/credentials.json",
    "deepl_api_key": "YOUR_KEY_HERE"
  },
  "default_settings": {
    "tts": {
      "engine": "gtts",
      "language": "en",
      "voice_gender": "female",
      "speed": 1.0,
      "pitch": 1.0
    },
    "stt": {
      "engine": "whisper",
      "whisper_model": "base",
      "language": "auto"
    },
    "audio_processing": {
      "target_lufs": -16,
      "sample_rate": 44100
    }
  }
}
```

## 🔧 Troubleshooting

### Common Issues

**1. FFmpeg not found**
- Ensure FFmpeg is installed and added to PATH
- Test with: `ffmpeg -version`

**2. Whisper model download fails**
- Check internet connection
- Models download automatically on first use
- Stored in `~/.cache/whisper/`

**3. Audio playback issues**
- Install audio codecs for your system
- Try different output formats (MP3, WAV)

**4. GPU not detected**
- Install CUDA for NVIDIA GPUs
- Install PyTorch with CUDA support
- Check: `torch.cuda.is_available()`

**5. Import errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Use virtual environment to avoid conflicts

## 📝 Supported Formats

### Input Formats
- **Audio**: MP3, WAV, M4A, FLAC, OGG, AAC
- **Video**: MP4, MKV, AVI, MOV, WMV, FLV
- **Text**: TXT, SRT, VTT

### Output Formats
- **Audio**: MP3, WAV
- **Video**: MP4
- **Subtitles**: SRT, TXT

## 🌐 Supported Languages

### TTS Languages (40+)
English, Korean, Japanese, Chinese (Simplified/Traditional), Spanish, French, German, Italian, Portuguese, Russian, Arabic, Hindi, Thai, Vietnamese, Indonesian, Turkish, Polish, Dutch, Swedish, and more...

### STT Languages (100+)
Automatic detection for all major world languages via Whisper

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

This project is provided as-is for educational and research purposes.

## 🙏 Acknowledgments

- **OpenAI Whisper**: Speech recognition
- **gTTS**: Google Text-to-Speech
- **Azure Cognitive Services**: Premium TTS
- **Google Cloud**: Premium TTS/STT
- **DeepFilterNet**: Noise reduction
- **Spleeter/Demucs**: Source separation
- **CustomTkinter**: Modern GUI framework

## 📧 Support

For issues and questions, please open an issue on GitHub.

## 🔮 Future Enhancements

- Full RVC voice cloning implementation
- Real-time dubbing preview
- Batch processing
- API server mode
- Web interface
- More language support
- Advanced lip-sync algorithms
- Voice effects and filters

---

**Version**: 1.0.0  
**Last Updated**: 2024