"""
쇼핑몰 크롤러
Shopping Mall Crawlers
"""
import logging
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re

logger = logging.getLogger('crawlers')


class BaseCrawler:
    """기본 크롤러 클래스"""
    
    def __init__(self, use_selenium=False):
        self.use_selenium = use_selenium
        self.driver = None
        
        if use_selenium:
            self.init_selenium()
    
    def init_selenium(self):
        """Selenium 초기화"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            logger.error(f'Selenium 초기화 실패: {str(e)}')
    
    def close(self):
        """크롤러 종료"""
        if self.driver:
            self.driver.quit()
    
    def extract_price(self, price_text: str) -> float:
        """가격 텍스트에서 숫자 추출"""
        if not price_text:
            return 0.0
        
        # 숫자만 추출
        price_str = re.sub(r'[^0-9]', '', price_text)
        
        try:
            return float(price_str)
        except ValueError:
            return 0.0


class CoupangCrawler(BaseCrawler):
    """쿠팡 크롤러"""
    
    def crawl(self, url: str) -> dict:
        """쿠팡 상품 정보 크롤링"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 상품명
            name_elem = soup.select_one('.prod-buy-header__title')
            name = name_elem.get_text(strip=True) if name_elem else '알 수 없음'
            
            # 가격
            price_elem = soup.select_one('.total-price strong')
            price_text = price_elem.get_text(strip=True) if price_elem else '0'
            price = self.extract_price(price_text)
            
            # 재고
            in_stock = True
            sold_out = soup.select_one('.prod-soldout')
            if sold_out:
                in_stock = False
            
            logger.info(f'쿠팡 크롤링 성공: {name}')
            
            return {
                'name': name,
                'price': price,
                'in_stock': in_stock,
                'site': '쿠팡'
            }
        
        except Exception as e:
            logger.error(f'쿠팡 크롤링 실패: {str(e)}')
            return None


class NaverShoppingCrawler(BaseCrawler):
    """네이버 쇼핑 크롤러"""
    
    def crawl(self, url: str) -> dict:
        """네이버 쇼핑 상품 정보 크롤링"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 상품명
            name_elem = soup.select_one('.h_product')
            name = name_elem.get_text(strip=True) if name_elem else '알 수 없음'
            
            # 가격
            price_elem = soup.select_one('.price_num')
            price_text = price_elem.get_text(strip=True) if price_elem else '0'
            price = self.extract_price(price_text)
            
            # 재고
            in_stock = True
            
            logger.info(f'네이버 쇼핑 크롤링 성공: {name}')
            
            return {
                'name': name,
                'price': price,
                'in_stock': in_stock,
                'site': '네이버쇼핑'
            }
        
        except Exception as e:
            logger.error(f'네이버 쇼핑 크롤링 실패: {str(e)}')
            return None


class ST11Crawler(BaseCrawler):
    """11번가 크롤러"""
    
    def crawl(self, url: str) -> dict:
        """11번가 상품 정보 크롤링"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 상품명
            name_elem = soup.select_one('.title')
            name = name_elem.get_text(strip=True) if name_elem else '알 수 없음'
            
            # 가격
            price_elem = soup.select_one('.sale_price')
            price_text = price_elem.get_text(strip=True) if price_elem else '0'
            price = self.extract_price(price_text)
            
            # 재고
            in_stock = True
            
            logger.info(f'11번가 크롤링 성공: {name}')
            
            return {
                'name': name,
                'price': price,
                'in_stock': in_stock,
                'site': '11번가'
            }
        
        except Exception as e:
            logger.error(f'11번가 크롤링 실패: {str(e)}')
            return None


class GmarketCrawler(BaseCrawler):
    """지마켓 크롤러"""
    
    def crawl(self, url: str) -> dict:
        """지마켓 상품 정보 크롤링"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 상품명
            name_elem = soup.select_one('.itemtit')
            name = name_elem.get_text(strip=True) if name_elem else '알 수 없음'
            
            # 가격
            price_elem = soup.select_one('.price_innerwrap')
            price_text = price_elem.get_text(strip=True) if price_elem else '0'
            price = self.extract_price(price_text)
            
            # 재고
            in_stock = True
            
            logger.info(f'지마켓 크롤링 성공: {name}')
            
            return {
                'name': name,
                'price': price,
                'in_stock': in_stock,
                'site': '지마켓'
            }
        
        except Exception as e:
            logger.error(f'지마켓 크롤링 실패: {str(e)}')
            return None


class AuctionCrawler(BaseCrawler):
    """옥션 크롤러"""
    
    def crawl(self, url: str) -> dict:
        """옥션 상품 정보 크롤링"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 상품명
            name_elem = soup.select_one('.itemtit')
            name = name_elem.get_text(strip=True) if name_elem else '알 수 없음'
            
            # 가격
            price_elem = soup.select_one('.price_innerwrap')
            price_text = price_elem.get_text(strip=True) if price_elem else '0'
            price = self.extract_price(price_text)
            
            # 재고
            in_stock = True
            
            logger.info(f'옥션 크롤링 성공: {name}')
            
            return {
                'name': name,
                'price': price,
                'in_stock': in_stock,
                'site': '옥션'
            }
        
        except Exception as e:
            logger.error(f'옥션 크롤링 실패: {str(e)}')
            return None


class CrawlerFactory:
    """크롤러 팩토리"""
    
    @staticmethod
    def get_crawler(url: str) -> BaseCrawler:
        """URL에 맞는 크롤러 반환"""
        if 'coupang.com' in url:
            return CoupangCrawler()
        elif 'shopping.naver.com' in url:
            return NaverShoppingCrawler()
        elif '11st.co.kr' in url:
            return ST11Crawler()
        elif 'gmarket.co.kr' in url:
            return GmarketCrawler()
        elif 'auction.co.kr' in url:
            return AuctionCrawler()
        else:
            return BaseCrawler()


if __name__ == '__main__':
    print("쇼핑몰 크롤러 모듈이 로드되었습니다.")
