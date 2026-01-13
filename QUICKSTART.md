# Quick Start Guide - Smart Video Editor Pro

## 5-Minute Setup

### Prerequisites Check

Before starting, ensure you have:
- ✓ Windows 10/11, macOS, or Linux
- ✓ Python 3.8 or higher
- ✓ At least 4GB RAM
- ✓ 2GB free disk space

### Step 1: Install Python (if needed)

**Windows:**
1. Download Python from https://python.org
2. Run installer and check "Add Python to PATH"
3. Verify: Open Command Prompt and type `python --version`

**macOS:**
```bash
# Using Homebrew
brew install python3
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### Step 2: Install FFmpeg

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH
4. Verify: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### Step 3: Get the Application

```bash
# Clone repository
git clone https://github.com/junggyeol4444/auto.git
cd auto

# Or download and extract ZIP from GitHub
```

### Step 4: Install Dependencies

**Windows:**
```cmd
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python main.py
```

The GUI window should open!

## First Use Tutorial

### Part 1: Learn an Editing Style (5 minutes)

1. **Find a YouTube video**
   - Choose a video (10-20 minutes recommended)
   - Pick one with clear editing style
   - Examples: Tech reviews, vlogs, tutorials

2. **In the application:**
   - Click "Learn Style" tab
   - Paste YouTube URL
   - Click "Download Video"
   - Wait for download to complete (~2-5 minutes)

3. **Create a profile:**
   - Enter profile name (e.g., "Tech Review Style")
   - Click "Learn Style"
   - Wait for analysis (~3-5 minutes)
   - Success message appears!

### Part 2: Edit Your Video (10 minutes)

1. **Prepare your video:**
   - Have a video file ready (MP4, AVI, MOV, etc.)
   - Keep first test under 5 minutes

2. **In the application:**
   - Click "Edit Video" tab
   - Click "Browse..." and select your video
   - Choose your learned profile from dropdown
   - Check "Remove Silence" (recommended)
   - Choose output location
   - Click "Edit Video"

3. **Wait for processing:**
   - Processing takes ~2-3x the video length
   - Watch progress bar
   - Check logs for details

4. **Result:**
   - Edited video saved to output location
   - Compare with original!

## Common First-Time Issues

### Issue: "Python not found"
**Solution:** Reinstall Python and check "Add to PATH" during installation

### Issue: "FFmpeg not found"
**Solution:** Install FFmpeg and add to system PATH (see Step 2 above)

### Issue: "Module not found"
**Solution:** 
```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Then install dependencies
pip install -r requirements.txt
```

### Issue: GUI doesn't open
**Solution:**
```bash
# Install PyQt5 specifically
pip install PyQt5

# Try running again
python main.py
```

### Issue: Download fails
**Solution:**
- Check internet connection
- Try a different YouTube video
- Some videos may be restricted

## Tips for Best Results

### For Learning:
1. ✓ Use videos from same creator
2. ✓ Choose videos 10-20 minutes long
3. ✓ Pick videos with clear editing style
4. ✗ Avoid music-heavy videos
5. ✗ Avoid livestreams or unedited content

### For Editing:
1. ✓ Test with short clips first (2-3 minutes)
2. ✓ Keep original files as backup
3. ✓ Use appropriate profile for your content type
4. ✓ Check output before processing long videos
5. ✗ Don't overwrite original files

## Next Steps

1. **Create Multiple Profiles:**
   - Learn from different YouTubers
   - Try various editing styles
   - Compare results

2. **Experiment:**
   - Try different videos with same profile
   - Test different profile combinations
   - Find what works best for your content

3. **Read Documentation:**
   - Check USAGE.md for detailed guide
   - Read ARCHITECTURE.md for technical details
   - Review README.md for full features

## Getting Help

- **GitHub Issues**: Report bugs or ask questions
- **README.md**: Full documentation
- **USAGE.md**: Detailed usage guide
- **ARCHITECTURE.md**: Technical documentation

## Quick Command Reference

```bash
# Activate environment
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Run application
python main.py

# Build executable (Windows)
build.bat

# Run demo
python demo.py

# Run tests
python test_basic.py
```

---

**Congratulations!** You're ready to start automating your video editing! 🎉
