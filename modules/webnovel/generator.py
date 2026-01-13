"""
Main web novel generator module
"""
import random
from .character import CharacterGenerator
from .plot import PlotGenerator
from .dialogue import DialogueGenerator


class WebNovelGenerator:
    """Main class for generating web novels"""
    
    def __init__(self, template, api_manager=None):
        self.template = template
        self.api_manager = api_manager
        
        self.character_gen = CharacterGenerator(template)
        self.plot_gen = PlotGenerator(template)
        self.dialogue_gen = DialogueGenerator(template)
        
        self.scene_templates = template.get('scene_templates', {})
        self.worldbuilding = template.get('worldbuilding', [])
    
    def generate_novel(self, title, protagonist_name=None, num_chapters=10, 
                      chapter_length=4000, plot_summary=None):
        """Generate complete web novel"""
        # Generate characters
        characters = self.character_gen.generate_cast(protagonist_name)
        
        # Generate plot
        plot = self.plot_gen.generate_plot(characters, num_chapters)
        
        # Generate novel structure
        novel = {
            'title': title,
            'genre': self.template.get('name', ''),
            'characters': characters,
            'plot': plot,
            'chapters': []
        }
        
        # Generate each chapter
        for chapter_outline in plot['chapters']:
            chapter_content = self._generate_chapter(
                chapter_outline, 
                characters, 
                chapter_length,
                plot_summary
            )
            novel['chapters'].append(chapter_content)
        
        return novel
    
    def _generate_chapter(self, outline, characters, target_length, plot_summary=None):
        """Generate a single chapter"""
        chapter = {
            'number': outline['chapter'],
            'title': outline['title'],
            'content': ''
        }
        
        # Use AI if available
        if self.api_manager and self.api_manager.is_available():
            content = self._generate_with_ai(outline, characters, target_length, plot_summary)
            if content:
                chapter['content'] = content
                return chapter
        
        # Template-based generation
        content = self._generate_with_template(outline, characters, target_length)
        chapter['content'] = content
        
        return chapter
    
    def _generate_with_ai(self, outline, characters, target_length, plot_summary):
        """Generate chapter using AI"""
        protagonist = characters.get('protagonist', {})
        
        prompt = f"""다음 조건에 맞는 웹소설 {outline['title']} 내용을 작성해주세요:

장르: {self.template.get('name', '')}
주인공: {protagonist.get('name', '')} - {protagonist.get('description', '')}
회차 개요: {outline['outline']}
장면: {', '.join(outline['scenes'])}
갈등: {outline['conflict']}
"""
        
        if plot_summary:
            prompt += f"\n전체 줄거리: {plot_summary}"
        
        prompt += f"\n\n약 {target_length}자 분량으로 작성해주세요. 생생한 묘사와 대화를 포함해주세요."
        
        # Try OpenAI first
        content = self.api_manager.generate_with_openai(prompt, max_tokens=target_length//2)
        
        # Try Anthropic if OpenAI fails
        if not content:
            content = self.api_manager.generate_with_anthropic(prompt, max_tokens=target_length//2)
        
        return content
    
    def _generate_with_template(self, outline, characters, target_length):
        """Generate chapter using templates"""
        content_parts = []
        
        # Chapter opening
        protagonist = characters.get('protagonist', {})
        opening = outline['outline']
        
        # Fill in template variables
        opening = opening.replace('{protagonist}', protagonist.get('name', '주인공'))
        opening = opening.replace('{occupation}', protagonist.get('background', '평범한 사람'))
        opening = opening.replace('{event}', '예상치 못한 일')
        opening = opening.replace('{place}', '낯선 곳')
        opening = opening.replace('{familiar_place}', '집')
        
        content_parts.append(opening)
        content_parts.append('\n\n')
        
        # Generate scenes
        for scene in outline['scenes']:
            scene_content = self._generate_scene(scene, characters)
            content_parts.append(scene_content)
            content_parts.append('\n\n')
        
        # Add dialogue if available
        if len(characters) >= 2:
            conversation = self.dialogue_gen.generate_conversation(characters, num_exchanges=3)
            for dialogue in conversation:
                formatted = self.dialogue_gen.format_dialogue(dialogue)
                content_parts.append(formatted)
                content_parts.append('\n\n')
        
        # Chapter closing
        closing = self._generate_closing(outline['act'])
        content_parts.append(closing)
        
        # Combine and adjust length
        content = ''.join(content_parts)
        
        # Pad if too short
        while len(content) < target_length * 0.7:
            filler = self._generate_filler_content(characters)
            content += '\n\n' + filler
        
        # Truncate if too long
        if len(content) > target_length * 1.3:
            content = content[:int(target_length * 1.2)]
            # Find last complete sentence
            last_period = max(content.rfind('.'), content.rfind('。'))
            if last_period > target_length * 0.9:
                content = content[:last_period + 1]
        
        return content
    
    def _generate_scene(self, scene_name, characters):
        """Generate content for a scene"""
        protagonist = characters.get('protagonist', {})
        
        scene_templates = {
            '주인공 등장': f"{protagonist.get('name', '주인공')}이(가) 등장했다. {protagonist.get('description', '')}",
            '배경 묘사': self._generate_description(),
            '사건 발생': '예상치 못한 일이 벌어졌다.',
            '갈등 표면화': '문제가 수면 위로 드러났다.',
            '캐릭터 성장 계기': f"{protagonist.get('name', '주인공')}은(는) 중요한 깨달음을 얻었다.",
            '새로운 정보 발견': '숨겨진 진실이 밝혀지기 시작했다.',
            '긴장감 고조': '긴장감이 최고조에 달했다.',
            '대결 장면': self._generate_action_scene(characters),
            '반전': '예상치 못한 반전이 일어났다.',
            '갈등 해결': '문제가 해결되었다.',
            '캐릭터 변화': f"{protagonist.get('name', '주인공')}은(는) 달라져 있었다.",
            '새로운 시작': '새로운 여정이 시작되었다.'
        }
        
        return scene_templates.get(scene_name, scene_name)
    
    def _generate_description(self):
        """Generate environmental description"""
        descriptions = [
            '하늘은 맑았고, 바람이 살랑이며 불어왔다.',
            '어둠이 깔리기 시작했다. 주변은 점점 조용해졌다.',
            '활기찬 거리의 모습이 눈에 들어왔다.',
            '고요한 적막만이 흘렀다.',
            '긴장감이 감도는 분위기였다.'
        ]
        return random.choice(descriptions)
    
    def _generate_action_scene(self, characters):
        """Generate action scene"""
        protagonist = characters.get('protagonist', {})
        
        scenes = self.scene_templates.get('battle', [])
        if scenes:
            scene = random.choice(scenes)
            scene = scene.replace('{character1}', protagonist.get('name', '주인공'))
            scene = scene.replace('{character2}', '상대방')
            scene = scene.replace('{weapon}', '무기')
            scene = scene.replace('{action}', '공격')
            scene = scene.replace('{character}', protagonist.get('name', '주인공'))
            return scene
        
        return f"{protagonist.get('name', '주인공')}이(가) 전투를 벌였다."
    
    def _generate_closing(self, act):
        """Generate chapter closing"""
        closings = {
            1: '이야기는 이제 시작이었다.',
            2: '시련은 계속되었다.',
            3: '모든 것이 결말을 향해 달려가고 있었다.'
        }
        return closings.get(act, '다음 화에 계속.')
    
    def _generate_filler_content(self, characters):
        """Generate filler content to meet length requirements"""
        protagonist = characters.get('protagonist', {})
        
        fillers = [
            f"{protagonist.get('name', '주인공')}은(는) 잠시 생각에 잠겼다. 앞으로 무엇을 해야 할지 고민이 되었다.",
            "시간이 흘렀다. 많은 일들이 일어났고, 많은 것들이 변했다.",
            f"{protagonist.get('name', '주인공')}은(는) 주변을 둘러보았다. 모든 것이 낯설면서도 익숙했다.",
            "긴 하루였다. 하지만 아직 끝나지 않았다.",
            "새로운 가능성이 보이기 시작했다. 희망이 싹트고 있었다."
        ]
        
        return random.choice(fillers)
