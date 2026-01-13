"""
Pinterest Publisher Module
Publishes content to Pinterest using Pinterest API
"""

import requests
import json
import os
from typing import Dict


class PinterestPublisher:
    """Publish content to Pinterest"""
    
    def __init__(self, config_path: str = 'config.json'):
        self.config_path = config_path
        self.access_token = None
        self.board_id = None
        self.api_url = 'https://api.pinterest.com/v5'
        
        # Load config
        self._load_config()
    
    def _load_config(self):
        """Load Pinterest configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                pinterest_config = config.get('platforms', {}).get('pinterest', {})
                self.access_token = pinterest_config.get('access_token', '')
                self.board_id = pinterest_config.get('board_id', '')
    
    def _get_headers(self) -> Dict:
        """Get API request headers"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def verify_token(self) -> bool:
        """
        Verify access token is valid
        
        Returns:
            True if token is valid
        """
        try:
            url = f"{self.api_url}/user_account"
            response = requests.get(url, headers=self._get_headers())
            
            if response.status_code == 200:
                print("Pinterest token is valid")
                return True
            else:
                raise Exception(f"Invalid token: {response.json()}")
            
        except Exception as e:
            raise Exception(f"Pinterest token verification failed: {str(e)}")
    
    def create_pin(self, image_path: str, title: str, description: str = '',
                   link: str = None, alt_text: str = None) -> Dict:
        """
        Create a pin on Pinterest
        
        Args:
            image_path: Path to image file
            title: Pin title (required)
            description: Pin description
            link: Optional destination link
            alt_text: Optional alt text for accessibility
            
        Returns:
            Dictionary with pin information
        """
        try:
            # First, upload the image
            upload_url = f"{self.api_url}/media"
            
            with open(image_path, 'rb') as image_file:
                files = {'file': image_file}
                upload_response = requests.post(
                    upload_url,
                    headers={'Authorization': f'Bearer {self.access_token}'},
                    files=files
                )
            
            if upload_response.status_code != 201:
                return {
                    'success': False,
                    'error': f"Image upload failed: {upload_response.text}"
                }
            
            media_id = upload_response.json().get('media_id')
            
            # Create the pin
            pin_url = f"{self.api_url}/pins"
            
            pin_data = {
                'board_id': self.board_id,
                'title': title,
                'description': description,
                'media_source': {
                    'source_type': 'image_upload',
                    'media_id': media_id
                }
            }
            
            if link:
                pin_data['link'] = link
            
            if alt_text:
                pin_data['alt_text'] = alt_text
            
            response = requests.post(
                pin_url,
                headers=self._get_headers(),
                json=pin_data
            )
            
            result = response.json()
            
            if response.status_code == 201:
                return {
                    'success': True,
                    'pin_id': result.get('id'),
                    'url': result.get('link', 'https://pinterest.com')
                }
            else:
                return {
                    'success': False,
                    'error': result.get('message', 'Unknown error')
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_pin_from_url(self, image_url: str, title: str, description: str = '',
                           link: str = None) -> Dict:
        """
        Create a pin from an image URL
        
        Args:
            image_url: URL of the image
            title: Pin title
            description: Pin description
            link: Optional destination link
            
        Returns:
            Dictionary with pin information
        """
        try:
            url = f"{self.api_url}/pins"
            
            pin_data = {
                'board_id': self.board_id,
                'title': title,
                'description': description,
                'media_source': {
                    'source_type': 'image_url',
                    'url': image_url
                }
            }
            
            if link:
                pin_data['link'] = link
            
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=pin_data
            )
            
            result = response.json()
            
            if response.status_code == 201:
                return {
                    'success': True,
                    'pin_id': result.get('id'),
                    'url': result.get('link', 'https://pinterest.com')
                }
            else:
                return {
                    'success': False,
                    'error': result.get('message', 'Unknown error')
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_boards(self) -> Dict:
        """Get list of user's boards"""
        try:
            url = f"{self.api_url}/boards"
            response = requests.get(url, headers=self._get_headers())
            
            if response.status_code == 200:
                result = response.json()
                boards = result.get('items', [])
                
                return {
                    'success': True,
                    'boards': [
                        {
                            'id': board.get('id'),
                            'name': board.get('name'),
                            'description': board.get('description')
                        }
                        for board in boards
                    ]
                }
            else:
                return {
                    'success': False,
                    'error': response.json().get('message', 'Unknown error')
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user_info(self) -> Dict:
        """Get Pinterest user account information"""
        try:
            url = f"{self.api_url}/user_account"
            response = requests.get(url, headers=self._get_headers())
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'username': result.get('username'),
                    'account_type': result.get('account_type'),
                    'profile_image': result.get('profile_image'),
                    'website_url': result.get('website_url')
                }
            else:
                return {'error': response.json().get('message', 'Unknown error')}
            
        except Exception as e:
            return {'error': str(e)}
