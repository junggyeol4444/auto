import random

class PlotGenerator:
    def __init__(self):
        self.genres = {
            "판타지": {
                "themes": ["용사의 귀환", "마왕 토벌", "던전 탐험", "마법사의 성장", "이계 전이"],
                "settings": ["중세 판타지", "현대 판타지", "게임 세계", "이세계"],
                "conflicts": ["선과 악의 대결", "권력 투쟁", "생존", "복수"]
            },
            "로맨스": {
                "themes": ["첫사랑", "재회", "금지된 사랑", "계약 결혼", "짝사랑"],
                "settings": ["학교", "회사", "왕궁", "현대 도시"],
                "conflicts": ["신분 차이", "오해", "삼각관계", "가족 반대"]
            },
            "무협": {
                "themes": ["복수", "무림맹주", "정파와 사파", "강호 제일"],
                "settings": ["무림", "강호", "중원", "비무대회"],
                "conflicts": ["복수", "문파 간 대립", "마교의 침입", "무공 탈취"]
            },
            "현대물": {
                "themes": ["성공", "역전", "재벌", "스타 탄생"],
                "settings": ["서울", "회사", "학교", "연예계"],
                "conflicts": ["빈부 격차", "경쟁", "배신", "사회 부조리"]
            },
            "SF": {
                "themes": ["우주 탐험", "AI 반란", "타임 패러독스", "외계 침공"],
                "settings": ["우주선", "미래 도시", "화성 기지", "사이버 세계"],
                "conflicts": ["인간 vs 기계", "시간 여행", "자원 전쟁", "외계 생명체"]
            }
        }
    
    def generate_plot(self, genre="판타지", custom_theme=None):
        """Generate a complete 3-act plot structure"""
        if genre not in self.genres:
            genre = "판타지"
        
        genre_data = self.genres[genre]
        theme = custom_theme if custom_theme else random.choice(genre_data["themes"])
        setting = random.choice(genre_data["settings"])
        conflict = random.choice(genre_data["conflicts"])
        
        plot = {
            "genre": genre,
            "theme": theme,
            "setting": setting,
            "conflict": conflict,
            "structure": self._generate_three_act_structure(theme, conflict),
            "foreshadowing": self._generate_foreshadowing(),
            "plot_twist": self._generate_plot_twist()
        }
        
        return plot
    
    def _generate_three_act_structure(self, theme, conflict):
        """Generate 3-act structure"""
        return {
            "act1": {
                "title": "1막 - 설정 (25%)",
                "scenes": [
                    "주인공 소개: 평범한 일상을 보내는 주인공의 모습",
                    f"배경 설정: {theme}와 관련된 세계관 소개",
                    "촉발 사건: 주인공의 삶을 바꿀 중대한 사건 발생",
                    "결심: 주인공이 모험/도전을 받아들이기로 결심"
                ],
                "key_points": [
                    "주인공의 평범한 일상",
                    "주인공의 성격과 약점 드러내기",
                    "사건의 씨앗 뿌리기"
                ]
            },
            "act2": {
                "title": "2막 - 갈등 (50%)",
                "scenes": [
                    f"문제 심화: {conflict}가 본격화됨",
                    "시련과 실패: 주인공이 여러 위기를 겪음",
                    "성장: 주인공이 능력을 키우고 변화함",
                    "중간 승리: 작은 성공을 거두지만...",
                    "최악의 순간: 모든 것이 무너지는 듯한 위기",
                    "각오: 주인공이 최후의 결전을 준비"
                ],
                "key_points": [
                    "주인공의 도전과 좌절",
                    "조력자와 적대자 등장",
                    "중간 반전 포인트",
                    "최저점에서의 깨달음"
                ]
            },
            "act3": {
                "title": "3막 - 해결 (25%)",
                "scenes": [
                    "최종 준비: 모든 것을 걸고 마지막 전투를 준비",
                    f"클라이맥스: {conflict}의 최종 대결",
                    "반전: 예상치 못한 진실이 밝혀짐",
                    "해결: 갈등이 해소되고 평화가 찾아옴",
                    "여운: 주인공의 변화와 새로운 시작"
                ],
                "key_points": [
                    "모든 복선의 회수",
                    "주인공의 최종 성장",
                    "카타르시스 제공",
                    "열린 결말 또는 완전한 해결"
                ]
            }
        }
    
    def _generate_foreshadowing(self):
        """Generate foreshadowing elements"""
        foreshadowing_types = [
            {
                "type": "정체 숨김",
                "act1": "조력자가 수상한 행동을 보임",
                "act2": "조력자의 과거에 대한 단서 발견",
                "act3": "조력자가 실은 적의 스파이였음이 밝혀짐"
            },
            {
                "type": "능력 각성",
                "act1": "주인공이 이상한 꿈을 꿈",
                "act2": "위기 상황에서 신비한 힘이 발현됨",
                "act3": "주인공의 진정한 정체가 드러남"
            },
            {
                "type": "숨겨진 진실",
                "act1": "오래된 예언이나 전설 언급",
                "act2": "예언과 현재 상황의 유사점 발견",
                "act3": "예언이 현실이 되어 결말을 좌우함"
            }
        ]
        return random.choice(foreshadowing_types)
    
    def _generate_plot_twist(self):
        """Generate plot twist ideas"""
        twists = [
            "주인공의 믿었던 스승이 실은 진짜 악당이었다",
            "주인공이 실은 예언의 선택받은 자가 아니라 저주받은 존재였다",
            "적대자가 실은 미래에서 온 주인공 자신이었다",
            "모든 사건이 주인공을 시험하기 위한 시뮬레이션이었다",
            "주인공이 구하려던 세계가 실은 가상 현실이었다",
            "죽은 줄 알았던 인물이 살아서 흑막으로 등장",
            "주인공의 능력이 실은 세계를 파괴할 수 있는 위험한 것"
        ]
        return random.choice(twists)
    
    def generate_episode_structure(self, total_episodes=50):
        """Generate episode-by-episode structure"""
        episodes = []
        
        # Act 1: Episodes 1-12 (24%)
        act1_count = int(total_episodes * 0.24)
        for i in range(1, act1_count + 1):
            episodes.append({
                "episode": i,
                "act": 1,
                "title": f"{i}화 - 시작",
                "content": "주인공 소개 및 일상" if i <= 3 else "사건 전개 및 갈등 시작",
                "cliffhanger": "다음 화를 기대하게 만드는 장면"
            })
        
        # Act 2: Episodes 13-37 (50%)
        act2_count = int(total_episodes * 0.50)
        for i in range(act1_count + 1, act1_count + act2_count + 1):
            episodes.append({
                "episode": i,
                "act": 2,
                "title": f"{i}화 - 시련",
                "content": "갈등 심화, 주인공 성장, 새로운 적 등장",
                "cliffhanger": "충격적인 반전이나 위기 상황"
            })
        
        # Act 3: Remaining episodes (26%)
        for i in range(act1_count + act2_count + 1, total_episodes + 1):
            episodes.append({
                "episode": i,
                "act": 3,
                "title": f"{i}화 - 결말",
                "content": "최종 결전 및 해결" if i < total_episodes else "대단원의 막",
                "cliffhanger": "여운을 남기는 마무리" if i == total_episodes else "긴장감 유지"
            })
        
        return episodes
