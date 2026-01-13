"""
Example Usage Script
Demonstrates programmatic usage of the Social Media Automation Suite
"""

import os
import sys

# Example 1: Generate Hashtags
print("=" * 60)
print("Example 1: Hashtag Generation")
print("=" * 60)

from modules.generator.hashtag_generator import HashtagGenerator

hashtag_gen = HashtagGenerator()

content = "Delicious homemade pasta recipe with fresh ingredients and Italian flavors"
hashtags = hashtag_gen.generate_hashtags(
    content=content,
    platform='instagram',
    category='food'
)

print(f"Content: {content}")
print(f"\nGenerated {len(hashtags)} hashtags:")
print(hashtag_gen.format_hashtags(hashtags, 'instagram'))

# Example 2: Generate Caption
print("\n" + "=" * 60)
print("Example 2: Caption Generation")
print("=" * 60)

from modules.generator.caption_generator import CaptionGenerator

caption_gen = CaptionGenerator()

content = "Amazing sunset view from the mountain peak"
hashtags_str = "#sunset #mountain #nature #photography"

caption = caption_gen.generate_caption(
    content=content,
    template_name='engaging',
    platform='instagram',
    hashtags=hashtags_str
)

print(f"Generated caption:\n{caption[:200]}...")

# Example 3: Video Conversion
print("\n" + "=" * 60)
print("Example 3: Video Format Conversion")
print("=" * 60)

from modules.converter.video_converter import VideoConverter

converter = VideoConverter()

print("Video converter initialized")
print("Supported formats: 16:9, 9:16, 1:1")
print("\nExample conversions:")
print("- 16:9 → 9:16 for Instagram Reels/TikTok/YouTube Shorts")
print("- 16:9 → 1:1 for Instagram Feed")
print("- Any format → Platform-optimized format")

# Uncomment to test with actual video file:
# if os.path.exists('input_video.mp4'):
#     output = converter.convert_to_vertical('input_video.mp4', 'output_vertical.mp4')
#     print(f"Converted: {output}")

# Example 4: Image Processing
print("\n" + "=" * 60)
print("Example 4: Image Processing")
print("=" * 60)

from modules.converter.image_processor import ImageProcessor

processor = ImageProcessor()

print("Image processor initialized")
print("Capabilities:")
print("- Resize images")
print("- Crop to aspect ratio (1:1, 9:16, 4:5)")
print("- Add text overlays")
print("- Enhance (brightness, contrast, saturation)")
print("- Create carousel images")

# Uncomment to test with actual image:
# if os.path.exists('input_image.jpg'):
#     output = processor.crop_to_aspect_ratio('input_image.jpg', 'output_square.jpg', '1:1')
#     print(f"Cropped: {output}")

# Example 5: Trend Analysis
print("\n" + "=" * 60)
print("Example 5: Trend Analysis")
print("=" * 60)

from modules.generator.trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer()

# Get trending hashtags
trending = analyzer.get_trending_hashtags('instagram', count=10)
print(f"Trending Instagram hashtags: {', '.join(trending)}")

# Analyze engagement potential
content_to_analyze = "🔥 Amazing tips for entrepreneurs! Follow for more business advice 💼"
analysis = analyzer.analyze_engagement(content_to_analyze)

print(f"\nEngagement Analysis:")
print(f"Score: {analysis['score']}/100")
print(f"Word count: {analysis['word_count']}")
print(f"Has emoji: {analysis['emoji_count'] > 0}")
print(f"Has CTA: {analysis['has_cta']}")
print(f"Recommendation: {analysis['recommendation']}")

# Get optimal posting times
times = analyzer.get_optimal_posting_times('instagram')
print(f"\nOptimal Instagram posting times: {', '.join(times)}")

# Example 6: Database Operations
print("\n" + "=" * 60)
print("Example 6: Database Operations")
print("=" * 60)

from database.database import Database

db = Database()

# Get statistics
stats = db.get_statistics()
print(f"Total posts: {stats['total_posts']}")
print(f"Successful: {stats['successful_posts']}")
print(f"Failed: {stats['failed_posts']}")
print(f"Scheduled: {stats['scheduled_posts']}")

if stats['by_platform']:
    print("\nPosts by platform:")
    for platform, count in stats['by_platform'].items():
        print(f"  {platform}: {count}")

# Example 7: Publishing Coordinator
print("\n" + "=" * 60)
print("Example 7: Publishing Coordinator")
print("=" * 60)

from modules.publishing_coordinator import PublishingCoordinator

coordinator = PublishingCoordinator()

print("Publishing coordinator initialized")
print(f"Available publishers: {list(coordinator.publishers.keys())}")

# Example publishing (commented out - requires credentials)
# result = coordinator.publish_to_platform(
#     platform='instagram',
#     content_path='my_image.jpg',
#     caption='My amazing post!',
#     hashtags='#instagram #photo'
# )
# print(f"Result: {result}")

# Example 8: Multi-Platform Publishing
print("\n" + "=" * 60)
print("Example 8: Multi-Platform Publishing")
print("=" * 60)

print("To publish to multiple platforms:")
print("""
coordinator = PublishingCoordinator()

results = coordinator.publish_to_multiple(
    platforms=['instagram', 'twitter', 'facebook'],
    content_path='content.jpg',
    caption='Amazing content!',
    hashtags='#socialmedia #content',
    callback=lambda msg: print(msg)
)

for platform, result in results.items():
    if result['success']:
        print(f"{platform}: {result['url']}")
    else:
        print(f"{platform}: Failed - {result['error']}")
""")

# Example 9: Template Usage
print("\n" + "=" * 60)
print("Example 9: Caption Templates")
print("=" * 60)

templates = caption_gen.get_template_names()
print(f"Available templates: {', '.join(templates)}")

print("\nExample captions with different templates:")
for template in ['simple', 'engaging', 'promotional']:
    caption = caption_gen.generate_caption(
        content="Great content here",
        template_name=template,
        platform='instagram',
        hashtags='#example'
    )
    print(f"\n{template.upper()}:")
    print(caption[:100])

# Example 10: Best Practices
print("\n" + "=" * 60)
print("Example 10: Platform Best Practices")
print("=" * 60)

best_practices = analyzer.get_platform_best_practices('instagram')
print(f"\nInstagram Best Practices:")
print(f"Optimal hashtags: {best_practices['optimal_hashtags']}")
print(f"Caption length: {best_practices['caption_length']}")
print(f"Posting frequency: {best_practices['posting_frequency']}")
print(f"Best times: {', '.join(best_practices['best_times'])}")
print("\nTips:")
for tip in best_practices['tips']:
    print(f"  • {tip}")

print("\n" + "=" * 60)
print("Examples Complete!")
print("=" * 60)
print("\nFor GUI usage, run: python main.py")
print("For testing, run: python test_suite.py")
print("For quick start guide, see: QUICKSTART.md")
