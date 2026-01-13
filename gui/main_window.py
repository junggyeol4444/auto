"""
Main window for AI Design Automation Suite
"""
import customtkinter as ctk
from gui.thumbnail_tab import ThumbnailTab
from gui.synthesis_tab import SynthesisTab


class MainWindow(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("AI Design Automation Suite")
        self.geometry("1200x800")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create tab view
        self.tabview = ctk.CTkTabview(self, width=1180, height=780)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Add tabs
        self.tabview.add("유튜브 썸네일")
        self.tabview.add("사진 합성")
        
        # Initialize tabs
        self.thumbnail_tab = ThumbnailTab(self.tabview.tab("유튜브 썸네일"))
        self.synthesis_tab = SynthesisTab(self.tabview.tab("사진 합성"))
    
    def run(self):
        """Run the application"""
        self.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
