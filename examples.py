"""
Example usage script for YouTube Auto Content Generator
"""
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.crawler import ContentCrawler
from src.content import ContentRestructurer
from src.tts import TTSManager
from src.video import VideoCreator
from src.youtube import YouTubeUploader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def example_basic_workflow():
    """Example: Basic content generation workflow"""
    logger.info("=" * 60)
    logger.info("Example: Basic Content Generation")
    logger.info("=" * 60)
    
    topic = "인공지능"
    
    # Step 1: Crawl content
    logger.info(f"Step 1: Crawling content for '{topic}'")
    crawler = ContentCrawler()
    content_data = crawler.crawl_content(topic, include_news=True, include_wiki=True)
    logger.info(f"Collected {len(content_data.get('news_articles', []))} news articles")
    
    # Step 2: Generate script
    logger.info("Step 2: Generating script")
    restructurer = ContentRestructurer()
    script = restructurer.generate_script(content_data, template_type="informational")
    logger.info(f"Generated script with {len(script)} characters")
    
    # Save script
    script_path = "output/example_script.txt"
    restructurer.save_script(script, script_path)
    logger.info(f"Script saved to {script_path}")
    
    # Step 3: Generate TTS
    logger.info("Step 3: Generating speech")
    tts_manager = TTSManager(engine_type="gtts")
    audio_path = "output/example_audio.mp3"
    success = tts_manager.text_to_speech(script, audio_path)
    
    if success:
        logger.info(f"Audio saved to {audio_path}")
    else:
        logger.error("Failed to generate audio")
        return
    
    # Step 4: Create video
    logger.info("Step 4: Creating video")
    video_creator = VideoCreator()
    video_path = "output/example_video.mp4"
    success = video_creator.create_simple_video(audio_path, video_path)
    
    if success:
        logger.info(f"Video saved to {video_path}")
    else:
        logger.error("Failed to create video")
        return
    
    logger.info("=" * 60)
    logger.info("Example completed successfully!")
    logger.info(f"Check the 'output' directory for generated files")
    logger.info("=" * 60)


def example_news_report():
    """Example: Generate a news report style video"""
    logger.info("=" * 60)
    logger.info("Example: News Report Generation")
    logger.info("=" * 60)
    
    topic = "기후변화"
    
    # Crawl news only
    crawler = ContentCrawler()
    content_data = crawler.crawl_content(topic, include_news=True, include_wiki=False)
    
    # Generate news report script
    restructurer = ContentRestructurer()
    script = restructurer.generate_script(content_data, template_type="news")
    
    logger.info(f"Generated news report script:")
    logger.info("-" * 60)
    logger.info(script)
    logger.info("-" * 60)


def example_tts_comparison():
    """Example: Compare different TTS engines"""
    logger.info("=" * 60)
    logger.info("Example: TTS Engine Comparison")
    logger.info("=" * 60)
    
    text = "안녕하세요. 이것은 TTS 테스트입니다."
    
    # Test gTTS
    logger.info("Testing gTTS...")
    gtts = TTSManager(engine_type="gtts")
    gtts.text_to_speech(text, "output/gtts_test.mp3")
    
    # Test pyttsx3
    logger.info("Testing pyttsx3...")
    pyttsx3 = TTSManager(engine_type="pyttsx3")
    pyttsx3.text_to_speech(text, "output/pyttsx3_test.mp3")
    
    logger.info("TTS comparison completed. Check output directory.")


def example_metadata_generation():
    """Example: Generate SEO-optimized metadata"""
    logger.info("=" * 60)
    logger.info("Example: Metadata Generation")
    logger.info("=" * 60)
    
    # Sample content data
    content_data = {
        'topic': '인공지능의 미래',
        'news_articles': [
            {'title': 'AI 기술 발전', 'description': '최신 AI 동향'}
        ]
    }
    
    script = "인공지능의 미래에 대해 알아봅니다..."
    
    # Generate metadata
    restructurer = ContentRestructurer()
    metadata = restructurer.generate_metadata(content_data, script)
    
    logger.info("Generated metadata:")
    logger.info(f"Title: {metadata['title']}")
    logger.info(f"Description: {metadata['description'][:100]}...")
    logger.info(f"Tags: {', '.join(metadata['tags'])}")
    logger.info(f"Category: {metadata['category']}")


if __name__ == "__main__":
    # Run examples
    print("\n" + "=" * 60)
    print("YouTube Auto Content Generator - Examples")
    print("=" * 60 + "\n")
    
    print("Available examples:")
    print("1. Basic workflow (crawl -> script -> TTS -> video)")
    print("2. News report generation")
    print("3. TTS engine comparison")
    print("4. Metadata generation")
    print()
    
    choice = input("Select example (1-4) or 'all' to run all: ").strip()
    
    try:
        if choice == "1":
            example_basic_workflow()
        elif choice == "2":
            example_news_report()
        elif choice == "3":
            example_tts_comparison()
        elif choice == "4":
            example_metadata_generation()
        elif choice.lower() == "all":
            example_metadata_generation()
            example_news_report()
            example_tts_comparison()
            example_basic_workflow()
        else:
            print("Invalid choice")
    except KeyboardInterrupt:
        print("\n\nExample interrupted by user")
    except Exception as e:
        logger.error(f"Example failed: {e}", exc_info=True)
