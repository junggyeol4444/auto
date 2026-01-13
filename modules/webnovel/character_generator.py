import random

class CharacterGenerator:
    def __init__(self):
        # Korean names
        self.korean_surnames = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황", "안", "송", "류", "전"]
        self.korean_names_male = ["민준", "서준", "도윤", "예준", "시우", "주원", "하준", "지호", "준서", "건우", "우진", "현우", "선우", "연우", "유준"]
        self.korean_names_female = ["서연", "민서", "지우", "서현", "지민", "수빈", "하은", "예은", "지원", "채원", "다은", "수아", "은서", "윤서", "지안"]
        
        # Fantasy names
        self.fantasy_prefixes = ["Ar", "El", "Gal", "Mor", "Thal", "Ara", "Cel", "Dra", "Fen", "Ky"]
        self.fantasy_suffixes = ["ion", "wyn", "dor", "wen", "ael", "ith", "or", "as", "en", "ris"]
        
        # MBTI types
        self.mbti_types = {
            "INTJ": {"traits": ["전략적", "독립적", "논리적", "완벽주의"], "description": "전략가형"},
            "INTP": {"traits": ["분석적", "호기심 많은", "객관적", "논리적"], "description": "논리술사형"},
            "ENTJ": {"traits": ["대담한", "결단력 있는", "카리스마", "리더십"], "description": "통솔자형"},
            "ENTP": {"traits": ["창의적", "논쟁을 즐기는", "똑똑한", "활발한"], "description": "변론가형"},
            "INFJ": {"traits": ["통찰력 있는", "이상주의적", "공감 능력", "헌신적"], "description": "옹호자형"},
            "INFP": {"traits": ["이상주의적", "충성스러운", "섬세한", "창의적"], "description": "중재자형"},
            "ENFJ": {"traits": ["카리스마 있는", "영감을 주는", "이타적", "리더십"], "description": "선도자형"},
            "ENFP": {"traits": ["열정적", "창의적", "사교적", "자유로운"], "description": "활동가형"},
            "ISTJ": {"traits": ["책임감 있는", "성실한", "논리적", "전통적"], "description": "현실주의자형"},
            "ISFJ": {"traits": ["헌신적", "따뜻한", "책임감 있는", "세심한"], "description": "수호자형"},
            "ESTJ": {"traits": ["조직적", "실용적", "전통적", "관리자"], "description": "경영자형"},
            "ESFJ": {"traits": ["사교적", "협조적", "배려심 깊은", "인기 있는"], "description": "집정관형"},
            "ISTP": {"traits": ["대담한", "실용적", "관찰력 좋은", "융통성"], "description": "장인형"},
            "ISFP": {"traits": ["예술적", "모험적", "유연한", "매력적"], "description": "모험가형"},
            "ESTP": {"traits": ["활동적", "현실적", "대담한", "즉흥적"], "description": "사업가형"},
            "ESFP": {"traits": ["즐거운", "사교적", "자발적", "열정적"], "description": "연예인형"}
        }
        
        # Appearance features
        self.heights = {
            "남성": ["160cm", "165cm", "170cm", "175cm", "180cm", "185cm", "190cm"],
            "여성": ["150cm", "155cm", "160cm", "165cm", "170cm", "175cm", "180cm"]
        }
        
        self.body_types = ["마른", "보통", "건장한", "근육질의", "통통한", "날씬한", "균형잡힌"]
        self.hair_colors = ["검은색", "갈색", "금색", "은색", "빨간색", "파란색", "보라색", "흰색"]
        self.hair_styles = ["단발", "장발", "묶은 머리", "웨이브", "곱슬", "생머리", "포니테일", "양갈래"]
        self.eye_colors = ["검은색", "갈색", "파란색", "녹색", "회색", "금색", "은색", "빨간색"]
        self.impressions = ["차갑고 냉정한", "따뜻하고 친근한", "날카로운", "부드러운", "강인한", "우아한", "신비로운", "밝고 쾌활한"]
    
    def generate_name(self, name_type="한국어", gender="남성"):
        """Generate character name"""
        if name_type == "한국어":
            surname = random.choice(self.korean_surnames)
            if gender == "남성":
                given_name = random.choice(self.korean_names_male)
            else:
                given_name = random.choice(self.korean_names_female)
            return surname + given_name
        elif name_type == "판타지":
            prefix = random.choice(self.fantasy_prefixes)
            suffix = random.choice(self.fantasy_suffixes)
            return prefix + suffix
        else:
            # English names
            if gender == "남성":
                names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Christopher"]
            else:
                names = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"]
            return random.choice(names)
    
    def generate_personality(self):
        """Generate personality based on MBTI"""
        mbti = random.choice(list(self.mbti_types.keys()))
        personality_data = self.mbti_types[mbti]
        
        return {
            "mbti": mbti,
            "type": personality_data["description"],
            "traits": personality_data["traits"],
            "strengths": random.sample(["리더십", "창의성", "공감 능력", "논리적 사고", "결단력", "인내심", "유머 감각", "책임감"], 3),
            "weaknesses": random.sample(["고집", "우유부단", "감정적", "완벽주의", "무관심", "소심함", "충동적"], 2)
        }
    
    def generate_appearance(self, gender="남성", age=25):
        """Generate appearance description"""
        height = random.choice(self.heights[gender])
        body_type = random.choice(self.body_types)
        hair_color = random.choice(self.hair_colors)
        hair_style = random.choice(self.hair_styles)
        eye_color = random.choice(self.eye_colors)
        impression = random.choice(self.impressions)
        
        age_group = "어린" if age < 18 else "젊은" if age < 30 else "중년의" if age < 50 else "노년의"
        
        description = f"키 {height}의 {body_type} {age_group} {gender}. "
        description += f"{hair_color} {hair_style}, {eye_color} 눈동자. "
        description += f"{impression} 인상."
        
        return {
            "height": height,
            "body_type": body_type,
            "hair_color": hair_color,
            "hair_style": hair_style,
            "eye_color": eye_color,
            "impression": impression,
            "description": description
        }
    
    def generate_background(self, character_name, age=25):
        """Generate character background story"""
        backgrounds = [
            f"{character_name}는 평범한 가정에서 태어났다. 어린 시절부터 남다른 재능을 보였지만, 가족의 반대로 꿈을 포기해야 했다.",
            f"{character_name}는 비극적인 과거를 가지고 있다. {age-10}살 때 사고로 부모를 잃고 고아원에서 자랐다.",
            f"{character_name}는 명문가의 후계자로 태어났다. 어린 시절부터 엄격한 교육을 받으며 자랐다.",
            f"{character_name}는 가난한 환경에서 자랐지만, 불굴의 의지로 자신의 길을 개척해왔다.",
            f"{character_name}는 신비로운 능력을 타고났다. 이 때문에 어린 시절 많은 차별과 편견에 시달렸다."
        ]
        
        return random.choice(backgrounds)
    
    def generate_abilities(self, genre="판타지"):
        """Generate character abilities"""
        abilities_by_genre = {
            "판타지": ["화염 마법", "빙결 마법", "치유 마법", "검술", "궁술", "암살술", "소환술", "결계술"],
            "무협": ["경공술", "검법", "도법", "장법", "권법", "암기술", "내공", "절학"],
            "현대물": ["격투기", "사격", "해킹", "의술", "요리", "경영", "협상", "예술"],
            "SF": ["사이버네틱 강화", "나노 기술", "에너지 조작", "시간 제어", "텔레파시", "순간이동"]
        }
        
        if genre not in abilities_by_genre:
            genre = "판타지"
        
        abilities = random.sample(abilities_by_genre[genre], random.randint(2, 4))
        
        return [{"name": ability, "level": random.choice(["초급", "중급", "고급", "달인"])} for ability in abilities]
    
    def generate_character(self, name_type="한국어", gender="남성", age=25, genre="판타지"):
        """Generate complete character"""
        name = self.generate_name(name_type, gender)
        personality = self.generate_personality()
        appearance = self.generate_appearance(gender, age)
        background = self.generate_background(name, age)
        abilities = self.generate_abilities(genre)
        
        character = {
            "name": name,
            "gender": gender,
            "age": age,
            "personality": personality,
            "appearance": appearance,
            "background": background,
            "abilities": abilities,
            "relationships": []
        }
        
        return character
    
    def generate_character_relationships(self, characters):
        """Generate relationships between characters"""
        relationship_types = ["친구", "연인", "적", "라이벌", "스승", "제자", "가족", "동료", "상사", "부하"]
        
        relationships = []
        for i, char1 in enumerate(characters):
            for j, char2 in enumerate(characters):
                if i < j:  # Avoid duplicate relationships
                    rel_type = random.choice(relationship_types)
                    relationships.append({
                        "character1": char1["name"],
                        "character2": char2["name"],
                        "type": rel_type,
                        "description": f"{char1['name']}와(과) {char2['name']}는 {rel_type} 관계"
                    })
        
        return relationships
