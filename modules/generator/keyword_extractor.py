# -*- coding: utf-8 -*-
"""
키워드 추출기
텍스트에서 중요 키워드를 추출합니다.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from rake_nltk import Rake
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KeywordExtractor:
    """키워드 추출 클래스"""
    
    def __init__(self):
        self.rake = Rake()
    
    def extract_with_tfidf(self, texts, max_keywords=10):
        """
        TF-IDF로 키워드 추출
        
        Args:
            texts (list): 텍스트 리스트
            max_keywords (int): 최대 키워드 수
            
        Returns:
            list: 키워드 리스트
        """
        try:
            if not texts or all(not text.strip() for text in texts):
                logger.warning("추출할 텍스트가 없습니다")
                return []
            
            vectorizer = TfidfVectorizer(
                max_features=max_keywords,
                stop_words=None,
                ngram_range=(1, 2)
            )
            
            tfidf_matrix = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()
            
            # TF-IDF 점수 계산
            scores = tfidf_matrix.sum(axis=0).A1
            keywords_with_scores = list(zip(feature_names, scores))
            keywords_with_scores.sort(key=lambda x: x[1], reverse=True)
            
            keywords = [kw for kw, score in keywords_with_scores[:max_keywords]]
            
            logger.info(f"{len(keywords)}개의 키워드 추출 완료 (TF-IDF)")
            return keywords
            
        except Exception as e:
            logger.error(f"TF-IDF 키워드 추출 실패: {e}")
            return []
    
    def extract_with_rake(self, text, max_keywords=10):
        """
        RAKE 알고리즘으로 키워드 추출
        
        Args:
            text (str): 텍스트
            max_keywords (int): 최대 키워드 수
            
        Returns:
            list: 키워드 리스트
        """
        try:
            if not text or not text.strip():
                logger.warning("추출할 텍스트가 없습니다")
                return []
            
            self.rake.extract_keywords_from_text(text)
            keywords = self.rake.get_ranked_phrases()[:max_keywords]
            
            logger.info(f"{len(keywords)}개의 키워드 추출 완료 (RAKE)")
            return keywords
            
        except Exception as e:
            logger.error(f"RAKE 키워드 추출 실패: {e}")
            return []
    
    def extract_simple(self, text, max_keywords=10):
        """
        간단한 키워드 추출 (빈도 기반)
        
        Args:
            text (str): 텍스트
            max_keywords (int): 최대 키워드 수
            
        Returns:
            list: 키워드 리스트
        """
        try:
            # 텍스트 정규화
            text = re.sub(r'[^\w\s가-힣]', ' ', text.lower())
            words = text.split()
            
            # 불용어 제거 (기본)
            stop_words = {'은', '는', '이', '가', '을', '를', '의', '에', '와', '과', '도', '로', '으로'}
            words = [w for w in words if w not in stop_words and len(w) > 1]
            
            # 빈도 계산
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # 정렬
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            keywords = [word for word, freq in sorted_words[:max_keywords]]
            
            logger.info(f"{len(keywords)}개의 키워드 추출 완료 (빈도 기반)")
            return keywords
            
        except Exception as e:
            logger.error(f"간단한 키워드 추출 실패: {e}")
            return []
    
    def extract_keywords(self, text, method='simple', max_keywords=10):
        """
        키워드 추출 (통합)
        
        Args:
            text (str): 텍스트
            method (str): 추출 방법 ('simple', 'rake', 'tfidf')
            max_keywords (int): 최대 키워드 수
            
        Returns:
            list: 키워드 리스트
        """
        if method == 'rake':
            return self.extract_with_rake(text, max_keywords)
        elif method == 'tfidf':
            return self.extract_with_tfidf([text], max_keywords)
        else:
            return self.extract_simple(text, max_keywords)
    
    def calculate_keyword_density(self, text, keyword):
        """
        키워드 밀도 계산
        
        Args:
            text (str): 텍스트
            keyword (str): 키워드
            
        Returns:
            float: 키워드 밀도 (%)
        """
        if not text or not keyword:
            return 0.0
        
        text_lower = text.lower()
        keyword_lower = keyword.lower()
        
        # 키워드 출현 횟수
        count = text_lower.count(keyword_lower)
        
        # 전체 단어 수
        words = text.split()
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        # 밀도 계산
        density = (count / total_words) * 100
        
        return round(density, 2)


if __name__ == '__main__':
    # 테스트 코드
    extractor = KeywordExtractor()
    
    sample_text = """
    인공지능은 현대 기술의 핵심입니다. 머신러닝과 딥러닝은 인공지능의 주요 분야입니다.
    자연어 처리와 컴퓨터 비전은 인공지능의 응용 분야입니다.
    인공지능 기술은 다양한 산업에서 활용되고 있습니다.
    """
    
    # 간단한 추출
    keywords = extractor.extract_keywords(sample_text, method='simple', max_keywords=5)
    print("추출된 키워드:", keywords)
    
    # 키워드 밀도 계산
    for keyword in keywords[:3]:
        density = extractor.calculate_keyword_density(sample_text, keyword)
        print(f"{keyword}: {density}%")
