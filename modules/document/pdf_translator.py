"""PDF document translator"""
from pathlib import Path
from typing import Optional


class PDFTranslator:
    """Translate PDF documents"""
    
    def __init__(self, translator):
        self.translator = translator
    
    def translate_file(self, input_path: str, output_path: str,
                      source_lang: str, target_lang: str,
                      glossary: Optional[dict] = None) -> bool:
        """
        Translate PDF file
        
        Args:
            input_path: Input PDF file path
            output_path: Output PDF file path
            source_lang: Source language code
            target_lang: Target language code
            glossary: Optional glossary dictionary
            
        Returns:
            True if successful
        """
        try:
            import pdfplumber
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import inch
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
        except ImportError:
            raise ImportError("pdfplumber and reportlab required. Install with: pip install pdfplumber reportlab")
        
        try:
            # Extract text from PDF
            texts = []
            with pdfplumber.open(input_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        texts.append(text)
            
            if not texts:
                print("No text extracted from PDF")
                return False
            
            # Translate all text
            translated_texts = []
            for text in texts:
                if glossary:
                    for source_term, target_term in glossary.items():
                        text = text.replace(source_term, target_term)
                
                translated = self.translator.translate(text, source_lang, target_lang)
                translated_texts.append(translated)
            
            # Create new PDF with translated text
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            c = canvas.Canvas(output_path, pagesize=letter)
            width, height = letter
            
            for translated_text in translated_texts:
                y_position = height - 1 * inch
                
                # Split text into lines
                lines = translated_text.split('\n')
                for line in lines:
                    if y_position < 1 * inch:
                        c.showPage()
                        y_position = height - 1 * inch
                    
                    c.drawString(1 * inch, y_position, line[:80])  # Limit line length
                    y_position -= 0.2 * inch
                
                c.showPage()
            
            c.save()
            return True
            
        except Exception as e:
            print(f"PDF translation error: {e}")
            return False
