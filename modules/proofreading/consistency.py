"""
Consistency checking module
"""
import re
from collections import defaultdict


class ConsistencyChecker:
    """Check consistency in narrative elements"""
    
    def check_character_names(self, text):
        """Check for character name consistency"""
        errors = []
        
        # Extract potential character names (Korean names: 2-4 characters)
        name_pattern = r'\b[가-힣]{2,4}\b'
        names = re.findall(name_pattern, text)
        
        # Build name frequency map
        name_freq = defaultdict(int)
        for name in names:
            # Skip common words that might be mistaken for names
            common_words = ['그래서', '그러나', '하지만', '그리고', '그런데', '아니', '대신', '계속']
            if name not in common_words and len(name) >= 2:
                name_freq[name] += 1
        
        # Find potential character names (used multiple times)
        character_names = {name: count for name, count in name_freq.items() if count >= 3}
        
        # Check for similar names that might be typos
        name_list = list(character_names.keys())
        for i, name1 in enumerate(name_list):
            for name2 in name_list[i+1:]:
                if self._is_similar(name1, name2):
                    errors.append({
                        'type': 'character_name',
                        'names': [name1, name2],
                        'message': f"유사한 이름 발견: '{name1}'와 '{name2}'. 오타이거나 일관성 확인 필요."
                    })
        
        return errors
    
    def check_perspective(self, text):
        """Check for perspective consistency (1st person vs 3rd person)"""
        errors = []
        
        # Korean perspective markers
        first_person_markers = ['나는', '내가', '우리', '우리는', '나의', '내']
        third_person_markers = ['그는', '그녀는', '그가', '그녀가']
        
        first_person_count = sum(text.count(marker) for marker in first_person_markers)
        third_person_count = sum(text.count(marker) for marker in third_person_markers)
        
        # Check if both perspectives are used significantly
        if first_person_count > 5 and third_person_count > 5:
            errors.append({
                'type': 'perspective',
                'first_person_count': first_person_count,
                'third_person_count': third_person_count,
                'message': '1인칭과 3인칭 시점이 혼용되고 있습니다. 일관된 시점 사용을 권장합니다.'
            })
        
        return errors
    
    def check_character_settings(self, text):
        """Check for contradictions in character settings"""
        errors = []
        
        # This is a simplified version
        # In a full implementation, this would track character attributes
        # and check for contradictions
        
        # Example: Look for age-related inconsistencies
        age_patterns = r'(\d+)세'
        age_mentions = re.findall(age_patterns, text)
        
        if len(age_mentions) > 1:
            ages = [int(age) for age in age_mentions]
            if len(set(ages)) > 1:
                errors.append({
                    'type': 'character_setting',
                    'ages': ages,
                    'message': f'나이 정보 불일치: {ages}. 캐릭터 설정을 확인하세요.'
                })
        
        return errors
    
    def check_timeline(self, text):
        """Check for timeline consistency"""
        errors = []
        
        # Look for time-related expressions
        time_patterns = [
            r'(\d+)년',
            r'(\d+)월',
            r'(\d+)일',
            r'(어제|오늘|내일|그제|모레)'
        ]
        
        time_references = []
        for pattern in time_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                time_references.append({
                    'position': match.start(),
                    'text': match.group(0)
                })
        
        # Simple check: if many time references exist, warn to check timeline
        if len(time_references) > 10:
            errors.append({
                'type': 'timeline',
                'count': len(time_references),
                'message': '시간 관련 표현이 많습니다. 시간 순서가 일관되는지 확인하세요.'
            })
        
        return errors
    
    def _is_similar(self, str1, str2):
        """Check if two strings are similar (simple edit distance)"""
        if len(str1) != len(str2):
            return False
        
        differences = sum(c1 != c2 for c1, c2 in zip(str1, str2))
        return differences == 1
    
    def check_all(self, text):
        """Run all consistency checks"""
        all_errors = []
        
        all_errors.extend(self.check_character_names(text))
        all_errors.extend(self.check_perspective(text))
        all_errors.extend(self.check_character_settings(text))
        all_errors.extend(self.check_timeline(text))
        
        return all_errors
