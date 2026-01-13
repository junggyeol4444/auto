import random

class SceneGenerator:
    def __init__(self):
        self.scene_types = {
            "전투": ["근접 전투", "마법 전투", "대규모 전투", "일대일 대결", "암살"],
            "로맨스": ["첫 만남", "데이트", "고백", "키스", "이별", "재회"],
            "일상": ["아침", "식사", "대화", "산책", "휴식"],
            "긴장": ["추격", "잠입", "조사", "위기", "탈출"],
            "감동": ["재회", "희생", "성장", "깨달음", "승리"]
        }
        
        self.atmospheres = {
            "긴장": ["공기가 팽팽하게 긴장했다.", "숨소리마저 조심스러웠다.", "예감이 좋지 않았다."],
            "평화": ["따뜻한 햇살이 내리쬐었다.", "평화로운 하루가 시작되었다.", "모든 것이 고요했다."],
            "공포": ["으스스한 기분이 들었다.", "등골이 오싹했다.", "무언가 잘못되었다."],
            "설렘": ["심장이 두근거렸다.", "기대감에 들떠있었다.", "왠지 모를 설렘이 느껴졌다."],
            "슬픔": ["눈물이 흘렀다.", "가슴이 미어졌다.", "아무 말도 할 수 없었다."]
        }
        
        self.senses = {
            "시각": ["눈앞에 펼쳐진", "보이는", "빛나는", "어두운", "찬란한"],
            "청각": ["들리는", "울리는", "고요한", "시끄러운", "속삭이는"],
            "촉각": ["차가운", "따뜻한", "거친", "부드러운", "날카로운"],
            "후각": ["향기로운", "역한", "신선한", "달콤한", "쓴"],
            "미각": ["달콤한", "쓴", "짠", "신", "매운"]
        }
    
    def generate_scene(self, scene_type="일상", atmosphere="평화", characters=None):
        """Generate a complete scene"""
        if scene_type not in self.scene_types:
            scene_type = "일상"
        
        scene = {
            "type": scene_type,
            "atmosphere": atmosphere,
            "description": self._generate_scene_description(scene_type, atmosphere),
            "action": self._generate_action_sequence(scene_type),
            "sensory": self._generate_sensory_description(),
            "characters": characters if characters else []
        }
        
        return scene
    
    def _generate_scene_description(self, scene_type, atmosphere):
        """Generate scene description"""
        atmosphere_text = random.choice(self.atmospheres.get(atmosphere, self.atmospheres["평화"]))
        
        descriptions = {
            "전투": f"{atmosphere_text}\n두 검사가 마주 보고 섰다. 긴장감이 극도로 고조되었다.",
            "로맨스": f"{atmosphere_text}\n달빛 아래, 두 사람이 마주 보고 있었다.",
            "일상": f"{atmosphere_text}\n평범하지만 소중한 하루가 흘러갔다.",
            "긴장": f"{atmosphere_text}\n무언가 잘못되었다는 느낌이 들었다.",
            "감동": f"{atmosphere_text}\n오랫동안 기다렸던 순간이었다."
        }
        
        return descriptions.get(scene_type, descriptions["일상"])
    
    def _generate_action_sequence(self, scene_type):
        """Generate action sequence for the scene"""
        sequences = {
            "전투": [
                "긴장감 조성: 양쪽 모두 움직이지 않고 서로를 주시했다.",
                "선제 공격: 그가 먼저 움직였다. 검이 섬광처럼 번뜩였다.",
                "교전: 철컹! 검과 검이 부딪치며 불꽃이 튀었다.",
                "역전: 그는 마나를 끌어올렸다. 화염 구체가 손에 생성되었다.",
                "클라이맥스: 화염이 폭발했다. 먼지가 가라앉자 승자가 드러났다."
            ],
            "로맨스": [
                "마주침: 우연히 눈이 마주쳤다.",
                "설렘: 심장이 빠르게 뛰었다. 얼굴이 뜨거워졌다.",
                "대화: 어색하지만 즐거운 대화가 이어졌다.",
                "분위기: 달빛이 그녀를 비췄다. 마치 여신 같았다.",
                "절정: 그녀가 말했다. '좋아해.' 시간이 멈춘 것 같았다."
            ],
            "일상": [
                "아침: 햇살에 눈을 떴다.",
                "준비: 새로운 하루를 준비했다.",
                "외출: 밖으로 나섰다.",
                "활동: 하루 일과를 보냈다.",
                "저녁: 하루를 마무리했다."
            ],
            "긴장": [
                "조짐: 뭔가 이상한 기분이 들었다.",
                "발견: 예상치 못한 것을 발견했다.",
                "위기: 상황이 급박하게 돌아갔다.",
                "대응: 빠르게 판단하고 행동했다.",
                "결과: 간신히 위기를 모면했다."
            ]
        }
        
        return sequences.get(scene_type, sequences["일상"])
    
    def _generate_sensory_description(self):
        """Generate sensory (five senses) description"""
        sight = random.choice(self.senses["시각"])
        sound = random.choice(self.senses["청각"])
        touch = random.choice(self.senses["촉각"])
        
        return f"{sight} 광경, {sound} 소리, {touch} 감촉이 느껴졌다."
    
    def generate_battle_scene(self, attacker, defender, power_system="마법"):
        """Generate detailed battle scene"""
        battle = {
            "title": f"{attacker.get('name', '공격자')} vs {defender.get('name', '방어자')}",
            "phases": [
                {
                    "phase": "1단계: 대치",
                    "description": f"{attacker.get('name', '공격자')}와(과) {defender.get('name', '방어자')}가 마주 섰다. 긴장감이 흘렀다."
                },
                {
                    "phase": "2단계: 선제공격",
                    "description": f"{attacker.get('name', '공격자')}가 먼저 움직였다. {self._generate_attack_description(power_system)}"
                },
                {
                    "phase": "3단계: 대응",
                    "description": f"{defender.get('name', '방어자')}가 재빠르게 반응했다. {self._generate_defense_description(power_system)}"
                },
                {
                    "phase": "4단계: 백병전",
                    "description": "치열한 공방이 이어졌다. 양쪽 모두 필살기를 준비했다."
                },
                {
                    "phase": "5단계: 결말",
                    "description": f"결정적인 순간! {random.choice([attacker.get('name', '공격자'), defender.get('name', '방어자')])}의 공격이 명중했다!"
                }
            ]
        }
        
        return battle
    
    def _generate_attack_description(self, power_system):
        """Generate attack description"""
        attacks = {
            "마법": "화염구를 날렸다. 뜨거운 열기가 사방으로 퍼졌다.",
            "무공": "검을 휘둘렀다. 검기가 허공을 갈랐다.",
            "초능력": "염동력을 발동했다. 주변 물체들이 공중으로 떠올랐다.",
            "물리": "빠른 속도로 돌진했다. 주먹에 힘을 실었다."
        }
        return attacks.get(power_system, attacks["물리"])
    
    def _generate_defense_description(self, power_system):
        """Generate defense description"""
        defenses = {
            "마법": "방어 마법을 전개했다. 푸른 장벽이 펼쳐졌다.",
            "무공": "경공술로 회피했다. 잔상만 남겼다.",
            "초능력": "방어막을 생성했다. 투명한 벽이 공격을 막았다.",
            "물리": "옆으로 피했다. 간발의 차이였다."
        }
        return defenses.get(power_system, defenses["물리"])
    
    def generate_romance_scene(self, character1, character2, scene_type="고백"):
        """Generate romance scene"""
        romance_scenes = {
            "첫 만남": {
                "description": f"{character1.get('name', '주인공')}은(는) {character2.get('name', '상대')}를 처음 보는 순간, 심장이 빠르게 뛰기 시작했다.",
                "dialogue": [
                    f"{character1.get('name', '주인공')}: '안녕하세요. 저는...'",
                    f"{character2.get('name', '상대')}: '반가워요. 저는 {character2.get('name', '상대')}예요.'",
                    "어색하지만 즐거운 대화가 이어졌다."
                ],
                "ending": "첫 만남은 이렇게 운명처럼 시작되었다."
            },
            "고백": {
                "description": f"드디어 용기를 낸 {character1.get('name', '주인공')}. 심장이 터질 것 같았다.",
                "dialogue": [
                    f"{character1.get('name', '주인공')}: '저기... 사실은...'",
                    "말이 나오지 않았다. 얼굴이 빨개졌다.",
                    f"{character1.get('name', '주인공')}: '나... 너를 좋아해.'",
                    f"{character2.get('name', '상대')}는 놀란 표정으로 그를 바라보았다."
                ],
                "ending": "시간이 멈춘 것 같았다."
            },
            "키스": {
                "description": "달빛 아래, 두 사람의 거리가 점점 가까워졌다.",
                "dialogue": [
                    f"{character1.get('name', '주인공')}은(는) 천천히 얼굴을 가까이했다.",
                    f"{character2.get('name', '상대')}는 눈을 감았다.",
                    "입술이 겹쳐졌다. 세상에 단둘만 남은 것 같았다."
                ],
                "ending": "영원히 기억될 순간이었다."
            }
        }
        
        if scene_type not in romance_scenes:
            scene_type = "고백"
        
        return romance_scenes[scene_type]
    
    def generate_background_description(self, location_type="숲"):
        """Generate background/setting description"""
        locations = {
            "숲": "울창한 숲이 펼쳐져 있었다. 나무들 사이로 햇빛이 스며들었다. 새소리가 들렸고, 신선한 공기가 느껴졌다.",
            "도시": "거대한 마천루들이 하늘을 찔렀다. 사람들로 붐비는 거리, 자동차 소음, 네온사인의 불빛이 도시의 밤을 밝혔다.",
            "던전": "어두운 던전 내부. 횃불의 불빛만이 유일한 빛이었다. 축축한 돌벽, 어디선가 들리는 괴물의 울음소리.",
            "왕궁": "화려한 왕궁의 대전. 금빛으로 장식된 기둥들, 붉은 융단이 깔린 바닥, 옥좌에 앉은 왕의 위엄.",
            "전장": "피로 물든 전장. 함성과 비명이 뒤섞였다. 검과 검이 부딪치는 소리, 마법의 섬광이 번뜩였다.",
            "우주": "무한한 우주 공간. 별들이 반짝이고, 거대한 행성들이 떠 있었다. 고요하지만 아름다운 광경.",
            "학교": "평범한 학교 교실. 창밖으로 운동장이 보였다. 학생들의 웃음소리, 선생님의 목소리, 평화로운 일상.",
            "산": "높은 산봉우리. 발 아래로 구름이 깔려있었다. 시원한 바람, 맑은 공기, 장엄한 경치."
        }
        
        return locations.get(location_type, locations["숲"])
