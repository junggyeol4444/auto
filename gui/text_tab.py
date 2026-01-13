"""Text translation tab"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from modules.translation.translation_engine import TranslationEngine


class TextTab:
    """Text translation tab"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        
        self._create_ui()
    
    def _create_ui(self):
        """Create UI elements"""
        # Options frame
        options_frame = ctk.CTkFrame(self.parent)
        options_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(options_frame, text="From:").grid(row=0, column=0, padx=10, pady=10)
        self.source_lang = ctk.CTkComboBox(
            options_frame,
            values=["auto", "ko", "en", "ja", "zh-CN", "es", "fr", "de"],
            width=100
        )
        self.source_lang.set(self.config.get('default_source_lang', 'ko'))
        self.source_lang.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(options_frame, text="To:").grid(row=0, column=2, padx=10, pady=10)
        self.target_lang = ctk.CTkComboBox(
            options_frame,
            values=["en", "ko", "ja", "zh-CN", "es", "fr", "de"],
            width=100
        )
        self.target_lang.set(self.config.get('default_target_lang', 'en'))
        self.target_lang.grid(row=0, column=3, padx=10, pady=10)
        
        ctk.CTkLabel(options_frame, text="Engine:").grid(row=0, column=4, padx=10, pady=10)
        self.engine = ctk.CTkComboBox(
            options_frame,
            values=["auto", "deepl", "google", "papago", "gpt4"],
            width=100
        )
        self.engine.set(self.config.get('default_engine', 'google'))
        self.engine.grid(row=0, column=5, padx=10, pady=10)
        
        # Text area frame
        text_frame = ctk.CTkFrame(self.parent)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Input text
        input_frame = ctk.CTkFrame(text_frame)
        input_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(input_frame, text="Input Text", font=("Arial", 14, "bold")).pack(pady=5)
        
        self.input_text = ctk.CTkTextbox(input_frame, height=400)
        self.input_text.pack(fill="both", expand=True, pady=5)
        
        input_buttons = ctk.CTkFrame(input_frame)
        input_buttons.pack(fill="x", pady=5)
        
        ctk.CTkButton(
            input_buttons,
            text="Load from File",
            command=self._load_file,
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            input_buttons,
            text="Clear",
            command=lambda: self.input_text.delete("1.0", "end"),
            width=80
        ).pack(side="left", padx=5)
        
        # Arrow button
        arrow_frame = ctk.CTkFrame(text_frame, width=80)
        arrow_frame.pack(side="left", padx=10, pady=100)
        
        ctk.CTkButton(
            arrow_frame,
            text="→\nTranslate",
            command=self._translate,
            width=80,
            height=80,
            font=("Arial", 14, "bold")
        ).pack(pady=20)
        
        # Output text
        output_frame = ctk.CTkFrame(text_frame)
        output_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(output_frame, text="Translated Text", font=("Arial", 14, "bold")).pack(pady=5)
        
        self.output_text = ctk.CTkTextbox(output_frame, height=400)
        self.output_text.pack(fill="both", expand=True, pady=5)
        
        output_buttons = ctk.CTkFrame(output_frame)
        output_buttons.pack(fill="x", pady=5)
        
        ctk.CTkButton(
            output_buttons,
            text="Save to File",
            command=self._save_file,
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            output_buttons,
            text="Copy",
            command=self._copy_output,
            width=80
        ).pack(side="left", padx=5)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(self.parent, text="", text_color="gray")
        self.progress_label.pack(pady=5)
    
    def _load_file(self):
        """Load text from file"""
        filename = filedialog.askopenfilename(
            title="Load text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    text = f.read()
                self.input_text.delete("1.0", "end")
                self.input_text.insert("1.0", text)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{e}")
    
    def _save_file(self):
        """Save translated text to file"""
        text = self.output_text.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Warning", "No text to save")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save translated text",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("Success", "File saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
    
    def _copy_output(self):
        """Copy output to clipboard"""
        text = self.output_text.get("1.0", "end-1c")
        if text.strip():
            self.parent.clipboard_clear()
            self.parent.clipboard_append(text)
            self.progress_label.configure(text="Copied to clipboard!")
    
    def _translate(self):
        """Translate text"""
        input_text = self.input_text.get("1.0", "end-1c").strip()
        
        if not input_text:
            messagebox.showwarning("Warning", "Please enter text to translate")
            return
        
        self.progress_label.configure(text="Translating...")
        self.parent.update()
        
        try:
            engine = TranslationEngine(self.config)
            engine_type = self.engine.get()
            
            source_lang = self.source_lang.get()
            target_lang = self.target_lang.get()
            
            # Auto-detect source language if set to auto
            if source_lang == "auto":
                from modules.utils.language_detector import LanguageDetector
                detector = LanguageDetector()
                if detector.is_available():
                    source_lang = detector.detect_language(input_text)
                    self.progress_label.configure(text=f"Detected language: {source_lang}")
                    self.parent.update()
                else:
                    source_lang = "en"  # Default fallback
            
            if engine_type == "auto":
                translator = engine.auto_select_engine(source_lang, target_lang, "general")
            else:
                translator = engine.get_translator(engine_type)
            
            if not translator:
                raise ValueError(f"Translation engine not available. Please configure API keys in Settings.")
            
            # Translate
            translated_text = translator.translate(input_text, source_lang, target_lang)
            
            # Display result
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", translated_text)
            
            self.progress_label.configure(text="Translation complete!")
            
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))
            self.progress_label.configure(text="Translation failed")
