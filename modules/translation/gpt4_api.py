"""OpenAI GPT-4 Translation API implementation"""
from typing import List, Optional
import requests
from .base_translator import BaseTranslator


class GPT4Translator(BaseTranslator):
    """GPT-4 API translator - Best for context-aware and technical translations"""
    
    API_URL = "https://api.openai.com/v1/chat/completions"
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate single text using GPT-4"""
        if not self.is_configured():
            raise ValueError("OpenAI API key not configured")
        
        if not text.strip():
            return text
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            prompt = f"Translate the following text from {self._get_language_name(source_lang)} to {self._get_language_name(target_lang)}. Preserve the meaning and context. Only return the translation, nothing else.\n\nText: {text}"
            
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are a professional translator. Translate accurately while preserving context and technical terms."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            }
            
            response = requests.post(self.API_URL, json=data, headers=headers, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
            
        except Exception as e:
            raise Exception(f"GPT-4 translation failed: {str(e)}")
    
    def translate_batch(self, texts: List[str], source_lang: str, target_lang: str) -> List[str]:
        """Translate multiple texts using GPT-4"""
        if not texts:
            return []
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            numbered_texts = "\n".join([f"{i+1}. {text}" for i, text in enumerate(texts)])
            prompt = f"Translate the following texts from {self._get_language_name(source_lang)} to {self._get_language_name(target_lang)}. Return only the translations in the same numbered format.\n\n{numbered_texts}"
            
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are a professional translator. Translate accurately while preserving context."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            }
            
            response = requests.post(self.API_URL, json=data, headers=headers, timeout=90)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()
            
            # Parse numbered results
            translations = []
            for line in content.split('\n'):
                line = line.strip()
                if line and '. ' in line:
                    translations.append(line.split('. ', 1)[1])
            
            return translations if len(translations) == len(texts) else texts
            
        except Exception as e:
            raise Exception(f"GPT-4 batch translation failed: {str(e)}")
    
    def _get_language_name(self, lang_code: str) -> str:
        """Get full language name from code"""
        names = {
            'ko': 'Korean',
            'en': 'English',
            'ja': 'Japanese',
            'zh-CN': 'Chinese (Simplified)',
            'zh-TW': 'Chinese (Traditional)',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German'
        }
        return names.get(lang_code, lang_code)
