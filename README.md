# Smart Video Editor Pro

> 📖 **한국어 문서**: [README_KR.md](README_KR.md) | [QUICKSTART_KR.md](QUICKSTART_KR.md) | [RUN_GUIDE_KR.md](RUN_GUIDE_KR.md)

**Smart Video Editor Pro** is a Windows desktop application that automates video editing tasks entirely offline. It learns editing styles from YouTube videos and applies those patterns to your own videos.

## 🚀 Quick Start (Recommended)

### Windows
1. Download/clone the repository
2. **Double-click `run.bat`**
3. First run: automatic setup
4. Application starts!

### macOS/Linux
1. Download/clone the repository
2. Terminal: **`./run.sh`**
3. First run: automatic setup
4. Application starts!

> 📘 Detailed guide: [RUN_GUIDE_KR.md](RUN_GUIDE_KR.md) (Korean)

## Features

### Phase 1 (MVP) - Implemented
- ✅ **YouTube Video Downloader**: Download videos to learn editing styles using yt-dlp
- ✅ **Scene Change Detection**: Automatically detect scene transitions and analyze cut timing
- ✅ **Voice Segment Detection**: Identify speech segments and their timing in videos
- ✅ **Silence Removal**: Automatically remove silent parts from videos
- ✅ **Pattern Learning**: Analyze videos and store editing patterns in a database
- ✅ **Profile Management**: Save and load editing profiles for different styles
- ✅ **Video Editing**: Apply learned patterns to edit new videos
- ✅ **User-Friendly GUI**: Intuitive tabbed interface for learning and editing

### Future Enhancements
- OCR-based subtitle generation and analysis
- Advanced effect pattern recognition
- Batch video processing
- Community profile sharing
- Thumbnail generation
- Additional editing styles

## Technology Stack

- **Python 3.8+**: Core programming language
- **PyQt5**: GUI framework
- **moviepy**: Video processing and editing
- **OpenCV**: Scene change detection
- **pydub**: Audio analysis and processing
- **yt-dlp**: YouTube video downloading
- **SQLAlchemy**: Database management
- **PyInstaller**: Windows executable creation

## Installation

### Option 1: Run from Source

1. **Prerequisites**:
   - Python 3.8 or higher
   - FFmpeg (required by moviepy)

2. **Clone the repository**:
   ```bash
   git clone https://github.com/junggyeol4444/auto.git
   cd auto
   ```

3. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

### Option 2: Build Windows Executable

1. **Follow steps 1-4 from Option 1**

2. **Build executable**:
   ```bash
   # On Windows
   build.bat
   
   # Or manually
   pyinstaller build.spec
   ```

3. **Run the executable**:
   ```
   dist\SmartVideoEditorPro.exe
   ```

## Usage Guide

### Learning from YouTube Videos

1. **Open the "Learn Style" tab**
2. **Enter a YouTube URL** of a video with the editing style you want to learn
3. **Click "Download Video"** to download the video
4. **Enter a profile name** (e.g., "MrBeast Style", "MKBHD Style")
5. **Click "Learn Style"** to analyze the video and save patterns
6. The application will:
   - Detect scene changes and calculate timing patterns
   - Analyze audio to identify voice segments and silence
   - Store the learned patterns in the database

### Editing Your Videos

1. **Open the "Edit Video" tab**
2. **Browse and select your input video**
3. **Select a learned profile** from the dropdown
4. **Choose editing options**:
   - ☑️ Remove Silence: Automatically cut out silent portions
5. **Specify output video location**
6. **Click "Edit Video"** to process
7. Wait for the processing to complete

### Profile Management

- Profiles are automatically saved when you learn from a video
- Use the "Refresh Profiles" button to update the profile list
- Each profile contains:
  - Scene change patterns (timing, durations, thresholds)
  - Audio patterns (silence detection, speech padding)

## Project Structure

```
auto/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── build.spec                       # PyInstaller configuration
├── build.bat                        # Windows build script
├── src/
│   ├── core/                        # Core functionality
│   │   ├── video_downloader.py      # YouTube downloader
│   │   ├── scene_detector.py        # Scene change detection
│   │   ├── audio_analyzer.py        # Audio/voice analysis
│   │   ├── style_learner.py         # Pattern learning
│   │   └── video_editor.py          # Video editing engine
│   ├── database/                    # Database layer
│   │   └── models.py                # SQLAlchemy models
│   └── gui/                         # User interface
│       └── main_window.py           # Main GUI window
├── data/                            # Data directory
│   ├── profiles/                    # Saved profiles
│   └── temp/                        # Temporary files
└── README.md                        # This file
```

## How It Works

### Learning Phase
1. **Download**: Uses yt-dlp to download YouTube videos
2. **Analyze Scenes**: OpenCV processes frames to detect scene changes
3. **Analyze Audio**: Pydub analyzes audio to find voice and silence segments
4. **Extract Patterns**: Calculates statistics about timing, durations, and thresholds
5. **Store**: Saves patterns to SQLite database for later use

### Editing Phase
1. **Load Profile**: Retrieves learned patterns from database
2. **Analyze Input**: Processes your video using the same algorithms
3. **Apply Patterns**: Uses learned thresholds and timings to make cuts
4. **Remove Silence**: Intelligently removes quiet sections while preserving speech
5. **Export**: Combines edited segments into final video

## Requirements

- **Operating System**: Windows 10/11 (primary target), also works on macOS/Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB for application + space for videos
- **FFmpeg**: Required for video processing

## Troubleshooting

### FFmpeg Not Found
If you get "FFmpeg not found" errors:
- **Windows**: Download from https://ffmpeg.org and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

### PyQt5 Issues
If GUI doesn't start:
```bash
pip install --upgrade PyQt5
```

### Video Processing Errors
- Ensure input video is in a supported format (MP4, AVI, MKV, MOV)
- Check that you have enough disk space for output
- Try with a shorter video first

## Development

### Running Tests
```bash
# Unit tests (when implemented)
pytest tests/
```

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source. See LICENSE file for details.

## Acknowledgments

- **yt-dlp**: YouTube video downloading
- **moviepy**: Video editing capabilities
- **OpenCV**: Computer vision tools
- **PyQt5**: GUI framework
- All open-source contributors

## Contact

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Note**: This application is for educational and personal use. Always respect copyright laws and YouTube's Terms of Service when downloading videos.