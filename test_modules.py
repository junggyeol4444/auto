#!/usr/bin/env python3
"""
Test script for Creative Writing Assistant Suite
Tests all core functionality without GUI
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.database import DatabaseHandler
from modules.webnovel.plot_generator import PlotGenerator
from modules.webnovel.character_generator import CharacterGenerator
from modules.webnovel.worldbuilding import WorldbuildingGenerator
from modules.webnovel.dialogue_generator import DialogueGenerator
from modules.webnovel.scene_generator import SceneGenerator
from modules.scenario.scenario_generator import ScenarioGenerator, SynopsisGenerator
from modules.game.quest_generator import QuestGenerator, NPCGenerator, DungeonDesigner
from modules.ideas.title_generator import TitleGenerator, TwistGenerator, IdeaGenerator

def test_all_modules():
    """Test all modules"""
    print('='*60)
    print('Creative Writing Assistant Suite - Module Tests')
    print('='*60)
    
    # 1. Plot Generator
    print('\n[1/10] Testing Plot Generator...')
    pg = PlotGenerator()
    plot = pg.generate_plot('판타지', '용사의 귀환')
    print(f'✓ Generated plot: {plot["theme"]}')
    print(f'  - Genre: {plot["genre"]}')
    print(f'  - Structure: {len(plot["structure"])} acts')
    
    # 2. Character Generator
    print('\n[2/10] Testing Character Generator...')
    cg = CharacterGenerator()
    char = cg.generate_character('한국어', '남성', 25, '판타지')
    print(f'✓ Generated character: {char["name"]}')
    print(f'  - Age: {char["age"]}, Gender: {char["gender"]}')
    print(f'  - MBTI: {char["personality"]["mbti"]}')
    print(f'  - Abilities: {len(char["abilities"])}')
    
    # 3. Worldbuilding
    print('\n[3/10] Testing Worldbuilding Generator...')
    wg = WorldbuildingGenerator()
    world = wg.generate_fantasy_world('에테리아')
    print(f'✓ Generated world: {world["name"]}')
    print(f'  - Type: {world["type"]}')
    print(f'  - Magic system: {world["magic_system"]["type"]}')
    print(f'  - Races: {len(world["races"])}')
    
    # 4. Dialogue Generator
    print('\n[4/10] Testing Dialogue Generator...')
    dg = DialogueGenerator()
    dialogue = dg.generate_dialogue(char, '전투', '시작')
    print(f'✓ Generated dialogue:')
    print(f'  - {dialogue["speaker"]}: "{dialogue["dialogue"]}"')
    print(f'  - Emotion: {dialogue["emotion"]}')
    
    # 5. Scene Generator
    print('\n[5/10] Testing Scene Generator...')
    sg = SceneGenerator()
    scene = sg.generate_scene('전투', '긴장')
    print(f'✓ Generated scene:')
    print(f'  - Type: {scene["type"]}')
    print(f'  - Atmosphere: {scene["atmosphere"]}')
    print(f'  - Actions: {len(scene["action"])}')
    
    # 6. Scenario Generator
    print('\n[6/10] Testing Scenario Generator...')
    scg = ScenarioGenerator()
    scenario = scg.generate_movie_scenario('액션', 120)
    print(f'✓ Generated movie scenario:')
    print(f'  - Title: {scenario["title"]}')
    print(f'  - Genre: {scenario["genre"]}')
    print(f'  - Duration: {scenario["duration"]}')
    
    # 7. Title Generator
    print('\n[7/10] Testing Title Generator...')
    tg = TitleGenerator()
    titles = tg.generate_title('판타지', 5)
    print(f'✓ Generated {len(titles)} titles:')
    for i, title in enumerate(titles[:3], 1):
        print(f'  {i}. {title}')
    
    # 8. Quest Generator
    print('\n[8/10] Testing Quest Generator...')
    qg = QuestGenerator()
    quest = qg.generate_main_quest(10)
    print(f'✓ Generated quest:')
    print(f'  - Name: {quest["name"]}')
    print(f'  - Level: {quest["level"]}')
    print(f'  - Objectives: {len(quest["objectives"])}')
    print(f'  - Rewards: {quest["rewards"]["exp"]} EXP, {quest["rewards"]["gold"]} Gold')
    
    # 9. NPC Generator
    print('\n[9/10] Testing NPC Generator...')
    ng = NPCGenerator()
    npc = ng.generate_npc('마법사')
    print(f'✓ Generated NPC:')
    print(f'  - Name: {npc["name"]}')
    print(f'  - Type: {npc["type"]}')
    print(f'  - Personality: {npc["personality"]}')
    
    # 10. Dungeon Designer
    print('\n[10/10] Testing Dungeon Designer...')
    dd = DungeonDesigner()
    dungeon = dd.generate_dungeon('어둠의 던전', 5)
    print(f'✓ Generated dungeon:')
    print(f'  - Name: {dungeon["name"]}')
    print(f'  - Type: {dungeon["type"]}')
    print(f'  - Floors: {dungeon["floors"]}')
    print(f'  - Difficulty: {dungeon["difficulty"]}')
    print(f'  - Boss: {dungeon["boss"]["name"]} (Lv.{dungeon["boss"]["level"]})')
    
    # Database test
    print('\n[Bonus] Testing Database...')
    db = DatabaseHandler('test.db')
    project_id = db.save_project('테스트 프로젝트', 'plot', plot)
    print(f'✓ Database test successful (Project ID: {project_id})')
    
    # Cleanup
    import os
    if os.path.exists('test.db'):
        os.remove('test.db')
    
    print('\n' + '='*60)
    print('✓ ALL TESTS PASSED!')
    print('='*60)
    print('\nNote: To test the GUI, run "python main.py" on a system')
    print('      with a display server (X11, Wayland, Windows, macOS)')

if __name__ == "__main__":
    try:
        test_all_modules()
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
