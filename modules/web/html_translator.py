"""HTML/Website translator"""
from pathlib import Path
from typing import Optional


class HTMLTranslator:
    """Translate HTML files while preserving tags"""
    
    def __init__(self, translator):
        self.translator = translator
    
    def translate_file(self, input_path: str, output_path: str,
                      source_lang: str, target_lang: str) -> bool:
        """
        Translate HTML file
        
        Args:
            input_path: Input HTML file path
            output_path: Output HTML file path
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            True if successful
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            raise ImportError("BeautifulSoup4 not installed. Install with: pip install beautifulsoup4")
        
        try:
            # Read HTML file
            with open(input_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Translate text nodes
            for element in soup.find_all(text=True):
                # Skip script and style tags
                if element.parent.name in ['script', 'style', 'code', 'pre']:
                    continue
                
                text = element.string
                if text and text.strip():
                    try:
                        translated = self.translator.translate(text.strip(), source_lang, target_lang)
                        element.replace_with(translated)
                    except Exception as e:
                        print(f"Translation error for text: {e}")
            
            # Translate specific attributes (title, alt, placeholder)
            for tag in soup.find_all(attrs={'title': True}):
                if tag['title'].strip():
                    try:
                        tag['title'] = self.translator.translate(tag['title'], source_lang, target_lang)
                    except:
                        pass
            
            for tag in soup.find_all(attrs={'alt': True}):
                if tag['alt'].strip():
                    try:
                        tag['alt'] = self.translator.translate(tag['alt'], source_lang, target_lang)
                    except:
                        pass
            
            for tag in soup.find_all(attrs={'placeholder': True}):
                if tag['placeholder'].strip():
                    try:
                        tag['placeholder'] = self.translator.translate(tag['placeholder'], source_lang, target_lang)
                    except:
                        pass
            
            # Save translated HTML
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            return True
            
        except Exception as e:
            print(f"HTML translation error: {e}")
            return False
    
    def translate_url(self, url: str, source_lang: str, target_lang: str) -> Optional[str]:
        """
        Translate content from URL
        
        Args:
            url: Website URL
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated HTML string or None
        """
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            raise ImportError("requests and BeautifulSoup4 required")
        
        try:
            # Fetch URL content
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse and translate
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for element in soup.find_all(text=True):
                if element.parent.name in ['script', 'style', 'code', 'pre']:
                    continue
                
                text = element.string
                if text and text.strip():
                    try:
                        translated = self.translator.translate(text.strip(), source_lang, target_lang)
                        element.replace_with(translated)
                    except:
                        pass
            
            return str(soup)
            
        except Exception as e:
            print(f"URL translation error: {e}")
            return None
