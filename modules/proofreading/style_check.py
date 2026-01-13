"""
Style checking module
"""
import re
from collections import Counter


class StyleChecker:
    """Check writing style issues"""
    
    def check_repetition(self, text):
        """Check for repetitive words or phrases"""
        errors = []
        
        # Split into words (Korean + English)
        words = re.findall(r'[가-힣]+|[A-Za-z]+', text)
        
        # Count word frequency
        word_counts = Counter(words)
        
        # Find words used too frequently (more than 5% of total)
        total_words = len(words)
        threshold = max(5, total_words * 0.05)
        
        for word, count in word_counts.most_common(20):
            if count > threshold and len(word) > 1:
                # Skip common words
                common_words = ['것', '그', '저', '이', '수', '등', '및', '때', '더', '매우', '정말']
                if word not in common_words:
                    errors.append({
                        'type': 'repetition',
                        'word': word,
                        'count': count,
                        'message': f"'{word}' 단어가 {count}회 반복됨. 다양한 표현 사용 권장."
                    })
        
        return errors
    
    def check_sentence_length(self, text):
        """Check for overly long sentences"""
        errors = []
        
        sentences = re.split(r'[.!?。]+', text)
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Korean sentences: generally 50-80 characters is comfortable
            if len(sentence) > 150:
                errors.append({
                    'type': 'sentence_length',
                    'sentence_num': i + 1,
                    'length': len(sentence),
                    'preview': sentence[:50] + '...',
                    'message': '문장이 너무 깁니다. 짧게 나누는 것을 권장합니다.'
                })
        
        return errors
    
    def check_passive_voice(self, text):
        """Check for excessive passive voice (Korean)"""
        errors = []
        
        # Korean passive voice markers
        passive_patterns = [
            r'[가-힣]+되다',
            r'[가-힣]+되어',
            r'[가-힣]+당하다',
            r'[가-힣]+받다'
        ]
        
        passive_count = 0
        for pattern in passive_patterns:
            matches = re.finditer(pattern, text)
            passive_count += len(list(matches))
        
        # Count sentences
        sentences = re.split(r'[.!?。]+', text)
        num_sentences = len([s for s in sentences if s.strip()])
        
        if num_sentences > 0:
            passive_ratio = passive_count / num_sentences
            
            if passive_ratio > 0.3:
                errors.append({
                    'type': 'passive_voice',
                    'count': passive_count,
                    'ratio': passive_ratio,
                    'message': f'피동 표현이 많습니다 ({passive_count}회). 능동 표현 사용 권장.'
                })
        
        return errors
    
    def check_awkward_expressions(self, text):
        """Check for commonly awkward expressions"""
        errors = []
        
        # Common awkward patterns in Korean
        awkward_patterns = [
            (r'되어지다', '되다', '불필요한 이중 피동'),
            (r'하여금', '에게/-로 하여금', '고어체 표현'),
            (r'함에 있어서', '할 때', '장황한 표현'),
            (r'등등', '등', '중복 표현'),
            (r'([가-힣]+)의의', r'\1의', '불필요한 중복')
        ]
        
        for pattern, suggestion, message in awkward_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                errors.append({
                    'type': 'awkward',
                    'position': match.start(),
                    'original': match.group(0),
                    'suggestion': suggestion,
                    'message': message
                })
        
        return errors
    
    def check_all(self, text):
        """Run all style checks"""
        all_errors = []
        
        all_errors.extend(self.check_repetition(text))
        all_errors.extend(self.check_sentence_length(text))
        all_errors.extend(self.check_passive_voice(text))
        all_errors.extend(self.check_awkward_expressions(text))
        
        return all_errors
