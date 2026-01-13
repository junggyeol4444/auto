import random

class TitleGenerator:
    def __init__(self):
        self.fantasy_patterns = [
            "{직업}인 내가 {사건}하게 되었다",
            "{특성} {주인공}의 {목표}",
            "{숫자} {명사} {동사}",
            "{장소}에서 {행동}",
            "{형용사} {명사}"
        ]
        
        self.romance_patterns = [
            "{관계}와 {관계}의 {감정}",
            "{수식어} {상황}",
            "{주인공}의 {감정} 일기",
            "{시간} {장소}에서"
        ]
        
        self.components = {
            "직업": ["평범한 학생", "최약 헌터", "망나니 귀족", "하급 마법사"],
            "사건": ["최강이 된", "회귀한", "용사가 된", "신이 된"],
            "특성": ["최강", "천재", "추방당한", "귀환한"],
            "주인공": ["검사", "마법사", "헌터", "용사"],
            "목표": ["귀환", "복수", "성장", "구원"],
            "숫자": ["100년 만의", "천 번째", "7일간의", "10년 후의"],
            "명사": ["귀환", "회귀", "전생", "각성", "복수"],
            "동사": ["시작되다", "깨어나다", "돌아오다", "부활하다"],
            "장소": ["던전", "이세계", "학원", "왕궁"],
            "행동": ["살아남기", "최강되기", "복수하기"],
            "형용사": ["전설의", "금단의", "잃어버린", "봉인된"],
            "관계": ["재벌", "비서", "왕자", "하녀", "의사", "환자"],
            "감정": ["사랑", "복수", "질투", "열정"],
            "수식어": ["달콤한", "위험한", "금지된", "운명적인"],
            "상황": ["만남", "사랑", "복수", "선택"],
            "시간": ["봄날", "여름밤", "가을", "겨울"]
        }
    
    def generate_title(self, genre="판타지", count=5):
        """Generate multiple titles"""
        titles = []
        
        if genre == "판타지":
            patterns = self.fantasy_patterns
        elif genre == "로맨스":
            patterns = self.romance_patterns
        else:
            patterns = self.fantasy_patterns
        
        for _ in range(count):
            pattern = random.choice(patterns)
            title = self._fill_pattern(pattern)
            titles.append(title)
        
        return titles
    
    def _fill_pattern(self, pattern):
        """Fill pattern with random components"""
        title = pattern
        
        for key, values in self.components.items():
            placeholder = "{" + key + "}"
            if placeholder in title:
                title = title.replace(placeholder, random.choice(values), 1)
        
        return title
    
    def generate_clickbait_title(self, genre="판타지"):
        """Generate clickbait-style titles"""
        clickbait_patterns = {
            "판타지": [
                "【충격】 {직업}이 {사건}!? 그 결과는?",
                "이것이 레전드... {특성} {주인공}의 {목표}",
                "[속보] {숫자} {동사}! 전세계가 경악!",
                "역대급 사건! {장소}에서 {행동}한 결과.txt"
            ],
            "로맨스": [
                "【19금?】{관계}와 {관계}의 {감정}적 {상황}",
                "실화인가...{수식어} {상황}의 전말",
                "{시간} {장소}에서 벌어진 충격적인 일"
            ]
        }
        
        patterns = clickbait_patterns.get(genre, clickbait_patterns["판타지"])
        pattern = random.choice(patterns)
        return self._fill_pattern(pattern)
    
    def generate_ab_test_titles(self, genre="판타지", concept=""):
        """Generate A/B test titles (multiple variations)"""
        base_titles = self.generate_title(genre, 3)
        clickbait = self.generate_clickbait_title(genre)
        
        return {
            "version_a": base_titles[0],
            "version_b": base_titles[1],
            "version_c": base_titles[2],
            "clickbait": clickbait,
            "recommendation": base_titles[0]  # First one as default recommendation
        }


class TwistGenerator:
    def __init__(self):
        self.twist_types = {
            "배신": [
                "믿었던 동료가 실은 적의 스파이였다",
                "스승이 실은 진짜 악당이었다",
                "연인이 복수를 위해 접근했다",
                "가장 친한 친구가 배후의 흑막이었다"
            ],
            "정체": [
                "주인공이 실은 예언의 선택받은 자였다",
                "평범한 인간이 아니라 신의 후예였다",
                "기억을 잃은 전 마왕이었다",
                "미래에서 온 타임 트래블러였다"
            ],
            "사실 반전": [
                "구하려던 세계가 실은 가상현실이었다",
                "적대자가 실은 미래의 주인공 자신이었다",
                "모든 사건이 주인공을 시험하기 위한 것이었다",
                "죽은 줄 알았던 인물이 살아있었다"
            ],
            "능력": [
                "주인공의 약점이 실은 최강의 능력이었다",
                "봉인된 힘이 깨어났다",
                "숨겨진 혈통이 각성했다",
                "저주받은 능력이 실은 축복이었다"
            ],
            "세계관": [
                "세계가 실은 누군가의 창조물이었다",
                "반복되는 시간 루프였다",
                "다중 우주의 하나였다",
                "시뮬레이션 속 세계였다"
            ]
        }
    
    def generate_plot_twist(self, twist_type=None):
        """Generate plot twist"""
        if not twist_type or twist_type not in self.twist_types:
            twist_type = random.choice(list(self.twist_types.keys()))
        
        twist = random.choice(self.twist_types[twist_type])
        
        return {
            "type": twist_type,
            "twist": twist,
            "foreshadowing": self._generate_foreshadowing(twist),
            "reveal_scene": self._generate_reveal_scene(twist)
        }
    
    def _generate_foreshadowing(self, twist):
        """Generate foreshadowing for the twist"""
        return [
            "1막: 미묘한 힌트를 배치 (독자가 알아차리기 어려운 수준)",
            "2막: 조금 더 명확한 단서 제공 (의심을 품게 만듦)",
            "3막: 모든 복선이 하나로 연결되며 진실이 밝혀짐"
        ]
    
    def _generate_reveal_scene(self, twist):
        """Generate reveal scene for the twist"""
        return f"""
[반전 장면]
긴장감 넘치는 순간, 충격적인 진실이 밝혀진다.
"{twist}"
모든 것이 이해되는 순간, 주인공은 경악을 금치 못한다.
독자들도 함께 놀라게 될 반전 포인트.
"""
    
    def generate_multiple_twists(self, count=3):
        """Generate multiple twist ideas"""
        twists = []
        types = list(self.twist_types.keys())
        
        for _ in range(min(count, len(types))):
            twist_type = random.choice(types)
            types.remove(twist_type)  # Avoid duplicate types
            twists.append(self.generate_plot_twist(twist_type))
        
        return twists


class IdeaGenerator:
    def __init__(self):
        self.themes = ["복수", "성장", "사랑", "우정", "배신", "희생", "구원", "자유"]
        self.settings = ["회귀", "게임", "학원", "현대", "판타지", "SF", "무협", "이세계"]
        self.protagonists = ["평범한 학생", "천재", "낙오자", "귀족", "서민", "헌터", "마법사"]
        
    def generate_random_idea(self):
        """Generate completely random story idea"""
        theme = random.choice(self.themes)
        setting1 = random.choice(self.settings)
        setting2 = random.choice([s for s in self.settings if s != setting1])
        protagonist = random.choice(self.protagonists)
        
        idea = {
            "concept": f"{protagonist}이(가) {setting1} + {setting2} 세계에서 {theme}을(를) 이루는 이야기",
            "themes": [theme, random.choice(self.themes)],
            "settings": [setting1, setting2],
            "protagonist": protagonist,
            "hook": self._generate_hook(protagonist, setting1, theme),
            "unique_point": self._generate_unique_point()
        }
        
        return idea
    
    def _generate_hook(self, protagonist, setting, theme):
        """Generate story hook"""
        return f"{protagonist}이(가) {setting} 세계에서 {theme}을(를) 위해 싸운다!"
    
    def _generate_unique_point(self):
        """Generate unique selling point"""
        unique_points = [
            "독특한 능력 시스템",
            "예측 불가능한 전개",
            "매력적인 캐릭터들",
            "탄탄한 세계관",
            "감동적인 스토리",
            "중독성 있는 전개"
        ]
        return random.choice(unique_points)
    
    def combine_themes(self, theme_count=3):
        """Combine multiple themes"""
        selected_themes = random.sample(self.themes, min(theme_count, len(self.themes)))
        
        return {
            "themes": selected_themes,
            "concept": f"{' + '.join(selected_themes)}를 결합한 스토리",
            "description": f"여러 테마가 복합적으로 얽힌 심도 있는 이야기"
        }
    
    def combine_settings(self, setting_count=3):
        """Combine multiple settings"""
        selected_settings = random.sample(self.settings, min(setting_count, len(self.settings)))
        
        return {
            "settings": selected_settings,
            "concept": f"{' + '.join(selected_settings)} 융합 세계관",
            "description": f"독특한 세계관 조합으로 신선한 이야기 전개"
        }
    
    def generate_idea_batch(self, count=10):
        """Generate multiple ideas at once"""
        ideas = []
        for _ in range(count):
            ideas.append(self.generate_random_idea())
        return ideas
