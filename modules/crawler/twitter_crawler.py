# -*- coding: utf-8 -*-
"""
트위터 크롤러
트위터에서 만화 관련 콘텐츠를 크롤링합니다.
"""

import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterCrawler:
    """트위터 크롤링 클래스 (공개 검색 기반)"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.hashtags = ['漫画', 'comic', 'manga', '웹툰', 'webtoon']
    
    def search_by_hashtag(self, hashtag, max_results=10):
        """
        해시태그로 검색 (시뮬레이션)
        
        실제 구현 시 Twitter API v2 또는 nitter 등을 사용
        
        Args:
            hashtag (str): 해시태그
            max_results (int): 최대 결과 수
            
        Returns:
            list: 트윗 정보 리스트
        """
        logger.info(f"해시태그 #{hashtag} 검색 중...")
        
        # 실제 구현 시 Twitter API 사용
        # 여기서는 데모 데이터 반환
        tweets = []
        
        try:
            # Twitter API 호출 로직
            # tweets = self._call_twitter_api(hashtag, max_results)
            
            # 데모 데이터
            tweets = self._generate_demo_data(hashtag, max_results)
            
            logger.info(f"{len(tweets)}개의 트윗 발견")
            return tweets
            
        except Exception as e:
            logger.error(f"트위터 검색 실패: {e}")
            return []
    
    def _generate_demo_data(self, hashtag, count):
        """데모 데이터 생성"""
        demo_tweets = []
        for i in range(min(count, 5)):
            demo_tweets.append({
                'text': f"#{hashtag} 관련 샘플 트윗 {i+1}",
                'author': f'manga_artist_{i+1}',
                'followers': 5000 + i * 1000,
                'likes': 100 + i * 20,
                'retweets': 20 + i * 5,
                'created_at': datetime.now().isoformat(),
                'url': f'https://twitter.com/sample/status/{i+1}',
                'media_urls': []
            })
        return demo_tweets
    
    def filter_by_followers(self, tweets, max_followers=10000):
        """
        팔로워 수로 필터링 (신인 작가)
        
        Args:
            tweets (list): 트윗 리스트
            max_followers (int): 최대 팔로워 수
            
        Returns:
            list: 필터링된 트윗 리스트
        """
        filtered = [
            tweet for tweet in tweets
            if tweet.get('followers', 0) < max_followers
        ]
        logger.info(f"{len(filtered)}개의 신인 작가 트윗 필터링됨")
        return filtered
    
    def crawl(self, hashtags=None, max_results=20, filter_new_artists=True):
        """
        여러 해시태그로 크롤링
        
        Args:
            hashtags (list): 해시태그 리스트
            max_results (int): 해시태그당 최대 결과 수
            filter_new_artists (bool): 신인 작가 필터링 여부
            
        Returns:
            list: 트윗 정보 리스트
        """
        if hashtags is None:
            hashtags = self.hashtags
        
        all_tweets = []
        
        for hashtag in hashtags:
            tweets = self.search_by_hashtag(hashtag, max_results)
            all_tweets.extend(tweets)
        
        # 중복 제거
        unique_tweets = self._remove_duplicates(all_tweets)
        
        # 신인 작가 필터링
        if filter_new_artists:
            unique_tweets = self.filter_by_followers(unique_tweets)
        
        logger.info(f"총 {len(unique_tweets)}개의 트윗 수집 완료")
        return unique_tweets
    
    def _remove_duplicates(self, tweets):
        """중복 제거"""
        seen = set()
        unique = []
        
        for tweet in tweets:
            tweet_id = tweet.get('url', '')
            if tweet_id not in seen:
                seen.add(tweet_id)
                unique.append(tweet)
        
        return unique


if __name__ == '__main__':
    # 테스트 코드
    crawler = TwitterCrawler()
    results = crawler.crawl(hashtags=['manga', 'comic'], max_results=5)
    
    print(f"\n총 {len(results)}개의 트윗 수집됨\n")
    
    for i, tweet in enumerate(results, 1):
        print(f"=== 트윗 {i} ===")
        print(f"작성자: {tweet['author']}")
        print(f"팔로워: {tweet['followers']:,}")
        print(f"내용: {tweet['text']}")
        print(f"좋아요: {tweet['likes']}, 리트윗: {tweet['retweets']}\n")
