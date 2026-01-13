"""
Dialogue generation module
"""
import random


class DialogueGenerator:
    """Generate dialogues for web novels"""
    
    def __init__(self, template):
        self.template = template
        self.scene_templates = template.get('scene_templates', {})
    
    def generate_dialogue(self, character1, character2, context='dialogue'):
        """Generate dialogue between two characters"""
        dialogue_templates = self.scene_templates.get(context, {})
        
        if isinstance(dialogue_templates, list) and dialogue_templates:
            template = random.choice(dialogue_templates)
        else:
            template = '"{dialogue1}" {character1}이(가) 말했다.'
        
        # Generate sample dialogues
        dialogues = []
        
        dialogue_samples = [
            "그게 무슨 말이야?",
            "정말 그렇게 생각해?",
            "이럴 줄 알았어.",
            "괜찮아, 내가 도와줄게.",
            "어떻게 이럴 수가...",
            "믿을 수 없어.",
            "고마워.",
            "미안해.",
            "이제 알겠어.",
            "함께 가자."
        ]
        
        for i in range(min(4, len(dialogue_samples))):
            dialogue = {
                'speaker': character1['name'] if i % 2 == 0 else character2['name'],
                'text': dialogue_samples[i],
                'emotion': random.choice(['평온하게', '화가 나서', '슬프게', '기쁘게', '당황하며'])
            }
            dialogues.append(dialogue)
        
        return dialogues
    
    def format_dialogue(self, dialogue):
        """Format dialogue for output"""
        speaker = dialogue['speaker']
        text = dialogue['text']
        emotion = dialogue.get('emotion', '')
        
        if emotion:
            return f'"{text}" {speaker}이(가) {emotion} 말했다.'
        else:
            return f'"{text}" {speaker}이(가) 말했다.'
    
    def generate_conversation(self, characters, num_exchanges=5):
        """Generate a full conversation"""
        if len(characters) < 2:
            return []
        
        char_list = list(characters.values())
        conversation = []
        
        for i in range(num_exchanges):
            char1 = char_list[i % len(char_list)]
            char2 = char_list[(i + 1) % len(char_list)]
            
            dialogues = self.generate_dialogue(char1, char2)
            conversation.extend(dialogues)
        
        return conversation[:num_exchanges]
