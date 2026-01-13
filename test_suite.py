"""
Test Script for Social Media Automation Suite
Run this to verify basic functionality
"""

import sys
import os

print("=" * 60)
print("Social Media Automation Suite - Test Script")
print("=" * 60)
print()

# Test 1: Import all core modules
print("Test 1: Importing core modules...")
try:
    from modules.converter.video_converter import VideoConverter
    from modules.converter.image_processor import ImageProcessor
    from modules.generator.hashtag_generator import HashtagGenerator
    from modules.generator.caption_generator import CaptionGenerator
    from modules.generator.trend_analyzer import TrendAnalyzer
    print("✓ Core modules imported successfully")
except Exception as e:
    print(f"✗ Failed to import core modules: {e}")
    sys.exit(1)

# Test 2: Import publisher modules
print("\nTest 2: Importing publisher modules...")
try:
    from modules.publisher.instagram_publisher import InstagramPublisher
    from modules.publisher.tiktok_publisher import TikTokPublisher
    from modules.publisher.youtube_publisher import YouTubePublisher
    from modules.publisher.twitter_publisher import TwitterPublisher
    from modules.publisher.facebook_publisher import FacebookPublisher
    from modules.publisher.pinterest_publisher import PinterestPublisher
    from modules.publisher.discord_publisher import DiscordPublisher
    print("✓ All 7 publisher modules imported successfully")
except Exception as e:
    print(f"✗ Failed to import publisher modules: {e}")
    sys.exit(1)

# Test 3: Import GUI modules
print("\nTest 3: Importing GUI modules...")
try:
    import customtkinter as ctk
    print("✓ customtkinter imported successfully")
except Exception as e:
    print(f"✗ Failed to import customtkinter: {e}")
    print("  Run: pip install customtkinter")

# Test 4: Import database module
print("\nTest 4: Importing database module...")
try:
    from database.database import Database
    print("✓ Database module imported successfully")
except Exception as e:
    print(f"✗ Failed to import database module: {e}")
    sys.exit(1)

# Test 5: Initialize components
print("\nTest 5: Initializing components...")
try:
    hashtag_gen = HashtagGenerator()
    caption_gen = CaptionGenerator()
    trend_analyzer = TrendAnalyzer()
    print("✓ Components initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize components: {e}")
    sys.exit(1)

# Test 6: Test hashtag generation
print("\nTest 6: Testing hashtag generation...")
try:
    test_content = "This is amazing content about social media marketing and digital strategy"
    hashtags = hashtag_gen.generate_hashtags(test_content, platform='instagram', category='business')
    print(f"✓ Generated {len(hashtags)} hashtags: {', '.join(hashtags[:5])}...")
except Exception as e:
    print(f"✗ Failed to generate hashtags: {e}")

# Test 7: Test caption generation
print("\nTest 7: Testing caption generation...")
try:
    test_content = "Check out this amazing content!"
    caption = caption_gen.generate_caption(test_content, template_name='simple')
    print(f"✓ Generated caption: {caption[:80]}...")
except Exception as e:
    print(f"✗ Failed to generate caption: {e}")

# Test 8: Test trend analysis
print("\nTest 8: Testing trend analysis...")
try:
    trending = trend_analyzer.get_trending_hashtags('instagram', count=5)
    print(f"✓ Got trending hashtags: {', '.join(trending)}")
except Exception as e:
    print(f"✗ Failed to get trending hashtags: {e}")

# Test 9: Test database
print("\nTest 9: Testing database...")
try:
    db = Database('database/test_posts.db')
    stats = db.get_statistics()
    print(f"✓ Database working - Total posts: {stats['total_posts']}")
    # Clean up test database
    if os.path.exists('database/test_posts.db'):
        os.remove('database/test_posts.db')
except Exception as e:
    print(f"✗ Failed to test database: {e}")

# Test 10: Config file
print("\nTest 10: Checking configuration...")
try:
    import json
    with open('config.json', 'r') as f:
        config = json.load(f)
    platforms = config.get('platforms', {})
    print(f"✓ Config file loaded - {len(platforms)} platforms configured")
except Exception as e:
    print(f"✗ Failed to load config: {e}")

print("\n" + "=" * 60)
print("Test Summary:")
print("=" * 60)
print("✓ All critical tests passed!")
print("\nNext steps:")
print("1. Configure your API credentials in config.json")
print("2. Run: python main.py")
print("3. Use the Settings window to add platform credentials")
print("=" * 60)
