# -*- coding: utf-8 -*-
"""
SEO 최적화기
블로그 콘텐츠의 SEO를 최적화합니다.
"""

import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SEOOptimizer:
    """SEO 최적화 클래스"""
    
    def __init__(self):
        self.target_keyword_density = (1.0, 3.0)  # 1-3% 권장
        self.min_word_count = 300
        self.recommended_word_count = 2000
    
    def analyze_keyword_density(self, text, keyword):
        """
        키워드 밀도 분석
        
        Args:
            text (str): 텍스트
            keyword (str): 키워드
            
        Returns:
            dict: 분석 결과
        """
        if not text or not keyword:
            return {'density': 0, 'count': 0, 'status': 'error'}
        
        text_lower = text.lower()
        keyword_lower = keyword.lower()
        
        # 키워드 출현 횟수
        count = text_lower.count(keyword_lower)
        
        # 전체 단어 수
        words = text.split()
        total_words = len(words)
        
        if total_words == 0:
            return {'density': 0, 'count': 0, 'status': 'error'}
        
        # 밀도 계산 (%)
        density = (count / total_words) * 100
        
        # 상태 판정
        min_density, max_density = self.target_keyword_density
        if density < min_density:
            status = 'low'
        elif density > max_density:
            status = 'high'
        else:
            status = 'optimal'
        
        return {
            'density': round(density, 2),
            'count': count,
            'total_words': total_words,
            'status': status
        }
    
    def optimize_keyword_density(self, text, keyword, target_density=2.0):
        """
        키워드 밀도 최적화
        
        Args:
            text (str): 텍스트
            keyword (str): 키워드
            target_density (float): 목표 밀도 (%)
            
        Returns:
            str: 최적화된 텍스트
        """
        current = self.analyze_keyword_density(text, keyword)
        
        if current['status'] == 'optimal':
            logger.info("키워드 밀도가 이미 최적 상태입니다")
            return text
        
        if current['status'] == 'low':
            # 키워드 추가 필요
            return self._add_keywords(text, keyword, current['density'], target_density)
        else:
            # 키워드 감소 (현재는 경고만)
            logger.warning(f"키워드 밀도가 높습니다 ({current['density']}%). 수동 조정 권장")
            return text
    
    def _add_keywords(self, text, keyword, current_density, target_density):
        """
        키워드 추가
        
        Args:
            text (str): 텍스트
            keyword (str): 키워드
            current_density (float): 현재 밀도
            target_density (float): 목표 밀도
            
        Returns:
            str: 수정된 텍스트
        """
        # 추가할 키워드 수 계산
        words = text.split()
        total_words = len(words)
        current_count = text.lower().count(keyword.lower())
        
        target_count = int((target_density / 100) * total_words)
        add_count = max(0, target_count - current_count)
        
        if add_count == 0:
            return text
        
        # 문장 분리
        sentences = re.split(r'([.!?]\s+)', text)
        
        # 키워드를 자연스럽게 추가할 위치 찾기
        insert_phrases = [
            f"{keyword}는 중요한 요소입니다.",
            f"{keyword}에 대해 알아보면,",
            f"{keyword}와 관련하여,",
            f"{keyword}의 경우,"
        ]
        
        added = 0
        for i in range(0, len(sentences), 4):  # 일정 간격으로
            if added >= add_count:
                break
            
            if i < len(sentences):
                phrase = insert_phrases[added % len(insert_phrases)]
                sentences.insert(i, phrase + ' ')
                added += 1
        
        optimized_text = ''.join(sentences)
        
        logger.info(f"키워드 {add_count}개 추가 완료")
        return optimized_text
    
    def create_heading_structure(self, sections):
        """
        헤딩 구조 생성 (H1, H2, H3)
        
        Args:
            sections (list): 섹션 리스트
            
        Returns:
            str: HTML 헤딩 구조
        """
        html = ""
        
        for i, section in enumerate(sections):
            title = section.get('title', f'섹션 {i+1}')
            content = section.get('content', '')
            
            html += f"<h2>{title}</h2>\n"
            html += f"<p>{content}</p>\n\n"
            
            # 하위 섹션이 있다면 H3 사용
            if 'subsections' in section:
                for subsection in section['subsections']:
                    subtitle = subsection.get('title', '')
                    subcontent = subsection.get('content', '')
                    html += f"<h3>{subtitle}</h3>\n"
                    html += f"<p>{subcontent}</p>\n\n"
        
        return html
    
    def add_internal_links(self, text, link_suggestions):
        """
        내부 링크 자동 삽입
        
        Args:
            text (str): 텍스트
            link_suggestions (list): [{'keyword': '키워드', 'url': 'URL'}, ...]
            
        Returns:
            str: 링크가 추가된 텍스트
        """
        modified_text = text
        
        for suggestion in link_suggestions:
            keyword = suggestion['keyword']
            url = suggestion['url']
            
            # 첫 번째 출현만 링크로 변환
            pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
            modified_text = pattern.sub(
                f'<a href="{url}">{keyword}</a>',
                modified_text,
                count=1
            )
        
        logger.info(f"{len(link_suggestions)}개의 내부 링크 추가됨")
        return modified_text
    
    def calculate_seo_score(self, content, keyword):
        """
        SEO 점수 계산
        
        Args:
            content (dict): 콘텐츠 구조
            keyword (str): 주요 키워드
            
        Returns:
            dict: SEO 점수 및 피드백
        """
        score = 0
        max_score = 100
        feedback = []
        
        # 1. 제목에 키워드 포함 (20점)
        title = content.get('title', '')
        if keyword.lower() in title.lower():
            score += 20
            feedback.append("✓ 제목에 키워드 포함")
        else:
            feedback.append("✗ 제목에 키워드 미포함")
        
        # 2. 인트로에 키워드 포함 (15점)
        intro = content.get('intro', '')
        if keyword.lower() in intro.lower():
            score += 15
            feedback.append("✓ 인트로에 키워드 포함")
        else:
            feedback.append("✗ 인트로에 키워드 미포함")
        
        # 3. 충분한 글자 수 (20점)
        full_text = intro + ' '.join([s.get('content', '') for s in content.get('sections', [])])
        word_count = len(full_text.split())
        
        if word_count >= self.recommended_word_count:
            score += 20
            feedback.append(f"✓ 충분한 글자 수 ({word_count} 단어)")
        elif word_count >= self.min_word_count:
            score += 10
            feedback.append(f"△ 글자 수 부족 ({word_count} 단어, 권장: {self.recommended_word_count})")
        else:
            feedback.append(f"✗ 글자 수 매우 부족 ({word_count} 단어)")
        
        # 4. 키워드 밀도 (25점)
        density_result = self.analyze_keyword_density(full_text, keyword)
        if density_result['status'] == 'optimal':
            score += 25
            feedback.append(f"✓ 키워드 밀도 최적 ({density_result['density']}%)")
        elif density_result['status'] == 'low':
            score += 10
            feedback.append(f"△ 키워드 밀도 낮음 ({density_result['density']}%)")
        else:
            score += 10
            feedback.append(f"△ 키워드 밀도 높음 ({density_result['density']}%)")
        
        # 5. 섹션 구조 (20점)
        sections = content.get('sections', [])
        if len(sections) >= 3:
            score += 20
            feedback.append(f"✓ 적절한 섹션 구조 ({len(sections)}개)")
        elif len(sections) >= 1:
            score += 10
            feedback.append(f"△ 섹션 수 부족 ({len(sections)}개)")
        else:
            feedback.append("✗ 섹션 구조 없음")
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': round((score / max_score) * 100, 1),
            'feedback': feedback
        }


if __name__ == '__main__':
    # 테스트 코드
    optimizer = SEOOptimizer()
    
    sample_text = """
    인공지능 기술이 발전하고 있습니다. 머신러닝과 딥러닝이 주목받고 있습니다.
    다양한 산업에서 활용되고 있습니다. 미래에는 더욱 중요해질 것입니다.
    """ * 10
    
    # 키워드 밀도 분석
    result = optimizer.analyze_keyword_density(sample_text, '인공지능')
    print(f"키워드 밀도: {result['density']}% (상태: {result['status']})")
    print(f"키워드 출현: {result['count']}회 / 총 {result['total_words']}단어")
    
    # SEO 점수 계산
    content = {
        'title': '인공지능의 모든 것',
        'intro': '인공지능에 대해 알아보겠습니다.',
        'sections': [
            {'title': '인공지능 정의', 'content': '인공지능은...' * 50},
            {'title': '인공지능 활용', 'content': '다양한 분야에서...' * 50},
            {'title': '인공지능 미래', 'content': '앞으로는...' * 50}
        ]
    }
    
    seo_result = optimizer.calculate_seo_score(content, '인공지능')
    print(f"\nSEO 점수: {seo_result['score']}/{seo_result['max_score']} ({seo_result['percentage']}%)")
    print("\n피드백:")
    for fb in seo_result['feedback']:
        print(f"  {fb}")
