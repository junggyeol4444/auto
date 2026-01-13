# -*- coding: utf-8 -*-
"""
메타 태그 생성기
SEO를 위한 메타 태그를 자동 생성합니다.
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetaGenerator:
    """메타 태그 생성 클래스"""
    
    def __init__(self):
        pass
    
    def generate_meta_description(self, content, max_length=160):
        """
        메타 디스크립션 생성
        
        Args:
            content (str): 콘텐츠 텍스트
            max_length (int): 최대 길이
            
        Returns:
            str: 메타 디스크립션
        """
        if not content:
            return ""
        
        # 첫 문장들을 사용
        sentences = content.split('. ')
        description = ""
        
        for sentence in sentences:
            if len(description + sentence) < max_length:
                description += sentence + '. '
            else:
                break
        
        # 길이 제한
        if len(description) > max_length:
            description = description[:max_length-3] + '...'
        
        logger.info(f"메타 디스크립션 생성: {len(description)} 자")
        return description.strip()
    
    def generate_meta_keywords(self, keywords, max_keywords=10):
        """
        메타 키워드 생성
        
        Args:
            keywords (list): 키워드 리스트
            max_keywords (int): 최대 키워드 수
            
        Returns:
            str: 메타 키워드 (쉼표로 구분)
        """
        if not keywords:
            return ""
        
        selected_keywords = keywords[:max_keywords]
        meta_keywords = ', '.join(selected_keywords)
        
        logger.info(f"메타 키워드 생성: {len(selected_keywords)}개")
        return meta_keywords
    
    def generate_og_tags(self, title, description, url, image_url=None):
        """
        Open Graph 태그 생성
        
        Args:
            title (str): 제목
            description (str): 설명
            url (str): URL
            image_url (str): 이미지 URL
            
        Returns:
            str: OG 태그 HTML
        """
        og_tags = f'<meta property="og:title" content="{title}" />\n'
        og_tags += f'<meta property="og:description" content="{description}" />\n'
        og_tags += f'<meta property="og:url" content="{url}" />\n'
        og_tags += '<meta property="og:type" content="article" />\n'
        
        if image_url:
            og_tags += f'<meta property="og:image" content="{image_url}" />\n'
        
        logger.info("Open Graph 태그 생성 완료")
        return og_tags
    
    def generate_twitter_cards(self, title, description, image_url=None):
        """
        Twitter Card 태그 생성
        
        Args:
            title (str): 제목
            description (str): 설명
            image_url (str): 이미지 URL
            
        Returns:
            str: Twitter Card 태그 HTML
        """
        twitter_tags = '<meta name="twitter:card" content="summary_large_image" />\n'
        twitter_tags += f'<meta name="twitter:title" content="{title}" />\n'
        twitter_tags += f'<meta name="twitter:description" content="{description}" />\n'
        
        if image_url:
            twitter_tags += f'<meta name="twitter:image" content="{image_url}" />\n'
        
        logger.info("Twitter Card 태그 생성 완료")
        return twitter_tags
    
    def generate_all_meta_tags(self, title, content, keywords, url, image_url=None):
        """
        모든 메타 태그 생성
        
        Args:
            title (str): 제목
            content (str): 본문 내용
            keywords (list): 키워드 리스트
            url (str): 페이지 URL
            image_url (str): 대표 이미지 URL
            
        Returns:
            str: 전체 메타 태그 HTML
        """
        meta_tags = ""
        
        # 기본 메타 태그
        description = self.generate_meta_description(content)
        meta_keywords = self.generate_meta_keywords(keywords)
        
        meta_tags += f'<meta name="description" content="{description}" />\n'
        meta_tags += f'<meta name="keywords" content="{meta_keywords}" />\n'
        meta_tags += '<meta name="author" content="Auto Blog Master" />\n'
        meta_tags += '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
        
        # Open Graph 태그
        meta_tags += '\n<!-- Open Graph -->\n'
        meta_tags += self.generate_og_tags(title, description, url, image_url)
        
        # Twitter Card 태그
        meta_tags += '\n<!-- Twitter Card -->\n'
        meta_tags += self.generate_twitter_cards(title, description, image_url)
        
        logger.info("모든 메타 태그 생성 완료")
        return meta_tags
    
    def generate_structured_data(self, title, description, author, date_published, image_url=None):
        """
        구조화된 데이터 (JSON-LD) 생성
        
        Args:
            title (str): 제목
            description (str): 설명
            author (str): 작성자
            date_published (str): 발행일 (ISO 8601)
            image_url (str): 이미지 URL
            
        Returns:
            str: JSON-LD 스크립트
        """
        json_ld = '<script type="application/ld+json">\n'
        json_ld += '{\n'
        json_ld += '  "@context": "https://schema.org",\n'
        json_ld += '  "@type": "Article",\n'
        json_ld += f'  "headline": "{title}",\n'
        json_ld += f'  "description": "{description}",\n'
        json_ld += f'  "author": {{\n'
        json_ld += f'    "@type": "Person",\n'
        json_ld += f'    "name": "{author}"\n'
        json_ld += f'  }},\n'
        json_ld += f'  "datePublished": "{date_published}"'
        
        if image_url:
            json_ld += f',\n  "image": "{image_url}"'
        
        json_ld += '\n}\n'
        json_ld += '</script>\n'
        
        logger.info("구조화된 데이터 생성 완료")
        return json_ld


if __name__ == '__main__':
    # 테스트 코드
    generator = MetaGenerator()
    
    sample_content = """
    인공지능은 현대 기술의 핵심입니다. 머신러닝과 딥러닝은 인공지능의 주요 분야입니다.
    자연어 처리와 컴퓨터 비전은 인공지능의 응용 분야입니다.
    """
    
    # 메타 디스크립션
    description = generator.generate_meta_description(sample_content)
    print(f"메타 디스크립션: {description}\n")
    
    # 메타 키워드
    keywords = ['인공지능', '머신러닝', '딥러닝', '자연어처리', '컴퓨터비전']
    meta_keywords = generator.generate_meta_keywords(keywords)
    print(f"메타 키워드: {meta_keywords}\n")
    
    # 전체 메타 태그
    all_meta = generator.generate_all_meta_tags(
        title='인공지능 완벽 가이드',
        content=sample_content,
        keywords=keywords,
        url='https://example.com/ai-guide',
        image_url='https://example.com/images/ai.jpg'
    )
    print("전체 메타 태그:")
    print(all_meta)
