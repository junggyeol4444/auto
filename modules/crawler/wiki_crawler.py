# -*- coding: utf-8 -*-
"""
위키피디아 크롤러
위키피디아에서 정보를 수집합니다.
"""

import wikipedia
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WikiCrawler:
    """위키피디아 크롤링 클래스"""
    
    def __init__(self, language='ko'):
        """
        Args:
            language (str): 위키피디아 언어 ('ko', 'en' 등)
        """
        wikipedia.set_lang(language)
        self.language = language
    
    def search(self, keyword, results=5):
        """
        키워드로 위키피디아 검색
        
        Args:
            keyword (str): 검색 키워드
            results (int): 검색 결과 수
            
        Returns:
            list: 검색 결과 제목 리스트
        """
        try:
            search_results = wikipedia.search(keyword, results=results)
            logger.info(f"{len(search_results)}개의 검색 결과 발견")
            return search_results
        except Exception as e:
            logger.error(f"검색 실패: {e}")
            return []
    
    def get_page_content(self, title):
        """
        페이지 내용 가져오기
        
        Args:
            title (str): 페이지 제목
            
        Returns:
            dict: 페이지 정보
        """
        try:
            page = wikipedia.page(title, auto_suggest=False)
            
            return {
                'title': page.title,
                'content': page.content,
                'summary': page.summary,
                'url': page.url,
                'sections': self._extract_sections(page.content)
            }
            
        except wikipedia.exceptions.DisambiguationError as e:
            logger.warning(f"동음이의어 페이지: {e.options[:5]}")
            # 첫 번째 옵션으로 재시도
            if e.options:
                return self.get_page_content(e.options[0])
            return None
            
        except wikipedia.exceptions.PageError:
            logger.error(f"페이지를 찾을 수 없음: {title}")
            return None
            
        except Exception as e:
            logger.error(f"페이지 추출 실패: {e}")
            return None
    
    def _extract_sections(self, content):
        """
        본문에서 섹션 추출
        
        Args:
            content (str): 페이지 본문
            
        Returns:
            list: 섹션 리스트
        """
        sections = []
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # 섹션 제목 감지 (== 제목 ==)
            if line.startswith('==') and line.endswith('=='):
                if current_section:
                    sections.append({
                        'title': current_section,
                        'content': '\n'.join(current_content).strip()
                    })
                current_section = line.strip('= ')
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
        
        # 마지막 섹션 추가
        if current_section:
            sections.append({
                'title': current_section,
                'content': '\n'.join(current_content).strip()
            })
        
        return sections
    
    def crawl(self, keyword, max_pages=3):
        """
        키워드로 위키 페이지들을 크롤링
        
        Args:
            keyword (str): 검색 키워드
            max_pages (int): 최대 페이지 수
            
        Returns:
            list: 페이지 정보 리스트
        """
        # 검색
        search_results = self.search(keyword, results=max_pages * 2)
        
        # 페이지 내용 추출
        pages = []
        for title in search_results[:max_pages]:
            page_content = self.get_page_content(title)
            if page_content:
                pages.append(page_content)
                
                if len(pages) >= max_pages:
                    break
        
        logger.info(f"총 {len(pages)}개의 위키 페이지 추출 완료")
        return pages
    
    def get_summary(self, keyword, sentences=3):
        """
        키워드의 요약 가져오기
        
        Args:
            keyword (str): 검색 키워드
            sentences (int): 요약 문장 수
            
        Returns:
            str: 요약 텍스트
        """
        try:
            summary = wikipedia.summary(keyword, sentences=sentences, auto_suggest=True)
            return summary
        except Exception as e:
            logger.error(f"요약 추출 실패: {e}")
            return ""


if __name__ == '__main__':
    # 테스트 코드
    crawler = WikiCrawler(language='ko')
    
    # 요약 테스트
    summary = crawler.get_summary('인공지능', sentences=2)
    print(f"요약:\n{summary}\n")
    
    # 전체 크롤링 테스트
    results = crawler.crawl('인공지능', max_pages=2)
    
    for i, page in enumerate(results, 1):
        print(f"\n=== 페이지 {i} ===")
        print(f"제목: {page.get('title', 'N/A')}")
        print(f"본문 길이: {len(page.get('content', ''))} 자")
        print(f"섹션 수: {len(page.get('sections', []))}")
        print(f"URL: {page.get('url', 'N/A')}")
