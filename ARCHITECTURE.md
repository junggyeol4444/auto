# Voice Service Integrated Suite - Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     VOICE SERVICE INTEGRATED SUITE                       │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                         GUI Layer (CustomTkinter)                │   │
│  │  ┌──────────┬──────────┬──────────┬──────────┬───────────────┐ │   │
│  │  │   TTS    │   STT    │ Dubbing  │  Voice   │     Audio     │ │   │
│  │  │   Tab    │   Tab    │   Tab    │ Cloning  │  Processing   │ │   │
│  │  └──────────┴──────────┴──────────┴──────────┴───────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                   │                                      │
│  ─────────────────────────────────┼──────────────────────────────────  │
│                                   │                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                         Core Modules                             │   │
│  │                                                                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐│   │
│  │  │    TTS      │  │    STT      │  │       Dubbing           ││   │
│  │  ├─────────────┤  ├─────────────┤  ├─────────────────────────┤│   │
│  │  │ • gTTS      │  │ • Whisper   │  │ • Video Processing      ││   │
│  │  │ • pyttsx3   │  │ • Google    │  │ • Translation           ││   │
│  │  │ • Azure     │  │ • Realtime  │  │ • Audio Mixing          ││   │
│  │  │ • Google    │  │             │  │ • Lip Sync              ││   │
│  │  │ • Emotion   │  │             │  │                         ││   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘│   │
│  │                                                                   │   │
│  │  ┌─────────────────────────┐  ┌────────────────────────────────┐│  │
│  │  │   Audio Processing      │  │     Voice Cloning (RVC)        ││  │
│  │  ├─────────────────────────┤  ├────────────────────────────────┤│  │
│  │  │ • Noise Removal         │  │ • Trainer (Placeholder)        ││  │
│  │  │ • Source Separation     │  │ • Converter (Placeholder)      ││  │
│  │  │ • LUFS Normalization    │  │ • Data Processor (Placeholder) ││  │
│  │  │ • Volume Control        │  │                                ││  │
│  │  └─────────────────────────┘  └────────────────────────────────┘│  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                   │                                      │
│  ─────────────────────────────────┼──────────────────────────────────  │
│                                   │                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                         Utilities Layer                          │   │
│  │  ┌──────────────┬──────────────────┬─────────────────────────┐ │   │
│  │  │   Logger     │ Config Manager   │     File Handler        │ │   │
│  │  ├──────────────┼──────────────────┼─────────────────────────┤ │   │
│  │  │ • Loguru     │ • JSON Config    │ • File Validation       │ │   │
│  │  │ • Rotation   │ • Dot Notation   │ • Format Detection      │ │   │
│  │  │ • Console    │ • API Keys       │ • Path Management       │ │   │
│  │  └──────────────┴──────────────────┴─────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                   │                                      │
│  ─────────────────────────────────┼──────────────────────────────────  │
│                                   │                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    External Dependencies                         │   │
│  │  ┌─────────────┬──────────────┬──────────────┬────────────────┐│   │
│  │  │   FFmpeg    │   Python     │   Optional   │    System      ││   │
│  │  │  (Video/    │  Libraries   │  Cloud APIs  │   Packages     ││   │
│  │  │   Audio)    │              │              │                ││   │
│  │  ├─────────────┼──────────────┼──────────────┼────────────────┤│   │
│  │  │ • Encoding  │ • torch      │ • Azure      │ • tkinter      ││   │
│  │  │ • Decoding  │ • whisper    │ • Google     │ • espeak       ││   │
│  │  │ • Mixing    │ • librosa    │ • DeepL      │                ││   │
│  │  └─────────────┴──────────────┴──────────────┴────────────────┘│   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘

DATA FLOW:
──────────

TTS Flow:
Text Input → Engine Selection → API/Local Processing → Audio Output → File Save

STT Flow:
Audio Input → Model Loading → Transcription → Text/SRT Output → File Save

Dubbing Flow:
Video → Audio Extract → STT → Translation → TTS → Audio Mix → Video Combine

Audio Processing Flow:
Audio Input → Processing Module → Algorithm Application → Enhanced Output

FEATURES BY CATEGORY:
──────────────────

🎤 TTS (Text-to-Speech)
   ├── Free: gTTS (40+ languages)
   ├── Offline: pyttsx3
   ├── Premium: Azure TTS, Google Cloud TTS
   └── Special: Emotion TTS with SSML

🎙️ STT (Speech-to-Text)
   ├── Local: Whisper (100+ languages)
   ├── Cloud: Google Cloud STT
   └── Live: Real-time microphone transcription

🎬 Video Dubbing
   ├── Complete pipeline: extract → transcribe → translate → TTS → mix
   ├── Translation: Google Translate, DeepL
   └── Audio mixing with volume control

🔊 Audio Processing
   ├── AI Noise Removal (DeepFilterNet)
   ├── Source Separation (Spleeter, Demucs)
   ├── LUFS Normalization (-16 LUFS standard)
   └── Volume Control (gain, fades, compression)

🎭 Voice Cloning (Experimental)
   └── RVC framework placeholders

SUPPORTED FORMATS:
────────────────

Input:
  Audio:  MP3, WAV, M4A, FLAC, OGG, AAC
  Video:  MP4, MKV, AVI, MOV, WMV, FLV
  Text:   TXT, SRT, VTT

Output:
  Audio:  MP3, WAV
  Video:  MP4
  Text:   TXT, SRT

DEPLOYMENT OPTIONS:
─────────────────

1. GUI Application (main.py)
   - Full-featured graphical interface
   - Tab-based navigation
   - Real-time progress tracking
   - Settings configuration

2. Programmatic Use (modules)
   - Import as Python libraries
   - Scriptable workflows
   - Custom integrations
   - API development ready

3. Command Line (examples.py)
   - Batch processing
   - Automation scripts
   - Testing and validation
```

## Module Interaction Diagram

```
┌───────────────┐
│  main.py      │  Application Entry Point
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  GUI Layer    │  User Interface
└───────┬───────┘
        │
        ├─────────────────────────────────────────┐
        │                                         │
        ▼                                         ▼
┌───────────────┐                        ┌────────────────┐
│  TTS Module   │                        │  STT Module    │
├───────────────┤                        ├────────────────┤
│ • Engines     │◄───┐                   │ • Whisper      │
│ • Synthesis   │    │                   │ • Cloud        │
└───────┬───────┘    │                   └────────┬───────┘
        │            │                            │
        │     ┌──────┴─────────┐                 │
        │     │  Config        │                 │
        │     │  Manager       │                 │
        │     └────────────────┘                 │
        │            │                            │
        ▼            ▼                            ▼
┌───────────────────────────────────────────────────────┐
│              Utilities (Logger, File Handler)         │
└───────────────────────────────────────────────────────┘
```

## Quality Metrics

- **Code Coverage**: All major features implemented
- **Error Handling**: Comprehensive try-except blocks throughout
- **Logging**: Detailed logging at all levels
- **Documentation**: 3 comprehensive documentation files
- **Testing**: Installation verification script included
- **Modularity**: Clean separation of concerns
- **Extensibility**: Easy to add new engines and features
- **Maintainability**: Well-organized code structure
