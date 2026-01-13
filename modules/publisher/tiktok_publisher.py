"""
TikTok Publisher Module
Publishes content to TikTok using Selenium web automation
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
import os
import time
from typing import Dict


class TikTokPublisher:
    """Publish content to TikTok using web automation"""
    
    def __init__(self, config_path: str = 'config.json'):
        self.config_path = config_path
        self.driver = None
        self.username = None
        self.password = None
        self.headless = False
        
        # Load config
        self._load_config()
    
    def _load_config(self):
        """Load TikTok configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                tiktok_config = config.get('platforms', {}).get('tiktok', {})
                self.username = tiktok_config.get('username', '')
                self.password = tiktok_config.get('password', '')
                self.headless = tiktok_config.get('headless', False)
    
    def _setup_driver(self):
        """Setup Selenium WebDriver"""
        options = Options()
        
        if self.headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # Disable automation flags
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def login(self) -> bool:
        """
        Login to TikTok
        
        Returns:
            True if login successful
        """
        try:
            if not self.driver:
                self._setup_driver()
            
            # Navigate to TikTok login
            self.driver.get('https://www.tiktok.com/login')
            time.sleep(3)
            
            # Click on "Use phone / email / username" button
            try:
                login_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Use phone / email / username')]"))
                )
                login_button.click()
                time.sleep(2)
            except:
                pass
            
            # Enter username
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(self.username)
            time.sleep(1)
            
            # Enter password
            password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
            password_input.send_keys(self.password)
            time.sleep(1)
            
            # Click login button
            login_submit = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_submit.click()
            time.sleep(5)
            
            # Check if login was successful
            if "tiktok.com" in self.driver.current_url and "/login" not in self.driver.current_url:
                print("TikTok login successful")
                return True
            else:
                raise Exception("Login may have failed - please check manually")
            
        except Exception as e:
            raise Exception(f"TikTok login failed: {str(e)}")
    
    def post_video(self, video_path: str, caption: str, hashtags: str = '') -> Dict:
        """
        Post a video to TikTok
        
        Args:
            video_path: Path to video file (vertical 9:16 format)
            caption: Video caption
            hashtags: Hashtags string
            
        Returns:
            Dictionary with post information
        """
        try:
            if not self.driver:
                self.login()
            
            # Navigate to upload page
            self.driver.get('https://www.tiktok.com/upload')
            time.sleep(3)
            
            # Upload video file
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            
            # Convert to absolute path
            abs_video_path = os.path.abspath(video_path)
            file_input.send_keys(abs_video_path)
            
            # Wait for video to upload
            time.sleep(10)
            
            # Enter caption
            caption_text = f"{caption}\n\n{hashtags}" if hashtags else caption
            
            try:
                caption_area = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
                )
                caption_area.click()
                caption_area.send_keys(caption_text)
                time.sleep(2)
            except:
                # Try alternative selector
                caption_input = self.driver.find_element(By.XPATH, "//textarea")
                caption_input.send_keys(caption_text)
                time.sleep(2)
            
            # Click post button
            try:
                post_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Post')]"))
                )
                post_button.click()
                time.sleep(5)
                
                return {
                    'success': True,
                    'message': 'Video posted to TikTok successfully'
                }
            except:
                return {
                    'success': False,
                    'error': 'Could not find post button - manual intervention may be required'
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def close(self):
        """Close browser"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def __del__(self):
        """Cleanup on deletion"""
        self.close()
