"""
Twitter Publisher Module
Publishes content to Twitter using Tweepy
"""

import tweepy
import json
import os
from typing import Dict, List


class TwitterPublisher:
    """Publish content to Twitter"""
    
    def __init__(self, config_path: str = 'config.json'):
        self.config_path = config_path
        self.client = None
        self.api = None
        self.api_key = None
        self.api_secret = None
        self.access_token = None
        self.access_token_secret = None
        self.bearer_token = None
        
        # Load config
        self._load_config()
    
    def _load_config(self):
        """Load Twitter configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                twitter_config = config.get('platforms', {}).get('twitter', {})
                self.api_key = twitter_config.get('api_key', '')
                self.api_secret = twitter_config.get('api_secret', '')
                self.access_token = twitter_config.get('access_token', '')
                self.access_token_secret = twitter_config.get('access_token_secret', '')
                self.bearer_token = twitter_config.get('bearer_token', '')
    
    def authenticate(self) -> bool:
        """
        Authenticate with Twitter API
        
        Returns:
            True if authentication successful
        """
        try:
            # V2 Client for new features
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )
            
            # V1 API for media upload
            auth = tweepy.OAuth1UserHandler(
                self.api_key,
                self.api_secret,
                self.access_token,
                self.access_token_secret
            )
            self.api = tweepy.API(auth)
            
            # Verify credentials
            self.api.verify_credentials()
            
            print("Twitter authentication successful")
            return True
            
        except Exception as e:
            raise Exception(f"Twitter authentication failed: {str(e)}")
    
    def post_tweet(self, text: str) -> Dict:
        """
        Post a text tweet
        
        Args:
            text: Tweet text (max 280 characters)
            
        Returns:
            Dictionary with tweet information
        """
        try:
            if not self.client:
                self.authenticate()
            
            # Ensure text is within limit
            if len(text) > 280:
                text = text[:277] + '...'
            
            response = self.client.create_tweet(text=text)
            
            tweet_id = response.data['id']
            
            return {
                'success': True,
                'tweet_id': tweet_id,
                'url': f"https://twitter.com/i/web/status/{tweet_id}",
                'text': text
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def post_tweet_with_media(self, text: str, media_paths: List[str]) -> Dict:
        """
        Post a tweet with images (max 4 images)
        
        Args:
            text: Tweet text
            media_paths: List of image paths (max 4)
            
        Returns:
            Dictionary with tweet information
        """
        try:
            if not self.client or not self.api:
                self.authenticate()
            
            # Limit to 4 images
            media_paths = media_paths[:4]
            
            # Upload media using API v1
            media_ids = []
            for media_path in media_paths:
                media = self.api.media_upload(media_path)
                media_ids.append(media.media_id)
            
            # Post tweet with media using API v2
            if len(text) > 280:
                text = text[:277] + '...'
            
            response = self.client.create_tweet(
                text=text,
                media_ids=media_ids
            )
            
            tweet_id = response.data['id']
            
            return {
                'success': True,
                'tweet_id': tweet_id,
                'url': f"https://twitter.com/i/web/status/{tweet_id}",
                'text': text,
                'media_count': len(media_ids)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def post_tweet_with_video(self, text: str, video_path: str) -> Dict:
        """
        Post a tweet with video
        
        Args:
            text: Tweet text
            video_path: Path to video file
            
        Returns:
            Dictionary with tweet information
        """
        try:
            if not self.client or not self.api:
                self.authenticate()
            
            # Upload video using API v1
            media = self.api.media_upload(
                video_path,
                media_category='tweet_video'
            )
            
            # Post tweet with video using API v2
            if len(text) > 280:
                text = text[:277] + '...'
            
            response = self.client.create_tweet(
                text=text,
                media_ids=[media.media_id]
            )
            
            tweet_id = response.data['id']
            
            return {
                'success': True,
                'tweet_id': tweet_id,
                'url': f"https://twitter.com/i/web/status/{tweet_id}",
                'text': text
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def post_thread(self, tweets: List[str]) -> Dict:
        """
        Post a thread of tweets
        
        Args:
            tweets: List of tweet texts
            
        Returns:
            Dictionary with thread information
        """
        try:
            if not self.client:
                self.authenticate()
            
            tweet_ids = []
            previous_tweet_id = None
            
            for tweet_text in tweets:
                if len(tweet_text) > 280:
                    tweet_text = tweet_text[:277] + '...'
                
                if previous_tweet_id:
                    response = self.client.create_tweet(
                        text=tweet_text,
                        in_reply_to_tweet_id=previous_tweet_id
                    )
                else:
                    response = self.client.create_tweet(text=tweet_text)
                
                tweet_id = response.data['id']
                tweet_ids.append(tweet_id)
                previous_tweet_id = tweet_id
            
            return {
                'success': True,
                'tweet_ids': tweet_ids,
                'thread_url': f"https://twitter.com/i/web/status/{tweet_ids[0]}",
                'tweet_count': len(tweet_ids)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user_info(self) -> Dict:
        """Get authenticated user information"""
        try:
            if not self.api:
                self.authenticate()
            
            user = self.api.verify_credentials()
            
            return {
                'username': user.screen_name,
                'name': user.name,
                'followers': user.followers_count,
                'following': user.friends_count,
                'tweets': user.statuses_count
            }
            
        except Exception as e:
            return {'error': str(e)}
