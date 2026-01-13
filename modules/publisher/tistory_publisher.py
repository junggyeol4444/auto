# -*- coding: utf-8 -*-
"""
티스토리 발행기
티스토리 API를 사용하여 블로그에 포스팅합니다.
"""

import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TistoryPublisher:
    """티스토리 발행 클래스"""
    
    def __init__(self, access_token="", blog_name=""):
        """
        Args:
            access_token (str): 티스토리 액세스 토큰
            blog_name (str): 블로그 이름
        """
        self.access_token = access_token
        self.blog_name = blog_name
        self.api_base = "https://www.tistory.com/apis"
    
    def test_connection(self):
        """
        연결 테스트
        
        Returns:
            bool: 연결 성공 여부
        """
        if not self.access_token:
            logger.error("액세스 토큰이 없습니다")
            return False
        
        try:
            url = f"{self.api_base}/blog/info"
            params = {
                'access_token': self.access_token,
                'output': 'json'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('tistory', {}).get('status') == '200':
                logger.info("티스토리 연결 성공")
                return True
            else:
                logger.error("티스토리 연결 실패")
                return False
                
        except Exception as e:
            logger.error(f"티스토리 연결 테스트 실패: {e}")
            return False
    
    def publish(self, title, content, category=0, visibility=3, tag=None):
        """
        포스트 발행
        
        Args:
            title (str): 포스트 제목
            content (str): 포스트 내용 (HTML)
            category (int): 카테고리 ID (0: 기본)
            visibility (int): 공개 설정 (0: 비공개, 1: 보호, 3: 공개)
            tag (str): 태그 (쉼표로 구분)
            
        Returns:
            dict: 발행 결과
        """
        if not self.access_token or not self.blog_name:
            logger.error("액세스 토큰 또는 블로그 이름이 없습니다")
            return {'success': False, 'error': 'Missing credentials'}
        
        try:
            url = f"{self.api_base}/post/write"
            
            data = {
                'access_token': self.access_token,
                'output': 'json',
                'blogName': self.blog_name,
                'title': title,
                'content': content,
                'visibility': visibility,
                'category': category
            }
            
            if tag:
                data['tag'] = tag
            
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('tistory', {}).get('status') == '200':
                post_url = result.get('tistory', {}).get('url', '')
                logger.info(f"티스토리 발행 성공: {post_url}")
                return {
                    'success': True,
                    'url': post_url,
                    'postId': result.get('tistory', {}).get('postId', '')
                }
            else:
                error_msg = result.get('tistory', {}).get('error_message', 'Unknown error')
                logger.error(f"티스토리 발행 실패: {error_msg}")
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            logger.error(f"티스토리 발행 실패: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_post(self, post_id, title, content, category=0, visibility=3, tag=None):
        """
        포스트 수정
        
        Args:
            post_id (str): 포스트 ID
            title (str): 포스트 제목
            content (str): 포스트 내용
            category (int): 카테고리 ID
            visibility (int): 공개 설정
            tag (str): 태그
            
        Returns:
            dict: 수정 결과
        """
        try:
            url = f"{self.api_base}/post/modify"
            
            data = {
                'access_token': self.access_token,
                'output': 'json',
                'blogName': self.blog_name,
                'postId': post_id,
                'title': title,
                'content': content,
                'visibility': visibility,
                'category': category
            }
            
            if tag:
                data['tag'] = tag
            
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('tistory', {}).get('status') == '200':
                logger.info(f"티스토리 포스트 수정 성공: {post_id}")
                return {'success': True, 'postId': post_id}
            else:
                error_msg = result.get('tistory', {}).get('error_message', 'Unknown error')
                logger.error(f"티스토리 수정 실패: {error_msg}")
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            logger.error(f"티스토리 수정 실패: {e}")
            return {'success': False, 'error': str(e)}


if __name__ == '__main__':
    # 테스트 코드
    publisher = TistoryPublisher()
    
    # 자격증명 없이는 실패
    result = publisher.test_connection()
    print(f"연결 테스트: {'성공' if result else '실패'}")
    
    # 발행 테스트 (데모)
    print("\n실제 발행을 위해서는 access_token과 blog_name이 필요합니다.")
