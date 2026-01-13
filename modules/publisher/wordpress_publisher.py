# -*- coding: utf-8 -*-
"""
워드프레스 발행기
WordPress XML-RPC API를 사용하여 포스팅합니다.
"""

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, EditPost
from wordpress_xmlrpc.methods import posts
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WordPressPublisher:
    """워드프레스 발행 클래스"""
    
    def __init__(self, url="", username="", password=""):
        """
        Args:
            url (str): 워드프레스 사이트 URL
            username (str): 사용자명
            password (str): 비밀번호 또는 앱 비밀번호
        """
        self.url = url
        self.username = username
        self.password = password
        self.client = None
        
        if url and username and password:
            self._init_client()
    
    def _init_client(self):
        """클라이언트 초기화"""
        try:
            xmlrpc_url = f"{self.url}/xmlrpc.php"
            self.client = Client(xmlrpc_url, self.username, self.password)
            logger.info("워드프레스 클라이언트 초기화 완료")
        except Exception as e:
            logger.error(f"워드프레스 클라이언트 초기화 실패: {e}")
            self.client = None
    
    def test_connection(self):
        """
        연결 테스트
        
        Returns:
            bool: 연결 성공 여부
        """
        if not self.client:
            logger.error("클라이언트가 초기화되지 않았습니다")
            return False
        
        try:
            # 최근 포스트 목록 가져오기 시도
            self.client.call(posts.GetPosts())
            logger.info("워드프레스 연결 성공")
            return True
        except Exception as e:
            logger.error(f"워드프레스 연결 실패: {e}")
            return False
    
    def publish(self, title, content, status='publish', tags=None, categories=None):
        """
        포스트 발행
        
        Args:
            title (str): 포스트 제목
            content (str): 포스트 내용 (HTML)
            status (str): 발행 상태 ('draft', 'publish', 'private')
            tags (list): 태그 리스트
            categories (list): 카테고리 리스트
            
        Returns:
            dict: 발행 결과
        """
        if not self.client:
            logger.error("클라이언트가 초기화되지 않았습니다")
            return {'success': False, 'error': 'Client not initialized'}
        
        try:
            post = WordPressPost()
            post.title = title
            post.content = content
            post.post_status = status
            
            if tags:
                post.terms_names = {
                    'post_tag': tags
                }
            
            if categories:
                post.terms_names = post.terms_names or {}
                post.terms_names['category'] = categories
            
            # 포스트 발행
            post_id = self.client.call(NewPost(post))
            
            # 포스트 URL 생성
            post_url = f"{self.url}/?p={post_id}"
            
            logger.info(f"워드프레스 발행 성공: {post_url}")
            return {
                'success': True,
                'post_id': post_id,
                'url': post_url
            }
            
        except Exception as e:
            logger.error(f"워드프레스 발행 실패: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_post(self, post_id, title=None, content=None, status=None):
        """
        포스트 수정
        
        Args:
            post_id (int): 포스트 ID
            title (str): 새 제목
            content (str): 새 내용
            status (str): 새 상태
            
        Returns:
            dict: 수정 결과
        """
        if not self.client:
            logger.error("클라이언트가 초기화되지 않았습니다")
            return {'success': False, 'error': 'Client not initialized'}
        
        try:
            post = WordPressPost()
            post.id = post_id
            
            if title:
                post.title = title
            if content:
                post.content = content
            if status:
                post.post_status = status
            
            self.client.call(EditPost(post_id, post))
            
            logger.info(f"워드프레스 포스트 수정 성공: {post_id}")
            return {'success': True, 'post_id': post_id}
            
        except Exception as e:
            logger.error(f"워드프레스 수정 실패: {e}")
            return {'success': False, 'error': str(e)}


if __name__ == '__main__':
    # 테스트 코드
    publisher = WordPressPublisher()
    
    print("워드프레스 발행기")
    print("실제 사용을 위해서는 워드프레스 사이트 URL, 사용자명, 비밀번호가 필요합니다.")
    print("XML-RPC가 활성화되어 있어야 합니다.")
