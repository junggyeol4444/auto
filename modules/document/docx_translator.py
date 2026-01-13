"""DOCX document translator"""
from pathlib import Path
from typing import Optional


class DocxTranslator:
    """Translate DOCX documents while preserving formatting"""
    
    def __init__(self, translator):
        self.translator = translator
    
    def translate_file(self, input_path: str, output_path: str, 
                      source_lang: str, target_lang: str,
                      glossary: Optional[dict] = None) -> bool:
        """
        Translate DOCX file
        
        Args:
            input_path: Input DOCX file path
            output_path: Output DOCX file path
            source_lang: Source language code
            target_lang: Target language code
            glossary: Optional glossary dictionary
            
        Returns:
            True if successful
        """
        try:
            from docx import Document
        except ImportError:
            raise ImportError("python-docx not installed. Install with: pip install python-docx")
        
        try:
            # Load document
            doc = Document(input_path)
            
            # Translate paragraphs
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    original_text = paragraph.text
                    
                    # Apply glossary if provided
                    if glossary:
                        for source_term, target_term in glossary.items():
                            original_text = original_text.replace(source_term, target_term)
                    
                    # Translate
                    translated_text = self.translator.translate(original_text, source_lang, target_lang)
                    
                    # Replace text while preserving formatting
                    paragraph.text = translated_text
            
            # Translate tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text.strip():
                            original_text = cell.text
                            
                            if glossary:
                                for source_term, target_term in glossary.items():
                                    original_text = original_text.replace(source_term, target_term)
                            
                            translated_text = self.translator.translate(original_text, source_lang, target_lang)
                            cell.text = translated_text
            
            # Save translated document
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            doc.save(output_path)
            return True
            
        except Exception as e:
            print(f"DOCX translation error: {e}")
            return False
