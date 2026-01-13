"""Document translation tab"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from modules.translation.translation_engine import TranslationEngine
from modules.document.docx_translator import DocxTranslator
from modules.document.pdf_translator import PDFTranslator
from modules.document.pptx_translator import PPTXTranslator
from modules.document.xlsx_translator import XLSXTranslator
from modules.utils.glossary import GlossaryManager


class DocumentTab:
    """Document translation tab"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.input_file = None
        self.glossary_manager = GlossaryManager()
        
        self._create_ui()
    
    def _create_ui(self):
        """Create UI elements"""
        # File selection
        file_frame = ctk.CTkFrame(self.parent)
        file_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(file_frame, text="Select Document:").pack(side="left", padx=10)
        
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
        
        # Domain selection
        ctk.CTkLabel(options_frame, text="Domain:").grid(row=1, column=0, padx=10, pady=10)
        domains = ["general"] + self.glossary_manager.get_available_domains()
        self.domain = ctk.CTkComboBox(
            options_frame,
            values=domains,
            width=120
        )
        self.domain.set("general")
        self.domain.grid(row=1, column=1, padx=10, pady=10)
        
        # Engine selection
        ctk.CTkLabel(options_frame, text="Engine:").grid(row=1, column=2, padx=10, pady=10)
        self.engine = ctk.CTkComboBox(
            options_frame,
            values=["auto", "deepl", "google", "papago", "gpt4"],
            width=100
        )
        self.engine.set(self.config.get('default_engine', 'google'))
        self.engine.grid(row=1, column=3, padx=10, pady=10)
        
        # Translate button
        ctk.CTkButton(
            options_frame,
            text="Translate Document",
            command=self._translate,
            width=200,
            height=40
        ).grid(row=0, column=4, rowspan=2, padx=20, pady=10)
        
        # Info frame
        info_frame = ctk.CTkFrame(self.parent)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(info_frame, text="Document Translation", font=("Arial", 16, "bold")).pack(pady=10)
        
        info_text = """
        Supported formats:
        • DOCX - Microsoft Word documents (preserves formatting)
        • PDF - Portable Document Format (text extraction)
        • PPTX - PowerPoint presentations (slide-by-slide)
        • XLSX - Excel spreadsheets (cell-by-cell)
        
        Domain glossaries will be applied automatically when selected.
        """
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            justify="left",
            text_color="gray"
        ).pack(pady=20)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(self.parent, text="", font=("Arial", 12))
        self.progress_label.pack(pady=10)
    
    def _browse_file(self):
        """Browse for document file"""
        filetypes = [
            ("Document files", "*.docx *.pdf *.pptx *.xlsx"),
            ("Word documents", "*.docx"),
            ("PDF files", "*.pdf"),
            ("PowerPoint", "*.pptx"),
            ("Excel", "*.xlsx"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select document",
            filetypes=filetypes
        )
        
        if filename:
            self.input_file = filename
            self.file_label.configure(text=Path(filename).name)
    
    def _translate(self):
        """Translate document"""
        if not self.input_file:
            messagebox.showerror("Error", "Please select a file first")
            return
        
        self.progress_label.configure(text="Translating document...")
        self.parent.update()
        
        try:
            # Initialize translation engine
            engine = TranslationEngine(self.config)
            
            # Get translator
            engine_type = self.engine.get()
            domain = self.domain.get()
            
            if engine_type == "auto":
                translator = engine.auto_select_engine(
                    self.source_lang.get(),
                    self.target_lang.get(),
                    domain
                )
            else:
                translator = engine.get_translator(engine_type)
            
            if not translator:
                raise ValueError(f"Translation engine '{engine_type}' not available. Please configure API keys in Settings.")
            
            # Get glossary
            glossary = None
            if domain != "general":
                glossary = self.glossary_manager.get_glossary(domain)
            
            # Get output filename
            file_ext = Path(self.input_file).suffix.lower()
            output_file = filedialog.asksaveasfilename(
                title="Save translated document",
                defaultextension=file_ext,
                filetypes=[(f"{file_ext.upper()} files", f"*{file_ext}"), ("All files", "*.*")],
                initialfile=f"{Path(self.input_file).stem}_translated{file_ext}"
            )
            
            if not output_file:
                self.progress_label.configure(text="Translation cancelled")
                return
            
            # Translate based on file type
            success = False
            if file_ext == '.docx':
                doc_translator = DocxTranslator(translator)
                success = doc_translator.translate_file(
                    self.input_file, output_file,
                    self.source_lang.get(), self.target_lang.get(),
                    glossary
                )
            elif file_ext == '.pdf':
                pdf_translator = PDFTranslator(translator)
                success = pdf_translator.translate_file(
                    self.input_file, output_file,
                    self.source_lang.get(), self.target_lang.get(),
                    glossary
                )
            elif file_ext == '.pptx':
                pptx_translator = PPTXTranslator(translator)
                success = pptx_translator.translate_file(
                    self.input_file, output_file,
                    self.source_lang.get(), self.target_lang.get(),
                    glossary
                )
            elif file_ext == '.xlsx':
                xlsx_translator = XLSXTranslator(translator)
                success = xlsx_translator.translate_file(
                    self.input_file, output_file,
                    self.source_lang.get(), self.target_lang.get(),
                    glossary
                )
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
            
            if success:
                self.progress_label.configure(text="Translation complete!")
                messagebox.showinfo("Success", f"Document saved to:\n{output_file}")
            else:
                raise Exception("Translation failed")
            
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))
            self.progress_label.configure(text="Translation failed")
