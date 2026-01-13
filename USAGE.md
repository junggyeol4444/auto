# Usage Guide - Smart Video Editor Pro

## Quick Start

### 1. Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### 2. Learn an Editing Style

**Step-by-step:**

1. Launch the application
2. Go to the "Learn Style" tab
3. Find a YouTube video with the editing style you want to replicate
4. Copy the video URL
5. Paste it into the "Video URL" field
6. Click "Download Video" and wait for download to complete
7. Enter a memorable profile name (e.g., "Fast Paced Vlog", "Tech Review Style")
8. Click "Learn Style" to analyze the video
9. Wait for analysis to complete (this may take several minutes)

**What gets learned:**
- Scene change frequency and patterns
- Average scene duration
- Voice vs. silence ratios
- Silence detection thresholds
- Speech padding preferences

### 3. Edit Your Video

**Step-by-step:**

1. Go to the "Edit Video" tab
2. Click "Browse..." next to Input Video
3. Select your video file (MP4, AVI, MKV, MOV, etc.)
4. Select a learned profile from the dropdown
5. Enable/disable editing options:
   - ☑️ **Remove Silence**: Cuts out silent portions automatically
6. Choose an output location (or accept the default)
7. Click "Edit Video"
8. Wait for processing to complete
9. Your edited video will be saved to the output location

## Advanced Usage

### Profile Management

**Creating Multiple Profiles:**
- Learn from different YouTubers to create distinct editing styles
- Example profiles:
  - "MrBeast" - Fast-paced with quick cuts
  - "MKBHD" - Smooth, professional pacing
  - "Casey Neistat" - Energetic vlog style

**When to Use Each Profile:**
- **Fast-paced profiles**: Gaming videos, vlogs, energetic content
- **Slow-paced profiles**: Tutorials, explanations, reviews
- **Speech-heavy profiles**: Podcasts, interviews, commentary

### Tips for Best Results

**For Learning:**
1. Choose representative videos (10-20 minutes ideal)
2. Avoid videos with heavy background music (affects silence detection)
3. Use videos from the same creator for consistent patterns
4. Learn multiple videos from the same creator and average the results

**For Editing:**
1. Test on a short clip first (1-2 minutes)
2. Adjust your input video audio levels if needed
3. Keep original files as backup
4. For long videos (>30 min), consider splitting into parts

### Understanding the Options

**Remove Silence:**
- **ON**: Automatically removes quiet sections between speech
- **OFF**: Keeps all audio, no silence removal
- **Best for**: Podcasts, interviews, vlogs, commentary
- **Not ideal for**: Music videos, ambient content

## Workflow Examples

### Example 1: Creating a YouTube Vlog

1. **Learn Phase:**
   - Download a vlog from your favorite vlogger
   - Create profile "My Vlog Style"
   - Let the app learn the pacing and cuts

2. **Edit Phase:**
   - Record your raw vlog footage
   - Select "My Vlog Style" profile
   - Enable "Remove Silence"
   - Process the video
   - Result: Your vlog with similar pacing and no dead air

### Example 2: Podcast/Interview Editing

1. **Learn Phase:**
   - Download a professionally edited podcast episode
   - Create profile "Podcast Style"

2. **Edit Phase:**
   - Import your raw podcast recording
   - Select "Podcast Style" profile
   - Enable "Remove Silence"
   - Process the video
   - Result: Clean podcast with pauses removed

### Example 3: Tutorial Video

1. **Learn Phase:**
   - Download a tutorial from a professional educator
   - Create profile "Tutorial Style"

2. **Edit Phase:**
   - Import your screen recording
   - Select "Tutorial Style" profile
   - Process with similar pacing
   - Result: Tutorial with professional pacing

## Common Issues and Solutions

### Issue: "No voice segments detected"
**Solution:**
- Your video might be too quiet
- Try a different video for learning
- Check your input video's audio levels

### Issue: "Too much content removed"
**Solution:**
- The silence threshold might be too sensitive
- Try learning from a video with more speech
- Use a different profile with less aggressive silence removal

### Issue: "Not enough content removed"
**Solution:**
- Learn from a video with tighter editing
- The source video might have less silence
- Try a different profile

### Issue: Processing takes too long
**Solution:**
- Use shorter videos for testing
- Close other applications to free up resources
- Consider upgrading your hardware for 4K videos

## Performance Tips

- **Video Length**: 10-30 minute videos process in 5-15 minutes
- **Resolution**: Lower resolution videos process faster
- **Format**: MP4 with H.264 is most efficient
- **Storage**: Ensure 2-3x the input video size in free space

## Keyboard Shortcuts

*To be implemented in future versions*

## Best Practices

1. **Always keep originals**: Never overwrite your source videos
2. **Test first**: Try a short sample before processing long videos
3. **Descriptive names**: Use clear profile names for easy identification
4. **Regular backups**: Back up your database regularly (data/video_editor.db)
5. **Update profiles**: Re-learn from new videos to keep styles current

## Output Quality

- **Video Codec**: H.264 (widely compatible)
- **Audio Codec**: AAC (high quality)
- **Resolution**: Matches input video
- **Frame Rate**: Matches input video
- **Bitrate**: Optimized automatically

## Next Steps

- Experiment with different profiles
- Compare outputs from different learned styles
- Fine-tune by learning from multiple sources
- Share your results!

---

For technical issues, check README.md or open an issue on GitHub.
