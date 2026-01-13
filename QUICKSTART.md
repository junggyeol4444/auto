# Quick Start Guide

## Installation

1. Install Python 3.8 or higher
2. Clone the repository and navigate to it:
   ```bash
   cd auto
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### GUI Mode (Recommended)
```bash
python main.py
```

The application will open with a modern GUI interface with the following tabs:
- **Subtitles**: Translate SRT, VTT, and ASS subtitle files
- **Documents**: Translate DOCX, PDF, PPTX, and XLSX files
- **Web**: Translate HTML files, URLs, and localization files
- **Text**: Direct text translation with auto-detection
- **Real-time**: Demo mode for real-time translation

### Headless Mode (Examples)
```bash
python examples.py
```

Run this to see working examples without the GUI.

### Testing
```bash
python test_core.py
```

Validates core functionality is working properly.

## First Time Setup

1. **Run the application**: `python main.py`
2. **Click "Settings"** button in the top right
3. **Configure API keys** (optional but recommended):
   - DeepL: For best Korean-English translation quality
   - Papago: For Korean-Japanese translation
   - OpenAI: For context-aware technical translation
   - Google: Uses free googletrans library (no key needed)

4. **Set default languages** and preferences
5. **Click "Save"**

## Quick Usage Examples

### Translate Subtitles
1. Go to "Subtitles" tab
2. Click "Browse" and select an SRT/VTT/ASS file
3. Select source and target languages
4. Choose translation engine (or "auto")
5. Click "Translate"
6. Review preview and click "Save Translated File"

### Translate Documents
1. Go to "Documents" tab
2. Click "Browse" and select a DOCX/PDF/PPTX/XLSX file
3. Select languages and domain (general/medical/legal/it)
4. Click "Translate Document"
5. Choose save location

### Translate Text
1. Go to "Text" tab
2. Type or paste text (or load from file)
3. Select languages (use "auto" for source detection)
4. Click "Translate" button (→)
5. Copy or save the result

## Tips

- **No API keys needed to start**: Google Translate works without configuration
- **Domain glossaries**: Select medical/legal/IT for specialized terminology
- **Cache system**: Translations are cached to reduce API calls
- **Batch processing**: Subtitle and document translators work in batches for efficiency

## Troubleshooting

### "Translation engine not available"
- Configure API keys in Settings
- Or select "google" engine which works without keys

### "googletrans not available"
```bash
pip install googletrans==4.0.0rc1
```

### GUI doesn't start
```bash
pip install customtkinter
```

### Module import errors
```bash
pip install -r requirements.txt
```

## What Works Out of the Box

Without any API keys configured, you can:
- ✓ Test all subtitle parsing (SRT, VTT, ASS)
- ✓ Use document structure (load/save files)
- ✓ Load and apply domain glossaries
- ✓ Use translation cache
- ✓ View the GUI interface

With Google Translate (free):
- ✓ Translate text between 100+ languages
- ✓ Translate subtitles
- ✓ Translate documents
- ✓ Translate web content

With Premium APIs (requires keys):
- ✓ Higher quality translations
- ✓ Better handling of technical terms
- ✓ Faster processing
- ✓ More language pairs

## Next Steps

1. Start with the built-in examples: `python examples.py`
2. Test the GUI: `python main.py`
3. Try translating a subtitle file
4. Configure API keys for better quality
5. Build EXE: `pyinstaller build.spec`

For detailed documentation, see README.md
