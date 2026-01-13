import random

class ScenarioGenerator:
    def __init__(self):
        self.scenario_types = ["영화", "드라마", "웹툰", "애니메이션"]
        
    def generate_movie_scenario(self, genre="액션", duration=120):
        """Generate movie scenario (3-act structure)"""
        scenes_count = duration // 5  # 5 minutes per scene average
        
        act1_scenes = scenes_count // 4
        act2_scenes = scenes_count // 2
        act3_scenes = scenes_count // 4
        
        scenario = {
            "title": self._generate_movie_title(genre),
            "genre": genre,
            "duration": f"{duration}분",
            "structure": "3막 구조",
            "acts": {
                "act1": self._generate_act_scenes(1, act1_scenes, genre),
                "act2": self._generate_act_scenes(2, act2_scenes, genre),
                "act3": self._generate_act_scenes(3, act3_scenes, genre)
            }
        }
        
        return scenario
    
    def _generate_movie_title(self, genre):
        """Generate movie title"""
        titles = {
            "액션": ["최후의 전투", "레드 미션", "다크 솔져"],
            "로맨스": ["봄날의 약속", "운명의 두 사람", "사랑의 시간"],
            "스릴러": ["침묵의 목격자", "7일간의 추격", "미스터리 코드"],
            "SF": ["2099: 미래 전쟁", "스타 오디세이", "네오 제네시스"]
        }
        return random.choice(titles.get(genre, ["무제"]))
    
    def _generate_act_scenes(self, act_number, scene_count, genre):
        """Generate scenes for an act"""
        scenes = []
        
        for i in range(scene_count):
            scene = {
                "scene_number": i + 1,
                "location": self._get_location(genre),
                "time": random.choice(["낮", "밤", "새벽", "저녁"]),
                "description": self._generate_scene_description(act_number, genre),
                "camera_angles": self._suggest_camera_angles(),
                "dialogue": "대사는 여기에..."
            }
            scenes.append(scene)
        
        return scenes
    
    def _get_location(self, genre):
        """Get location based on genre"""
        locations = {
            "액션": ["빌딩 옥상", "도심 거리", "비밀 기지", "공장"],
            "로맨스": ["카페", "공원", "집", "해변"],
            "스릴러": ["어두운 골목", "폐건물", "경찰서", "병원"],
            "SF": ["우주선 내부", "연구소", "미래 도시", "사이버 공간"]
        }
        return random.choice(locations.get(genre, ["실내"]))
    
    def _generate_scene_description(self, act, genre):
        """Generate scene description"""
        if act == 1:
            return "주인공 등장 및 일상 묘사. 사건의 발단."
        elif act == 2:
            return "갈등 심화. 주인공의 시련과 성장."
        else:
            return "클라이맥스. 최종 대결 및 해결."
    
    def _suggest_camera_angles(self):
        """Suggest camera angles"""
        angles = ["클로즈업", "미디엄 샷", "롱 샷", "버드 아이 뷰", "오버 더 숄더"]
        return random.sample(angles, 2)
    
    def generate_drama_synopsis(self, episodes=16):
        """Generate drama synopsis"""
        synopsis = {
            "title": "운명의 시간",
            "genre": "로맨스 멜로",
            "episodes": episodes,
            "main_plot": "재벌 2세와 평범한 회사원의 운명적인 만남과 사랑",
            "sub_plots": [
                "가족 간의 갈등",
                "비즈니스 음모",
                "과거의 비밀"
            ],
            "characters": self._generate_drama_characters(),
            "episode_summaries": self._generate_episode_summaries(episodes)
        }
        
        return synopsis
    
    def _generate_drama_characters(self):
        """Generate drama characters"""
        return [
            {
                "name": "강민준",
                "role": "남자 주인공",
                "description": "재벌 2세, 냉정하지만 따뜻한 마음을 가짐"
            },
            {
                "name": "이서연",
                "role": "여자 주인공",
                "description": "평범한 회사원, 밝고 긍정적"
            },
            {
                "name": "박지훈",
                "role": "조연",
                "description": "민준의 라이벌, 서연을 좋아함"
            }
        ]
    
    def _generate_episode_summaries(self, episodes):
        """Generate episode summaries"""
        summaries = []
        
        for ep in range(1, episodes + 1):
            if ep <= 4:
                stage = "만남과 갈등"
            elif ep <= 8:
                stage = "사랑의 시작"
            elif ep <= 12:
                stage = "위기"
            else:
                stage = "해결과 결말"
            
            summaries.append({
                "episode": ep,
                "stage": stage,
                "summary": f"{ep}회: {stage} 단계의 주요 사건 전개"
            })
        
        return summaries
    
    def generate_webtoon_storyboard(self, episode_number=1):
        """Generate webtoon storyboard"""
        cuts_count = random.randint(40, 60)
        
        storyboard = {
            "episode": episode_number,
            "title": f"{episode_number}화 - 시작",
            "cuts": []
        }
        
        for cut in range(1, cuts_count + 1):
            cut_data = {
                "cut_number": cut,
                "description": self._generate_cut_description(cut, cuts_count),
                "dialogue": self._generate_webtoon_dialogue(),
                "sound_effects": random.choice(["쾅!", "휘익", "펑!", "드르륵", "콰당!", ""])
            }
            storyboard["cuts"].append(cut_data)
        
        return storyboard
    
    def _generate_cut_description(self, cut, total):
        """Generate cut description"""
        if cut <= 5:
            return "도입부: 배경 및 상황 설정"
        elif cut >= total - 5:
            return "결말: 클리프행어로 다음 화 기대감 조성"
        else:
            return "전개: 스토리 진행"
    
    def _generate_webtoon_dialogue(self):
        """Generate webtoon dialogue"""
        dialogues = [
            "이게 대체 무슨 일이야?!",
            "조심해!",
            "드디어... 찾았어.",
            "너는 누구지?",
            "이럴 수가..."
        ]
        return random.choice(dialogues)


class SynopsisGenerator:
    def __init__(self):
        self.genres = ["판타지", "로맨스", "스릴러", "SF", "드라마", "액션"]
    
    def generate_synopsis(self, genre="판타지", length="short"):
        """Generate story synopsis"""
        if length == "short":
            return self._generate_short_synopsis(genre)
        else:
            return self._generate_long_synopsis(genre)
    
    def _generate_short_synopsis(self, genre):
        """Generate short synopsis (1-2 paragraphs)"""
        templates = {
            "판타지": """
평범한 학생이었던 주인공이 어느 날 이세계로 소환된다.
그곳에서 전설의 용사로 선택받은 그는 마왕을 물리치기 위한 여정을 시작한다.
동료들과 함께 성장하며, 숨겨진 자신의 진정한 힘을 깨닫게 된다.
""",
            "로맨스": """
서로 다른 세계에 살던 두 사람이 우연히 만나게 된다.
처음에는 오해와 갈등으로 얽히지만, 점차 서로에게 끌리게 된다.
수많은 장애물을 넘어 결국 진정한 사랑을 찾게 되는 이야기.
""",
            "스릴러": """
연쇄 살인 사건을 추적하는 형사.
사건을 파헤칠수록 자신의 과거와 연결되어 있음을 발견한다.
범인과의 치열한 두뇌 싸움, 충격적인 진실이 밝혀진다.
"""
        }
        return templates.get(genre, templates["판타지"])
    
    def _generate_long_synopsis(self, genre):
        """Generate long synopsis (detailed)"""
        return {
            "장르": genre,
            "배경": "현대/판타지 세계관",
            "주인공": "평범한 대학생 김민준 (22세)",
            "사건": "어느 날 게임 세계에 빠지게 됨",
            "목표": "현실 세계로 돌아가기",
            "갈등": [
                "게임 세계의 마왕을 쓰러뜨려야 함",
                "현실로 돌아가면 게임 속 동료들이 사라짐",
                "선택의 기로에 놓임"
            ],
            "클라이맥스": "마왕과의 최종 결전",
            "결말": "두 세계를 연결하는 방법을 찾음",
            "메시지": "진정한 용기와 우정의 가치"
        }
    
    def generate_character_relationship_chart(self, characters):
        """Generate character relationship chart"""
        chart = {
            "title": "인물 관계도",
            "relationships": []
        }
        
        for i, char1 in enumerate(characters):
            for j, char2 in enumerate(characters):
                if i < j:
                    relationship = random.choice([
                        "친구", "연인", "적", "라이벌", 
                        "스승-제자", "가족", "동료"
                    ])
                    chart["relationships"].append({
                        "from": char1["name"],
                        "to": char2["name"],
                        "type": relationship
                    })
        
        return chart
