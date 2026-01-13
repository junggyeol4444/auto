# -*- coding: utf-8 -*-
"""
이미지 검색기
무료 스톡 이미지를 검색합니다.
"""

import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageSearcher:
    """이미지 검색 클래스"""
    
    def __init__(self, unsplash_key="", pexels_key=""):
        """
        Args:
            unsplash_key (str): Unsplash API 키
            pexels_key (str): Pexels API 키
        """
        self.unsplash_key = unsplash_key
        self.pexels_key = pexels_key
        self.unsplash_url = "https://api.unsplash.com/search/photos"
        self.pexels_url = "https://api.pexels.com/v1/search"
    
    def search_unsplash(self, keyword, per_page=10):
        """
        Unsplash에서 이미지 검색
        
        Args:
            keyword (str): 검색 키워드
            per_page (int): 페이지당 결과 수
            
        Returns:
            list: 이미지 정보 리스트
        """
        if not self.unsplash_key:
            logger.warning("Unsplash API 키가 없습니다")
            return []
        
        try:
            headers = {
                'Authorization': f'Client-ID {self.unsplash_key}'
            }
            params = {
                'query': keyword,
                'per_page': per_page
            }
            
            response = requests.get(self.unsplash_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            images = []
            for item in results:
                images.append({
                    'url': item['urls']['regular'],
                    'thumb_url': item['urls']['thumb'],
                    'download_url': item['urls']['full'],
                    'author': item['user']['name'],
                    'author_url': item['user']['links']['html'],
                    'description': item.get('description', ''),
                    'source': 'unsplash'
                })
            
            logger.info(f"Unsplash: {len(images)}개 이미지 검색 완료")
            return images
            
        except Exception as e:
            logger.error(f"Unsplash 검색 실패: {e}")
            return []
    
    def search_pexels(self, keyword, per_page=10):
        """
        Pexels에서 이미지 검색
        
        Args:
            keyword (str): 검색 키워드
            per_page (int): 페이지당 결과 수
            
        Returns:
            list: 이미지 정보 리스트
        """
        if not self.pexels_key:
            logger.warning("Pexels API 키가 없습니다")
            return []
        
        try:
            headers = {
                'Authorization': self.pexels_key
            }
            params = {
                'query': keyword,
                'per_page': per_page
            }
            
            response = requests.get(self.pexels_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            photos = data.get('photos', [])
            
            images = []
            for photo in photos:
                images.append({
                    'url': photo['src']['large'],
                    'thumb_url': photo['src']['small'],
                    'download_url': photo['src']['original'],
                    'author': photo['photographer'],
                    'author_url': photo['photographer_url'],
                    'description': '',
                    'source': 'pexels'
                })
            
            logger.info(f"Pexels: {len(images)}개 이미지 검색 완료")
            return images
            
        except Exception as e:
            logger.error(f"Pexels 검색 실패: {e}")
            return []
    
    def search(self, keyword, source='both', max_results=10):
        """
        이미지 검색 (통합)
        
        Args:
            keyword (str): 검색 키워드
            source (str): 소스 ('unsplash', 'pexels', 'both')
            max_results (int): 최대 결과 수
            
        Returns:
            list: 이미지 정보 리스트
        """
        images = []
        
        if source in ['unsplash', 'both']:
            unsplash_images = self.search_unsplash(keyword, per_page=max_results)
            images.extend(unsplash_images)
        
        if source in ['pexels', 'both'] and len(images) < max_results:
            remaining = max_results - len(images)
            pexels_images = self.search_pexels(keyword, per_page=remaining)
            images.extend(pexels_images)
        
        logger.info(f"총 {len(images)}개 이미지 검색 완료")
        return images[:max_results]
    
    def generate_image_credit(self, image_info):
        """
        이미지 크레딧 텍스트 생성
        
        Args:
            image_info (dict): 이미지 정보
            
        Returns:
            str: 크레딧 HTML
        """
        author = image_info.get('author', 'Unknown')
        author_url = image_info.get('author_url', '#')
        source = image_info.get('source', 'Unknown')
        
        if source == 'unsplash':
            credit = f'Photo by <a href="{author_url}">{author}</a> on <a href="https://unsplash.com">Unsplash</a>'
        elif source == 'pexels':
            credit = f'Photo by <a href="{author_url}">{author}</a> on <a href="https://pexels.com">Pexels</a>'
        else:
            credit = f'Photo by {author}'
        
        return f'<small>{credit}</small>'


if __name__ == '__main__':
    # 테스트 코드 (데모 모드)
    searcher = ImageSearcher()
    
    # API 키 없이는 빈 리스트 반환
    results = searcher.search('technology', max_results=5)
    print(f"검색 결과: {len(results)}개")
    
    if results:
        for i, img in enumerate(results, 1):
            print(f"\n이미지 {i}:")
            print(f"  URL: {img['url']}")
            print(f"  작성자: {img['author']}")
            print(f"  출처: {img['source']}")
