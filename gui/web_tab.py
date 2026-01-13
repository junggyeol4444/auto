"""Web translation tab"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from modules.translation.translation_engine import TranslationEngine
from modules.web.html_translator import HTMLTranslator
from modules.web.localization import LocalizationTranslator


class WebTab:
    """Web translation tab"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        
        self._create_ui()
    
    def _create_ui(self):
        """Create UI elements"""
        # Mode selection
        mode_frame = ctk.CTkFrame(self.parent)
        mode_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(mode_frame, text="Translation Mode:", font=("Arial", 14)).pack(side="left", padx=10)
        
        self.mode = ctk.CTkSegmentedButton(
            mode_frame,
            values=["HTML File", "URL", "Localization File"]
        )
        self.mode.set("HTML File")
        self.mode.pack(side="left", padx=20)
        
        # Input frame
        input_frame = ctk.CTkFrame(self.parent)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        self.input_label = ctk.CTkLabel(input_frame, text="Select HTML File:")
        self.input_label.pack(side="left", padx=10)
        
        self.file_label = ctk.CTkLabel(input_frame, text="No file selected", text_color="gray")
        self.file_label.pack(side="left", padx=10)
        
        self.browse_button = ctk.CTkButton(
            input_frame,
            text="Browse",
            width=100,
            command=self._browse_file
        )
        self.browse_button.pack(side="right", padx=10)
        
        # URL entry (hidden by default)
        self.url_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter URL", width=400)
        
        # Language options
        options_frame = ctk.CTkFrame(self.parent)
        options_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(options_frame, text="From:").grid(row=0, column=0, padx=10, pady=10)
        self.source_lang = ctk.CTkComboBox(
            options_frame,
            values=["ko", "en", "ja", "zh-CN", "es", "fr", "de"],
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
        
        ctk.CTkLabel(preview_frame, text="Result", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.preview_text = ctk.CTkTextbox(preview_frame, height=400)
        self.preview_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(self.parent, text="", text_color="gray")
        self.progress_label.pack(pady=5)
        
        # Update mode callback
        self.mode.configure(command=self._on_mode_change)
        self.input_file = None
    
    def _on_mode_change(self, value):
        """Handle mode change"""
        if value == "URL":
            self.file_label.pack_forget()
            self.browse_button.pack_forget()
            self.input_label.configure(text="Enter URL:")
            self.url_entry.pack(side="left", padx=10, fill="x", expand=True)
        else:
            self.url_entry.pack_forget()
            if value == "HTML File":
                self.input_label.configure(text="Select HTML File:")
            else:
                self.input_label.configure(text="Select Localization File:")
            self.file_label.pack(side="left", padx=10)
            self.browse_button.pack(side="right", padx=10)
    
    def _browse_file(self):
        """Browse for file"""
        mode = self.mode.get()
        
        if mode == "HTML File":
            filetypes = [("HTML files", "*.html *.htm"), ("All files", "*.*")]
        else:  # Localization File
            filetypes = [
                ("Localization files", "*.json *.xml"),
                ("JSON files", "*.json"),
                ("XML files", "*.xml"),
                ("All files", "*.*")
            ]
        
        filename = filedialog.askopenfilename(
            title="Select file",
            filetypes=filetypes
        )
        
        if filename:
            self.input_file = filename
            self.file_label.configure(text=Path(filename).name)
    
    def _translate(self):
        """Translate web content"""
        mode = self.mode.get()
        
        if mode == "URL":
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showerror("Error", "Please enter a URL")
                return
            self._translate_url(url)
        elif mode == "HTML File":
            if not self.input_file:
                messagebox.showerror("Error", "Please select a file")
                return
            self._translate_html()
        else:  # Localization File
            if not self.input_file:
                messagebox.showerror("Error", "Please select a file")
                return
            self._translate_localization()
    
    def _translate_html(self):
        """Translate HTML file"""
        self.progress_label.configure(text="Translating HTML...")
        self.parent.update()
        
        try:
            engine = TranslationEngine(self.config)
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
                raise ValueError(f"Translation engine not available")
            
            # Get output filename
            output_file = filedialog.asksaveasfilename(
                title="Save translated HTML",
                defaultextension=".html",
                filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
                initialfile=f"{Path(self.input_file).stem}_translated.html"
            )
            
            if not output_file:
                self.progress_label.configure(text="Cancelled")
                return
            
            html_translator = HTMLTranslator(translator)
            success = html_translator.translate_file(
                self.input_file, output_file,
                self.source_lang.get(), self.target_lang.get()
            )
            
            if success:
                self.progress_label.configure(text="Translation complete!")
                messagebox.showinfo("Success", f"File saved to:\n{output_file}")
            else:
                raise Exception("Translation failed")
                
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))
            self.progress_label.configure(text="Translation failed")
    
    def _translate_url(self, url):
        """Translate URL content"""
        self.progress_label.configure(text="Translating URL...")
        self.parent.update()
        
        try:
            engine = TranslationEngine(self.config)
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
                raise ValueError(f"Translation engine not available")
            
            html_translator = HTMLTranslator(translator)
            translated_html = html_translator.translate_url(
                url,
                self.source_lang.get(),
                self.target_lang.get()
            )
            
            if translated_html:
                self.preview_text.delete("1.0", "end")
                self.preview_text.insert("1.0", translated_html[:5000])  # Show first 5000 chars
                self.progress_label.configure(text="Translation complete!")
            else:
                raise Exception("Translation failed")
                
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))
            self.progress_label.configure(text="Translation failed")
    
    def _translate_localization(self):
        """Translate localization file"""
        self.progress_label.configure(text="Translating localization file...")
        self.parent.update()
        
        try:
            engine = TranslationEngine(self.config)
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
                raise ValueError(f"Translation engine not available")
            
            file_ext = Path(self.input_file).suffix.lower()
            
            output_file = filedialog.asksaveasfilename(
                title="Save translated file",
                defaultextension=file_ext,
                filetypes=[(f"{file_ext.upper()} files", f"*{file_ext}"), ("All files", "*.*")],
                initialfile=f"{Path(self.input_file).stem}_translated{file_ext}"
            )
            
            if not output_file:
                self.progress_label.configure(text="Cancelled")
                return
            
            loc_translator = LocalizationTranslator(translator)
            
            if file_ext == '.json':
                success = loc_translator.translate_json(
                    self.input_file, output_file,
                    self.source_lang.get(), self.target_lang.get()
                )
            elif file_ext == '.xml':
                success = loc_translator.translate_xml(
                    self.input_file, output_file,
                    self.source_lang.get(), self.target_lang.get()
                )
            else:
                raise ValueError(f"Unsupported format: {file_ext}")
            
            if success:
                self.progress_label.configure(text="Translation complete!")
                messagebox.showinfo("Success", f"File saved to:\n{output_file}")
            else:
                raise Exception("Translation failed")
                
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))
            self.progress_label.configure(text="Translation failed")
