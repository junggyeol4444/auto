import random

class QuestGenerator:
    def __init__(self):
        self.quest_types = ["메인 퀘스트", "서브 퀘스트", "히든 퀘스트", "반복 퀘스트"]
        
    def generate_main_quest(self, level=1):
        """Generate main quest"""
        quest = {
            "type": "메인 퀘스트",
            "name": self._generate_quest_name(level),
            "level": level,
            "description": self._generate_quest_description(level),
            "objectives": self._generate_objectives(level),
            "rewards": self._generate_rewards(level, "main"),
            "story": self._generate_quest_story(level)
        }
        
        return quest
    
    def _generate_quest_name(self, level):
        """Generate quest name"""
        quest_names = {
            1: ["첫 번째 시련", "초보자의 도전", "시작의 여정"],
            5: ["던전의 비밀", "잃어버린 유물", "어둠의 그림자"],
            10: ["드래곤의 보물", "고대의 성역", "금단의 마법"],
            20: ["마왕의 부활", "최후의 전투", "운명의 결전"]
        }
        
        level_bracket = (level // 5) * 5
        if level_bracket > 20:
            level_bracket = 20
        
        names = quest_names.get(level_bracket, quest_names[1])
        return random.choice(names)
    
    def _generate_quest_description(self, level):
        """Generate quest description"""
        descriptions = [
            f"레벨 {level} 이상의 모험가를 찾습니다.",
            "위험한 임무이지만, 그만큼 보상도 풍성합니다.",
            "이 의뢰를 완수하면 당신의 명성이 높아질 것입니다."
        ]
        return " ".join(descriptions)
    
    def _generate_objectives(self, level):
        """Generate quest objectives"""
        objective_types = [
            f"몬스터 처치: 고블린 {level * 10}마리 처치",
            f"아이템 수집: 마법석 {level * 5}개 수집",
            f"NPC 호위: 상인을 목적지까지 안전하게 호위",
            f"던전 탐험: {level}층 던전 클리어",
            f"보스 처치: 던전 보스 처치"
        ]
        
        return random.sample(objective_types, min(3, len(objective_types)))
    
    def _generate_rewards(self, level, quest_type="main"):
        """Generate quest rewards"""
        multiplier = 2 if quest_type == "main" else 1
        
        return {
            "exp": level * 1000 * multiplier,
            "gold": level * 500 * multiplier,
            "items": self._generate_reward_items(level, quest_type)
        }
    
    def _generate_reward_items(self, level, quest_type):
        """Generate reward items"""
        items = []
        
        if quest_type == "main":
            items.append({
                "name": f"전설의 {random.choice(['검', '갑옷', '방패', '반지'])}",
                "grade": "전설",
                "level": level
            })
        
        items.append({
            "name": f"고급 {random.choice(['포션', '마법석', '강화석'])}",
            "grade": "고급",
            "quantity": random.randint(5, 10)
        })
        
        return items
    
    def _generate_quest_story(self, level):
        """Generate quest story/lore"""
        stories = [
            "오래전부터 전해 내려오는 전설이 있습니다...",
            "마을에 위기가 찾아왔습니다. 당신의 도움이 필요합니다.",
            "고대 유적에서 이상한 기운이 감지되었습니다.",
            "마왕군이 움직이기 시작했습니다. 서둘러야 합니다."
        ]
        return random.choice(stories)
    
    def generate_side_quest(self, level=1):
        """Generate side quest"""
        quest = {
            "type": "서브 퀘스트",
            "name": random.choice(["잃어버린 고양이", "마을의 문제", "소소한 부탁"]),
            "level": level,
            "description": "간단한 의뢰입니다.",
            "objectives": [random.choice([
                "잃어버린 물건 찾기",
                "NPC와 대화하기",
                "몬스터 5마리 처치"
            ])],
            "rewards": self._generate_rewards(level, "side")
        }
        
        return quest


class NPCGenerator:
    def __init__(self):
        self.npc_types = ["상인", "기사", "마법사", "농부", "대장장이", "여관 주인", "퀘스트 제공자"]
        
    def generate_npc(self, npc_type=None):
        """Generate NPC"""
        if not npc_type or npc_type not in self.npc_types:
            npc_type = random.choice(self.npc_types)
        
        npc = {
            "name": self._generate_npc_name(),
            "type": npc_type,
            "age": random.randint(20, 60),
            "personality": random.choice(["친절함", "무뚝뚝함", "유쾌함", "신중함", "수상함"]),
            "dialogue": self._generate_npc_dialogue(npc_type),
            "quests": self._generate_npc_quests(npc_type),
            "shop_items": self._generate_shop_items() if npc_type == "상인" else None
        }
        
        return npc
    
    def _generate_npc_name(self):
        """Generate NPC name"""
        names = [
            "알렉산더", "엘리자베스", "토마스", "마리아",
            "김철수", "이영희", "박민수", "정서연"
        ]
        return random.choice(names)
    
    def _generate_npc_dialogue(self, npc_type):
        """Generate NPC dialogue"""
        dialogues = {
            "상인": {
                "greeting": "어서오세요! 좋은 물건들이 많답니다!",
                "buy": "좋은 선택이십니다!",
                "sell": "이 정도면 되겠습니까?",
                "farewell": "또 오세요!"
            },
            "기사": {
                "greeting": "안녕하시오, 모험가님.",
                "quest": "부탁이 하나 있소.",
                "complete": "잘 해주었소!",
                "farewell": "무운을 빕니다."
            },
            "default": {
                "greeting": "안녕하세요.",
                "chat": "날씨가 좋네요.",
                "farewell": "안녕히 가세요."
            }
        }
        
        return dialogues.get(npc_type, dialogues["default"])
    
    def _generate_npc_quests(self, npc_type):
        """Generate quests that NPC offers"""
        if npc_type in ["기사", "마법사", "퀘스트 제공자"]:
            return [f"{npc_type}의 의뢰 #{i}" for i in range(1, random.randint(2, 4))]
        return []
    
    def _generate_shop_items(self):
        """Generate shop items"""
        items = []
        for i in range(random.randint(5, 15)):
            items.append({
                "name": random.choice(["포션", "무기", "방어구", "장신구", "소모품"]),
                "price": random.randint(100, 10000),
                "stock": random.randint(1, 99)
            })
        return items


class DungeonDesigner:
    def __init__(self):
        self.dungeon_types = ["동굴", "성", "유적", "숲", "지하", "차원"]
        
    def generate_dungeon(self, name="Unknown", floors=5):
        """Generate dungeon"""
        dungeon = {
            "name": name,
            "type": random.choice(self.dungeon_types),
            "floors": floors,
            "difficulty": self._calculate_difficulty(floors),
            "description": self._generate_dungeon_description(),
            "floor_details": [self._generate_floor(i) for i in range(1, floors + 1)],
            "boss": self._generate_boss(floors)
        }
        
        return dungeon
    
    def _calculate_difficulty(self, floors):
        """Calculate dungeon difficulty"""
        if floors <= 3:
            return "하급"
        elif floors <= 7:
            return "중급"
        elif floors <= 10:
            return "상급"
        else:
            return "최상급"
    
    def _generate_dungeon_description(self):
        """Generate dungeon description"""
        descriptions = [
            "어둡고 음산한 분위기의 던전. 위험이 도사리고 있다.",
            "고대의 비밀이 숨겨진 신비로운 장소.",
            "강력한 몬스터들이 서식하는 위험 지역.",
            "전설의 보물이 잠들어 있다는 던전."
        ]
        return random.choice(descriptions)
    
    def _generate_floor(self, floor_num):
        """Generate floor details"""
        floor = {
            "floor": floor_num,
            "layout": self._generate_floor_layout(),
            "monsters": self._generate_monsters(floor_num),
            "traps": self._generate_traps(),
            "treasures": self._generate_treasures(floor_num),
            "puzzle": self._generate_puzzle() if random.random() > 0.7 else None
        }
        
        return floor
    
    def _generate_floor_layout(self):
        """Generate floor layout (text-based)"""
        layouts = [
            "직선형 복도",
            "미로형 구조",
            "여러 방으로 나뉜 구조",
            "원형 대홀",
            "분기형 통로"
        ]
        return random.choice(layouts)
    
    def _generate_monsters(self, floor):
        """Generate monsters for floor"""
        monsters = [
            {"name": "고블린", "level": floor, "count": random.randint(3, 8)},
            {"name": "오크", "level": floor + 2, "count": random.randint(2, 5)},
            {"name": "스켈레톤", "level": floor + 1, "count": random.randint(3, 6)}
        ]
        return random.sample(monsters, random.randint(1, 3))
    
    def _generate_traps(self):
        """Generate traps"""
        trap_types = ["화염 함정", "낙석 함정", "독침 함정", "낙하 함정", "마법 함정"]
        return random.sample(trap_types, random.randint(0, 3))
    
    def _generate_treasures(self, floor):
        """Generate treasures"""
        treasures = [
            {"type": "상자", "grade": random.choice(["일반", "고급", "희귀"]), "gold": floor * 100},
            {"type": "아이템", "name": f"레벨 {floor} 장비"}
        ]
        return treasures
    
    def _generate_puzzle(self):
        """Generate puzzle"""
        puzzles = [
            "순서대로 레버를 당기기",
            "올바른 문 선택하기",
            "암호 해독하기",
            "퍼즐 조각 맞추기"
        ]
        return random.choice(puzzles)
    
    def _generate_boss(self, floors):
        """Generate dungeon boss"""
        boss_names = ["드래곤", "리치", "데몬", "거대 골렘", "어둠의 기사"]
        
        boss = {
            "name": random.choice(boss_names),
            "level": floors * 5,
            "hp": floors * 10000,
            "skills": [
                "강력한 공격",
                "광역 마법",
                "부하 소환",
                "버프/디버프"
            ],
            "drop_items": [
                {"name": "보스 전용 장비", "grade": "전설"},
                {"name": "희귀 재료", "quantity": random.randint(5, 10)}
            ]
        }
        
        return boss
    
    def generate_random_encounter_table(self):
        """Generate random encounter table for TRPG"""
        encounters = []
        
        for i in range(1, 21):  # d20 table
            encounter_type = random.choice(["몬스터", "NPC", "이벤트", "함정", "보물"])
            
            if encounter_type == "몬스터":
                description = f"몬스터 조우: {random.choice(['고블린 무리', '오크 전사', '야생 늑대'])}"
            elif encounter_type == "NPC":
                description = f"NPC 조우: {random.choice(['여행 상인', '부상당한 모험가', '수상한 인물'])}"
            elif encounter_type == "이벤트":
                description = f"이벤트: {random.choice(['폭풍우', '신비한 빛', '이상한 소리'])}"
            elif encounter_type == "함정":
                description = f"함정: {random.choice(['낙석', '독침', '함정 구덩이'])}"
            else:
                description = f"보물: {random.choice(['보물 상자', '희귀 재료', '금화'])}"
            
            encounters.append({
                "roll": i,
                "type": encounter_type,
                "description": description
            })
        
        return encounters
