"""
Web Crawler Module
Crawls news sites (Naver, Daum) and Wikipedia/NamuWiki for content collection
"""
import requests
from bs4 import BeautifulSoup
import logging
import time
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseCrawler:
    """Base class for web crawlers"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page"""
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None


class NaverNewsCrawler(BaseCrawler):
    """Crawler for Naver News"""
    
    def search_news(self, keyword: str, max_results: int = 10) -> List[Dict]:
        """Search news articles by keyword"""
        articles = []
        base_url = "https://search.naver.com/search.naver"
        
        try:
            params = {
                'where': 'news',
                'query': keyword,
                'sort': 0  # Latest
            }
            
            soup = self.fetch_page(base_url + '?' + '&'.join([f"{k}={v}" for k, v in params.items()]))
            if not soup:
                return articles
            
            news_items = soup.select('.news_area')[:max_results]
            
            for item in news_items:
                try:
                    title_elem = item.select_one('.news_tit')
                    title = title_elem.text.strip() if title_elem else ""
                    link = title_elem['href'] if title_elem and 'href' in title_elem.attrs else ""
                    
                    desc_elem = item.select_one('.news_dsc')
                    description = desc_elem.text.strip() if desc_elem else ""
                    
                    articles.append({
                        'title': title,
                        'link': link,
                        'description': description,
                        'source': 'Naver News',
                        'timestamp': datetime.now().isoformat()
                    })
                except Exception as e:
                    logger.warning(f"Error parsing news item: {e}")
                    continue
            
            logger.info(f"Crawled {len(articles)} articles from Naver News")
            
        except Exception as e:
            logger.error(f"Error searching Naver News: {e}")
        
        return articles


class DaumNewsCrawler(BaseCrawler):
    """Crawler for Daum News"""
    
    def search_news(self, keyword: str, max_results: int = 10) -> List[Dict]:
        """Search news articles by keyword"""
        articles = []
        base_url = "https://search.daum.net/search"
        
        try:
            params = {
                'w': 'news',
                'q': keyword,
                'sort': 'recency'
            }
            
            soup = self.fetch_page(base_url + '?' + '&'.join([f"{k}={v}" for k, v in params.items()]))
            if not soup:
                return articles
            
            news_items = soup.select('.c-item-doc')[:max_results]
            
            for item in news_items:
                try:
                    title_elem = item.select_one('.tit-g')
                    title = title_elem.text.strip() if title_elem else ""
                    link = title_elem.find('a')['href'] if title_elem and title_elem.find('a') else ""
                    
                    desc_elem = item.select_one('.c-contents-desc')
                    description = desc_elem.text.strip() if desc_elem else ""
                    
                    articles.append({
                        'title': title,
                        'link': link,
                        'description': description,
                        'source': 'Daum News',
                        'timestamp': datetime.now().isoformat()
                    })
                except Exception as e:
                    logger.warning(f"Error parsing news item: {e}")
                    continue
            
            logger.info(f"Crawled {len(articles)} articles from Daum News")
            
        except Exception as e:
            logger.error(f"Error searching Daum News: {e}")
        
        return articles


class WikipediaCrawler(BaseCrawler):
    """Crawler for Wikipedia"""
    
    def get_article(self, topic: str, lang: str = 'ko') -> Optional[Dict]:
        """Get Wikipedia article content"""
        try:
            url = f"https://{lang}.wikipedia.org/wiki/{topic.replace(' ', '_')}"
            soup = self.fetch_page(url)
            
            if not soup:
                return None
            
            # Get main content
            content_div = soup.select_one('#mw-content-text')
            if not content_div:
                return None
            
            # Extract paragraphs
            paragraphs = []
            for p in content_div.select('p'):
                text = p.text.strip()
                if text and len(text) > 50:  # Filter short paragraphs
                    paragraphs.append(text)
            
            # Get title
            title_elem = soup.select_one('#firstHeading')
            title = title_elem.text.strip() if title_elem else topic
            
            return {
                'title': title,
                'content': '\n\n'.join(paragraphs[:10]),  # Limit to first 10 paragraphs
                'url': url,
                'source': 'Wikipedia',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error crawling Wikipedia: {e}")
            return None


class NamuWikiCrawler(BaseCrawler):
    """Crawler for NamuWiki"""
    
    def get_article(self, topic: str) -> Optional[Dict]:
        """Get NamuWiki article content"""
        try:
            url = f"https://namu.wiki/w/{topic.replace(' ', '%20')}"
            soup = self.fetch_page(url)
            
            if not soup:
                return None
            
            # Get main content
            content_div = soup.select_one('.wiki-content')
            if not content_div:
                return None
            
            # Extract paragraphs
            paragraphs = []
            for p in content_div.select('p'):
                text = p.text.strip()
                if text and len(text) > 50:
                    paragraphs.append(text)
            
            return {
                'title': topic,
                'content': '\n\n'.join(paragraphs[:10]),
                'url': url,
                'source': 'NamuWiki',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error crawling NamuWiki: {e}")
            return None


class ContentCrawler:
    """Main crawler class that aggregates all crawlers"""
    
    def __init__(self):
        self.naver_crawler = NaverNewsCrawler()
        self.daum_crawler = DaumNewsCrawler()
        self.wikipedia_crawler = WikipediaCrawler()
        self.namuwiki_crawler = NamuWikiCrawler()
    
    def crawl_news(self, keyword: str, max_results: int = 5) -> List[Dict]:
        """Crawl news from multiple sources"""
        all_articles = []
        
        # Crawl from Naver
        naver_articles = self.naver_crawler.search_news(keyword, max_results)
        all_articles.extend(naver_articles)
        
        time.sleep(1)  # Be polite
        
        # Crawl from Daum
        daum_articles = self.daum_crawler.search_news(keyword, max_results)
        all_articles.extend(daum_articles)
        
        return all_articles
    
    def crawl_wiki(self, topic: str) -> Dict:
        """Crawl from Wikipedia and NamuWiki"""
        results = {
            'wikipedia': None,
            'namuwiki': None
        }
        
        # Try Wikipedia first
        results['wikipedia'] = self.wikipedia_crawler.get_article(topic)
        time.sleep(1)
        
        # Try NamuWiki
        results['namuwiki'] = self.namuwiki_crawler.get_article(topic)
        
        return results
    
    def crawl_content(self, topic: str, include_news: bool = True, 
                     include_wiki: bool = True) -> Dict:
        """Crawl all available content for a topic"""
        content = {
            'topic': topic,
            'news_articles': [],
            'wiki_content': {},
            'timestamp': datetime.now().isoformat()
        }
        
        if include_news:
            logger.info(f"Crawling news for: {topic}")
            content['news_articles'] = self.crawl_news(topic)
        
        if include_wiki:
            logger.info(f"Crawling wiki content for: {topic}")
            content['wiki_content'] = self.crawl_wiki(topic)
        
        return content
