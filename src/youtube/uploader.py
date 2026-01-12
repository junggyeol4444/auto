"""
YouTube API Module
Handles video uploads and metadata management
"""
import logging
import os
import pickle
from typing import Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class YouTubeUploader:
    """Class for uploading videos to YouTube using YouTube Data API v3"""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize YouTube uploader
        
        Args:
            credentials_path: Path to client_secrets.json or credentials file
        """
        self.credentials_path = credentials_path or 'credentials.json'
        self.youtube = None
        self.credentials = None
        
        # Try to initialize YouTube service
        if os.path.exists(self.credentials_path):
            self._initialize_service()
    
    def _initialize_service(self):
        """Initialize YouTube API service"""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
            
            creds = None
            token_path = 'token.pickle'
            
            # Check if we have saved credentials
            if os.path.exists(token_path):
                with open(token_path, 'rb') as token:
                    creds = pickle.load(token)
            
            # If no valid credentials, let user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if os.path.exists(self.credentials_path):
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.credentials_path, SCOPES)
                        creds = flow.run_local_server(port=0)
                    else:
                        logger.error(f"Credentials file not found: {self.credentials_path}")
                        return
                
                # Save credentials for future use
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)
            
            # Build YouTube service
            self.youtube = build('youtube', 'v3', credentials=creds)
            self.credentials = creds
            logger.info("YouTube API service initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing YouTube service: {e}")
            logger.info("Make sure you have a valid credentials.json file from Google Cloud Console")
    
    def upload_video(self, video_path: str, metadata: Dict) -> Optional[str]:
        """
        Upload video to YouTube
        
        Args:
            video_path: Path to video file
            metadata: Dictionary containing title, description, tags, etc.
        
        Returns:
            Video ID if successful, None otherwise
        """
        if not self.youtube:
            logger.error("YouTube service not initialized. Check credentials.")
            return None
        
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return None
        
        try:
            from googleapiclient.http import MediaFileUpload
            
            # Prepare request body
            body = {
                'snippet': {
                    'title': metadata.get('title', 'Untitled Video'),
                    'description': metadata.get('description', ''),
                    'tags': metadata.get('tags', []),
                    'categoryId': metadata.get('category', '22')
                },
                'status': {
                    'privacyStatus': metadata.get('privacy_status', 'private'),
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Create media upload
            media = MediaFileUpload(
                video_path,
                mimetype='video/*',
                resumable=True,
                chunksize=1024*1024  # 1MB chunks
            )
            
            # Create upload request
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            # Execute upload
            logger.info(f"Starting upload: {video_path}")
            response = None
            
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.info(f"Upload progress: {progress}%")
            
            video_id = response['id']
            logger.info(f"Video uploaded successfully! Video ID: {video_id}")
            logger.info(f"Video URL: https://www.youtube.com/watch?v={video_id}")
            
            return video_id
            
        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            return None
    
    def update_video_metadata(self, video_id: str, metadata: Dict) -> bool:
        """
        Update metadata for an existing video
        
        Args:
            video_id: YouTube video ID
            metadata: Dictionary containing updated metadata
        
        Returns:
            True if successful, False otherwise
        """
        if not self.youtube:
            logger.error("YouTube service not initialized")
            return False
        
        try:
            body = {
                'id': video_id,
                'snippet': {
                    'title': metadata.get('title'),
                    'description': metadata.get('description'),
                    'tags': metadata.get('tags'),
                    'categoryId': metadata.get('category', '22')
                }
            }
            
            self.youtube.videos().update(
                part='snippet',
                body=body
            ).execute()
            
            logger.info(f"Video metadata updated successfully: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating video metadata: {e}")
            return False
    
    def set_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """
        Set custom thumbnail for a video
        
        Args:
            video_id: YouTube video ID
            thumbnail_path: Path to thumbnail image
        
        Returns:
            True if successful, False otherwise
        """
        if not self.youtube:
            logger.error("YouTube service not initialized")
            return False
        
        if not os.path.exists(thumbnail_path):
            logger.error(f"Thumbnail not found: {thumbnail_path}")
            return False
        
        try:
            from googleapiclient.http import MediaFileUpload
            
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            ).execute()
            
            logger.info(f"Thumbnail set successfully: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting thumbnail: {e}")
            return False
    
    def get_video_info(self, video_id: str) -> Optional[Dict]:
        """
        Get information about an uploaded video
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            Dictionary with video information or None
        """
        if not self.youtube:
            logger.error("YouTube service not initialized")
            return None
        
        try:
            response = self.youtube.videos().list(
                part='snippet,status,statistics',
                id=video_id
            ).execute()
            
            if not response['items']:
                logger.error(f"Video not found: {video_id}")
                return None
            
            return response['items'][0]
            
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None
    
    def is_authenticated(self) -> bool:
        """Check if YouTube service is authenticated"""
        return self.youtube is not None
