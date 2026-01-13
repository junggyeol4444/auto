"""
YouTube Publisher Module
Publishes content to YouTube using YouTube Data API v3
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json
import os
import pickle
from typing import Dict


class YouTubePublisher:
    """Publish content to YouTube"""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self, config_path: str = 'config.json'):
        self.config_path = config_path
        self.youtube = None
        self.credentials = None
        self.client_secrets_file = None
        self.credentials_file = None
        
        # Load config
        self._load_config()
    
    def _load_config(self):
        """Load YouTube configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                youtube_config = config.get('platforms', {}).get('youtube', {})
                self.client_secrets_file = youtube_config.get('client_secrets_file', 'client_secrets.json')
                self.credentials_file = youtube_config.get('credentials_file', 'cache/sessions/youtube_credentials.json')
    
    def authenticate(self) -> bool:
        """
        Authenticate with YouTube API
        
        Returns:
            True if authentication successful
        """
        try:
            creds = None
            
            # Load existing credentials
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'rb') as token:
                    creds = pickle.load(token)
            
            # If credentials are invalid or don't exist, authenticate
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.client_secrets_file):
                        raise FileNotFoundError(
                            f"Client secrets file not found: {self.client_secrets_file}\n"
                            "Please download it from Google Cloud Console"
                        )
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.client_secrets_file, self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                
                # Save credentials
                os.makedirs(os.path.dirname(self.credentials_file), exist_ok=True)
                with open(self.credentials_file, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.credentials = creds
            self.youtube = build('youtube', 'v3', credentials=creds)
            
            print("YouTube authentication successful")
            return True
            
        except Exception as e:
            raise Exception(f"YouTube authentication failed: {str(e)}")
    
    def upload_video(self, video_path: str, title: str, description: str,
                    category_id: str = '22', privacy_status: str = 'public',
                    tags: list = None) -> Dict:
        """
        Upload video to YouTube
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            category_id: YouTube category ID (22 = People & Blogs)
            privacy_status: 'public', 'private', or 'unlisted'
            tags: List of tags
            
        Returns:
            Dictionary with video information
        """
        try:
            if not self.youtube:
                self.authenticate()
            
            # Prepare request body
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'categoryId': category_id
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            if tags:
                body['snippet']['tags'] = tags
            
            # Create media upload
            media = MediaFileUpload(
                video_path,
                mimetype='video/*',
                resumable=True,
                chunksize=1024*1024
            )
            
            # Execute upload
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"Upload progress: {int(status.progress() * 100)}%")
            
            video_id = response['id']
            
            return {
                'success': True,
                'video_id': video_id,
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'title': title
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def upload_short(self, video_path: str, title: str, description: str,
                    tags: list = None, privacy_status: str = 'public') -> Dict:
        """
        Upload YouTube Short
        
        Args:
            video_path: Path to vertical video file (9:16 format, < 60 seconds)
            title: Short title
            description: Short description (must include #Shorts)
            tags: List of tags
            privacy_status: 'public', 'private', or 'unlisted'
            
        Returns:
            Dictionary with video information
        """
        # Ensure #Shorts is in description
        if '#Shorts' not in description and '#shorts' not in description:
            description = f"{description}\n\n#Shorts"
        
        return self.upload_video(
            video_path=video_path,
            title=title,
            description=description,
            category_id='22',
            privacy_status=privacy_status,
            tags=tags
        )
    
    def get_channel_info(self) -> Dict:
        """Get channel information"""
        try:
            if not self.youtube:
                self.authenticate()
            
            request = self.youtube.channels().list(
                part='snippet,statistics',
                mine=True
            )
            response = request.execute()
            
            if 'items' in response and len(response['items']) > 0:
                channel = response['items'][0]
                snippet = channel['snippet']
                stats = channel['statistics']
                
                return {
                    'channel_id': channel['id'],
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'subscribers': stats.get('subscriberCount', 'Hidden'),
                    'views': stats.get('viewCount', '0'),
                    'videos': stats.get('videoCount', '0')
                }
            else:
                return {'error': 'No channel found'}
            
        except Exception as e:
            return {'error': str(e)}
