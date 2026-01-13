# -*- coding: utf-8 -*-
"""
콘텐츠 생성기
크롤링된 데이터를 기반으로 블로그 콘텐츠를 생성합니다.
"""

import re
from gensim.summarization import summarize as gensim_summarize
from gensim.summarization import keywords as gensim_keywords
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentGenerator:
    """콘텐츠 생성 클래스"""
    
    def __init__(self, template_manager=None):
        """
        Args:
            template_manager: 템플릿 관리자 인스턴스
        """
        self.template_manager = template_manager
    
    def summarize_text(self, text, ratio=0.3):
        """
        TextRank 알고리즘으로 텍스트 요약
        
        Args:
            text (str): 원본 텍스트
            ratio (float): 요약 비율 (0.1 ~ 1.0)
            
        Returns:
            str: 요약된 텍스트
        """
        try:
            if not text or len(text.split()) < 10:
                logger.warning("텍스트가 너무 짧아 요약할 수 없습니다")
                return text
            
            # Gensim의 TextRank 기반 요약
            summary = gensim_summarize(text, ratio=ratio)
            
            if not summary:
                # 요약 실패 시 간단한 문장 추출
                summary = self._simple_summarize(text, ratio)
            
            logger.info(f"텍스트 요약 완료 (원본: {len(text)} → 요약: {len(summary)} 자)")
            return summary
            
        except Exception as e:
            logger.warning(f"TextRank 요약 실패, 간단한 요약 사용: {e}")
            return self._simple_summarize(text, ratio)
    
    def _simple_summarize(self, text, ratio=0.3):
        """
        간단한 문장 추출 요약
        
        Args:
            text (str): 원본 텍스트
            ratio (float): 요약 비율
            
        Returns:
            str: 요약된 텍스트
        """
        # 문장 분리
        sentences = re.split(r'[.!?]\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # 요약할 문장 수 계산
        num_sentences = max(1, int(len(sentences) * ratio))
        
        # 앞쪽 문장 선택 (간단한 방법)
        summary_sentences = sentences[:num_sentences]
        
        return '. '.join(summary_sentences) + '.'
    
    def extract_key_sentences(self, text, num_sentences=5):
        """
        핵심 문장 추출
        
        Args:
            text (str): 원본 텍스트
            num_sentences (int): 추출할 문장 수
            
        Returns:
            list: 핵심 문장 리스트
        """
        try:
            sentences = re.split(r'[.!?]\s+', text)
            sentences = [s.strip() for s in sentences if s.strip() and len(s) > 10]
            
            # 간단한 점수 계산 (문장 길이와 위치 기반)
            scored_sentences = []
            for i, sent in enumerate(sentences):
                # 점수: 길이 점수 + 위치 점수
                length_score = min(len(sent.split()), 20) / 20.0
                position_score = 1.0 - (i / len(sentences))
                score = length_score * 0.5 + position_score * 0.5
                
                scored_sentences.append((sent, score))
            
            # 점수순 정렬
            scored_sentences.sort(key=lambda x: x[1], reverse=True)
            
            # 상위 문장 선택
            key_sentences = [sent for sent, score in scored_sentences[:num_sentences]]
            
            logger.info(f"{len(key_sentences)}개의 핵심 문장 추출 완료")
            return key_sentences
            
        except Exception as e:
            logger.error(f"핵심 문장 추출 실패: {e}")
            return []
    
    def restructure_content(self, source_texts, topic, target_word_count=2000):
        """
        여러 소스 텍스트를 재구성하여 새로운 콘텐츠 생성
        
        Args:
            source_texts (list): 소스 텍스트 리스트
            topic (str): 주제
            target_word_count (int): 목표 단어 수
            
        Returns:
            dict: 생성된 콘텐츠
        """
        try:
            # 모든 텍스트 결합
            combined_text = '\n\n'.join(source_texts)
            
            # 요약
            summary_ratio = min(target_word_count / len(combined_text.split()), 0.5)
            summarized = self.summarize_text(combined_text, ratio=summary_ratio)
            
            # 섹션 생성
            sections = self._create_sections(summarized)
            
            # 템플릿 적용
            if self.template_manager:
                structure = self.template_manager.create_blog_structure(topic, sections)
            else:
                structure = {
                    'title': f"{topic}에 대한 완벽 가이드",
                    'intro': f"{topic}에 대해 알아보겠습니다.",
                    'sections': sections,
                    'outro': "이상으로 마치겠습니다."
                }
            
            logger.info("콘텐츠 재구성 완료")
            return structure
            
        except Exception as e:
            logger.error(f"콘텐츠 재구성 실패: {e}")
            return None
    
    def _create_sections(self, text, num_sections=3):
        """
        텍스트를 섹션으로 분할
        
        Args:
            text (str): 텍스트
            num_sections (int): 섹션 수
            
        Returns:
            list: 섹션 리스트
        """
        # 문단 분리
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        if len(paragraphs) < num_sections:
            num_sections = len(paragraphs)
        
        # 섹션 생성
        sections = []
        section_size = len(paragraphs) // num_sections
        
        for i in range(num_sections):
            start_idx = i * section_size
            end_idx = start_idx + section_size if i < num_sections - 1 else len(paragraphs)
            
            section_paragraphs = paragraphs[start_idx:end_idx]
            section_content = '\n\n'.join(section_paragraphs)
            
            # 첫 문장을 제목으로 사용
            first_sentence = section_paragraphs[0].split('.')[0] if section_paragraphs else f"섹션 {i+1}"
            
            sections.append({
                'title': first_sentence[:50] + '...' if len(first_sentence) > 50 else first_sentence,
                'content': section_content
            })
        
        return sections
    
    def generate_title(self, topic, keywords=None):
        """
        SEO 친화적인 제목 생성
        
        Args:
            topic (str): 주제
            keywords (list): 키워드 리스트
            
        Returns:
            str: 생성된 제목
        """
        templates = [
            f"{topic} 완벽 가이드 | 2024 최신 정보",
            f"{topic}의 모든 것 - 초보자를 위한 완벽 가이드",
            f"{topic} 총정리 | 알아야 할 핵심 정보",
            f"{topic} 완전 정복 - 꼭 알아야 할 정보",
            f"{topic} 가이드 | 전문가가 알려주는 핵심"
        ]
        
        import random
        return random.choice(templates)


if __name__ == '__main__':
    # 테스트 코드
    generator = ContentGenerator()
    
    sample_text = """
    인공지능은 인간의 지능을 모방한 컴퓨터 시스템입니다.
    머신러닝은 인공지능의 한 분야로, 데이터로부터 학습하는 알고리즘입니다.
    딥러닝은 인공신경망을 기반으로 한 머신러닝 기법입니다.
    자연어 처리는 인간의 언어를 컴퓨터가 이해하고 처리하는 기술입니다.
    컴퓨터 비전은 이미지와 비디오를 분석하는 인공지능 기술입니다.
    인공지능은 의료, 금융, 제조업 등 다양한 분야에서 활용되고 있습니다.
    """
    
    # 요약
    summary = generator.summarize_text(sample_text, ratio=0.5)
    print("요약:\n", summary)
    
    # 핵심 문장 추출
    key_sentences = generator.extract_key_sentences(sample_text, num_sentences=3)
    print("\n핵심 문장:")
    for i, sent in enumerate(key_sentences, 1):
        print(f"{i}. {sent}")
    
    # 제목 생성
    title = generator.generate_title("인공지능")
    print(f"\n생성된 제목: {title}")
