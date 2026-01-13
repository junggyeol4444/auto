# Translation Automation Platform

A comprehensive translation automation platform with GUI support for translating various content types including subtitles, documents, web content, and real-time text.

## Features

### 🎬 Subtitle Translation
- Support for **SRT**, **VTT**, and **ASS** subtitle formats
- Preserves timestamps and formatting
- Batch translation for efficient processing
- Subtitle length adjustment for optimal display

### 📚 Document Translation
- **DOCX**: Microsoft Word documents (preserves formatting)
- **PDF**: Extracts and translates text content
- **PPTX**: PowerPoint presentations (slide-by-slide translation)
- **XLSX**: Excel spreadsheets (cell-by-cell translation)
- **Domain-specific glossaries**: Medical, Legal, IT terminology support

### 🌐 Web Translation
- **HTML files**: Preserves tags and structure
- **URL translation**: Fetch and translate web pages
- **Localization files**: JSON and XML resource files

### ✏️ Text Translation
- Direct text input and translation
- Load from and save to text files
- Auto-language detection
- Copy to clipboard functionality

### 🎤 Real-time Translation (Demo)
- Text-based demo mode included
- Framework for audio capture integration
- Suitable for extending with Whisper STT

## Translation Engines

The platform automatically selects the best translation engine based on language pair and content domain:

- **DeepL**: Best for Korean ↔ English (requires API key)
- **Papago**: Specialized for Korean ↔ Japanese (requires API key)
- **Google Translate**: General purpose, many languages (uses googletrans library)
- **GPT-4**: Context-aware translation for technical content (requires API key)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/junggyeol4444/auto.git
cd auto
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API keys:
   - Run the application and go to Settings
   - Enter your API keys for the services you want to use
   - At minimum, Google Translate works without API keys

## Usage

### Running the Application

```bash
python main.py
```

### Using Different Features

#### Subtitle Translation
1. Go to the **Subtitles** tab
2. Click **Browse** to select an SRT, VTT, or ASS file
3. Select source and target languages
4. Choose translation engine (or use "auto")
5. Click **Translate**
6. Preview the results
7. Click **Save Translated File** to export

#### Document Translation
1. Go to the **Documents** tab
2. Click **Browse** to select a DOCX, PDF, PPTX, or XLSX file
3. Select languages and domain (general, medical, legal, it)
4. Choose translation engine
5. Click **Translate Document**
6. Select output location and save

#### Web Translation
1. Go to the **Web** tab
2. Choose mode: HTML File, URL, or Localization File
3. Enter URL or select file
4. Configure languages and engine
5. Click **Translate**
6. Save the translated output

#### Text Translation
1. Go to the **Text** tab
2. Enter or load text from file
3. Select languages (use "auto" for source language detection)
4. Click **Translate**
5. Copy or save the translated text

#### Real-time Translation Demo
1. Go to the **Real-time** tab
2. Select languages and engine
3. Click **Start**
4. Enter text in the demo input to see real-time translation
5. Click **Stop** when finished

### API Key Configuration

#### DeepL
1. Sign up at [DeepL API](https://www.deepl.com/pro-api)
2. Get your API key
3. Enter in Settings → DeepL API Key

#### Papago
1. Register at [Naver Developers](https://developers.naver.com/)
2. Create an application for Papago Translation
3. Get Client ID and Client Secret
4. Enter in Settings

#### OpenAI GPT-4
1. Sign up at [OpenAI](https://platform.openai.com/)
2. Generate an API key
3. Enter in Settings → OpenAI API Key

#### Google Translate
- Uses the `googletrans` library
- No API key required
- Works out of the box

## Building Executable

To build a standalone Windows executable:

```bash
pyinstaller build.spec
```

The executable will be created in the `dist` folder.

## Project Structure

```
Translation_Platform/
├── main.py                      # Application entry point
├── config.json                  # Configuration file
├── requirements.txt             # Python dependencies
├── build.spec                   # PyInstaller build specification
├── README.md                    # This file
│
├── modules/                     # Core modules
│   ├── translation/            # Translation engines
│   │   ├── base_translator.py
│   │   ├── deepl_api.py
│   │   ├── google_api.py
│   │   ├── papago_api.py
│   │   ├── gpt4_api.py
│   │   └── translation_engine.py
│   │
│   ├── subtitle/               # Subtitle processing
│   │   ├── srt_parser.py
│   │   ├── vtt_parser.py
│   │   ├── ass_parser.py
│   │   └── realtime_subtitle.py
│   │
│   ├── document/               # Document translation
│   │   ├── docx_translator.py
│   │   ├── pdf_translator.py
│   │   ├── pptx_translator.py
│   │   └── xlsx_translator.py
│   │
│   ├── web/                    # Web translation
│   │   ├── html_translator.py
│   │   └── localization.py
│   │
│   └── utils/                  # Utilities
│       ├── glossary.py
│       ├── quality_check.py
│       ├── cache_manager.py
│       └── language_detector.py
│
├── gui/                        # GUI modules
│   ├── main_window.py
│   ├── subtitle_tab.py
│   ├── document_tab.py
│   ├── web_tab.py
│   ├── text_tab.py
│   ├── realtime_tab.py
│   └── settings_window.py
│
├── data/
│   ├── glossaries/            # Domain glossaries
│   │   ├── medical.json
│   │   ├── legal.json
│   │   └── it.json
│   └── database/              # Cache database
│       └── translation_cache.db
│
└── output/                    # Output directory
    ├── subtitles/
    └── documents/
```

## Supported Languages

- Korean (ko)
- English (en)
- Japanese (ja)
- Chinese Simplified (zh-CN)
- Chinese Traditional (zh-TW)
- Spanish (es)
- French (fr)
- German (de)
- And more via Google Translate

## Features in Detail

### Domain Glossaries
The platform includes pre-configured glossaries for specialized domains:
- **Medical**: Anatomy, diseases, treatments
- **Legal**: Contracts, litigation, legal terms
- **IT**: Technology, programming, software terms

Add custom terms through the glossary JSON files in `data/glossaries/`.

### Translation Cache
- Automatically caches translations to reduce API calls
- Configurable cache size (default: 100MB)
- Stored in SQLite database
- Can be disabled in settings

### Quality Checking
- Validates translation completeness
- Checks for unusual length ratios
- Preserves placeholders and numbers
- Ensures subtitle length constraints

## Troubleshooting

### Import Errors
If you encounter import errors:
```bash
pip install --upgrade -r requirements.txt
```

### API Errors
- Verify your API keys are correct in Settings
- Check your internet connection
- Ensure you have API credits/quota available

### GUI Not Launching
- Ensure Python 3.8+ is installed
- Install customtkinter: `pip install customtkinter`
- Check for display/graphics driver issues

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting section

## Acknowledgments

- CustomTkinter for the modern GUI framework
- Translation API providers (DeepL, Google, Papago, OpenAI)
- Open source libraries used in this project