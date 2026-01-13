import random

class DialogueGenerator:
    def __init__(self):
        self.personality_speech_patterns = {
            "냉정한": {
                "prefix": ["", "흠.", "..."],
                "style": "간결하고 단호한 어조",
                "patterns": ["{상황}.", "이해했다.", "그렇군."]
            },
            "열정적": {
                "prefix": ["오!", "와!", "좋아!"],
                "style": "감탄사가 많고 활기찬 어조",
                "patterns": ["{상황}! 정말 굉장한데!", "불타오른다!", "최고야!"]
            },
            "소심한": {
                "prefix": ["으음...", "저, 저기...", "혹시..."],
                "style": "머뭇거리고 조심스러운 어조",
                "patterns": ["그게... {상황}인 것 같은데...", "괜찮을까요?", "죄송해요..."]
            },
            "거만한": {
                "prefix": ["흥!", "하!", "케케케"],
                "style": "우월감을 드러내는 어조",
                "patterns": ["나를 누구라고 생각하는가?", "감히 나에게?", "우습군."]
            },
            "친근한": {
                "prefix": ["야!", "어이!", "이봐!"],
                "style": "친구같이 편한 어조",
                "patterns": ["그치? 맞지?", "우리 {행동}하자!", "완전 대박이야!"]
            }
        }
        
        self.situation_dialogues = {
            "전투": {
                "시작": ["전투 준비!", "적이다!", "조심해!", "갈 준비는 됐나?"],
                "공격": ["받아라!", "이걸로 끝이다!", "피할 수 있겠나?"],
                "방어": ["막아!", "위험해!", "뒤로 물러서!"],
                "승리": ["해냈다!", "끝났군.", "이 정도였나?"],
                "패배": ["이럴 수가...", "물러서자!", "다음을 기약하지..."]
            },
            "일상": {
                "인사": ["안녕!", "좋은 아침이야.", "오랜만이야!"],
                "대화": ["오늘 날씨 좋지?", "잘 지냈어?", "요즘 어때?"],
                "작별": ["그럼 또 봐!", "다음에 만나자.", "안녕히 가."]
            },
            "로맨스": {
                "설렘": ["너를 보면 심장이 빨리 뛰어.", "왜 이렇게 떨리지?"],
                "고백": ["사실은... 너를 좋아해.", "나와 함께 해줄래?"],
                "거절": ["미안해... 나는...", "좋은 친구로 지내자."],
                "수락": ["나도... 같은 마음이야.", "정말? 꿈같아!"]
            },
            "긴장": {
                "위협": ["뭔가 이상해...", "조심해야겠어.", "위험한 느낌이야."],
                "공포": ["무서워...", "이건 너무해...", "도망쳐야 해!"],
                "안도": ["휴... 다행이야.", "끝났구나.", "살았다..."]
            }
        }
    
    def generate_dialogue(self, character, situation="일상", context="대화"):
        """Generate dialogue based on character personality and situation"""
        personality_type = self._determine_personality_type(character)
        
        if situation not in self.situation_dialogues:
            situation = "일상"
        if context not in self.situation_dialogues[situation]:
            context = list(self.situation_dialogues[situation].keys())[0]
        
        base_dialogue = random.choice(self.situation_dialogues[situation][context])
        
        # Apply personality speech pattern
        speech_pattern = self.personality_speech_patterns.get(personality_type, self.personality_speech_patterns["친근한"])
        prefix = random.choice(speech_pattern["prefix"])
        
        if prefix:
            dialogue = f"{prefix} {base_dialogue}"
        else:
            dialogue = base_dialogue
        
        return {
            "speaker": character.get("name", "캐릭터"),
            "dialogue": dialogue,
            "emotion": self._determine_emotion(situation, context),
            "action": self._generate_action_description(situation, context)
        }
    
    def _determine_personality_type(self, character):
        """Determine personality type from character data"""
        if isinstance(character, dict):
            personality = character.get("personality", {})
            if isinstance(personality, dict):
                traits = personality.get("traits", [])
                if "냉정한" in str(traits) or "논리적" in str(traits):
                    return "냉정한"
                elif "열정적" in str(traits) or "활발한" in str(traits):
                    return "열정적"
                elif "소심한" in str(traits) or "섬세한" in str(traits):
                    return "소심한"
                elif "대담한" in str(traits) or "카리스마" in str(traits):
                    return "거만한"
        return "친근한"
    
    def _determine_emotion(self, situation, context):
        """Determine emotion based on situation"""
        emotion_map = {
            "전투": {"시작": "긴장", "공격": "분노", "방어": "두려움", "승리": "기쁨", "패배": "슬픔"},
            "일상": {"인사": "평온", "대화": "즐거움", "작별": "아쉬움"},
            "로맨스": {"설렘": "설렘", "고백": "긴장", "거절": "미안함", "수락": "행복"},
            "긴장": {"위협": "경계", "공포": "공포", "안도": "안도"}
        }
        return emotion_map.get(situation, {}).get(context, "평온")
    
    def _generate_action_description(self, situation, context):
        """Generate action description for dialogue"""
        actions = {
            "전투": "칼을 뽑으며",
            "일상": "미소를 지으며",
            "로맨스": "얼굴을 붉히며",
            "긴장": "주위를 경계하며"
        }
        return actions.get(situation, "")
    
    def generate_conversation(self, characters, situation="일상", turns=5):
        """Generate a conversation between multiple characters"""
        if len(characters) < 2:
            return []
        
        conversation = []
        contexts = list(self.situation_dialogues.get(situation, {"대화": []}).keys())
        
        for i in range(turns):
            character = characters[i % len(characters)]
            context = random.choice(contexts)
            dialogue = self.generate_dialogue(character, situation, context)
            conversation.append(dialogue)
        
        return conversation
    
    def generate_natural_dialogue(self, character, emotion="평온"):
        """Generate natural dialogue based on emotion"""
        natural_expressions = {
            "기쁨": ["너무 좋아!", "정말 기뻐!", "최고야!", "와! 대박!", "꿈만 같아!"],
            "슬픔": ["너무 슬퍼...", "왜 이런 일이...", "견딜 수가 없어...", "힘들어..."],
            "분노": ["화가 나!", "용서할 수 없어!", "이건 너무해!", "참을 수 없어!"],
            "두려움": ["무서워...", "어떡하지...", "이대로는 안 돼...", "살려줘..."],
            "놀람": ["헉!", "뭐라고?!", "이게 무슨 일이야?!", "믿을 수 없어!"],
            "평온": ["그래.", "알겠어.", "좋아.", "괜찮아.", "이해해."]
        }
        
        if emotion not in natural_expressions:
            emotion = "평온"
        
        return random.choice(natural_expressions[emotion])
