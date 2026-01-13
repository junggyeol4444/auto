# Smart Video Editor Pro - Architecture Documentation

## Overview

Smart Video Editor Pro is a desktop application for automated video editing that learns editing styles from YouTube videos and applies those patterns offline without requiring AI APIs.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    GUI Layer (PyQt5)                     │
│  ┌──────────────────┐       ┌──────────────────┐        │
│  │  Learning Tab    │       │   Editing Tab    │        │
│  └──────────────────┘       └──────────────────┘        │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Business Logic Layer                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│  │  Style     │  │   Video    │  │  Profile   │        │
│  │  Learner   │  │  Editor    │  │  Manager   │        │
│  └────────────┘  └────────────┘  └────────────┘        │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Core Processing Layer                   │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ Video   │  │  Scene   │  │  Audio   │  │ YouTube │ │
│  │Processor│  │ Detector │  │ Analyzer │  │Download │ │
│  └─────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Data Layer (SQLite)                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│  │  Profiles  │  │   Scene    │  │   Audio    │        │
│  │            │  │  Patterns  │  │  Patterns  │        │
│  └────────────┘  └────────────┘  └────────────┘        │
└─────────────────────────────────────────────────────────┘
```

## Component Details

### 1. GUI Layer (`src/gui/`)

**main_window.py**
- Main application window using PyQt5
- Tabbed interface with Learning and Editing tabs
- Worker threads for background processing
- Progress tracking and logging

**Components:**
- `MainWindow`: Main application window
- `LearningTab`: Interface for downloading and learning from videos
- `EditingTab`: Interface for editing videos with learned patterns
- `WorkerThread`: Background thread for long-running operations

### 2. Core Processing Layer (`src/core/`)

**video_downloader.py**
- Downloads YouTube videos using yt-dlp
- Retrieves video metadata
- Progress callback support

**scene_detector.py**
- Detects scene changes using OpenCV
- Analyzes frame differences
- Calculates scene statistics (duration, frequency)
- Configurable sensitivity threshold

**audio_analyzer.py**
- Extracts audio from video files
- Detects voice/speech segments
- Identifies silence periods
- Calculates audio statistics
- Uses pydub for audio processing

**style_learner.py**
- Orchestrates scene and audio analysis
- Learns editing patterns from videos
- Stores patterns in database
- Retrieves learned patterns for editing

**video_editor.py**
- Applies learned patterns to edit videos
- Removes silence based on learned thresholds
- Concatenates video segments
- Uses moviepy for video editing

### 3. Data Layer (`src/database/`)

**models.py**
- SQLAlchemy ORM models
- Database management
- Profile CRUD operations

**Database Schema:**

```
EditingProfile
├── id (PK)
├── name (unique)
├── description
├── created_at
├── updated_at
└── Relationships:
    ├── scene_patterns (1:N)
    └── audio_patterns (1:N)

ScenePattern
├── id (PK)
├── profile_id (FK)
├── avg_scene_duration
├── min_scene_duration
├── max_scene_duration
└── scene_change_threshold

AudioPattern
├── id (PK)
├── profile_id (FK)
├── silence_threshold
├── min_silence_duration
├── speech_padding_before
└── speech_padding_after
```

## Data Flow

### Learning Flow

1. **User Input**: YouTube URL + Profile Name
2. **Download**: yt-dlp downloads video to temp directory
3. **Scene Analysis**: OpenCV processes video frames
   - Compares consecutive frames
   - Detects significant changes
   - Calculates timing statistics
4. **Audio Analysis**: pydub processes audio
   - Detects voice vs silence
   - Measures segment durations
   - Calculates audio statistics
5. **Pattern Storage**: SQLAlchemy saves to database
   - Scene patterns (timings, thresholds)
   - Audio patterns (silence detection parameters)
6. **Output**: Profile saved for future use

### Editing Flow

1. **User Input**: Video file + Profile selection
2. **Pattern Retrieval**: Load learned patterns from database
3. **Audio Extraction**: moviepy extracts audio from input video
4. **Segment Detection**: Apply learned thresholds
   - Detect voice segments
   - Identify silence to remove
5. **Video Editing**: moviepy cuts and concatenates
   - Create clips for voice segments
   - Add padding around speech
   - Concatenate all clips
6. **Export**: Write final video with H.264/AAC codecs

## Technology Stack

### Core Libraries

| Library | Purpose | Usage |
|---------|---------|-------|
| PyQt5 | GUI framework | Main window, tabs, widgets, threading |
| moviepy | Video processing | Video I/O, cutting, concatenation |
| OpenCV | Computer vision | Frame analysis, scene detection |
| pydub | Audio processing | Audio analysis, segment detection |
| yt-dlp | YouTube downloader | Video downloading, metadata extraction |
| SQLAlchemy | ORM | Database models, queries |
| NumPy | Numerical computing | Array operations, statistics |
| SciPy | Scientific computing | Signal processing support |
| PyInstaller | Executable builder | Windows .exe generation |

### File Formats

**Input:**
- Video: MP4, AVI, MKV, MOV, FLV, WMV, WebM
- Audio: WAV (extracted), M4A, MP3

**Output:**
- Video: MP4 (H.264 video, AAC audio)
- Database: SQLite (.db)

## Performance Considerations

### Processing Time

- **Download**: Depends on video size and internet speed
- **Scene Detection**: ~1-2 minutes per 10 minutes of video
- **Audio Analysis**: ~30-60 seconds per 10 minutes of video
- **Video Editing**: ~2-3 minutes per 10 minutes of video

### Resource Usage

- **CPU**: Intensive during video processing
- **Memory**: ~500MB-2GB depending on video size
- **Storage**: 2-3x input video size temporarily
- **GPU**: Not utilized (can be future enhancement)

### Optimization Strategies

1. **Frame Sampling**: Process every Nth frame for scene detection
2. **Progressive Processing**: Show progress to user
3. **Temp File Management**: Clean up after processing
4. **Batch Operations**: Process multiple clips in memory
5. **Codec Selection**: Use hardware-accelerated H.264

## Error Handling

### Common Errors

1. **Download Failures**
   - Network issues
   - Invalid URLs
   - Age-restricted content
   - Geographic restrictions

2. **Processing Errors**
   - Corrupted video files
   - Unsupported formats
   - Insufficient disk space
   - FFmpeg not found

3. **Database Errors**
   - Duplicate profile names
   - Database locked
   - Corrupted database

### Error Recovery

- User-friendly error messages
- Detailed logging for debugging
- Graceful degradation
- Automatic cleanup of temp files

## Security Considerations

1. **Input Validation**
   - URL validation before downloading
   - File path sanitization
   - Profile name validation

2. **Resource Limits**
   - Maximum video duration checks
   - Disk space validation
   - Memory usage monitoring

3. **Data Privacy**
   - All processing done offline
   - No data sent to external servers
   - Local database storage only

## Future Enhancements

### Planned Features

1. **OCR Subtitles**
   - Extract text from video frames
   - Analyze subtitle patterns
   - Generate subtitles for new videos

2. **Effect Recognition**
   - Detect transitions and effects
   - Learn effect timing patterns
   - Apply similar effects

3. **Batch Processing**
   - Process multiple videos at once
   - Queue management
   - Progress tracking for all jobs

4. **Community Profiles**
   - Export/import profiles
   - Share profiles with community
   - Profile marketplace

5. **Advanced Editing**
   - Music detection and preservation
   - Multi-track audio handling
   - Color grading patterns
   - Thumbnail generation

### Technical Improvements

1. **GPU Acceleration**
   - Use CUDA for video processing
   - Faster scene detection
   - Real-time preview

2. **Machine Learning**
   - Neural network for scene detection
   - Audio classification models
   - Style transfer

3. **Cloud Integration** (optional)
   - Cloud storage for profiles
   - Collaborative editing
   - Remote processing

## Building and Deployment

### Development Setup

```bash
# Clone repository
git clone https://github.com/junggyeol4444/auto.git
cd auto

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Building Windows Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller build.spec

# Output location
dist/SmartVideoEditorPro.exe
```

### Distribution

1. **Standalone Executable**: Single .exe file (large, ~200-300MB)
2. **Installer**: NSIS or Inno Setup installer
3. **Portable**: ZIP archive with all dependencies

## Testing Strategy

### Unit Tests
- Database operations
- Scene detection algorithms
- Audio analysis functions
- Pattern calculations

### Integration Tests
- End-to-end learning flow
- End-to-end editing flow
- Error handling scenarios

### Manual Testing
- GUI responsiveness
- Progress feedback
- Various video formats
- Edge cases (very short/long videos)

## Maintenance

### Logging
- Application logs stored in `logs/` directory
- Different log levels (DEBUG, INFO, WARNING, ERROR)
- Rotation to prevent large log files

### Updates
- Check for library updates regularly
- Test with new Python versions
- Keep yt-dlp updated for YouTube compatibility

### Support
- GitHub Issues for bug reports
- Documentation in README and USAGE guides
- Example videos and tutorials

## Conclusion

Smart Video Editor Pro provides a solid foundation for automated video editing based on learned patterns. The modular architecture allows for easy extension and enhancement while maintaining offline functionality and user privacy.
