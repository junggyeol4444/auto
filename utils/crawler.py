"""
Web crawler utility
"""
import requests
from bs4 import BeautifulSoup


class Crawler:
    """Web crawler for gathering information"""
    
    @staticmethod
    def fetch_url(url, timeout=10):
        """Fetch content from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            raise Exception(f"URL 접근 오류: {str(e)}")
    
    @staticmethod
    def parse_html(html_content):
        """Parse HTML content"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup
        except Exception as e:
            raise Exception(f"HTML 파싱 오류: {str(e)}")
    
    @staticmethod
    def extract_text(soup):
        """Extract text from BeautifulSoup object"""
        try:
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            raise Exception(f"텍스트 추출 오류: {str(e)}")
