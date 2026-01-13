"""ASS (Advanced SubStation Alpha) subtitle parser and translator"""
import re
from typing import List
from pathlib import Path
from .srt_parser import SubtitleEntry


class ASSParser:
    """Parse and translate ASS subtitle files"""
    
    @staticmethod
    def parse(file_path: str) -> List[SubtitleEntry]:
        """
        Parse ASS file into subtitle entries
        
        Args:
            file_path: Path to ASS file
            
        Returns:
            List of SubtitleEntry objects
        """
        entries = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Find Events section
        in_events = False
        format_line = None
        index = 1
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('[Events]'):
                in_events = True
                continue
            
            if in_events:
                if line.startswith('Format:'):
                    format_line = line
                    continue
                
                if line.startswith('Dialogue:'):
                    try:
                        # Parse dialogue line
                        parts = line.split(':', 1)[1].split(',', 9)
                        if len(parts) >= 10:
                            start_time = ASSParser._convert_ass_time(parts[1].strip())
                            end_time = ASSParser._convert_ass_time(parts[2].strip())
                            text = parts[9].strip()
                            
                            # Remove ASS formatting tags
                            text = re.sub(r'\{[^}]+\}', '', text)
                            text = text.replace('\\N', '\n')
                            
                            entries.append(SubtitleEntry(index, start_time, end_time, text))
                            index += 1
                    except (ValueError, IndexError):
                        continue
        
        return entries
    
    @staticmethod
    def _convert_ass_time(ass_time: str) -> str:
        """Convert ASS time format (0:00:00.00) to SRT format (00:00:00,000)"""
        parts = ass_time.split(':')
        if len(parts) == 3:
            h, m, s = parts
            s_parts = s.split('.')
            if len(s_parts) == 2:
                ms = s_parts[1].ljust(3, '0')[:3]
                return f"{h.zfill(2)}:{m.zfill(2)}:{s_parts[0].zfill(2)},{ms}"
        return ass_time
    
    @staticmethod
    def save(entries: List[SubtitleEntry], output_path: str):
        """
        Save subtitle entries to ASS file
        
        Args:
            entries: List of SubtitleEntry objects
            output_path: Output file path
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write ASS header
            f.write('[Script Info]\n')
            f.write('Title: Translated Subtitles\n')
            f.write('ScriptType: v4.00+\n')
            f.write('Collisions: Normal\n\n')
            
            f.write('[V4+ Styles]\n')
            f.write('Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n')
            f.write('Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n\n')
            
            f.write('[Events]\n')
            f.write('Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')
            
            for entry in entries:
                start = ASSParser._convert_srt_to_ass_time(entry.start_time)
                end = ASSParser._convert_srt_to_ass_time(entry.end_time)
                text = entry.text.replace('\n', '\\N')
                f.write(f'Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n')
    
    @staticmethod
    def _convert_srt_to_ass_time(srt_time: str) -> str:
        """Convert SRT time format to ASS format"""
        srt_time = srt_time.replace(',', '.')
        parts = srt_time.split(':')
        if len(parts) == 3:
            h, m, s = parts
            s_parts = s.split('.')
            if len(s_parts) == 2:
                ms = s_parts[1][:2].ljust(2, '0')
                return f"{h}:{m}:{s_parts[0]}.{ms}"
        return srt_time
    
    @staticmethod
    def translate_entries(entries: List[SubtitleEntry], translator, source_lang: str, target_lang: str) -> List[SubtitleEntry]:
        """Translate subtitle entries"""
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
