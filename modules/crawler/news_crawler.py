# -*- coding: utf-8 -*-
"""
뉴스 크롤러
네이버 뉴스 검색 결과를 크롤링하고 본문을 추출합니다.
"""

import requests
from bs4 import BeautifulSoup
from newspaper import Article
import time
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsCrawler:
    """네이버 뉴스 크롤링 클래스"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.base_url = 'https://search.naver.com/search.naver'
    
    def search_news(self, keyword, max_results=10):
        """
        키워드로 네이버 뉴스 검색
        
        Args:
            keyword (str): 검색 키워드
            max_results (int): 최대 결과 수
            
        Returns:
            list: 뉴스 기사 정보 리스트
        """
        try:
            params = {
                'where': 'news',
                'query': keyword,
                'sm': 'tab_jum',
                'start': 1
            }
            
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = soup.select('.news_area')
            
            articles = []
            for item in news_items[:max_results]:
                try:
                    # 제목과 링크 추출
                    title_elem = item.select_one('.news_tit')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href')
                    
                    # 요약 추출
                    summary_elem = item.select_one('.news_dsc')
                    summary = summary_elem.get_text(strip=True) if summary_elem else ''
                    
                    # 언론사 추출
                    source_elem = item.select_one('.info_group .press')
                    source = source_elem.get_text(strip=True) if source_elem else ''
                    
                    articles.append({
                        'title': title,
                        'link': link,
                        'summary': summary,
                        'source': source,
                        'crawled_at': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    logger.warning(f"기사 항목 파싱 실패: {e}")
                    continue
            
            logger.info(f"{len(articles)}개의 뉴스 기사 검색 완료")
            return articles
            
        except Exception as e:
            logger.error(f"뉴스 검색 실패: {e}")
            return []
    
    def extract_article_content(self, url, max_retries=3):
        """
        기사 본문 추출
        
        Args:
            url (str): 기사 URL
            max_retries (int): 최대 재시도 횟수
            
        Returns:
            dict: 기사 정보
        """
        for attempt in range(max_retries):
            try:
                article = Article(url, language='ko')
                article.download()
                article.parse()
                
                return {
                    'title': article.title,
                    'text': article.text,
                    'authors': article.authors,
                    'publish_date': article.publish_date.isoformat() if article.publish_date else None,
                    'url': url
                }
                
            except Exception as e:
                logger.warning(f"기사 추출 실패 (시도 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    return None
        
        return None
    
    def crawl(self, keyword, max_articles=5):
        """
        키워드로 뉴스를 검색하고 본문을 추출
        
        Args:
            keyword (str): 검색 키워드
            max_articles (int): 추출할 최대 기사 수
            
        Returns:
            list: 전체 기사 정보 리스트
        """
        # 뉴스 검색
        news_list = self.search_news(keyword, max_results=max_articles * 2)
        
        # 본문 추출
        full_articles = []
        for news in news_list[:max_articles]:
            time.sleep(1)  # 요청 간격
            content = self.extract_article_content(news['link'])
            
            if content:
                # 검색 결과와 본문 병합
                full_article = {**news, **content}
                full_articles.append(full_article)
                
                if len(full_articles) >= max_articles:
                    break
        
        logger.info(f"총 {len(full_articles)}개의 기사 본문 추출 완료")
        return full_articles


if __name__ == '__main__':
    # 테스트 코드
    crawler = NewsCrawler()
    results = crawler.crawl('인공지능', max_articles=3)
    
    for i, article in enumerate(results, 1):
        print(f"\n=== 기사 {i} ===")
        print(f"제목: {article.get('title', 'N/A')}")
        print(f"본문 길이: {len(article.get('text', ''))} 자")
        print(f"URL: {article.get('url', 'N/A')}")
