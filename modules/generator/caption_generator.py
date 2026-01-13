"""
Caption Generator Module
Generates captions using templates and emojis
"""

import json
import random
import os
from typing import Dict, List


class CaptionGenerator:
    """Generate captions for social media posts"""
    
    def __init__(self, templates_path: str = 'templates/caption_templates.json',
                 emoji_path: str = 'templates/emoji_library.json',
                 config_path: str = 'config.json'):
        
        # Load templates
        if os.path.exists(templates_path):
            with open(templates_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.templates = data.get('templates', {})
                self.platform_limits = data.get('platform_specific', {})
        else:
            self.templates = {}
            self.platform_limits = {}
        
        # Load emoji library
        if os.path.exists(emoji_path):
            with open(emoji_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.emojis = data.get('categories', {})
                self.emoji_combos = data.get('common_combinations', [])
        else:
            self.emojis = {}
            self.emoji_combos = []
        
        # Load config
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.caption_settings = config.get('caption_settings', {})
        else:
            self.caption_settings = {
                'use_emoji': True,
                'add_cta': True,
                'default_template': 'simple'
            }
    
    def generate_caption(self, content: str, template_name: str = None,
                        platform: str = 'instagram', hashtags: str = '',
                        custom_cta: str = None) -> str:
        """
        Generate caption using template
        
        Args:
            content: Main content text
            template_name: Template to use (None = use default)
            platform: Target platform
            hashtags: Hashtags string (already formatted)
            custom_cta: Custom call-to-action (optional)
            
        Returns:
            Generated caption
        """
        # Select template
        if not template_name:
            template_name = self.caption_settings.get('default_template', 'simple')
        
        if template_name not in self.templates:
            template_name = 'simple'
        
        template = self.templates.get(template_name, {})
        format_str = template.get('format', '{content}\n\n{hashtags}')
        default_cta = template.get('cta', '')
        
        # Prepare caption
        cta = custom_cta if custom_cta else default_cta
        
        # Add emojis if enabled
        if self.caption_settings.get('use_emoji', True):
            content = self.add_emojis(content)
        
        # Format caption
        caption = format_str.format(
            content=content,
            cta=cta,
            hashtags=hashtags
        )
        
        # Enforce platform limits
        caption = self.enforce_platform_limit(caption, platform)
        
        return caption
    
    def add_emojis(self, text: str, category: str = None, count: int = 2) -> str:
        """
        Add emojis to text
        
        Args:
            text: Input text
            category: Emoji category (None = random)
            count: Number of emojis to add
            
        Returns:
            Text with emojis
        """
        if not self.emojis:
            return text
        
        # Select category
        if category and category in self.emojis:
            emoji_list = self.emojis[category]
        else:
            # Random category
            emoji_list = random.choice(list(self.emojis.values()))
        
        # Select random emojis
        selected_emojis = random.sample(emoji_list, min(count, len(emoji_list)))
        
        # Add to text (at the beginning or end)
        if random.choice([True, False]):
            return ' '.join(selected_emojis) + ' ' + text
        else:
            return text + ' ' + ' '.join(selected_emojis)
    
    def enforce_platform_limit(self, caption: str, platform: str) -> str:
        """
        Enforce character limit for platform
        
        Args:
            caption: Caption text
            platform: Target platform
            
        Returns:
            Trimmed caption if necessary
        """
        if platform not in self.platform_limits:
            return caption
        
        limit = self.platform_limits[platform].get('max_length', 5000)
        
        if len(caption) <= limit:
            return caption
        
        # Trim caption
        trimmed = caption[:limit-3] + '...'
        return trimmed
    
    def create_simple_caption(self, content: str, hashtags: str = '') -> str:
        """Create a simple caption"""
        return f"{content}\n\n{hashtags}" if hashtags else content
    
    def create_engaging_caption(self, content: str, hashtags: str = '',
                               question: str = "What do you think?") -> str:
        """Create an engaging caption with a question"""
        return f"✨ {content}\n\n💬 {question}\n\n{hashtags}"
    
    def create_promotional_caption(self, content: str, hashtags: str = '',
                                  cta: str = "Click the link in bio!") -> str:
        """Create a promotional caption"""
        return f"🔥 {content}\n\n🎯 {cta}\n\n{hashtags}"
    
    def create_story_caption(self, content: str, hook: str = None) -> str:
        """Create a story-style caption"""
        if hook:
            return f"{hook}\n\n{content}"
        return content
    
    def add_line_breaks(self, text: str, platform: str = 'instagram') -> str:
        """
        Add appropriate line breaks for platform
        
        Args:
            text: Input text
            platform: Target platform
            
        Returns:
            Text with line breaks
        """
        if platform not in self.platform_limits:
            return text
        
        line_breaks = self.platform_limits[platform].get('line_breaks', 2)
        separator = '\n' * line_breaks
        
        # Replace single line breaks with platform-specific breaks
        text = text.replace('\n', separator)
        
        return text
    
    def get_cta_suggestions(self) -> List[str]:
        """Get list of CTA suggestions"""
        return [
            "Follow for more! 👉",
            "Click the link in bio! 🔗",
            "Tag a friend who needs this! 👥",
            "Double tap if you agree! ❤️",
            "Save this for later! 📌",
            "Share with someone who needs to hear this! 📤",
            "Comment below! 💬",
            "Turn on post notifications! 🔔",
            "Check out our website! 🌐",
            "DM us for more info! 📩"
        ]
    
    def get_template_names(self) -> List[str]:
        """Get list of available template names"""
        return list(self.templates.keys())
    
    def get_emoji_categories(self) -> List[str]:
        """Get list of available emoji categories"""
        return list(self.emojis.keys())
