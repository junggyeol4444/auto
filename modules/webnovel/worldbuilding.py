import random

class WorldbuildingGenerator:
    def __init__(self):
        self.magic_systems = {
            "원소 마법": {
                "elements": ["불", "물", "바람", "땅", "빛", "어둠", "시공간"],
                "levels": ["1서클", "2서클", "3서클", "4서클", "5서클", "6서클", "7서클", "8서클", "9서클"],
                "constraints": ["마나 소모", "영창 시간", "재사용 대기시간", "정신력 소모"]
            },
            "룬 마법": {
                "runes": ["힘의 룬", "지혜의 룬", "보호의 룬", "파괴의 룬", "생명의 룬"],
                "levels": ["하급", "중급", "상급", "최상급", "신화급"],
                "constraints": ["룬 각인 시간", "마법석 필요", "정신 집중"]
            },
            "계약 마법": {
                "entities": ["정령", "악마", "신", "고대 존재", "환수"],
                "levels": ["하급 계약", "중급 계약", "상급 계약", "혈약", "영혼 계약"],
                "constraints": ["계약 대가", "소환 제한", "반동"]
            }
        }
        
        self.power_systems = {
            "헌터": {
                "ranks": ["F", "E", "D", "C", "B", "A", "S", "SS", "SSS"],
                "types": ["전사형", "마법사형", "탱커형", "힐러형", "암살자형", "소환사형"],
                "stats": ["힘", "민첩", "체력", "마력", "지능", "행운"]
            },
            "무공": {
                "ranks": ["삼류", "이류", "일류", "초일류", "절정고수", "화경", "현경"],
                "types": ["검법", "도법", "장법", "권법", "암기술", "경공술"],
                "stats": ["내공", "무공", "경공", "암기", "의술"]
            },
            "초능력": {
                "ranks": ["레벨1", "레벨2", "레벨3", "레벨4", "레벨5", "레벨6", "레벨7"],
                "types": ["염동력", "텔레파시", "순간이동", "예지", "치유", "변신", "시간 조작"],
                "stats": ["능력치", "제어력", "정신력", "각성도"]
            }
        }
        
        self.races = {
            "인간": {"lifespan": 80, "traits": ["적응력", "다재다능"], "special": "마법 적성 보통"},
            "엘프": {"lifespan": 500, "traits": ["민첩", "우아함"], "special": "자연 마법 특화"},
            "드워프": {"lifespan": 200, "traits": ["힘", "완고함"], "special": "대장 기술 최고"},
            "오크": {"lifespan": 50, "traits": ["전투력", "야성"], "special": "근접 전투 특화"},
            "용인": {"lifespan": 300, "traits": ["마력", "고귀함"], "special": "용의 힘 사용"},
            "반인": {"lifespan": 100, "traits": ["감각", "순발력"], "special": "동물 특성 보유"}
        }
    
    def generate_fantasy_world(self, world_name="아르카디아"):
        """Generate fantasy world setting"""
        magic_system = random.choice(list(self.magic_systems.keys()))
        magic_data = self.magic_systems[magic_system]
        
        world = {
            "name": world_name,
            "type": "판타지",
            "magic_system": {
                "type": magic_system,
                "details": magic_data,
                "description": self._generate_magic_description(magic_system, magic_data)
            },
            "races": self._generate_race_info(),
            "geography": self._generate_geography(),
            "political_system": self._generate_political_system(),
            "economy": self._generate_economy(),
            "history": self._generate_history(),
            "mythology": self._generate_mythology()
        }
        
        return world
    
    def _generate_magic_description(self, system_type, data):
        """Generate magic system description"""
        if system_type == "원소 마법":
            return f"""
원소 마법 시스템:
- 4대 기본 원소: 불, 물, 바람, 땅
- 상급 원소: 빛, 어둠, 시공간
- 마법 등급: 1서클부터 9서클까지
- 각 서클마다 필요한 마나량이 기하급수적으로 증가
- 제약 조건: {', '.join(data['constraints'])}
- 9서클 마법사는 전설적인 존재로 세계에 10명도 되지 않음
"""
        elif system_type == "룬 마법":
            return f"""
룬 마법 시스템:
- 고대 문자인 룬을 새겨 마법을 발동
- 룬의 등급: {', '.join(data['levels'])}
- 주요 룬: {', '.join(data['runes'])}
- 제약 조건: {', '.join(data['constraints'])}
- 강력하지만 준비 시간이 오래 걸림
"""
        else:
            return f"""
계약 마법 시스템:
- 초자연적 존재와 계약을 맺어 힘을 빌림
- 계약 대상: {', '.join(data['entities'])}
- 계약 등급: {', '.join(data['levels'])}
- 제약 조건: {', '.join(data['constraints'])}
- 계약에는 반드시 대가가 따름
"""
    
    def _generate_race_info(self):
        """Generate race information"""
        return self.races
    
    def _generate_geography(self):
        """Generate world geography"""
        continents = random.randint(3, 7)
        return {
            "continents": continents,
            "major_regions": [
                {"name": "북부 설원", "climate": "극한의 추위", "features": "얼음 던전, 고대 유적"},
                {"name": "중앙 평원", "climate": "온난", "features": "비옥한 농토, 대도시"},
                {"name": "동부 산맥", "climate": "고산", "features": "드워프 왕국, 광산"},
                {"name": "서부 숲", "climate": "온대", "features": "엘프 왕국, 세계수"},
                {"name": "남부 사막", "climate": "건조", "features": "고대 왕국 유적, 모래 던전"}
            ],
            "special_locations": [
                "세계수 - 마나의 원천",
                "고대 던전 - 봉인된 마왕",
                "마법 학원 - 최고의 마법 교육 기관",
                "용의 둥지 - 드래곤들의 서식지"
            ]
        }
    
    def _generate_political_system(self):
        """Generate political system"""
        systems = ["왕정", "제국", "공화정", "연방제", "마법정"]
        system = random.choice(systems)
        
        return {
            "type": system,
            "major_powers": [
                {"name": "아스트라 왕국", "type": "인간 왕국", "strength": "강력한 군대"},
                {"name": "엘프 연합", "type": "엘프 연합체", "strength": "마법 기술"},
                {"name": "드워프 왕국", "type": "지하 왕국", "strength": "최고급 무기"},
                {"name": "마법사 길드", "type": "초국가 조직", "strength": "마법 독점"}
            ],
            "conflicts": [
                "인간과 아인종의 갈등",
                "마법사 길드의 권력 독점",
                "대륙 통일 전쟁의 위기"
            ]
        }
    
    def _generate_economy(self):
        """Generate economic system"""
        return {
            "currency": "골드",
            "sub_currency": ["실버", "브론즈"],
            "conversion": "1 골드 = 100 실버 = 10000 브론즈",
            "major_industries": [
                "마법석 채굴",
                "마법 도구 제작",
                "몬스터 토벌",
                "던전 탐험",
                "농업"
            ],
            "trade_routes": [
                "대륙 횡단 무역로",
                "해상 무역로",
                "마법 포탈 네트워크"
            ]
        }
    
    def _generate_history(self):
        """Generate world history timeline"""
        return {
            "epochs": [
                {
                    "era": "창세기",
                    "period": "???",
                    "events": ["신들의 전쟁", "세계의 창조", "종족의 탄생"]
                },
                {
                    "era": "고대",
                    "period": "10,000년 전",
                    "events": ["최초의 문명", "마법의 발견", "드래곤과의 전쟁"]
                },
                {
                    "era": "중세",
                    "period": "1,000년 전",
                    "events": ["왕국의 성립", "마왕의 출현", "용사의 봉인"]
                },
                {
                    "era": "현대",
                    "period": "현재",
                    "events": ["마법 학원 설립", "던전의 출현", "새로운 위협"]
                }
            ]
        }
    
    def _generate_mythology(self):
        """Generate world mythology"""
        return {
            "creation_myth": "태초에 창조신이 혼돈에서 세계를 만들었다. 그리고 다섯 원소의 정령을 창조하여 세계를 다스리게 했다.",
            "prophecy": "천 년마다 한 번씩 선택받은 용사가 나타나 세계를 구원한다.",
            "legends": [
                "전설의 12성검 - 고대 영웅들이 사용했던 성검",
                "세계수의 비밀 - 세계수 아래 잠든 고대의 힘",
                "마왕의 부활 - 천 년마다 부활하는 어둠의 존재"
            ],
            "artifacts": [
                {"name": "성검 엑스칼리버", "power": "악을 베는 검", "location": "왕가 보물"},
                {"name": "현자의 돌", "power": "무한 마나", "location": "행방불명"},
                {"name": "시간의 모래시계", "power": "시간 조작", "location": "고대 유적"}
            ]
        }
    
    def generate_sf_world(self, world_name="네오 어스"):
        """Generate SF world setting"""
        return {
            "name": world_name,
            "type": "SF",
            "tech_level": self._generate_tech_level(),
            "planets": self._generate_planets(),
            "factions": self._generate_factions(),
            "technology": self._generate_technology(),
            "conflicts": self._generate_conflicts()
        }
    
    def _generate_tech_level(self):
        """Generate technology level"""
        return {
            "kardashev_scale": "Type 1.5",
            "description": "항성계 식민지화 시작 단계",
            "achievements": [
                "행성 간 여행 가능",
                "인공지능 고도화",
                "사이버네틱 기술 발달",
                "나노 기술 상용화",
                "핵융합 에너지"
            ]
        }
    
    def _generate_planets(self):
        """Generate planet settings"""
        return [
            {
                "name": "지구",
                "status": "본성",
                "population": "100억",
                "features": "통합 정부, 메가시티"
            },
            {
                "name": "화성",
                "status": "식민지",
                "population": "10억",
                "features": "테라포밍 진행 중, 채굴 기지"
            },
            {
                "name": "타이탄",
                "status": "전초 기지",
                "population": "1억",
                "features": "연구 시설, 군사 기지"
            }
        ]
    
    def _generate_factions(self):
        """Generate SF factions"""
        return [
            {"name": "지구 연합", "ideology": "통합", "strength": "군사력"},
            {"name": "화성 자치령", "ideology": "독립", "strength": "자원"},
            {"name": "기업 연합", "ideology": "이익", "strength": "기술"},
            {"name": "AI 해방전선", "ideology": "AI 권리", "strength": "해킹"}
        ]
    
    def _generate_technology(self):
        """Generate technology list"""
        return [
            "워프 드라이브 - 초광속 항해",
            "사이버네틱 강화 - 인체 개조",
            "나노 의료 - 즉각 치유",
            "AI 어시스턴트 - 개인 AI",
            "홀로그램 통신 - 3D 영상통화"
        ]
    
    def _generate_conflicts(self):
        """Generate conflict scenarios"""
        return [
            "지구 vs 화성 독립 전쟁",
            "AI의 권리 문제",
            "외계 신호 발견",
            "기업의 권력 독점"
        ]
    
    def generate_power_system(self, system_type="헌터"):
        """Generate power system"""
        if system_type not in self.power_systems:
            system_type = "헌터"
        
        system = self.power_systems[system_type]
        
        return {
            "type": system_type,
            "ranks": system["ranks"],
            "types": system["types"],
            "stats": system["stats"],
            "growth": self._generate_growth_system(system_type),
            "balance": self._generate_balance_rules(system_type)
        }
    
    def _generate_growth_system(self, system_type):
        """Generate growth/leveling system"""
        if system_type == "헌터":
            return {
                "method": "레벨업",
                "requirements": "경험치 획득 (몬스터 사냥, 던전 클리어)",
                "stat_growth": "레벨당 스탯 포인트 5점 획득",
                "skill_acquisition": "레벨업 시 스킬 포인트로 스킬 습득"
            }
        elif system_type == "무공":
            return {
                "method": "수련",
                "requirements": "내공 수련, 무공 익히기",
                "stat_growth": "수련 시간에 비례하여 내공 증가",
                "skill_acquisition": "비급을 통한 무공 습득"
            }
        else:
            return {
                "method": "각성",
                "requirements": "능력 사용, 극한 상황",
                "stat_growth": "각성도가 높아질수록 능력 강화",
                "skill_acquisition": "각성을 통한 새로운 능력 개방"
            }
    
    def _generate_balance_rules(self, system_type):
        """Generate balance rules"""
        return {
            "power_ceiling": "최고 등급은 극소수만 도달 가능",
            "weaknesses": "모든 능력은 약점이 존재",
            "costs": "강력한 능력일수록 대가가 큼",
            "counters": "상성 관계가 존재하여 절대 강자는 없음"
        }
