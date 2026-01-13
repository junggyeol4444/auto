"""Glossary/terminology management"""
import json
from pathlib import Path
from typing import Dict, Optional


class GlossaryManager:
    """Manage domain-specific glossaries"""
    
    def __init__(self, glossary_dir: str = "data/glossaries"):
        self.glossary_dir = Path(glossary_dir)
        self.glossaries = {}
        self._load_glossaries()
    
    def _load_glossaries(self):
        """Load all glossary files"""
        if not self.glossary_dir.exists():
            return
        
        for glossary_file in self.glossary_dir.glob("*.json"):
            domain = glossary_file.stem
            try:
                with open(glossary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.glossaries[domain] = self._parse_glossary(data)
            except Exception as e:
                print(f"Error loading glossary {domain}: {e}")
    
    def _parse_glossary(self, data: dict) -> Dict[str, str]:
        """Parse glossary JSON into source-target mapping"""
        glossary = {}
        if 'terms' in data:
            for term in data['terms']:
                if 'source' in term and 'target' in term:
                    glossary[term['source']] = term['target']
        return glossary
    
    def get_glossary(self, domain: str) -> Optional[Dict[str, str]]:
        """
        Get glossary for specific domain
        
        Args:
            domain: Domain name (medical, legal, it, etc.)
            
        Returns:
            Dictionary mapping source terms to target terms
        """
        return self.glossaries.get(domain)
    
    def apply_glossary(self, text: str, domain: str) -> str:
        """
        Apply glossary terms to text
        
        Args:
            text: Text to apply glossary to
            domain: Domain name
            
        Returns:
            Text with glossary terms applied
        """
        glossary = self.get_glossary(domain)
        if not glossary:
            return text
        
        result = text
        for source_term, target_term in glossary.items():
            result = result.replace(source_term, target_term)
        
        return result
    
    def add_term(self, domain: str, source: str, target: str, category: str = ""):
        """
        Add term to glossary
        
        Args:
            domain: Domain name
            source: Source term
            target: Target term
            category: Optional category
        """
        if domain not in self.glossaries:
            self.glossaries[domain] = {}
        
        self.glossaries[domain][source] = target
        
        # Save to file
        self._save_glossary(domain)
    
    def _save_glossary(self, domain: str):
        """Save glossary to file"""
        self.glossary_dir.mkdir(parents=True, exist_ok=True)
        
        glossary = self.glossaries.get(domain, {})
        data = {
            "terms": [
                {"source": source, "target": target, "category": domain}
                for source, target in glossary.items()
            ]
        }
        
        glossary_file = self.glossary_dir / f"{domain}.json"
        with open(glossary_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_available_domains(self) -> list:
        """Get list of available glossary domains"""
        return list(self.glossaries.keys())
