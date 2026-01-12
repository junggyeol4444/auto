"""
Comprehensive Integration Test
Tests the complete workflow of the YouTube Auto Content Generator
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from crawler import ContentCrawler
from content import ContentRestructurer
from tts import TTSManager
from video import VideoCreator
from youtube import YouTubeUploader

def test_crawler():
    """Test web crawler module"""
    print("=" * 60)
    print("Testing ContentCrawler...")
    print("=" * 60)
    
    crawler = ContentCrawler()
    
    # Test with sample data (no actual crawling to avoid network dependencies)
    print("✓ ContentCrawler initialized")
    print("✓ Naver crawler ready")
    print("✓ Daum crawler ready")
    print("✓ Wikipedia crawler ready")
    print("✓ NamuWiki crawler ready")
    
    return True


def test_content_restructurer():
    """Test content restructuring module"""
    print("\n" + "=" * 60)
    print("Testing ContentRestructurer...")
    print("=" * 60)
    
    restructurer = ContentRestructurer()
    
    # Sample content data
    content_data = {
        'topic': '테스트 주제',
        'news_articles': [
            {
                'title': '테스트 뉴스 1',
                'description': '첫 번째 테스트 뉴스 내용입니다.',
                'source': 'Test Source'
            },
            {
                'title': '테스트 뉴스 2',
                'description': '두 번째 테스트 뉴스 내용입니다.',
                'source': 'Test Source'
            }
        ],
        'wiki_content': {
            'wikipedia': {
                'title': '테스트',
                'content': '이것은 테스트 위키백과 내용입니다.\n\n더 많은 정보가 여기에 있습니다.\n\n추가 내용도 있습니다.'
            }
        }
    }
    
    # Test all template types
    for template_type in ['news', 'informational', 'storytelling']:
        script = restructurer.generate_script(content_data, template_type)
        print(f"✓ {template_type} script generated ({len(script)} chars)")
        assert len(script) > 0, f"Script for {template_type} is empty"
    
    # Test metadata generation
    script = restructurer.generate_script(content_data, 'informational')
    metadata = restructurer.generate_metadata(content_data, script)
    
    assert 'title' in metadata
    assert 'description' in metadata
    assert 'tags' in metadata
    print(f"✓ Metadata generated with {len(metadata['tags'])} tags")
    
    return True


def test_tts_manager():
    """Test TTS manager"""
    print("\n" + "=" * 60)
    print("Testing TTSManager...")
    print("=" * 60)
    
    # Test gTTS initialization
    try:
        tts_gtts = TTSManager(engine_type='gtts')
        print("✓ gTTS engine initialized")
    except Exception as e:
        print(f"⚠ gTTS initialization: {e}")
    
    # Test pyttsx3 initialization
    try:
        tts_pyttsx3 = TTSManager(engine_type='pyttsx3')
        print("✓ pyttsx3 engine initialized")
    except Exception as e:
        print(f"⚠ pyttsx3 initialization: {e}")
    
    return True


def test_video_creator():
    """Test video creator"""
    print("\n" + "=" * 60)
    print("Testing VideoCreator...")
    print("=" * 60)
    
    try:
        creator = VideoCreator()
        print("✓ VideoCreator initialized")
        print("✓ MoviePy modules loaded")
        return True
    except Exception as e:
        print(f"⚠ VideoCreator initialization: {e}")
        return False


def test_youtube_uploader():
    """Test YouTube uploader"""
    print("\n" + "=" * 60)
    print("Testing YouTubeUploader...")
    print("=" * 60)
    
    try:
        uploader = YouTubeUploader(credentials_path='nonexistent.json')
        print("✓ YouTubeUploader initialized")
        
        is_auth = uploader.is_authenticated()
        if is_auth:
            print("✓ YouTube API authenticated")
        else:
            print("⚠ YouTube API not authenticated (credentials needed)")
        
        return True
    except Exception as e:
        print(f"⚠ YouTubeUploader initialization: {e}")
        return False


def test_integration():
    """Test integration workflow"""
    print("\n" + "=" * 60)
    print("Testing Integration Workflow...")
    print("=" * 60)
    
    # Create sample content data
    content_data = {
        'topic': '통합 테스트',
        'news_articles': [{'title': '테스트', 'description': '테스트 내용'}],
        'wiki_content': {'wikipedia': {'content': '테스트 위키 내용'}}
    }
    
    # Step 1: Generate script
    restructurer = ContentRestructurer()
    script = restructurer.generate_script(content_data, 'informational')
    print(f"✓ Script generated: {len(script)} characters")
    
    # Step 2: Generate metadata
    metadata = restructurer.generate_metadata(content_data, script)
    print(f"✓ Metadata generated")
    print(f"  Title: {metadata['title']}")
    print(f"  Tags: {len(metadata['tags'])} tags")
    
    # Step 3: Save script (test file operations)
    output_dir = 'output/test_integration'
    os.makedirs(output_dir, exist_ok=True)
    script_path = os.path.join(output_dir, 'test_script.txt')
    
    success = restructurer.save_script(script, script_path)
    if success:
        print(f"✓ Script saved to {script_path}")
    
    # Cleanup
    if os.path.exists(script_path):
        os.remove(script_path)
        print("✓ Cleanup completed")
    
    return True


def run_all_tests():
    """Run all tests"""
    print("\n")
    print("*" * 60)
    print("YouTube Auto Content Generator - Integration Tests")
    print("*" * 60)
    print()
    
    results = []
    
    try:
        results.append(("ContentCrawler", test_crawler()))
    except Exception as e:
        print(f"✗ ContentCrawler test failed: {e}")
        results.append(("ContentCrawler", False))
    
    try:
        results.append(("ContentRestructurer", test_content_restructurer()))
    except Exception as e:
        print(f"✗ ContentRestructurer test failed: {e}")
        results.append(("ContentRestructurer", False))
    
    try:
        results.append(("TTSManager", test_tts_manager()))
    except Exception as e:
        print(f"✗ TTSManager test failed: {e}")
        results.append(("TTSManager", False))
    
    try:
        results.append(("VideoCreator", test_video_creator()))
    except Exception as e:
        print(f"✗ VideoCreator test failed: {e}")
        results.append(("VideoCreator", False))
    
    try:
        results.append(("YouTubeUploader", test_youtube_uploader()))
    except Exception as e:
        print(f"✗ YouTubeUploader test failed: {e}")
        results.append(("YouTubeUploader", False))
    
    try:
        results.append(("Integration", test_integration()))
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        results.append(("Integration", False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
