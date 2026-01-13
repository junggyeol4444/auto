# Installation Guide

## Prerequisites

### Python Requirements
- Python 3.8 or higher
- pip package manager

### System Requirements

#### For GUI (Required)
The application uses CustomTkinter for the graphical user interface, which requires tkinter.

**Windows:**
- tkinter is included with Python by default

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
- tkinter is included with Python by default

#### For Video Processing (Required for Dubbing)
**FFmpeg** is required for video/audio processing.

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract and add to PATH

**Linux:**
```bash
sudo apt-get install ffmpeg  # Ubuntu/Debian
sudo dnf install ffmpeg       # Fedora/RHEL
```

**macOS:**
```bash
brew install ffmpeg
```

#### For Offline TTS (Optional)
**eSpeak** or **eSpeak-NG** for pyttsx3 offline TTS.

**Linux:**
```bash
sudo apt-get install espeak  # or espeak-ng
```

**Windows:**
- Download from http://espeak.sourceforge.net/

**macOS:**
```bash
brew install espeak
```

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/junggyeol4444/auto.git
cd auto
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/macOS
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Note:** This will install all dependencies. Some heavy packages like PyTorch may take several minutes.

### 4. Verify Installation
```bash
python test_installation.py
```

This script will test all modules and report any missing dependencies.

### 5. Configure API Keys (Optional)
For premium features, you'll need to configure API keys:

1. Copy `config.json` template (already present)
2. Run the application: `python main.py`
3. Click "⚙ Settings" and enter your API keys:
   - **Azure Speech API Key & Region** (for Azure TTS)
   - **Google Cloud Credentials Path** (for Google Cloud TTS/STT)
   - **DeepL API Key** (for DeepL translation)

## Running the Application

```bash
python main.py
```

## Minimal Installation (Core Features Only)

If you want to install only core dependencies without heavy packages:

```bash
# Core TTS/STT
pip install loguru customtkinter gtts pyttsx3 pydub

# For basic audio processing
pip install librosa soundfile

# For translation
pip install deep-translator
```

Then install additional features as needed:
```bash
# For Whisper STT
pip install openai-whisper

# For Azure TTS
pip install azure-cognitiveservices-speech

# For Google Cloud
pip install google-cloud-texttospeech google-cloud-speech

# For advanced audio processing
pip install pyloudnorm spleeter demucs df-py
```

## Troubleshooting

### "No module named 'tkinter'"
- Install tkinter system package (see Prerequisites above)
- On some systems: `python3-tk` or `python3-tkinter`

### "Failed to initialize pyttsx3"
- Install eSpeak or eSpeak-NG (see Prerequisites above)
- Restart your terminal after installation

### "FFmpeg not found"
- Install FFmpeg and ensure it's in your PATH
- Test with: `ffmpeg -version`

### "CUDA not available" (for GPU acceleration)
- Install CUDA toolkit from NVIDIA
- Install PyTorch with CUDA support:
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Use a virtual environment to avoid conflicts
- Check Python version: `python --version` (should be 3.8+)

## Feature Availability

### Always Available (Free, No API Keys)
- ✅ gTTS (Text-to-Speech) - requires internet
- ✅ pyttsx3 (Offline TTS) - requires eSpeak
- ✅ Basic audio processing
- ✅ Translation (Google Translate via deep-translator)

### Requires Installation
- ⚙️ Whisper STT - `pip install openai-whisper`
- ⚙️ Advanced audio processing - see requirements.txt

### Requires API Keys
- 🔑 Azure Text-to-Speech
- 🔑 Google Cloud TTS/STT
- 🔑 DeepL Translation (premium)

### Experimental/Placeholder
- 🚧 Voice Cloning (RVC) - requires additional setup
- 🚧 Real-time STT - requires microphone access

## Getting Help

If you encounter issues:
1. Check this installation guide
2. Run `python test_installation.py` to diagnose problems
3. Check the logs in `logs/` directory
4. Open an issue on GitHub with error details
