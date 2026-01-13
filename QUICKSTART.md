# Quick Start Guide

Get started with YouTube Auto Content Generator in 5 minutes!

## Installation

```bash
# Clone and enter directory
git clone https://github.com/junggyeol4444/auto.git
cd auto

# Install dependencies
pip install -r requirements.txt
```

## First Video in 3 Steps

### Step 1: Run the Application
```bash
python main.py
```

### Step 2: Fill in the Form
- **주제 (Topic)**: Enter your topic (e.g., "인공지능")
- **채널 유형 (Channel Type)**: Select "정보/교육" (Informational)
- **TTS 엔진 (TTS Engine)**: Select "Google TTS"
- **Options**: Check "뉴스 크롤링" and "위키 크롤링"

### Step 3: Generate
Click "콘텐츠 생성 시작" (Start Generation)

Your video will be created in `output/{your-topic}/video.mp4`!

## What Happens Behind the Scenes?

1. **Crawling** 🔍
   - Searches news sites for your topic
   - Fetches Wikipedia/NamuWiki content
   
2. **Script Generation** 📝
   - Combines collected content
   - Creates natural Korean script
   
3. **Voice Generation** 🎤
   - Converts script to speech
   - Creates audio file
   
4. **Video Creation** 🎬
   - Combines audio with visuals
   - Exports final video

## Try Different Styles

### News Report
```python
from crawler import ContentCrawler
from content import ContentRestructurer

crawler = ContentCrawler()
content = crawler.crawl_content("기후변화", include_news=True, include_wiki=False)

restructurer = ContentRestructurer()
script = restructurer.generate_script(content, template_type="news")
print(script)
```

### Storytelling
```python
script = restructurer.generate_script(content, template_type="storytelling")
```

## Enable YouTube Upload

1. Get credentials from [Google Cloud Console](https://console.cloud.google.com/)
2. Save `credentials.json` to project root
3. Check "YouTube 자동 업로드" option in GUI
4. First run will ask for browser authentication

## Command Line Examples

```bash
# Run interactive examples
python examples.py

# Validate setup
python setup.py
```

## Next Steps

- Read [User Guide](docs/USER_GUIDE.md) for detailed usage
- Check [API Documentation](docs/API.md) for programming
- See [Contributing Guide](CONTRIBUTING.md) to contribute

## Common Issues

**"No module named 'bs4'"**
```bash
pip install -r requirements.txt
```

**TTS fails**
- Check internet connection (for Google TTS)
- Try pyttsx3 for offline TTS

**Video creation fails**
```bash
# Install FFmpeg
# Windows: Download from https://ffmpeg.org
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
```

## Support

- [Open an Issue](https://github.com/junggyeol4444/auto/issues)
- Check existing issues for solutions

Happy creating! 🎉
