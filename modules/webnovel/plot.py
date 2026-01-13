"""
Plot generation module
"""
import random


class PlotGenerator:
    """Generate plot structure for web novels"""
    
    def __init__(self, template):
        self.template = template
        self.plot_templates = template.get('plot_templates', {})
        self.conflicts = template.get('conflicts', [])
    
    def generate_plot(self, characters, num_chapters=10):
        """Generate complete plot structure"""
        plot = {
            'structure': '3막 구조',
            'acts': [],
            'chapters': []
        }
        
        # Determine act distribution
        act1_chapters = max(1, num_chapters // 3)
        act2_chapters = max(1, num_chapters // 2)
        act3_chapters = num_chapters - act1_chapters - act2_chapters
        
        # Act 1: Setup (발단)
        plot['acts'].append({
            'act': 1,
            'name': '발단',
            'chapters': list(range(1, act1_chapters + 1)),
            'focus': '주인공 소개, 배경 설정, 사건 발생'
        })
        
        # Act 2: Confrontation (전개)
        plot['acts'].append({
            'act': 2,
            'name': '전개',
            'chapters': list(range(act1_chapters + 1, act1_chapters + act2_chapters + 1)),
            'focus': '갈등 심화, 시련과 성장, 복선 전개'
        })
        
        # Act 3: Resolution (결말)
        plot['acts'].append({
            'act': 3,
            'name': '결말',
            'chapters': list(range(act1_chapters + act2_chapters + 1, num_chapters + 1)),
            'focus': '클라이맥스, 갈등 해결, 결말'
        })
        
        # Generate chapter outlines
        for i in range(1, num_chapters + 1):
            chapter_outline = self._generate_chapter_outline(i, characters, plot['acts'])
            plot['chapters'].append(chapter_outline)
        
        return plot
    
    def _generate_chapter_outline(self, chapter_num, characters, acts):
        """Generate outline for a single chapter"""
        # Determine which act this chapter belongs to
        act_info = None
        for act in acts:
            if chapter_num in act['chapters']:
                act_info = act
                break
        
        if not act_info:
            act_info = acts[0]
        
        # Select appropriate plot template based on act
        act_num = act_info['act']
        if act_num == 1:
            template_type = 'opening'
        elif act_num == 2:
            template_type = 'development'
        else:
            template_type = 'climax' if chapter_num < acts[-1]['chapters'][-1] else 'resolution'
        
        templates = self.plot_templates.get(template_type, ['이야기가 계속됩니다.'])
        
        outline = {
            'chapter': chapter_num,
            'act': act_num,
            'title': f"제{chapter_num}화",
            'outline': random.choice(templates),
            'scenes': self._generate_scene_list(template_type, characters),
            'conflict': random.choice(self.conflicts) if self.conflicts else '갈등'
        }
        
        return outline
    
    def _generate_scene_list(self, template_type, characters):
        """Generate list of scenes for a chapter"""
        scenes = []
        
        if template_type == 'opening':
            scenes = [
                '주인공 등장',
                '배경 묘사',
                '사건 발생'
            ]
        elif template_type == 'development':
            scenes = [
                '갈등 표면화',
                '캐릭터 성장 계기',
                '새로운 정보 발견'
            ]
        elif template_type == 'climax':
            scenes = [
                '긴장감 고조',
                '대결 장면',
                '반전'
            ]
        else:  # resolution
            scenes = [
                '갈등 해결',
                '캐릭터 변화',
                '새로운 시작'
            ]
        
        return scenes
    
    def generate_chapter_beats(self, chapter_outline):
        """Generate detailed beats for a chapter"""
        beats = []
        
        for scene in chapter_outline['scenes']:
            beat = {
                'scene': scene,
                'description': f"{scene}에 대한 상세 묘사",
                'purpose': '스토리 진행'
            }
            beats.append(beat)
        
        return beats
