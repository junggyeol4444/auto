"""
Publishing Coordinator
Coordinates publishing across multiple platforms
"""

import os
import json
from typing import Dict, List
from datetime import datetime
import threading
import time

from modules.publisher.instagram_publisher import InstagramPublisher
from modules.publisher.tiktok_publisher import TikTokPublisher
from modules.publisher.youtube_publisher import YouTubePublisher
from modules.publisher.twitter_publisher import TwitterPublisher
from modules.publisher.facebook_publisher import FacebookPublisher
from modules.publisher.pinterest_publisher import PinterestPublisher
from modules.publisher.discord_publisher import DiscordPublisher
from modules.converter.video_converter import VideoConverter
from modules.converter.image_processor import ImageProcessor
from database.database import Database


class PublishingCoordinator:
    """Coordinates content publishing across platforms"""
    
    def __init__(self, config_path: str = 'config.json'):
        self.config_path = config_path
        self.config = self.load_config()
        self.database = Database()
        
        # Initialize converters
        self.video_converter = VideoConverter()
        self.image_processor = ImageProcessor()
        
        # Initialize publishers
        self.publishers = {}
        self.init_publishers()
    
    def load_config(self) -> Dict:
        """Load configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def init_publishers(self):
        """Initialize all publishers"""
        platforms = self.config.get('platforms', {})
        
        if platforms.get('instagram', {}).get('enabled'):
            self.publishers['instagram'] = InstagramPublisher(self.config_path)
        
        if platforms.get('tiktok', {}).get('enabled'):
            self.publishers['tiktok'] = TikTokPublisher(self.config_path)
        
        if platforms.get('youtube', {}).get('enabled'):
            self.publishers['youtube'] = YouTubePublisher(self.config_path)
        
        if platforms.get('twitter', {}).get('enabled'):
            self.publishers['twitter'] = TwitterPublisher(self.config_path)
        
        if platforms.get('facebook', {}).get('enabled'):
            self.publishers['facebook'] = FacebookPublisher(self.config_path)
        
        if platforms.get('pinterest', {}).get('enabled'):
            self.publishers['pinterest'] = PinterestPublisher(self.config_path)
        
        if platforms.get('discord', {}).get('enabled'):
            self.publishers['discord'] = DiscordPublisher(self.config_path)
    
    def prepare_content(self, content_path: str, platform: str) -> str:
        """
        Prepare content for specific platform
        
        Args:
            content_path: Path to original content
            platform: Target platform
            
        Returns:
            Path to prepared content
        """
        is_video = content_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))
        
        # Determine required format
        format_map = {
            'instagram': '9:16',  # Reels
            'tiktok': '9:16',
            'youtube': '9:16',    # Shorts
            'twitter': '16:9',
            'facebook': '9:16',   # Reels
            'pinterest': '2:3',
            'discord': None       # No conversion needed
        }
        
        target_format = format_map.get(platform)
        
        if not target_format:
            return content_path
        
        # Create output path
        filename = os.path.basename(content_path)
        name, ext = os.path.splitext(filename)
        output_dir = 'output/converted'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{name}_{platform}_{target_format.replace(':', 'x')}{ext}")
        
        # Skip if already converted
        if os.path.exists(output_path):
            return output_path
        
        try:
            if is_video:
                # Convert video
                self.video_converter.convert_format(content_path, output_path, target_format)
            else:
                # Convert image
                self.image_processor.crop_to_aspect_ratio(content_path, output_path, target_format)
            
            return output_path
        except Exception as e:
            print(f"Error preparing content for {platform}: {str(e)}")
            return content_path
    
    def publish_to_platform(self, platform: str, content_path: str,
                           caption: str, hashtags: str) -> Dict:
        """
        Publish content to a specific platform
        
        Args:
            platform: Platform name
            content_path: Path to content file
            caption: Post caption
            hashtags: Hashtags string
            
        Returns:
            Result dictionary
        """
        if platform not in self.publishers:
            return {
                'success': False,
                'error': f'{platform} publisher not initialized'
            }
        
        publisher = self.publishers[platform]
        
        # Prepare content for platform
        prepared_path = self.prepare_content(content_path, platform)
        
        # Combine caption and hashtags
        full_caption = f"{caption}\n\n{hashtags}" if hashtags else caption
        
        is_video = prepared_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))
        
        try:
            # Platform-specific publishing
            if platform == 'instagram':
                if is_video:
                    result = publisher.post_reel(prepared_path, full_caption)
                else:
                    result = publisher.post_photo(prepared_path, full_caption)
            
            elif platform == 'tiktok':
                result = publisher.post_video(prepared_path, caption, hashtags)
            
            elif platform == 'youtube':
                title = caption[:100] if len(caption) > 100 else caption
                description = f"{caption}\n\n{hashtags}"
                result = publisher.upload_short(prepared_path, title, description)
            
            elif platform == 'twitter':
                if is_video:
                    result = publisher.post_tweet_with_video(full_caption, prepared_path)
                else:
                    result = publisher.post_tweet_with_media(full_caption, [prepared_path])
            
            elif platform == 'facebook':
                if is_video:
                    result = publisher.post_reel(prepared_path, full_caption)
                else:
                    result = publisher.post_photo(prepared_path, full_caption)
            
            elif platform == 'pinterest':
                title = caption[:100] if len(caption) > 100 else caption
                result = publisher.create_pin(prepared_path, title, full_caption)
            
            elif platform == 'discord':
                result = publisher.send_file(prepared_path, full_caption)
            
            else:
                result = {
                    'success': False,
                    'error': f'Unknown platform: {platform}'
                }
            
            # Record in database
            if result.get('success'):
                self.database.add_post(
                    platform=platform,
                    content_path=content_path,
                    caption=caption,
                    hashtags=hashtags,
                    post_url=result.get('url', ''),
                    status='success'
                )
                self.database.increment_post_count(platform)
            else:
                self.database.add_post(
                    platform=platform,
                    content_path=content_path,
                    caption=caption,
                    hashtags=hashtags,
                    status='failed'
                )
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def publish_to_multiple(self, platforms: List[str], content_path: str,
                           caption: str, hashtags: str,
                           callback=None) -> Dict[str, Dict]:
        """
        Publish content to multiple platforms
        
        Args:
            platforms: List of platform names
            content_path: Path to content file
            caption: Post caption
            hashtags: Hashtags string
            callback: Optional callback function for progress updates
            
        Returns:
            Dictionary mapping platform names to results
        """
        results = {}
        
        for platform in platforms:
            if callback:
                callback(f"Publishing to {platform}...")
            
            result = self.publish_to_platform(platform, content_path, caption, hashtags)
            results[platform] = result
            
            if callback:
                if result.get('success'):
                    callback(f"✓ Successfully published to {platform}")
                else:
                    callback(f"✗ Failed to publish to {platform}: {result.get('error', 'Unknown error')}")
            
            # Small delay between posts
            time.sleep(2)
        
        return results
    
    def publish_async(self, platforms: List[str], content_path: str,
                     caption: str, hashtags: str, callback=None):
        """Publish asynchronously in background thread"""
        thread = threading.Thread(
            target=self.publish_to_multiple,
            args=(platforms, content_path, caption, hashtags, callback)
        )
        thread.daemon = True
        thread.start()
        return thread
    
    def get_publisher(self, platform: str):
        """Get publisher instance for a platform"""
        return self.publishers.get(platform)
    
    def cleanup(self):
        """Cleanup resources"""
        for platform, publisher in self.publishers.items():
            if hasattr(publisher, 'close'):
                try:
                    publisher.close()
                except:
                    pass
