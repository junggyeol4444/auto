"""
Facebook Publisher Module
Publishes content to Facebook using Graph API
"""

import requests
import json
import os
from typing import Dict, List


class FacebookPublisher:
    """Publish content to Facebook"""
    
    def __init__(self, config_path: str = 'config.json'):
        self.config_path = config_path
        self.access_token = None
        self.page_id = None
        self.graph_api_url = 'https://graph.facebook.com/v18.0'
        
        # Load config
        self._load_config()
    
    def _load_config(self):
        """Load Facebook configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                facebook_config = config.get('platforms', {}).get('facebook', {})
                self.access_token = facebook_config.get('access_token', '')
                self.page_id = facebook_config.get('page_id', '')
    
    def verify_token(self) -> bool:
        """
        Verify access token is valid
        
        Returns:
            True if token is valid
        """
        try:
            url = f"{self.graph_api_url}/me"
            params = {'access_token': self.access_token}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                print("Facebook token is valid")
                return True
            else:
                raise Exception(f"Invalid token: {response.json()}")
            
        except Exception as e:
            raise Exception(f"Facebook token verification failed: {str(e)}")
    
    def post_text(self, message: str) -> Dict:
        """
        Post text to Facebook page
        
        Args:
            message: Post message
            
        Returns:
            Dictionary with post information
        """
        try:
            url = f"{self.graph_api_url}/{self.page_id}/feed"
            
            data = {
                'message': message,
                'access_token': self.access_token
            }
            
            response = requests.post(url, data=data)
            result = response.json()
            
            if 'id' in result:
                return {
                    'success': True,
                    'post_id': result['id'],
                    'url': f"https://www.facebook.com/{result['id']}"
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', {}).get('message', 'Unknown error')
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def post_photo(self, image_path: str, message: str = '') -> Dict:
        """
        Post a photo to Facebook page
        
        Args:
            image_path: Path to image file
            message: Optional caption
            
        Returns:
            Dictionary with post information
        """
        try:
            url = f"{self.graph_api_url}/{self.page_id}/photos"
            
            with open(image_path, 'rb') as image_file:
                files = {'source': image_file}
                data = {
                    'message': message,
                    'access_token': self.access_token
                }
                
                response = requests.post(url, data=data, files=files)
                result = response.json()
            
            if 'id' in result:
                return {
                    'success': True,
                    'post_id': result['id'],
                    'url': f"https://www.facebook.com/{result['id']}"
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', {}).get('message', 'Unknown error')
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def post_video(self, video_path: str, description: str = '') -> Dict:
        """
        Post a video to Facebook page
        
        Args:
            video_path: Path to video file
            description: Optional description
            
        Returns:
            Dictionary with post information
        """
        try:
            url = f"{self.graph_api_url}/{self.page_id}/videos"
            
            with open(video_path, 'rb') as video_file:
                files = {'source': video_file}
                data = {
                    'description': description,
                    'access_token': self.access_token
                }
                
                response = requests.post(url, data=data, files=files)
                result = response.json()
            
            if 'id' in result:
                return {
                    'success': True,
                    'video_id': result['id'],
                    'url': f"https://www.facebook.com/{result['id']}"
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', {}).get('message', 'Unknown error')
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def post_reel(self, video_path: str, description: str = '') -> Dict:
        """
        Post a Reel to Facebook page
        
        Args:
            video_path: Path to vertical video file
            description: Optional description
            
        Returns:
            Dictionary with post information
        """
        # Facebook Reels are posted similarly to videos
        # but with specific aspect ratio requirements (9:16)
        return self.post_video(video_path, description)
    
    def post_link(self, link: str, message: str = '') -> Dict:
        """
        Post a link to Facebook page
        
        Args:
            link: URL to share
            message: Optional message
            
        Returns:
            Dictionary with post information
        """
        try:
            url = f"{self.graph_api_url}/{self.page_id}/feed"
            
            data = {
                'link': link,
                'message': message,
                'access_token': self.access_token
            }
            
            response = requests.post(url, data=data)
            result = response.json()
            
            if 'id' in result:
                return {
                    'success': True,
                    'post_id': result['id'],
                    'url': f"https://www.facebook.com/{result['id']}"
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', {}).get('message', 'Unknown error')
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_page_info(self) -> Dict:
        """Get Facebook page information"""
        try:
            url = f"{self.graph_api_url}/{self.page_id}"
            params = {
                'fields': 'name,followers_count,fan_count',
                'access_token': self.access_token
            }
            
            response = requests.get(url, params=params)
            result = response.json()
            
            if 'name' in result:
                return {
                    'page_id': self.page_id,
                    'name': result.get('name'),
                    'followers': result.get('followers_count', 'N/A'),
                    'likes': result.get('fan_count', 'N/A')
                }
            else:
                return {'error': result.get('error', {}).get('message', 'Unknown error')}
            
        except Exception as e:
            return {'error': str(e)}
