"""Localization file translator (JSON, XML)"""
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any


class LocalizationTranslator:
    """Translate localization resource files"""
    
    def __init__(self, translator):
        self.translator = translator
    
    def translate_json(self, input_path: str, output_path: str,
                      source_lang: str, target_lang: str) -> bool:
        """
        Translate JSON localization file
        
        Args:
            input_path: Input JSON file path
            output_path: Output JSON file path
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            True if successful
        """
        try:
            # Load JSON
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Translate values
            translated_data = self._translate_dict(data, source_lang, target_lang)
            
            # Save translated JSON
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(translated_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"JSON translation error: {e}")
            return False
    
    def _translate_dict(self, data: Any, source_lang: str, target_lang: str) -> Any:
        """Recursively translate dictionary values"""
        if isinstance(data, dict):
            return {key: self._translate_dict(value, source_lang, target_lang) 
                   for key, value in data.items()}
        elif isinstance(data, list):
            return [self._translate_dict(item, source_lang, target_lang) 
                   for item in data]
        elif isinstance(data, str) and data.strip():
            try:
                return self.translator.translate(data, source_lang, target_lang)
            except:
                return data
        else:
            return data
    
    def translate_xml(self, input_path: str, output_path: str,
                     source_lang: str, target_lang: str) -> bool:
        """
        Translate XML localization file
        
        Args:
            input_path: Input XML file path
            output_path: Output XML file path
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            True if successful
        """
        try:
            # Parse XML
            tree = ET.parse(input_path)
            root = tree.getroot()
            
            # Translate text in all elements
            for element in root.iter():
                if element.text and element.text.strip():
                    try:
                        element.text = self.translator.translate(element.text, source_lang, target_lang)
                    except:
                        pass
            
            # Save translated XML
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            tree.write(output_path, encoding='utf-8', xml_declaration=True)
            
            return True
            
        except Exception as e:
            print(f"XML translation error: {e}")
            return False
