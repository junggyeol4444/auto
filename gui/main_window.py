import customtkinter as ctk
import json
import os
from modules.database import DatabaseHandler
from gui.editor_window import EditorWindow

class MainWindow:
    def __init__(self):
        # Load config
        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)
        
        # Initialize database
        self.db = DatabaseHandler(self.config["database"])
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title(self.config["app_name"])
        self.root.geometry("1200x700")
        
        # Set theme
        ctk.set_appearance_mode(self.config["ui"]["theme"])
        ctk.set_default_color_theme("blue")
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create main UI layout"""
        # Main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Menu
        self.left_panel = ctk.CTkFrame(self.main_container, width=200)
        self.left_panel.pack(side="left", fill="y", padx=(0, 10))
        self.left_panel.pack_propagate(False)
        
        # Center panel - Content
        self.center_panel = ctk.CTkFrame(self.main_container)
        self.center_panel.pack(side="left", fill="both", expand=True)
        
        # Create menu
        self.create_menu()
        
        # Create welcome screen
        self.show_welcome()
    
    def create_menu(self):
        """Create left menu panel"""
        # Title
        title_label = ctk.CTkLabel(
            self.left_panel, 
            text="기능 메뉴",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Menu buttons
        menu_items = [
            ("📖 웹소설", self.show_webnovel_menu),
            ("🎬 시나리오", self.show_scenario_menu),
            ("🎮 게임", self.show_game_menu),
            ("💡 아이디어", self.show_ideas_menu),
            ("📂 프로젝트", self.show_projects),
            ("⚙️ 설정", self.show_settings)
        ]
        
        for text, command in menu_items:
            btn = ctk.CTkButton(
                self.left_panel,
                text=text,
                command=command,
                height=40,
                font=ctk.CTkFont(size=14)
            )
            btn.pack(pady=5, padx=10, fill="x")
    
    def clear_center_panel(self):
        """Clear center panel"""
        for widget in self.center_panel.winfo_children():
            widget.destroy()
    
    def show_welcome(self):
        """Show welcome screen"""
        self.clear_center_panel()
        
        welcome_frame = ctk.CTkFrame(self.center_panel)
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text="Creative Writing Assistant Suite",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        welcome_label.pack(pady=40)
        
        description = ctk.CTkLabel(
            welcome_frame,
            text="웹소설, 시나리오, 게임 등 모든 창작을 위한 도구입니다.\n\n좌측 메뉴에서 원하는 기능을 선택하세요.",
            font=ctk.CTkFont(size=16),
            justify="center"
        )
        description.pack(pady=20)
        
        # Quick start buttons
        quick_frame = ctk.CTkFrame(welcome_frame)
        quick_frame.pack(pady=40)
        
        ctk.CTkButton(
            quick_frame,
            text="🚀 빠른 시작: 플롯 생성",
            command=self.quick_plot,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16)
        ).pack(pady=10)
        
        ctk.CTkButton(
            quick_frame,
            text="👤 빠른 시작: 캐릭터 생성",
            command=self.quick_character,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16)
        ).pack(pady=10)
    
    def show_webnovel_menu(self):
        """Show webnovel submenu"""
        self.clear_center_panel()
        
        title = ctk.CTkLabel(
            self.center_panel,
            text="웹소설 창작",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        # Button grid
        button_frame = ctk.CTkFrame(self.center_panel)
        button_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        buttons = [
            ("📖 플롯 생성", self.show_plot_generator),
            ("👤 캐릭터 생성", self.show_character_generator),
            ("🌍 세계관 구축", self.show_worldbuilding),
            ("💬 대화 생성", self.show_dialogue_generator),
            ("🖼️ 장면 묘사", self.show_scene_generator),
            ("⚡ 파워 시스템", self.show_power_system)
        ]
        
        for i, (text, command) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                width=300,
                height=80,
                font=ctk.CTkFont(size=18)
            )
            btn.grid(row=row, column=col, padx=20, pady=20)
    
    def show_scenario_menu(self):
        """Show scenario submenu"""
        self.clear_center_panel()
        
        title = ctk.CTkLabel(
            self.center_panel,
            text="시나리오 창작",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        button_frame = ctk.CTkFrame(self.center_panel)
        button_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        buttons = [
            ("🎬 영화 시나리오", self.show_movie_scenario),
            ("📺 드라마 시놉시스", self.show_drama_synopsis),
            ("📚 웹툰 스토리보드", self.show_webtoon_storyboard)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                width=300,
                height=80,
                font=ctk.CTkFont(size=18)
            )
            btn.grid(row=i // 2, column=i % 2, padx=20, pady=20)
    
    def show_game_menu(self):
        """Show game submenu"""
        self.clear_center_panel()
        
        title = ctk.CTkLabel(
            self.center_panel,
            text="게임 창작",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        button_frame = ctk.CTkFrame(self.center_panel)
        button_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        buttons = [
            ("🎮 퀘스트 생성", self.show_quest_generator),
            ("🧙 NPC 생성", self.show_npc_generator),
            ("🏰 던전 디자인", self.show_dungeon_designer),
            ("🎲 TRPG 테이블", self.show_trpg_tools)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                width=300,
                height=80,
                font=ctk.CTkFont(size=18)
            )
            btn.grid(row=i // 2, column=i % 2, padx=20, pady=20)
    
    def show_ideas_menu(self):
        """Show ideas submenu"""
        self.clear_center_panel()
        
        title = ctk.CTkLabel(
            self.center_panel,
            text="아이디어 생성",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        button_frame = ctk.CTkFrame(self.center_panel)
        button_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        buttons = [
            ("💡 소설 아이디어", self.show_idea_generator),
            ("📌 제목 생성", self.show_title_generator),
            ("🔄 플롯 트위스트", self.show_twist_generator)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                width=300,
                height=80,
                font=ctk.CTkFont(size=18)
            )
            btn.grid(row=i // 2, column=i % 2, padx=20, pady=20)
    
    def show_projects(self):
        """Show projects list"""
        self.clear_center_panel()
        
        title = ctk.CTkLabel(
            self.center_panel,
            text="프로젝트 관리",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        # Projects list
        projects = self.db.get_projects()
        
        if not projects:
            no_projects = ctk.CTkLabel(
                self.center_panel,
                text="프로젝트가 없습니다.\n새 프로젝트를 생성하세요.",
                font=ctk.CTkFont(size=16)
            )
            no_projects.pack(pady=40)
        else:
            # Scrollable frame for projects
            scroll_frame = ctk.CTkScrollableFrame(self.center_panel, width=700, height=400)
            scroll_frame.pack(pady=20, padx=20)
            
            for project in projects:
                project_id, name, proj_type, created, updated = project
                
                proj_frame = ctk.CTkFrame(scroll_frame)
                proj_frame.pack(fill="x", pady=5, padx=10)
                
                ctk.CTkLabel(
                    proj_frame,
                    text=f"{name} ({proj_type})",
                    font=ctk.CTkFont(size=14, weight="bold")
                ).pack(side="left", padx=10)
                
                ctk.CTkButton(
                    proj_frame,
                    text="열기",
                    width=80,
                    command=lambda pid=project_id: self.open_project(pid)
                ).pack(side="right", padx=5)
    
    def show_settings(self):
        """Show settings"""
        self.clear_center_panel()
        
        title = ctk.CTkLabel(
            self.center_panel,
            text="설정",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        settings_frame = ctk.CTkFrame(self.center_panel)
        settings_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Theme setting
        ctk.CTkLabel(
            settings_frame,
            text="테마:",
            font=ctk.CTkFont(size=16)
        ).pack(pady=10)
        
        theme_var = ctk.StringVar(value=self.config["ui"]["theme"])
        theme_menu = ctk.CTkOptionMenu(
            settings_frame,
            values=["dark", "light"],
            variable=theme_var,
            command=self.change_theme
        )
        theme_menu.pack(pady=10)
    
    def change_theme(self, theme):
        """Change application theme"""
        ctk.set_appearance_mode(theme)
        self.config["ui"]["theme"] = theme
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    # Quick start functions
    def quick_plot(self):
        """Quick start plot generation"""
        self.show_webnovel_menu()
        self.root.after(100, self.show_plot_generator)
    
    def quick_character(self):
        """Quick start character generation"""
        self.show_webnovel_menu()
        self.root.after(100, self.show_character_generator)
    
    # Feature functions (to be implemented in editor_window)
    def show_plot_generator(self):
        """Show plot generator"""
        EditorWindow(self.root, "plot", self.db)
    
    def show_character_generator(self):
        """Show character generator"""
        EditorWindow(self.root, "character", self.db)
    
    def show_worldbuilding(self):
        """Show worldbuilding"""
        EditorWindow(self.root, "worldbuilding", self.db)
    
    def show_dialogue_generator(self):
        """Show dialogue generator"""
        EditorWindow(self.root, "dialogue", self.db)
    
    def show_scene_generator(self):
        """Show scene generator"""
        EditorWindow(self.root, "scene", self.db)
    
    def show_power_system(self):
        """Show power system"""
        EditorWindow(self.root, "power", self.db)
    
    def show_movie_scenario(self):
        """Show movie scenario generator"""
        EditorWindow(self.root, "movie", self.db)
    
    def show_drama_synopsis(self):
        """Show drama synopsis generator"""
        EditorWindow(self.root, "drama", self.db)
    
    def show_webtoon_storyboard(self):
        """Show webtoon storyboard generator"""
        EditorWindow(self.root, "webtoon", self.db)
    
    def show_quest_generator(self):
        """Show quest generator"""
        EditorWindow(self.root, "quest", self.db)
    
    def show_npc_generator(self):
        """Show NPC generator"""
        EditorWindow(self.root, "npc", self.db)
    
    def show_dungeon_designer(self):
        """Show dungeon designer"""
        EditorWindow(self.root, "dungeon", self.db)
    
    def show_trpg_tools(self):
        """Show TRPG tools"""
        EditorWindow(self.root, "trpg", self.db)
    
    def show_idea_generator(self):
        """Show idea generator"""
        EditorWindow(self.root, "idea", self.db)
    
    def show_title_generator(self):
        """Show title generator"""
        EditorWindow(self.root, "title", self.db)
    
    def show_twist_generator(self):
        """Show twist generator"""
        EditorWindow(self.root, "twist", self.db)
    
    def open_project(self, project_id):
        """Open existing project"""
        project = self.db.get_project(project_id)
        if project:
            # Open project in editor
            EditorWindow(self.root, "project", self.db, project)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()
