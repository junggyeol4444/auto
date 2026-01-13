# Quick Start Guide

## Initial Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download NLTK Data
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### Step 3: Test Installation
```bash
python test_suite.py
```

## Using the Application

### Launch GUI
```bash
python main.py
```

### First Time Setup

1. **Click Settings (⚙️)**
   - Go to each platform tab
   - Enable the platforms you want to use
   - Enter your credentials
   - Click "Save Settings"

2. **Configure Each Platform:**

   **Instagram:**
   - Username: your_instagram_username
   - Password: your_password

   **TikTok:**
   - Username: your_tiktok_username
   - Password: your_password
   - Enable "Headless Mode" for background operation

   **YouTube:**
   - Download OAuth credentials from Google Cloud Console
   - Save as `client_secrets.json`
   - Browse and select the file

   **Twitter:**
   - Get API keys from Twitter Developer Portal
   - Enter all 5 credentials (API Key, Secret, Access Token, etc.)

   **Facebook:**
   - Get Page Access Token from Facebook Developers
   - Enter your Page ID

   **Pinterest:**
   - Get Access Token from Pinterest Developers
   - Find your Board ID

   **Discord:**
   - Create a webhook in your server
   - Paste the webhook URL

### Posting Content

1. **Select File**
   - Click "Select File"
   - Choose an image or video

2. **Choose Platforms**
   - Check the platforms you want to post to
   - Multiple selections allowed

3. **Add Caption**
   - Type your caption manually
   - OR click "Auto Generate" for AI-generated caption

4. **Add Hashtags**
   - Type hashtags manually
   - OR click "Auto Generate" for smart hashtags

5. **Preview (Optional)**
   - Click "Preview" to see how it looks on each platform
   - Review formatting and aspect ratios

6. **Publish**
   - Click "Publish" to post immediately
   - OR enable "Schedule" and set a date/time

## Tips for Best Results

### Video Content
- **For Reels/Shorts/TikTok:** Use vertical (9:16) videos
- **For Feed Posts:** Square (1:1) works best
- **Duration:** Keep under 60 seconds for best engagement

### Image Content
- **Instagram:** 1080x1080 (square) or 1080x1350 (portrait)
- **TikTok:** 1080x1920 (vertical)
- **Pinterest:** 1000x1500 (2:3 ratio)
- **High Quality:** Always use high-resolution images

### Captions
- **Instagram/Facebook:** Can be longer (2200 chars)
- **Twitter:** Keep under 280 characters
- **TikTok:** Short and catchy works best

### Hashtags
- **Instagram:** 20-30 hashtags for maximum reach
- **TikTok:** 3-5 relevant + trending hashtags
- **YouTube:** 10-15 in description
- **Twitter:** 1-2 hashtags only

## Common Issues

### "Module not found" error
```bash
pip install -r requirements.txt --upgrade
```

### Instagram login fails
- Check username/password
- Disable 2FA temporarily
- Try logging in manually first
- Check for Instagram notifications

### TikTok automation detected
- Run with headless mode disabled first
- Complete CAPTCHA manually
- Enable headless after successful login

### YouTube OAuth fails
- Ensure client_secrets.json is correct
- Check OAuth redirect URIs in Google Console
- Delete old credentials and re-authenticate

### Video conversion errors
```bash
# Install FFmpeg
# Windows: Download from ffmpeg.org
# Linux: sudo apt-get install ffmpeg
# Mac: brew install ffmpeg
```

## Advanced Usage

### Scheduled Posting
1. Enable "Schedule" checkbox
2. Enter date/time in format: YYYY-MM-DD HH:MM
3. Posts will publish automatically at scheduled time

### Batch Processing
- Select multiple platforms
- Content automatically optimized for each
- Posts publish sequentially with delays

### Custom Templates
- Edit `templates/caption_templates.json`
- Add your own templates
- Use in caption generation

## Getting API Credentials

### Instagram
No API credentials needed - uses instagrapi library with username/password

### YouTube
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials
5. Download JSON as `client_secrets.json`

### Twitter
1. Apply at [Twitter Developer Portal](https://developer.twitter.com/)
2. Create app
3. Generate keys: API Key, API Secret, Access Token, Access Secret, Bearer Token

### Facebook
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create app
3. Get Page Access Token (never expires)
4. Find Page ID from page settings

### Pinterest
1. Visit [Pinterest Developers](https://developers.pinterest.com/)
2. Create app
3. Generate Access Token
4. Get Board ID from board URL

### Discord
1. Open Discord server settings
2. Go to Integrations → Webhooks
3. Create webhook
4. Copy webhook URL

## Need Help?

- Check the main README.md
- Run test_suite.py to diagnose issues
- Review error messages in the Activity Log
- Check platform-specific API documentation
