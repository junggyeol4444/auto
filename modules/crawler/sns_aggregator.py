# -*- coding: utf-8 -*-
"""
SNS 통합 크롤러
여러 SNS 플랫폼에서 만화/웹툰 콘텐츠를 수집합니다.
"""

import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SnsAggregator:
    """SNS 통합 크롤링 클래스"""
    
    def __init__(self):
        self.platforms = []
    
    def add_crawler(self, crawler, platform_name):
        """
        크롤러 추가
        
        Args:
            crawler: 크롤러 인스턴스
            platform_name (str): 플랫폼 이름
        """
        self.platforms.append({
            'crawler': crawler,
            'name': platform_name
        })
        logger.info(f"{platform_name} 크롤러 추가됨")
    
    def crawl_all(self, keyword=None, max_results_per_platform=10):
        """
        모든 플랫폼에서 크롤링
        
        Args:
            keyword (str): 검색 키워드
            max_results_per_platform (int): 플랫폼당 최대 결과 수
            
        Returns:
            dict: 플랫폼별 결과
        """
        results = {}
        
        for platform in self.platforms:
            platform_name = platform['name']
            crawler = platform['crawler']
            
            try:
                logger.info(f"{platform_name}에서 크롤링 중...")
                
                # 크롤러 메서드 호출
                if hasattr(crawler, 'crawl'):
                    data = crawler.crawl(max_results=max_results_per_platform)
                elif hasattr(crawler, 'search'):
                    data = crawler.search(keyword, max_results=max_results_per_platform)
                else:
                    logger.warning(f"{platform_name} 크롤러에 적절한 메서드가 없음")
                    data = []
                
                results[platform_name] = data
                logger.info(f"{platform_name}: {len(data)}개 수집")
                
            except Exception as e:
                logger.error(f"{platform_name} 크롤링 실패: {e}")
                results[platform_name] = []
        
        return results
    
    def aggregate_and_rank(self, results, ranking_criteria='engagement'):
        """
        결과 집계 및 랭킹
        
        Args:
            results (dict): 플랫폼별 결과
            ranking_criteria (str): 랭킹 기준 ('engagement', 'followers', 'recent')
            
        Returns:
            list: 랭킹된 콘텐츠 리스트
        """
        all_content = []
        
        # 모든 플랫폼 결과 병합
        for platform_name, content_list in results.items():
            for content in content_list:
                content['platform'] = platform_name
                all_content.append(content)
        
        # 랭킹 기준에 따라 정렬
        if ranking_criteria == 'engagement':
            # 좋아요 + 리트윗/공유 등의 합
            all_content.sort(
                key=lambda x: x.get('likes', 0) + x.get('retweets', 0) + x.get('shares', 0),
                reverse=True
            )
        elif ranking_criteria == 'followers':
            all_content.sort(
                key=lambda x: x.get('followers', 0),
                reverse=True
            )
        elif ranking_criteria == 'recent':
            all_content.sort(
                key=lambda x: x.get('created_at', ''),
                reverse=True
            )
        
        logger.info(f"총 {len(all_content)}개의 콘텐츠 집계 완료")
        return all_content
    
    def filter_new_artists(self, content_list, max_followers=10000):
        """
        신인 작가 필터링
        
        Args:
            content_list (list): 콘텐츠 리스트
            max_followers (int): 최대 팔로워 수
            
        Returns:
            list: 필터링된 리스트
        """
        filtered = [
            content for content in content_list
            if content.get('followers', 0) < max_followers
        ]
        logger.info(f"{len(filtered)}개의 신인 작가 콘텐츠 필터링됨")
        return filtered
    
    def create_summary_report(self, results):
        """
        요약 보고서 생성
        
        Args:
            results (dict): 플랫폼별 결과
            
        Returns:
            str: 요약 보고서
        """
        report = "=== SNS 크롤링 요약 ===\n\n"
        
        total_count = 0
        for platform_name, content_list in results.items():
            count = len(content_list)
            total_count += count
            report += f"{platform_name}: {count}개\n"
        
        report += f"\n총 수집 콘텐츠: {total_count}개\n"
        report += f"수집 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return report


if __name__ == '__main__':
    # 테스트 코드
    from twitter_crawler import TwitterCrawler
    
    aggregator = SnsAggregator()
    
    # 트위터 크롤러 추가
    twitter = TwitterCrawler()
    aggregator.add_crawler(twitter, 'Twitter')
    
    # 크롤링 실행
    results = aggregator.crawl_all(keyword='manga', max_results_per_platform=5)
    
    # 요약 보고서
    report = aggregator.create_summary_report(results)
    print(report)
    
    # 랭킹
    ranked = aggregator.aggregate_and_rank(results, ranking_criteria='engagement')
    
    print("\n=== 상위 콘텐츠 ===")
    for i, content in enumerate(ranked[:3], 1):
        print(f"{i}. [{content['platform']}] {content.get('author', 'N/A')}")
        print(f"   팔로워: {content.get('followers', 0):,}")
        print(f"   인게이지먼트: 좋아요 {content.get('likes', 0)}, 리트윗 {content.get('retweets', 0)}\n")
