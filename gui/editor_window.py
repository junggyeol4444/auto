import customtkinter as ctk
import json
from tkinter import filedialog, messagebox
from modules.webnovel.plot_generator import PlotGenerator
from modules.webnovel.character_generator import CharacterGenerator
from modules.webnovel.worldbuilding import WorldbuildingGenerator
from modules.webnovel.dialogue_generator import DialogueGenerator
from modules.webnovel.scene_generator import SceneGenerator
from modules.scenario.scenario_generator import ScenarioGenerator, SynopsisGenerator
from modules.game.quest_generator import QuestGenerator, NPCGenerator, DungeonDesigner
from modules.ideas.title_generator import TitleGenerator, TwistGenerator, IdeaGenerator

class EditorWindow:
    def __init__(self, parent, editor_type, db, project=None):
        self.parent = parent
        self.editor_type = editor_type
        self.db = db
        self.project = project
        
        # Create new window
        self.window = ctk.CTkToplevel(parent)
        self.window.title(self.get_window_title())
        self.window.geometry("900x700")
        
        # Initialize generators
        self.plot_gen = PlotGenerator()
        self.char_gen = CharacterGenerator()
        self.world_gen = WorldbuildingGenerator()
        self.dialogue_gen = DialogueGenerator()
        self.scene_gen = SceneGenerator()
        self.scenario_gen = ScenarioGenerator()
        self.synopsis_gen = SynopsisGenerator()
        self.quest_gen = QuestGenerator()
        self.npc_gen = NPCGenerator()
        self.dungeon_gen = DungeonDesigner()
        self.title_gen = TitleGenerator()
        self.twist_gen = TwistGenerator()
        self.idea_gen = IdeaGenerator()
        
        # Create UI based on type
        self.create_editor_ui()
    
    def get_window_title(self):
        """Get window title based on editor type"""
        titles = {
            "plot": "플롯 생성",
            "character": "캐릭터 생성",
            "worldbuilding": "세계관 구축",
            "dialogue": "대화 생성",
            "scene": "장면 묘사",
            "power": "파워 시스템",
            "movie": "영화 시나리오",
            "drama": "드라마 시놉시스",
            "webtoon": "웹툰 스토리보드",
            "quest": "퀘스트 생성",
            "npc": "NPC 생성",
            "dungeon": "던전 디자인",
            "trpg": "TRPG 도구",
            "idea": "아이디어 생성",
            "title": "제목 생성",
            "twist": "플롯 트위스트"
        }
        return titles.get(self.editor_type, "편집기")
    
    def create_editor_ui(self):
        """Create editor UI based on type"""
        # Title
        title = ctk.CTkLabel(
            self.window,
            text=self.get_window_title(),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)
        
        # Input frame
        input_frame = ctk.CTkFrame(self.window)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        # Create inputs based on type
        self.create_inputs(input_frame)
        
        # Generate button
        generate_btn = ctk.CTkButton(
            self.window,
            text="생성",
            command=self.generate_content,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        generate_btn.pack(pady=10)
        
        # Output frame (scrollable)
        self.output_text = ctk.CTkTextbox(self.window, width=850, height=400)
        self.output_text.pack(padx=20, pady=10)
        
        # Action buttons
        action_frame = ctk.CTkFrame(self.window)
        action_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            action_frame,
            text="저장",
            command=self.save_content,
            width=100
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            action_frame,
            text="내보내기",
            command=self.export_content,
            width=100
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            action_frame,
            text="닫기",
            command=self.window.destroy,
            width=100
        ).pack(side="right", padx=5)
    
    def create_inputs(self, parent):
        """Create input fields based on editor type"""
        if self.editor_type == "plot":
            self.create_plot_inputs(parent)
        elif self.editor_type == "character":
            self.create_character_inputs(parent)
        elif self.editor_type == "worldbuilding":
            self.create_worldbuilding_inputs(parent)
        elif self.editor_type == "dialogue":
            self.create_dialogue_inputs(parent)
        elif self.editor_type == "scene":
            self.create_scene_inputs(parent)
        elif self.editor_type == "power":
            self.create_power_inputs(parent)
        elif self.editor_type in ["movie", "drama", "webtoon"]:
            self.create_scenario_inputs(parent)
        elif self.editor_type in ["quest", "npc", "dungeon", "trpg"]:
            self.create_game_inputs(parent)
        elif self.editor_type in ["idea", "title", "twist"]:
            self.create_idea_inputs(parent)
    
    def create_plot_inputs(self, parent):
        """Create plot generation inputs"""
        ctk.CTkLabel(parent, text="장르:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        self.genre_var = ctk.StringVar(value="판타지")
        ctk.CTkOptionMenu(
            parent,
            values=["판타지", "로맨스", "무협", "현대물", "SF"],
            variable=self.genre_var
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="주제 (선택):", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        self.theme_entry = ctk.CTkEntry(parent, placeholder_text="예: 용사의 귀환")
        self.theme_entry.pack(fill="x", padx=10, pady=5)
    
    def create_character_inputs(self, parent):
        """Create character generation inputs"""
        ctk.CTkLabel(parent, text="이름 형식:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        self.name_type_var = ctk.StringVar(value="한국어")
        ctk.CTkOptionMenu(
            parent,
            values=["한국어", "판타지", "영어"],
            variable=self.name_type_var
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="성별:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        self.gender_var = ctk.StringVar(value="남성")
        ctk.CTkOptionMenu(
            parent,
            values=["남성", "여성"],
            variable=self.gender_var
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="나이:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        self.age_var = ctk.StringVar(value="25")
        ctk.CTkEntry(parent, textvariable=self.age_var).pack(fill="x", padx=10, pady=5)
    
    def create_worldbuilding_inputs(self, parent):
        """Create worldbuilding inputs"""
        ctk.CTkLabel(parent, text="세계관 타입:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        self.world_type_var = ctk.StringVar(value="판타지")
        ctk.CTkOptionMenu(
            parent,
            values=["판타지", "SF"],
            variable=self.world_type_var
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="세계 이름:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        self.world_name_entry = ctk.CTkEntry(parent, placeholder_text="예: 아르카디아")
        self.world_name_entry.pack(fill="x", padx=10, pady=5)
    
    def create_dialogue_inputs(self, parent):
        """Create dialogue generation inputs"""
        ctk.CTkLabel(parent, text="상황:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        self.situation_var = ctk.StringVar(value="일상")
        ctk.CTkOptionMenu(
            parent,
            values=["일상", "전투", "로맨스", "긴장"],
            variable=self.situation_var
        ).pack(fill="x", padx=10, pady=5)
    
    def create_scene_inputs(self, parent):
        """Create scene generation inputs"""
        ctk.CTkLabel(parent, text="장면 유형:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        self.scene_type_var = ctk.StringVar(value="전투")
        ctk.CTkOptionMenu(
            parent,
            values=["전투", "로맨스", "일상", "긴장", "감동"],
            variable=self.scene_type_var
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="분위기:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        self.atmosphere_var = ctk.StringVar(value="긴장")
        ctk.CTkOptionMenu(
            parent,
            values=["긴장", "평화", "공포", "설렘", "슬픔"],
            variable=self.atmosphere_var
        ).pack(fill="x", padx=10, pady=5)
    
    def create_power_inputs(self, parent):
        """Create power system inputs"""
        ctk.CTkLabel(parent, text="파워 시스템:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        self.power_type_var = ctk.StringVar(value="헌터")
        ctk.CTkOptionMenu(
            parent,
            values=["헌터", "무공", "초능력"],
            variable=self.power_type_var
        ).pack(fill="x", padx=10, pady=5)
    
    def create_scenario_inputs(self, parent):
        """Create scenario inputs"""
        if self.editor_type == "movie":
            ctk.CTkLabel(parent, text="장르:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
            self.movie_genre_var = ctk.StringVar(value="액션")
            ctk.CTkOptionMenu(
                parent,
                values=["액션", "로맨스", "스릴러", "SF"],
                variable=self.movie_genre_var
            ).pack(fill="x", padx=10, pady=5)
        elif self.editor_type == "drama":
            ctk.CTkLabel(parent, text="회차 수:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
            self.episodes_var = ctk.StringVar(value="16")
            ctk.CTkEntry(parent, textvariable=self.episodes_var).pack(fill="x", padx=10, pady=5)
    
    def create_game_inputs(self, parent):
        """Create game inputs"""
        if self.editor_type == "quest":
            ctk.CTkLabel(parent, text="레벨:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
            self.level_var = ctk.StringVar(value="1")
            ctk.CTkEntry(parent, textvariable=self.level_var).pack(fill="x", padx=10, pady=5)
        elif self.editor_type == "dungeon":
            ctk.CTkLabel(parent, text="던전 이름:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
            self.dungeon_name_entry = ctk.CTkEntry(parent, placeholder_text="예: 어둠의 던전")
            self.dungeon_name_entry.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(parent, text="층수:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
            self.floors_var = ctk.StringVar(value="5")
            ctk.CTkEntry(parent, textvariable=self.floors_var).pack(fill="x", padx=10, pady=5)
    
    def create_idea_inputs(self, parent):
        """Create idea generation inputs"""
        if self.editor_type == "title":
            ctk.CTkLabel(parent, text="장르:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
            self.title_genre_var = ctk.StringVar(value="판타지")
            ctk.CTkOptionMenu(
                parent,
                values=["판타지", "로맨스"],
                variable=self.title_genre_var
            ).pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(parent, text="개수:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
            self.title_count_var = ctk.StringVar(value="5")
            ctk.CTkEntry(parent, textvariable=self.title_count_var).pack(fill="x", padx=10, pady=5)
    
    def generate_content(self):
        """Generate content based on editor type"""
        try:
            result = ""
            
            if self.editor_type == "plot":
                genre = self.genre_var.get()
                theme = self.theme_entry.get() if self.theme_entry.get() else None
                plot = self.plot_gen.generate_plot(genre, theme)
                result = self.format_plot(plot)
            
            elif self.editor_type == "character":
                name_type = self.name_type_var.get()
                gender = self.gender_var.get()
                age = int(self.age_var.get())
                character = self.char_gen.generate_character(name_type, gender, age)
                result = self.format_character(character)
            
            elif self.editor_type == "worldbuilding":
                world_type = self.world_type_var.get()
                world_name = self.world_name_entry.get() if self.world_name_entry.get() else "신세계"
                if world_type == "판타지":
                    world = self.world_gen.generate_fantasy_world(world_name)
                else:
                    world = self.world_gen.generate_sf_world(world_name)
                result = self.format_world(world)
            
            elif self.editor_type == "dialogue":
                situation = self.situation_var.get()
                # Create a dummy character for dialogue generation
                dummy_char = {"name": "캐릭터", "personality": {"traits": ["친근한"]}}
                dialogue = self.dialogue_gen.generate_dialogue(dummy_char, situation)
                result = self.format_dialogue(dialogue)
            
            elif self.editor_type == "scene":
                scene_type = self.scene_type_var.get()
                atmosphere = self.atmosphere_var.get()
                scene = self.scene_gen.generate_scene(scene_type, atmosphere)
                result = self.format_scene(scene)
            
            elif self.editor_type == "power":
                power_type = self.power_type_var.get()
                power = self.world_gen.generate_power_system(power_type)
                result = self.format_power(power)
            
            elif self.editor_type == "movie":
                genre = self.movie_genre_var.get()
                scenario = self.scenario_gen.generate_movie_scenario(genre)
                result = self.format_scenario(scenario)
            
            elif self.editor_type == "drama":
                episodes = int(self.episodes_var.get())
                synopsis = self.scenario_gen.generate_drama_synopsis(episodes)
                result = self.format_synopsis(synopsis)
            
            elif self.editor_type == "webtoon":
                storyboard = self.scenario_gen.generate_webtoon_storyboard()
                result = self.format_storyboard(storyboard)
            
            elif self.editor_type == "quest":
                level = int(self.level_var.get())
                quest = self.quest_gen.generate_main_quest(level)
                result = self.format_quest(quest)
            
            elif self.editor_type == "npc":
                npc = self.npc_gen.generate_npc()
                result = self.format_npc(npc)
            
            elif self.editor_type == "dungeon":
                name = self.dungeon_name_entry.get() if self.dungeon_name_entry.get() else "Unknown"
                floors = int(self.floors_var.get())
                dungeon = self.dungeon_gen.generate_dungeon(name, floors)
                result = self.format_dungeon(dungeon)
            
            elif self.editor_type == "trpg":
                table = self.dungeon_gen.generate_random_encounter_table()
                result = self.format_encounter_table(table)
            
            elif self.editor_type == "idea":
                idea = self.idea_gen.generate_random_idea()
                result = self.format_idea(idea)
            
            elif self.editor_type == "title":
                genre = self.title_genre_var.get()
                count = int(self.title_count_var.get())
                titles = self.title_gen.generate_title(genre, count)
                result = self.format_titles(titles)
            
            elif self.editor_type == "twist":
                twist = self.twist_gen.generate_plot_twist()
                result = self.format_twist(twist)
            
            # Display result
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", result)
            
        except Exception as e:
            messagebox.showerror("오류", f"생성 중 오류 발생: {str(e)}")
    
    # Format functions
    def format_plot(self, plot):
        """Format plot for display"""
        text = f"장르: {plot['genre']}\n"
        text += f"주제: {plot['theme']}\n"
        text += f"배경: {plot['setting']}\n"
        text += f"갈등: {plot['conflict']}\n\n"
        
        for act, data in plot['structure'].items():
            text += f"\n=== {data['title']} ===\n"
            text += "\n장면:\n"
            for scene in data['scenes']:
                text += f"  - {scene}\n"
            text += "\n핵심 포인트:\n"
            for point in data['key_points']:
                text += f"  - {point}\n"
        
        text += f"\n\n복선:\n{plot['foreshadowing']}\n"
        text += f"\n플롯 트위스트:\n{plot['plot_twist']}\n"
        
        return text
    
    def format_character(self, char):
        """Format character for display"""
        text = f"이름: {char['name']}\n"
        text += f"성별: {char['gender']}\n"
        text += f"나이: {char['age']}\n\n"
        
        text += f"성격:\n"
        text += f"  MBTI: {char['personality']['mbti']} ({char['personality']['type']})\n"
        text += f"  특성: {', '.join(char['personality']['traits'])}\n"
        text += f"  강점: {', '.join(char['personality']['strengths'])}\n"
        text += f"  약점: {', '.join(char['personality']['weaknesses'])}\n\n"
        
        text += f"외모:\n  {char['appearance']['description']}\n\n"
        text += f"배경:\n  {char['background']}\n\n"
        
        text += f"능력:\n"
        for ability in char['abilities']:
            text += f"  - {ability['name']} ({ability['level']})\n"
        
        return text
    
    def format_world(self, world):
        """Format world for display"""
        text = f"세계명: {world['name']}\n"
        text += f"타입: {world['type']}\n\n"
        
        if world['type'] == "판타지":
            text += f"마법 시스템:\n{world['magic_system']['description']}\n"
        else:
            text += f"기술 수준: {world['tech_level']['description']}\n"
        
        return text
    
    def format_dialogue(self, dialogue):
        """Format dialogue for display"""
        text = f"{dialogue['speaker']}: \"{dialogue['dialogue']}\"\n"
        text += f"감정: {dialogue['emotion']}\n"
        text += f"동작: {dialogue['action']}\n"
        return text
    
    def format_scene(self, scene):
        """Format scene for display"""
        text = f"장면 유형: {scene['type']}\n"
        text += f"분위기: {scene['atmosphere']}\n\n"
        text += f"{scene['description']}\n\n"
        text += f"액션 시퀀스:\n"
        for action in scene['action']:
            text += f"  {action}\n"
        return text
    
    def format_power(self, power):
        """Format power system for display"""
        text = f"파워 시스템: {power['type']}\n\n"
        text += f"등급: {', '.join(power['ranks'])}\n"
        text += f"유형: {', '.join(power['types'])}\n"
        text += f"스탯: {', '.join(power['stats'])}\n\n"
        text += f"성장 시스템:\n{json.dumps(power['growth'], indent=2, ensure_ascii=False)}\n"
        return text
    
    def format_scenario(self, scenario):
        """Format scenario for display"""
        text = f"제목: {scenario['title']}\n"
        text += f"장르: {scenario['genre']}\n"
        text += f"러닝타임: {scenario['duration']}\n\n"
        text += "시나리오 구조가 생성되었습니다.\n"
        return text
    
    def format_synopsis(self, synopsis):
        """Format synopsis for display"""
        text = f"제목: {synopsis['title']}\n"
        text += f"장르: {synopsis['genre']}\n"
        text += f"회차: {synopsis['episodes']}부작\n\n"
        text += f"메인 플롯: {synopsis['main_plot']}\n"
        return text
    
    def format_storyboard(self, storyboard):
        """Format storyboard for display"""
        text = f"{storyboard['episode']}화: {storyboard['title']}\n"
        text += f"총 {len(storyboard['cuts'])}컷\n"
        return text
    
    def format_quest(self, quest):
        """Format quest for display"""
        text = f"퀘스트명: {quest['name']}\n"
        text += f"타입: {quest['type']}\n"
        text += f"레벨: {quest['level']}\n\n"
        text += f"설명: {quest['description']}\n\n"
        text += f"목표:\n"
        for obj in quest['objectives']:
            text += f"  - {obj}\n"
        text += f"\n보상:\n"
        text += f"  경험치: {quest['rewards']['exp']}\n"
        text += f"  골드: {quest['rewards']['gold']}\n"
        return text
    
    def format_npc(self, npc):
        """Format NPC for display"""
        text = f"이름: {npc['name']}\n"
        text += f"직업: {npc['type']}\n"
        text += f"나이: {npc['age']}\n"
        text += f"성격: {npc['personality']}\n"
        return text
    
    def format_dungeon(self, dungeon):
        """Format dungeon for display"""
        text = f"던전명: {dungeon['name']}\n"
        text += f"타입: {dungeon['type']}\n"
        text += f"층수: {dungeon['floors']}\n"
        text += f"난이도: {dungeon['difficulty']}\n\n"
        text += f"설명: {dungeon['description']}\n"
        return text
    
    def format_encounter_table(self, table):
        """Format encounter table for display"""
        text = "랜덤 조우 테이블 (d20)\n\n"
        for encounter in table:
            text += f"{encounter['roll']:2d}. {encounter['description']}\n"
        return text
    
    def format_idea(self, idea):
        """Format idea for display"""
        text = f"컨셉: {idea['concept']}\n\n"
        text += f"테마: {', '.join(idea['themes'])}\n"
        text += f"세팅: {', '.join(idea['settings'])}\n"
        text += f"주인공: {idea['protagonist']}\n\n"
        text += f"훅: {idea['hook']}\n"
        text += f"차별화 포인트: {idea['unique_point']}\n"
        return text
    
    def format_titles(self, titles):
        """Format titles for display"""
        text = "생성된 제목들:\n\n"
        for i, title in enumerate(titles, 1):
            text += f"{i}. {title}\n"
        return text
    
    def format_twist(self, twist):
        """Format twist for display"""
        text = f"반전 유형: {twist['type']}\n\n"
        text += f"반전 내용:\n{twist['twist']}\n\n"
        text += f"복선:\n"
        for f in twist['foreshadowing']:
            text += f"  - {f}\n"
        text += f"\n{twist['reveal_scene']}\n"
        return text
    
    def save_content(self):
        """Save content to database"""
        content = self.output_text.get("1.0", "end")
        
        if not content.strip():
            messagebox.showwarning("경고", "저장할 내용이 없습니다.")
            return
        
        # Simple save dialog
        name = ctk.CTkInputDialog(
            text="프로젝트 이름을 입력하세요:",
            title="저장"
        ).get_input()
        
        if name:
            try:
                self.db.save_project(name, self.editor_type, {"content": content})
                messagebox.showinfo("성공", "저장되었습니다.")
            except Exception as e:
                messagebox.showerror("오류", f"저장 실패: {str(e)}")
    
    def export_content(self):
        """Export content to file"""
        content = self.output_text.get("1.0", "end")
        
        if not content.strip():
            messagebox.showwarning("경고", "내보낼 내용이 없습니다.")
            return
        
        # Ask for file location
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("성공", "파일이 내보내졌습니다.")
            except Exception as e:
                messagebox.showerror("오류", f"내보내기 실패: {str(e)}")
