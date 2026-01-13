"""
Discord Publisher Module
Publishes content to Discord using Webhooks
"""

import requests
import json
import os
from typing import Dict, List


class DiscordPublisher:
    """Publish content to Discord via Webhooks"""
    
    def __init__(self, config_path: str = 'config.json'):
        self.config_path = config_path
        self.webhook_url = None
        
        # Load config
        self._load_config()
    
    def _load_config(self):
        """Load Discord configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                discord_config = config.get('platforms', {}).get('discord', {})
                self.webhook_url = discord_config.get('webhook_url', '')
    
    def verify_webhook(self) -> bool:
        """
        Verify webhook URL is valid
        
        Returns:
            True if webhook is valid
        """
        try:
            if not self.webhook_url:
                raise ValueError("Webhook URL not configured")
            
            response = requests.get(self.webhook_url)
            
            if response.status_code == 200:
                print("Discord webhook is valid")
                return True
            else:
                raise Exception(f"Invalid webhook: {response.status_code}")
            
        except Exception as e:
            raise Exception(f"Discord webhook verification failed: {str(e)}")
    
    def send_message(self, content: str, username: str = None, avatar_url: str = None) -> Dict:
        """
        Send a text message to Discord
        
        Args:
            content: Message content (max 2000 characters)
            username: Optional custom username
            avatar_url: Optional custom avatar URL
            
        Returns:
            Dictionary with send status
        """
        try:
            if len(content) > 2000:
                content = content[:1997] + '...'
            
            data = {'content': content}
            
            if username:
                data['username'] = username
            
            if avatar_url:
                data['avatar_url'] = avatar_url
            
            response = requests.post(
                self.webhook_url,
                json=data
            )
            
            if response.status_code == 204:
                return {
                    'success': True,
                    'message': 'Message sent successfully'
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to send message: {response.status_code}"
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_embed(self, title: str, description: str, color: int = 0x3498db,
                   fields: List[Dict] = None, image_url: str = None,
                   thumbnail_url: str = None, footer: str = None,
                   author_name: str = None, url: str = None) -> Dict:
        """
        Send an embed message to Discord
        
        Args:
            title: Embed title
            description: Embed description
            color: Embed color (hex integer, default: blue)
            fields: List of field dictionaries with 'name' and 'value'
            image_url: URL of image to display
            thumbnail_url: URL of thumbnail image
            footer: Footer text
            author_name: Author name
            url: URL to link the title
            
        Returns:
            Dictionary with send status
        """
        try:
            embed = {
                'title': title,
                'description': description,
                'color': color
            }
            
            if url:
                embed['url'] = url
            
            if fields:
                embed['fields'] = fields
            
            if image_url:
                embed['image'] = {'url': image_url}
            
            if thumbnail_url:
                embed['thumbnail'] = {'url': thumbnail_url}
            
            if footer:
                embed['footer'] = {'text': footer}
            
            if author_name:
                embed['author'] = {'name': author_name}
            
            data = {'embeds': [embed]}
            
            response = requests.post(
                self.webhook_url,
                json=data
            )
            
            if response.status_code == 204:
                return {
                    'success': True,
                    'message': 'Embed sent successfully'
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to send embed: {response.status_code}"
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_file(self, file_path: str, content: str = None) -> Dict:
        """
        Send a file to Discord
        
        Args:
            file_path: Path to file
            content: Optional message content
            
        Returns:
            Dictionary with send status
        """
        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                data = {}
                
                if content:
                    if len(content) > 2000:
                        content = content[:1997] + '...'
                    data['content'] = content
                
                response = requests.post(
                    self.webhook_url,
                    data=data,
                    files=files
                )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'File sent successfully'
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to send file: {response.status_code}"
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_announcement(self, title: str, content: str, image_url: str = None) -> Dict:
        """
        Send an announcement-style message
        
        Args:
            title: Announcement title
            content: Announcement content
            image_url: Optional image URL
            
        Returns:
            Dictionary with send status
        """
        return self.send_embed(
            title=f"📢 {title}",
            description=content,
            color=0xe74c3c,  # Red
            image_url=image_url,
            footer="Announcement from Social Media Automation Suite"
        )
    
    def send_update(self, platform: str, status: str, url: str = None) -> Dict:
        """
        Send a post update notification
        
        Args:
            platform: Platform name
            status: Status message
            url: Optional post URL
            
        Returns:
            Dictionary with send status
        """
        fields = [
            {'name': 'Platform', 'value': platform, 'inline': True},
            {'name': 'Status', 'value': status, 'inline': True}
        ]
        
        if url:
            fields.append({'name': 'URL', 'value': url, 'inline': False})
        
        return self.send_embed(
            title="🎉 New Post Published",
            description=f"Successfully posted to {platform}",
            color=0x2ecc71,  # Green
            fields=fields,
            footer="Social Media Automation Suite"
        )
