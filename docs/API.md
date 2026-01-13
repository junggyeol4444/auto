# API Documentation

## Module: crawler

### ContentCrawler

Main crawler class for collecting content from various sources.

#### Methods

##### `crawl_news(keyword: str, max_results: int = 5) -> List[Dict]`
Crawl news articles from Naver and Daum.

**Parameters:**
- `keyword`: Search keyword
- `max_results`: Maximum number of results per source (default: 5)

**Returns:** List of article dictionaries

##### `crawl_wiki(topic: str) -> Dict`
Crawl content from Wikipedia and NamuWiki.

**Parameters:**
- `topic`: Topic to search for

**Returns:** Dictionary with 'wikipedia' and 'namuwiki' keys

##### `crawl_content(topic: str, include_news: bool = True, include_wiki: bool = True) -> Dict`
Crawl all available content for a topic.

**Parameters:**
- `topic`: Topic to search for
- `include_news`: Whether to include news articles
- `include_wiki`: Whether to include wiki content

**Returns:** Complete content dictionary

---

## Module: content

### ContentRestructurer

Restructures crawled content into scripts using templates.

#### Methods

##### `generate_script(content_data: Dict, template_type: str = 'informational') -> str`
Generate a script from content data.

**Parameters:**
- `content_data`: Content dictionary from crawler
- `template_type`: Type of template ('news', 'informational', 'storytelling')

**Returns:** Generated script text

##### `generate_metadata(content_data: Dict, script: str) -> Dict`
Generate SEO-optimized metadata for YouTube.

**Parameters:**
- `content_data`: Content dictionary
- `script`: Generated script

**Returns:** Metadata dictionary with title, description, tags

---

## Module: tts

### TTSManager

Manager for Text-to-Speech operations.

#### Methods

##### `__init__(engine_type: str = 'gtts', **kwargs)`
Initialize TTS manager.

**Parameters:**
- `engine_type`: 'gtts', 'pyttsx3', or 'custom'
- `**kwargs`: Engine-specific parameters

##### `text_to_speech(text: str, output_path: str) -> bool`
Convert text to speech.

**Parameters:**
- `text`: Text to convert
- `output_path`: Output file path

**Returns:** True if successful

---

## Module: video

### VideoCreator

Creates videos using MoviePy.

#### Methods

##### `create_simple_video(audio_path: str, output_path: str, background_image: Optional[str] = None, background_color: Tuple[int, int, int] = (0, 0, 0), resolution: Tuple[int, int] = (1280, 720)) -> bool`
Create a video with audio and static background.

**Parameters:**
- `audio_path`: Path to audio file
- `output_path`: Output video path
- `background_image`: Optional background image
- `background_color`: RGB background color
- `resolution`: Video resolution (width, height)

**Returns:** True if successful

---

## Module: youtube

### YouTubeUploader

Uploads videos to YouTube using YouTube Data API v3.

#### Methods

##### `__init__(credentials_path: Optional[str] = None)`
Initialize YouTube uploader.

**Parameters:**
- `credentials_path`: Path to credentials.json

##### `upload_video(video_path: str, metadata: Dict) -> Optional[str]`
Upload video to YouTube.

**Parameters:**
- `video_path`: Path to video file
- `metadata`: Dictionary with title, description, tags, etc.

**Returns:** Video ID if successful, None otherwise

##### `update_video_metadata(video_id: str, metadata: Dict) -> bool`
Update metadata for existing video.

**Parameters:**
- `video_id`: YouTube video ID
- `metadata`: Updated metadata

**Returns:** True if successful

##### `set_thumbnail(video_id: str, thumbnail_path: str) -> bool`
Set custom thumbnail for video.

**Parameters:**
- `video_id`: YouTube video ID
- `thumbnail_path`: Path to thumbnail image

**Returns:** True if successful
