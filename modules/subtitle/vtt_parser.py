"""VTT (WebVTT) subtitle parser and translator"""
import re
from typing import List
from pathlib import Path
from .srt_parser import SubtitleEntry


class VTTParser:
    """Parse and translate VTT subtitle files"""
    
    @staticmethod
    def parse(file_path: str) -> List[SubtitleEntry]:
        """
        Parse VTT file into subtitle entries
        
        Args:
            file_path: Path to VTT file
            
        Returns:
            List of SubtitleEntry objects
        """
        entries = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip WEBVTT header
        if content.startswith('WEBVTT'):
            content = content.split('\n', 1)[1] if '\n' in content else ''
        
        # Split by double newlines
        blocks = re.split(r'\n\n+', content.strip())
        
        index = 1
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 2:
                # Skip cue identifier if present
                start_idx = 0
                if '-->' not in lines[0]:
                    start_idx = 1
                
                if start_idx < len(lines):
                    time_line = lines[start_idx]
                    if '-->' in time_line:
                        try:
                            time_parts = time_line.split(' --> ')
                            start_time = time_parts[0].strip()
                            end_time = time_parts[1].strip().split()[0]  # Remove cue settings
                            text = '\n'.join(lines[start_idx + 1:])
                            entries.append(SubtitleEntry(index, start_time, end_time, text))
                            index += 1
                        except (ValueError, IndexError):
                            continue
        
        return entries
    
    @staticmethod
    def save(entries: List[SubtitleEntry], output_path: str):
        """
        Save subtitle entries to VTT file
        
        Args:
            entries: List of SubtitleEntry objects
            output_path: Output file path
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('WEBVTT\n\n')
            for entry in entries:
                # Convert SRT time format (,) to VTT format (.)
                start = entry.start_time.replace(',', '.')
                end = entry.end_time.replace(',', '.')
                f.write(f"{start} --> {end}\n{entry.text}\n\n")
    
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
        
        texts = [entry.text for entry in entries]
        translated_texts = translator.translate_batch(texts, source_lang, target_lang)
        
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
