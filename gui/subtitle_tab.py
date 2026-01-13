"""Subtitle translation tab"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from modules.translation.translation_engine import TranslationEngine
from modules.subtitle.srt_parser import SRTParser
from modules.subtitle.vtt_parser import VTTParser
from modules.subtitle.ass_parser import ASSParser


class SubtitleTab:
    """Subtitle translation tab"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.input_file = None
        self.entries = []
        
        self._create_ui()
    
    def _create_ui(self):
        """Create UI elements"""
        # File selection frame
        file_frame = ctk.CTkFrame(self.parent)
        file_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(file_frame, text="Select Subtitle File:").pack(side="left", padx=10)
        
        self.file_label = ctk.CTkLabel(file_frame, text="No file selected", text_color="gray")
        self.file_label.pack(side="left", padx=10)
        
        ctk.CTkButton(
            file_frame,
            text="Browse",
            width=100,
            command=self._browse_file
        ).pack(side="right", padx=10)
        
        # Options frame
        options_frame = ctk.CTkFrame(self.parent)
        options_frame.pack(fill="x", padx=20, pady=10)
        
        # Source language
        ctk.CTkLabel(options_frame, text="From:").grid(row=0, column=0, padx=10, pady=10)
        self.source_lang = ctk.CTkComboBox(
            options_frame,
            values=["ko", "en", "ja", "zh-CN", "es", "fr", "de"],
            width=100
        )
        self.source_lang.set(self.config.get('default_source_lang', 'ko'))
        self.source_lang.grid(row=0, column=1, padx=10, pady=10)
        
        # Target language
        ctk.CTkLabel(options_frame, text="To:").grid(row=0, column=2, padx=10, pady=10)
        self.target_lang = ctk.CTkComboBox(
            options_frame,
            values=["en", "ko", "ja", "zh-CN", "es", "fr", "de"],
            width=100
        )
        self.target_lang.set(self.config.get('default_target_lang', 'en'))
        self.target_lang.grid(row=0, column=3, padx=10, pady=10)
        
        # Engine selection
        ctk.CTkLabel(options_frame, text="Engine:").grid(row=0, column=4, padx=10, pady=10)
        self.engine = ctk.CTkComboBox(
            options_frame,
            values=["auto", "deepl", "google", "papago", "gpt4"],
            width=100
        )
        self.engine.set(self.config.get('default_engine', 'google'))
        self.engine.grid(row=0, column=5, padx=10, pady=10)
        
        # Translate button
        ctk.CTkButton(
            options_frame,
            text="Translate",
            command=self._translate,
            width=150,
            height=40
        ).grid(row=0, column=6, padx=20, pady=10)
        
        # Preview frame
        preview_frame = ctk.CTkFrame(self.parent)
        preview_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(preview_frame, text="Preview", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Text widget for preview
        self.preview_text = ctk.CTkTextbox(preview_frame, height=400)
        self.preview_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Save button
        ctk.CTkButton(
            self.parent,
            text="Save Translated File",
            command=self._save_file,
            width=200,
            height=40
        ).pack(pady=10)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(self.parent, text="", text_color="gray")
        self.progress_label.pack(pady=5)
    
    def _browse_file(self):
        """Browse for subtitle file"""
        filetypes = [
            ("Subtitle files", "*.srt *.vtt *.ass"),
            ("SRT files", "*.srt"),
            ("VTT files", "*.vtt"),
            ("ASS files", "*.ass"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select subtitle file",
            filetypes=filetypes
        )
        
        if filename:
            self.input_file = filename
            self.file_label.configure(text=Path(filename).name)
    
    def _translate(self):
        """Translate subtitle file"""
        if not self.input_file:
            messagebox.showerror("Error", "Please select a file first")
            return
        
        self.progress_label.configure(text="Translating...")
        self.parent.update()
        
        try:
            # Initialize translation engine
            engine = TranslationEngine(self.config)
            
            # Get translator
            engine_type = self.engine.get()
            if engine_type == "auto":
                translator = engine.auto_select_engine(
                    self.source_lang.get(),
                    self.target_lang.get(),
                    "general"
                )
            else:
                translator = engine.get_translator(engine_type)
            
            if not translator:
                raise ValueError(f"Translation engine '{engine_type}' not available. Please configure API keys in Settings.")
            
            # Parse subtitle file
            file_ext = Path(self.input_file).suffix.lower()
            if file_ext == '.srt':
                parser = SRTParser
            elif file_ext == '.vtt':
                parser = VTTParser
            elif file_ext == '.ass':
                parser = ASSParser
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
            
            # Parse
            self.entries = parser.parse(self.input_file)
            
            # Translate
            self.translated_entries = parser.translate_entries(
                self.entries,
                translator,
                self.source_lang.get(),
                self.target_lang.get()
            )
            
            # Show preview
            self._show_preview()
            
            self.progress_label.configure(text="Translation complete!")
            
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))
            self.progress_label.configure(text="Translation failed")
    
    def _show_preview(self):
        """Show translation preview"""
        self.preview_text.delete("1.0", "end")
        
        preview_lines = []
        for i, entry in enumerate(self.translated_entries[:10]):  # Show first 10
            preview_lines.append(f"[{i+1}] {entry.start_time} --> {entry.end_time}")
            preview_lines.append(entry.text)
            preview_lines.append("")
        
        if len(self.translated_entries) > 10:
            preview_lines.append(f"... and {len(self.translated_entries) - 10} more entries")
        
        self.preview_text.insert("1.0", "\n".join(preview_lines))
    
    def _save_file(self):
        """Save translated subtitle file"""
        if not hasattr(self, 'translated_entries') or not self.translated_entries:
            messagebox.showerror("Error", "No translation to save")
            return
        
        # Get output filename
        file_ext = Path(self.input_file).suffix.lower()
        filetypes = [(f"{file_ext.upper()} files", f"*{file_ext}"), ("All files", "*.*")]
        
        output_file = filedialog.asksaveasfilename(
            title="Save translated file",
            defaultextension=file_ext,
            filetypes=filetypes,
            initialfile=f"{Path(self.input_file).stem}_translated{file_ext}"
        )
        
        if output_file:
            try:
                # Save based on format
                file_ext = Path(self.input_file).suffix.lower()
                if file_ext == '.srt':
                    SRTParser.save(self.translated_entries, output_file)
                elif file_ext == '.vtt':
                    VTTParser.save(self.translated_entries, output_file)
                elif file_ext == '.ass':
                    ASSParser.save(self.translated_entries, output_file)
                
                messagebox.showinfo("Success", f"File saved to:\n{output_file}")
                
            except Exception as e:
                messagebox.showerror("Save Error", str(e))
