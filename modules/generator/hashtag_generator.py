"""
Hashtag Generator Module
Generates hashtags using RAKE algorithm and trending hashtags
"""

from rake_nltk import Rake
import json
import random
import re
from typing import List, Dict
import os


class HashtagGenerator:
    """Generate hashtags for social media posts"""
    
    def __init__(self, config_path: str = 'config.json'):
        self.rake = Rake()
        
        # Load config
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.hashtag_settings = config.get('hashtag_settings', {})
        else:
            self.hashtag_settings = {
                'instagram_count': 30,
                'tiktok_count': 20,
                'youtube_count': 15,
                'twitter_count': 5,
                'default_hashtags': []
            }
        
        # Popular hashtags by category
        self.popular_hashtags = {
            'general': ['viral', 'trending', 'fyp', 'foryou', 'explore', 'instagood', 
                       'photooftheday', 'love', 'like', 'follow'],
            'lifestyle': ['lifestyle', 'lifestyleblogger', 'dailylife', 'motivation',
                         'inspiration', 'goals', 'success', 'mindset'],
            'business': ['business', 'entrepreneur', 'marketing', 'success',
                        'motivation', 'startup', 'hustle', 'businessowner'],
            'fitness': ['fitness', 'gym', 'workout', 'health', 'fitfam',
                       'bodybuilding', 'exercise', 'training'],
            'food': ['food', 'foodie', 'foodporn', 'yummy', 'delicious',
                    'foodstagram', 'instafood', 'cooking'],
            'travel': ['travel', 'traveling', 'travelphotography', 'wanderlust',
                      'adventure', 'explore', 'vacation', 'travelgram'],
            'fashion': ['fashion', 'style', 'ootd', 'fashionblogger', 'fashionista',
                       'outfit', 'instafashion', 'styling'],
            'beauty': ['beauty', 'makeup', 'skincare', 'beautyblogger', 'cosmetics',
                      'makeupartist', 'beautytips', 'selfcare'],
            'technology': ['tech', 'technology', 'innovation', 'digital', 'gadgets',
                          'ai', 'coding', 'programming'],
            'art': ['art', 'artist', 'artwork', 'creative', 'design',
                   'illustration', 'drawing', 'painting']
        }
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        Extract keywords from text using RAKE algorithm
        
        Args:
            text: Input text
            max_keywords: Maximum number of keywords to extract
            
        Returns:
            List of keywords
        """
        try:
            self.rake.extract_keywords_from_text(text)
            keywords = self.rake.get_ranked_phrases()
            
            # Convert to hashtag format (remove spaces, make lowercase)
            hashtags = []
            for keyword in keywords[:max_keywords]:
                # Remove special characters and spaces
                clean = re.sub(r'[^a-zA-Z0-9\s]', '', keyword)
                # Convert to camelCase for multi-word hashtags
                words = clean.split()
                if words:
                    hashtag = words[0].lower() + ''.join(w.capitalize() for w in words[1:])
                    if hashtag and len(hashtag) > 2:
                        hashtags.append(hashtag)
            
            return hashtags
            
        except Exception as e:
            print(f"Error extracting keywords: {str(e)}")
            return []
    
    def get_category_hashtags(self, category: str, count: int = 10) -> List[str]:
        """
        Get popular hashtags for a specific category
        
        Args:
            category: Category name
            count: Number of hashtags to return
            
        Returns:
            List of hashtags
        """
        if category in self.popular_hashtags:
            hashtags = self.popular_hashtags[category].copy()
            random.shuffle(hashtags)
            return hashtags[:count]
        return []
    
    def generate_hashtags(self, content: str, platform: str = 'instagram',
                         category: str = 'general', include_trending: bool = True) -> List[str]:
        """
        Generate hashtags for content
        
        Args:
            content: Content text to analyze
            platform: Target platform
            category: Content category
            include_trending: Whether to include trending hashtags
            
        Returns:
            List of hashtags
        """
        # Get target count for platform
        count_key = f'{platform}_count'
        target_count = self.hashtag_settings.get(count_key, 15)
        
        # Extract keywords from content
        keyword_hashtags = self.extract_keywords(content, max_keywords=target_count // 2)
        
        # Add category-specific hashtags
        category_hashtags = self.get_category_hashtags(category, count=target_count // 3)
        
        # Add general popular hashtags
        general_hashtags = self.get_category_hashtags('general', count=target_count // 4)
        
        # Combine all hashtags
        all_hashtags = keyword_hashtags + category_hashtags + general_hashtags
        
        # Add default hashtags from config
        default_hashtags = self.hashtag_settings.get('default_hashtags', [])
        all_hashtags.extend(default_hashtags)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_hashtags = []
        for tag in all_hashtags:
            if tag.lower() not in seen:
                seen.add(tag.lower())
                unique_hashtags.append(tag)
        
        # Trim to target count
        hashtags = unique_hashtags[:target_count]
        
        return hashtags
    
    def format_hashtags(self, hashtags: List[str], platform: str = 'instagram') -> str:
        """
        Format hashtags for a specific platform
        
        Args:
            hashtags: List of hashtags (without # symbol)
            platform: Target platform
            
        Returns:
            Formatted hashtag string
        """
        if not hashtags:
            return ''
        
        # Add # symbol
        formatted = ['#' + tag for tag in hashtags]
        
        # Platform-specific formatting
        if platform in ['instagram', 'tiktok', 'facebook']:
            # Space-separated on one or multiple lines
            return ' '.join(formatted)
        elif platform == 'twitter':
            # Keep it compact for Twitter
            return ' '.join(formatted)
        elif platform == 'youtube':
            # Comma-separated for YouTube description
            return ', '.join(formatted)
        else:
            return ' '.join(formatted)
    
    def add_custom_hashtags(self, hashtags: List[str], custom: List[str]) -> List[str]:
        """
        Add custom hashtags to the list
        
        Args:
            hashtags: Existing hashtag list
            custom: Custom hashtags to add
            
        Returns:
            Combined hashtag list
        """
        # Remove # if present in custom hashtags
        custom_clean = [tag.lstrip('#') for tag in custom]
        
        # Combine and remove duplicates
        all_tags = hashtags + custom_clean
        seen = set()
        unique = []
        for tag in all_tags:
            if tag.lower() not in seen:
                seen.add(tag.lower())
                unique.append(tag)
        
        return unique
    
    def get_platform_limit(self, platform: str) -> int:
        """Get hashtag limit for platform"""
        count_key = f'{platform}_count'
        return self.hashtag_settings.get(count_key, 15)
