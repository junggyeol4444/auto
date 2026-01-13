# -*- coding: utf-8 -*-
"""
네이버 블로그 발행기
Selenium을 사용하여 네이버 블로그에 자동으로 포스팅합니다.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NaverPublisher:
    """네이버 블로그 발행 클래스"""
    
    def __init__(self, user_id="", password=""):
        """
        Args:
            user_id (str): 네이버 ID
            password (str): 네이버 비밀번호
        """
        self.user_id = user_id
        self.password = password
        self.driver = None
    
    def init_driver(self, headless=False):
        """
        웹 드라이버 초기화
        
        Args:
            headless (bool): 헤드리스 모드 여부
        """
        try:
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            logger.info("웹 드라이버 초기화 완료")
            
        except Exception as e:
            logger.error(f"웹 드라이버 초기화 실패: {e}")
            raise
    
    def login(self):
        """
        네이버 로그인
        
        Returns:
            bool: 로그인 성공 여부
        """
        if not self.user_id or not self.password:
            logger.error("네이버 ID 또는 비밀번호가 없습니다")
            return False
        
        if not self.driver:
            self.init_driver()
        
        try:
            # 로그인 페이지 이동
            self.driver.get("https://nid.naver.com/nidlogin.login")
            time.sleep(2)
            
            # ID/PW 입력 (JavaScript 사용 - 자동화 감지 우회)
            self.driver.execute_script(
                f"document.getElementById('id').value = '{self.user_id}';"
            )
            time.sleep(1)
            
            self.driver.execute_script(
                f"document.getElementById('pw').value = '{self.password}';"
            )
            time.sleep(1)
            
            # 로그인 버튼 클릭
            login_btn = self.driver.find_element(By.ID, "log.login")
            login_btn.click()
            
            time.sleep(3)
            
            # 로그인 성공 확인
            if "naver.com" in self.driver.current_url:
                logger.info("네이버 로그인 성공")
                return True
            else:
                logger.error("네이버 로그인 실패")
                return False
                
        except Exception as e:
            logger.error(f"네이버 로그인 실패: {e}")
            return False
    
    def publish(self, title, content, category=None):
        """
        블로그 포스트 발행
        
        Args:
            title (str): 포스트 제목
            content (str): 포스트 내용 (HTML)
            category (str): 카테고리명
            
        Returns:
            dict: 발행 결과
        """
        if not self.driver:
            if not self.login():
                return {'success': False, 'error': 'Login failed'}
        
        try:
            # 블로그 글쓰기 페이지 이동
            self.driver.get("https://blog.naver.com/")
            time.sleep(2)
            
            # 글쓰기 버튼 클릭
            write_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "btn_post"))
            )
            write_btn.click()
            time.sleep(3)
            
            # iframe으로 전환
            self.driver.switch_to.frame("mainFrame")
            
            # 제목 입력
            title_input = self.driver.find_element(By.CLASS_NAME, "se-input")
            title_input.send_keys(title)
            time.sleep(1)
            
            # 본문 입력 (HTML 모드)
            content_area = self.driver.find_element(By.CLASS_NAME, "se-component-content")
            self.driver.execute_script(
                f"arguments[0].innerHTML = '{content}';",
                content_area
            )
            time.sleep(2)
            
            # 발행 버튼 클릭
            publish_btn = self.driver.find_element(By.CLASS_NAME, "btn_publish")
            publish_btn.click()
            time.sleep(3)
            
            logger.info("네이버 블로그 발행 성공")
            return {'success': True, 'url': self.driver.current_url}
            
        except Exception as e:
            logger.error(f"네이버 블로그 발행 실패: {e}")
            return {'success': False, 'error': str(e)}
    
    def close(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()
            logger.info("웹 드라이버 종료")


if __name__ == '__main__':
    # 테스트 코드
    publisher = NaverPublisher()
    
    print("네이버 블로그 발행기")
    print("실제 사용을 위해서는 네이버 ID와 비밀번호가 필요합니다.")
    print("주의: 자동화 감지 시스템으로 인해 실제 사용에 제한이 있을 수 있습니다.")
