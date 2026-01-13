"""
API Manager for AI services
"""
import os


class APIManager:
    """Manage API connections for AI services"""
    
    def __init__(self, config):
        self.config = config
        self.openai_key = config.get('api', {}).get('openai_key', '')
        self.anthropic_key = config.get('api', {}).get('anthropic_key', '')
        self.use_ai = config.get('api', {}).get('use_ai', False)
        
        self.openai_client = None
        self.anthropic_client = None
        
        if self.use_ai and self.openai_key:
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=self.openai_key)
            except ImportError:
                print("OpenAI 라이브러리가 설치되지 않았습니다.")
        
        if self.use_ai and self.anthropic_key:
            try:
                import anthropic
                self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key)
            except ImportError:
                print("Anthropic 라이브러리가 설치되지 않았습니다.")
    
    def generate_with_openai(self, prompt, max_tokens=2000):
        """Generate text using OpenAI GPT"""
        if not self.openai_client:
            return None
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 전문 작가입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API 오류: {str(e)}")
            return None
    
    def generate_with_anthropic(self, prompt, max_tokens=2000):
        """Generate text using Anthropic Claude"""
        if not self.anthropic_client:
            return None
        
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Anthropic API 오류: {str(e)}")
            return None
    
    def is_available(self):
        """Check if any AI service is available"""
        return self.use_ai and (self.openai_client is not None or self.anthropic_client is not None)
