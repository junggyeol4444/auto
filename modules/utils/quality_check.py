"""Translation quality checker"""
import re
from typing import List, Tuple


class QualityChecker:
    """Check translation quality and identify issues"""
    
    @staticmethod
    def check_translation(original: str, translated: str, source_lang: str, target_lang: str) -> List[str]:
        """
        Check translation quality
        
        Args:
            original: Original text
            translated: Translated text
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            List of quality issues found
        """
        issues = []
        
        # Check if translation is empty
        if not translated or not translated.strip():
            issues.append("Translation is empty")
            return issues
        
        # Check if translation is same as original (possible error)
        if original.strip() == translated.strip():
            issues.append("Translation identical to original")
        
        # Check length ratio (extreme differences might indicate issues)
        orig_len = len(original)
        trans_len = len(translated)
        if orig_len > 0:
            ratio = trans_len / orig_len
            if ratio < 0.3 or ratio > 3.0:
                issues.append(f"Unusual length ratio: {ratio:.2f}")
        
        # Check for untranslated placeholder patterns
        placeholders = re.findall(r'\{[^}]+\}|\[[^\]]+\]|\$\{[^}]+\}', original)
        for placeholder in placeholders:
            if placeholder not in translated:
                issues.append(f"Placeholder missing in translation: {placeholder}")
        
        # Check for preserved numbers
        original_numbers = re.findall(r'\d+', original)
        translated_numbers = re.findall(r'\d+', translated)
        if set(original_numbers) != set(translated_numbers):
            issues.append("Numbers differ between original and translation")
        
        return issues
    
    @staticmethod
    def validate_subtitle_length(text: str, max_chars: int = 42, max_lines: int = 2) -> bool:
        """
        Validate subtitle length constraints
        
        Args:
            text: Subtitle text
            max_chars: Maximum characters per line
            max_lines: Maximum number of lines
            
        Returns:
            True if valid
        """
        lines = text.split('\n')
        
        if len(lines) > max_lines:
            return False
        
        for line in lines:
            if len(line) > max_chars:
                return False
        
        return True
    
    @staticmethod
    def adjust_subtitle_length(text: str, max_chars: int = 42) -> str:
        """
        Adjust subtitle to fit length constraints
        
        Args:
            text: Subtitle text
            max_chars: Maximum characters per line
            
        Returns:
            Adjusted text
        """
        if len(text) <= max_chars:
            return text
        
        # Try to break at natural points
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if len(test_line) <= max_chars:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Limit to 2 lines
        return '\n'.join(lines[:2])
