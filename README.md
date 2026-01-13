# Social Media Automation Suite

A comprehensive Windows desktop application for automating content creation and publishing across 7 major social media platforms.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 📱 Supported Platforms

1. **Instagram** - Feed posts, Reels, Stories (via instagrapi)
2. **TikTok** - Short-form videos (via Selenium automation)
3. **YouTube Shorts** - Vertical short videos (via YouTube Data API v3)
4. **Twitter/X** - Tweets with media (via Tweepy)
5. **Facebook** - Posts, Reels (via Graph API)
6. **Pinterest** - Image pins (via Pinterest API)
7. **Discord** - Webhook messages and embeds

## ✨ Key Features

### 🎬 Content Processing
- **Video Format Conversion**: Automatic conversion between 16:9, 9:16, and 1:1 aspect ratios
- **Image Processing**: Resize, crop, enhance, and add text overlays
- **Smart Cropping**: Center-focused cropping for optimal framing

### #️⃣ Hashtag Generation
- **AI-Powered Keywords**: RAKE algorithm for keyword extraction
- **Platform-Specific**: Optimal hashtag counts per platform
- **Trending Hashtags**: Integration with trending topics
- **Category-Based**: Pre-defined hashtag libraries by category

### ✍️ Caption Generation
- **Template System**: Multiple caption templates (simple, engaging, promotional, etc.)
- **Emoji Integration**: Smart emoji insertion
- **Platform Limits**: Automatic character limit enforcement
- **CTA Addition**: Call-to-action phrases

### 📅 Scheduling
- **Date/Time Scheduling**: Schedule posts for specific times
- **Optimal Time Suggestions**: Platform-specific best posting times
- **Recurring Posts**: Set up repeated posting schedules

### 🚀 Multi-Platform Publishing
- **Simultaneous Publishing**: Post to multiple platforms at once
- **Format Optimization**: Automatic format conversion per platform
- **Retry Logic**: Automatic retry on failures
- **Status Tracking**: Real-time publishing status

## 🛠️ Technology Stack

### Core Libraries
- **customtkinter** - Modern GUI framework
- **instagrapi** - Instagram automation
- **selenium** - Web automation for TikTok
- **tweepy** - Twitter API client
- **google-api-python-client** - YouTube API
- **facebook-sdk** - Facebook Graph API

### Media Processing
- **moviepy** - Video editing and conversion
- **opencv-python** - Video analysis and processing
- **Pillow** - Image manipulation
- **imageio** - Media I/O operations

### NLP & Analysis
- **rake-nltk** - Keyword extraction
- **konlpy** - Korean language support
- **nltk** - Natural language processing

### Utilities
- **APScheduler** - Job scheduling
- **pandas** - Data management
- **sqlite3** - Local database
- **requests** - HTTP requests
- **BeautifulSoup4** - Web scraping

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Windows OS (for EXE build)
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/junggyeol4444/auto.git
   cd auto
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data** (first time only)
   ```python
   python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
   ```

4. **Configure platforms**
   - Edit `config.json` with your API credentials
   - See [Configuration](#-configuration) section below

5. **Run the application**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### Platform Setup

#### Instagram
```json
{
  "instagram": {
    "enabled": true,
    "username": "your_username",
    "password": "your_password"
  }
}
```

#### YouTube
1. Create a project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable YouTube Data API v3
3. Create OAuth 2.0 credentials
4. Download `client_secrets.json`

#### Twitter
1. Apply for [Twitter Developer Account](https://developer.twitter.com/)
2. Create an app and get API keys
3. Add credentials to config.json

#### Facebook
1. Create an app in [Facebook Developers](https://developers.facebook.com/)
2. Get Page Access Token
3. Add token and Page ID to config

#### Pinterest
1. Create app in [Pinterest Developers](https://developers.pinterest.com/)
2. Generate access token
3. Get Board ID from Pinterest

#### Discord
1. Create a webhook in your Discord server settings
2. Copy webhook URL to config

## 🎯 Usage

### Quick Start

1. **Launch Application**
   ```bash
   python main.py
   ```

2. **Select Content**
   - Click "Select File" to choose image or video

3. **Choose Platforms**
   - Check the platforms you want to publish to

4. **Generate Caption & Hashtags**
   - Click "Auto Generate" or write your own

5. **Publish**
   - Click "Preview" to see how it will look
   - Click "Publish" to post immediately
   - Or schedule for later

### Command Line Usage

```python
from modules.publisher.instagram_publisher import InstagramPublisher

# Initialize
publisher = InstagramPublisher()
publisher.login()

# Post a photo
result = publisher.post_photo(
    image_path="path/to/image.jpg",
    caption="My caption #hashtag"
)

print(result['url'])
```

## 📂 Project Structure

```
Social_Media_Automation/
├── main.py                      # Main entry point
├── config.json                  # Configuration file
├── requirements.txt             # Dependencies
├── README.md                    # This file
│
├── modules/
│   ├── converter/
│   │   ├── video_converter.py   # Video format conversion
│   │   └── image_processor.py   # Image processing
│   │
│   ├── generator/
│   │   ├── hashtag_generator.py # Hashtag generation
│   │   ├── caption_generator.py # Caption generation
│   │   └── trend_analyzer.py    # Trend analysis
│   │
│   └── publisher/
│       ├── instagram_publisher.py
│       ├── tiktok_publisher.py
│       ├── youtube_publisher.py
│       ├── twitter_publisher.py
│       ├── facebook_publisher.py
│       ├── pinterest_publisher.py
│       └── discord_publisher.py
│
├── gui/
│   ├── main_window.py           # Main GUI
│   ├── preview_window.py        # Preview window
│   └── settings_window.py       # Settings window
│
├── templates/
│   ├── caption_templates.json   # Caption templates
│   └── emoji_library.json       # Emoji library
│
├── database/
│   ├── database.py              # Database manager
│   └── posts.db                 # SQLite database
│
├── output/
│   ├── converted/               # Converted media files
│   └── logs/                    # Application logs
│
└── cache/
    ├── sessions/                # Login sessions
    └── temp/                    # Temporary files
```

## 🔧 Building EXE

To create a Windows executable:

```bash
pip install pyinstaller

pyinstaller --name "Social Media Suite" \
            --windowed \
            --onefile \
            --icon=icon.ico \
            --add-data "templates;templates" \
            --add-data "config.json;." \
            main.py
```

The executable will be in the `dist` folder.

## 🎨 Screenshots

### Main Window
The main interface features:
- File upload area
- Platform selection checkboxes
- Caption and hashtag generators
- Scheduling options
- Activity log

### Settings Window
Configure all platform credentials and preferences in one place.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please comply with each platform's Terms of Service and API usage guidelines. Automated posting may violate some platforms' policies. Use responsibly.

## 🐛 Known Issues

- TikTok automation may be detected on some accounts
- Instagram 2FA requires manual intervention
- Rate limits vary by platform

## 🔒 Security

Security is a priority. We regularly update dependencies to patch known vulnerabilities. See [SECURITY.md](SECURITY.md) for:
- Security advisories
- Vulnerability reports
- Reporting security issues
- Best practices

**Latest Security Update (v1.0.1)**: Updated nltk (3.9) and Pillow (10.3.0) to fix critical vulnerabilities.

## 📮 Support

For issues and questions:
- Open an issue on GitHub
- Email: support@example.com

## 🙏 Acknowledgments

- Built with Python and customtkinter
- Uses official APIs where available
- Community contributions welcome

---

**Made with ❤️ by junggyeol4444**