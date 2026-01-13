"""SRT (SubRip) subtitle parser and translator"""
import re
from typing import List, Tuple
from pathlib import Path


class SubtitleEntry:
    """Represents a single subtitle entry"""
    def __init__(self, index: int, start_time: str, end_time: str, text: str):
        self.index = index
        self.start_time = start_time
        self.end_time = end_time
        self.text = text
    
    def __str__(self):
        return f"{self.index}\n{self.start_time} --> {self.end_time}\n{self.text}\n"


class SRTParser:
    """Parse and translate SRT subtitle files"""
    
    @staticmethod
    def parse(file_path: str) -> List[SubtitleEntry]:
        """
        Parse SRT file into subtitle entries
        
        Args:
            file_path: Path to SRT file
            
        Returns:
            List of SubtitleEntry objects
        """
        entries = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by double newlines
        blocks = re.split(r'\n\n+', content.strip())
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                try:
                    index = int(lines[0])
                    # Time format: 00:00:00,000 --> 00:00:02,000
                    time_parts = lines[1].split(' --> ')
                    if len(time_parts) == 2:
                        start_time = time_parts[0].strip()
                        end_time = time_parts[1].strip()
                        text = '\n'.join(lines[2:])
                        entries.append(SubtitleEntry(index, start_time, end_time, text))
                except (ValueError, IndexError):
                    continue
        
        return entries
    
    @staticmethod
    def save(entries: List[SubtitleEntry], output_path: str):
        """
        Save subtitle entries to SRT file
        
        Args:
            entries: List of SubtitleEntry objects
            output_path: Output file path
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for entry in entries:
                f.write(str(entry) + '\n')
    
    @staticmethod
    def translate_entries(entries: List[SubtitleEntry], translator, source_lang: str, target_lang: str) -> List[SubtitleEntry]:
        """
        Translate subtitle entries
        
        Args:
            entries: List of SubtitleEntry objects
            translator: Translator instance
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            List of translated SubtitleEntry objects
        """
        if not entries:
            return []
        
        # Extract texts
        texts = [entry.text for entry in entries]
        
        # Translate in batch
        translated_texts = translator.translate_batch(texts, source_lang, target_lang)
        
        # Create new entries with translated text
        translated_entries = []
        for i, entry in enumerate(entries):
            translated_entry = SubtitleEntry(
                entry.index,
                entry.start_time,
                entry.end_time,
                translated_texts[i] if i < len(translated_texts) else entry.text
            )
            translated_entries.append(translated_entry)
        
        return translated_entries
