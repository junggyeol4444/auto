# -*- coding: utf-8 -*-
"""
Instagram 크롤러
Instagram에서 만화/웹툰 콘텐츠를 수집합니다.
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstagramCrawler:
    """Instagram 크롤링 클래스 (데모)"""
    
    def __init__(self):
        logger.info("Instagram 크롤러 초기화")
        self.hashtags = ['webtoon', 'comic', 'manga', '웹툰']
    
    def crawl(self, max_results=10):
        """
        Instagram 크롤링
        
        실제 구현 시 instaloader 또는 Instagram Graph API 사용
        
        Args:
            max_results (int): 최대 결과 수
            
        Returns:
            list: 포스트 정보 리스트
        """
        logger.info("Instagram 크롤링 (데모 모드)")
        
        # 데모 데이터
        posts = []
        for i in range(min(max_results, 5)):
            posts.append({
                'caption': f'Instagram 포스트 {i+1} #webtoon #comic',
                'author': f'webtoon_artist_{i+1}',
                'followers': 4000 + i * 800,
                'likes': 200 + i * 40,
                'comments': 15 + i * 3,
                'url': f'https://www.instagram.com/p/sample{i+1}/'
            })
        
        logger.info(f"{len(posts)}개의 포스트 수집 완료")
        return posts


if __name__ == '__main__':
    crawler = InstagramCrawler()
    results = crawler.crawl(max_results=5)
    
    for i, post in enumerate(results, 1):
        print(f"=== 포스트 {i} ===")
        print(f"작성자: {post['author']} (팔로워: {post['followers']:,})")
        print(f"캡션: {post['caption']}")
        print(f"좋아요: {post['likes']}, 댓글: {post['comments']}\n")
