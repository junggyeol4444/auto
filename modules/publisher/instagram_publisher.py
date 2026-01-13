"""
Instagram Publisher Module
Publishes content to Instagram using instagrapi
"""

from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import json
import os
from typing import List, Dict
import time


class InstagramPublisher:
    """Publish content to Instagram"""
    
    def __init__(self, config_path: str = 'config.json'):
        self.client = Client()
        self.config_path = config_path
        self.session_file = None
        self.username = None
        self.password = None
        
        # Load config
        self._load_config()
    
    def _load_config(self):
        """Load Instagram configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                instagram_config = config.get('platforms', {}).get('instagram', {})
                self.username = instagram_config.get('username', '')
                self.password = instagram_config.get('password', '')
                self.session_file = instagram_config.get('session_file', 'cache/sessions/instagram_session.json')
    
    def login(self) -> bool:
        """
        Login to Instagram
        
        Returns:
            True if login successful
        """
        try:
            # Try to load existing session
            if os.path.exists(self.session_file):
                try:
                    self.client.load_settings(self.session_file)
                    self.client.login(self.username, self.password)
                    
                    # Verify session is still valid
                    self.client.get_timeline_feed()
                    print("Loaded existing Instagram session")
                    return True
                except Exception as e:
                    print(f"Existing session invalid: {str(e)}")
            
            # Fresh login
            if not self.username or not self.password:
                raise ValueError("Instagram username and password not configured")
            
            self.client.login(self.username, self.password)
            
            # Save session
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            self.client.dump_settings(self.session_file)
            
            print("Instagram login successful")
            return True
            
        except Exception as e:
            raise Exception(f"Instagram login failed: {str(e)}")
    
    def post_photo(self, image_path: str, caption: str) -> Dict:
        """
        Post a photo to Instagram feed
        
        Args:
            image_path: Path to image file
            caption: Post caption
            
        Returns:
            Dictionary with post information
        """
        try:
            if not self.client.user_id:
                self.login()
            
            media = self.client.photo_upload(
                path=image_path,
                caption=caption
            )
            
            return {
                'success': True,
                'media_id': media.id,
                'media_pk': media.pk,
                'code': media.code,
                'url': f"https://www.instagram.com/p/{media.code}/"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def post_carousel(self, image_paths: List[str], caption: str) -> Dict:
        """
        Post a carousel (multiple images) to Instagram
        
        Args:
            image_paths: List of image file paths
            caption: Post caption
            
        Returns:
            Dictionary with post information
        """
        try:
            if not self.client.user_id:
                self.login()
            
            media = self.client.album_upload(
                paths=image_paths,
                caption=caption
            )
            
            return {
                'success': True,
                'media_id': media.id,
                'media_pk': media.pk,
                'code': media.code,
                'url': f"https://www.instagram.com/p/{media.code}/"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def post_reel(self, video_path: str, caption: str, cover_path: str = None) -> Dict:
        """
        Post a Reel to Instagram
        
        Args:
            video_path: Path to video file (must be vertical 9:16)
            caption: Post caption
            cover_path: Optional path to cover image
            
        Returns:
            Dictionary with post information
        """
        try:
            if not self.client.user_id:
                self.login()
            
            media = self.client.clip_upload(
                path=video_path,
                caption=caption,
                thumbnail=cover_path
            )
            
            return {
                'success': True,
                'media_id': media.id,
                'media_pk': media.pk,
                'code': media.code,
                'url': f"https://www.instagram.com/reel/{media.code}/"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def post_story(self, media_path: str, caption: str = '') -> Dict:
        """
        Post a story to Instagram
        
        Args:
            media_path: Path to image or video file
            caption: Optional story caption
            
        Returns:
            Dictionary with post information
        """
        try:
            if not self.client.user_id:
                self.login()
            
            # Determine if it's a photo or video
            if media_path.lower().endswith(('.mp4', '.mov', '.avi')):
                media = self.client.video_upload_to_story(
                    path=media_path,
                    caption=caption
                )
            else:
                media = self.client.photo_upload_to_story(
                    path=media_path,
                    caption=caption
                )
            
            return {
                'success': True,
                'media_id': media.id,
                'media_pk': media.pk
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_account_info(self) -> Dict:
        """Get account information"""
        try:
            if not self.client.user_id:
                self.login()
            
            user_info = self.client.account_info()
            
            return {
                'username': user_info.username,
                'full_name': user_info.full_name,
                'followers': user_info.follower_count,
                'following': user_info.following_count,
                'posts': user_info.media_count
            }
            
        except Exception as e:
            return {
                'error': str(e)
            }
    
    def logout(self):
        """Logout from Instagram"""
        try:
            self.client.logout()
        except:
            pass
