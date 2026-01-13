"""
Grammar checking module
"""
import re


class GrammarChecker:
    """Check grammar and spelling in Korean text"""
    
    def __init__(self):
        self.hanspell_available = False
        try:
            from hanspell import spell_checker
            self.spell_checker = spell_checker
            self.hanspell_available = True
        except ImportError:
            print("py-hanspell not available. Spell checking will be limited.")
    
    def check_spelling(self, text):
        """Check spelling using hanspell"""
        errors = []
        
        if not self.hanspell_available:
            return errors
        
        try:
            # Split text into sentences for processing
            sentences = self._split_sentences(text)
            
            for sentence in sentences:
                if len(sentence.strip()) < 5:
                    continue
                
                try:
                    result = self.spell_checker.check(sentence)
                    
                    if result.original != result.checked:
                        errors.append({
                            'type': 'spelling',
                            'original': result.original,
                            'corrected': result.checked,
                            'message': '맞춤법 오류'
                        })
                except:
                    continue
        
        except Exception as e:
            print(f"맞춤법 검사 오류: {str(e)}")
        
        return errors
    
    def check_spacing(self, text):
        """Check spacing issues"""
        errors = []
        
        # Check for missing spaces after punctuation
        pattern = r'([.!?:,])([가-힣A-Za-z])'
        matches = re.finditer(pattern, text)
        
        for match in matches:
            errors.append({
                'type': 'spacing',
                'position': match.start(),
                'original': match.group(0),
                'corrected': match.group(1) + ' ' + match.group(2),
                'message': '구두점 뒤 띄어쓰기 필요'
            })
        
        return errors
    
    def check_particle_usage(self, text):
        """Check Korean particle usage (조사)"""
        errors = []
        
        # Basic particle checking patterns
        # Check for common particle errors
        patterns = [
            (r'([가-힣])를을', r'\1을', '을/를 중복'),
            (r'([가-힣])가이', r'\1이', '가/이 중복'),
            (r'([가-힣])은는', r'\1는', '은/는 중복'),
        ]
        
        for pattern, replacement, message in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                errors.append({
                    'type': 'particle',
                    'position': match.start(),
                    'original': match.group(0),
                    'corrected': re.sub(pattern, replacement, match.group(0)),
                    'message': message
                })
        
        return errors
    
    def check_tense_consistency(self, text):
        """Check tense consistency in text"""
        errors = []
        
        # Split into sentences
        sentences = self._split_sentences(text)
        
        # Detect tense markers
        past_markers = ['했다', '됐다', '었다', '았다', '였다']
        present_markers = ['한다', '된다', '는다', '이다']
        
        tenses = []
        for sentence in sentences:
            if any(marker in sentence for marker in past_markers):
                tenses.append('past')
            elif any(marker in sentence for marker in present_markers):
                tenses.append('present')
            else:
                tenses.append('unknown')
        
        # Check for inconsistency (simplified check)
        if len(tenses) > 3:
            past_count = tenses.count('past')
            present_count = tenses.count('present')
            
            if past_count > 0 and present_count > 0:
                if abs(past_count - present_count) < len(tenses) * 0.3:
                    errors.append({
                        'type': 'tense',
                        'message': '시제 불일치 가능성 (과거형과 현재형 혼용)',
                        'suggestion': '전체 텍스트의 시제를 일관되게 유지하세요.'
                    })
        
        return errors
    
    def _split_sentences(self, text):
        """Split text into sentences"""
        # Split by common Korean sentence endings
        sentences = re.split(r'[.!?。]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def check_all(self, text):
        """Run all grammar checks"""
        all_errors = []
        
        # Spelling check (may be slow)
        # all_errors.extend(self.check_spelling(text))
        
        # Spacing check
        all_errors.extend(self.check_spacing(text))
        
        # Particle usage
        all_errors.extend(self.check_particle_usage(text))
        
        # Tense consistency
        all_errors.extend(self.check_tense_consistency(text))
        
        return all_errors
