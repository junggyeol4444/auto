# 사용 예제 (Usage Examples)

이 문서는 Creative Writing Assistant Suite의 핵심 기능들을 프로그래밍 방식으로 사용하는 예제를 제공합니다.

## 웹소설 창작 예제

### 1. 플롯 생성

```python
from modules.webnovel.plot_generator import PlotGenerator

# 플롯 생성기 초기화
plot_gen = PlotGenerator()

# 판타지 플롯 생성
plot = plot_gen.generate_plot(genre="판타지", custom_theme="용사의 귀환")

# 결과 출력
print(f"장르: {plot['genre']}")
print(f"주제: {plot['theme']}")
print(f"배경: {plot['setting']}")
print(f"갈등: {plot['conflict']}")

# 3막 구조 확인
for act_name, act_data in plot['structure'].items():
    print(f"\n{act_data['title']}")
    for scene in act_data['scenes']:
        print(f"  - {scene}")
```

### 2. 캐릭터 생성

```python
from modules.webnovel.character_generator import CharacterGenerator

# 캐릭터 생성기 초기화
char_gen = CharacterGenerator()

# 한국어 이름의 남성 캐릭터 생성
character = char_gen.generate_character(
    name_type="한국어",
    gender="남성",
    age=25,
    genre="판타지"
)

# 캐릭터 정보 출력
print(f"이름: {character['name']}")
print(f"나이: {character['age']}")
print(f"성격: {character['personality']['mbti']}")
print(f"외모: {character['appearance']['description']}")

# 능력 출력
for ability in character['abilities']:
    print(f"- {ability['name']} ({ability['level']})")
```

### 3. 세계관 구축

```python
from modules.webnovel.worldbuilding import WorldbuildingGenerator

# 세계관 생성기 초기화
world_gen = WorldbuildingGenerator()

# 판타지 세계관 생성
world = world_gen.generate_fantasy_world("아르카디아")

# 세계관 정보
print(f"세계명: {world['name']}")
print(f"마법 시스템: {world['magic_system']['type']}")
print(f"종족: {list(world['races'].keys())}")

# SF 세계관 생성
sf_world = world_gen.generate_sf_world("네오 어스")
print(f"\nSF 세계: {sf_world['name']}")
print(f"기술 수준: {sf_world['tech_level']['kardashev_scale']}")
```

### 4. 대화 생성

```python
from modules.webnovel.dialogue_generator import DialogueGenerator

# 대화 생성기 초기화
dialogue_gen = DialogueGenerator()

# 캐릭터 데이터 (위에서 생성한 캐릭터 사용)
dialogue = dialogue_gen.generate_dialogue(
    character=character,
    situation="전투",
    context="시작"
)

# 대화 출력
print(f"{dialogue['speaker']}: \"{dialogue['dialogue']}\"")
print(f"감정: {dialogue['emotion']}")
print(f"동작: {dialogue['action']}")
```

### 5. 장면 묘사

```python
from modules.webnovel.scene_generator import SceneGenerator

# 장면 생성기 초기화
scene_gen = SceneGenerator()

# 전투 장면 생성
scene = scene_gen.generate_scene(
    scene_type="전투",
    atmosphere="긴장"
)

# 장면 설명
print(scene['description'])

# 액션 시퀀스
for action in scene['action']:
    print(f"  {action}")

# 전투 장면 상세 생성
battle = scene_gen.generate_battle_scene(
    attacker={"name": "주인공"},
    defender={"name": "적"},
    power_system="마법"
)

for phase in battle['phases']:
    print(f"\n{phase['phase']}")
    print(phase['description'])
```

## 시나리오 창작 예제

### 영화 시나리오 생성

```python
from modules.scenario.scenario_generator import ScenarioGenerator

# 시나리오 생성기 초기화
scenario_gen = ScenarioGenerator()

# 영화 시나리오 생성
movie = scenario_gen.generate_movie_scenario(
    genre="액션",
    duration=120
)

print(f"제목: {movie['title']}")
print(f"장르: {movie['genre']}")
print(f"러닝타임: {movie['duration']}")
```

### 드라마 시놉시스 생성

```python
# 드라마 시놉시스 생성
drama = scenario_gen.generate_drama_synopsis(episodes=16)

print(f"제목: {drama['title']}")
print(f"장르: {drama['genre']}")
print(f"메인 플롯: {drama['main_plot']}")

# 캐릭터 정보
for char in drama['characters']:
    print(f"- {char['name']} ({char['role']}): {char['description']}")
```

## 게임 창작 예제

### 퀘스트 생성

```python
from modules.game.quest_generator import QuestGenerator

# 퀘스트 생성기 초기화
quest_gen = QuestGenerator()

# 메인 퀘스트 생성
quest = quest_gen.generate_main_quest(level=10)

print(f"퀘스트명: {quest['name']}")
print(f"레벨: {quest['level']}")
print(f"설명: {quest['description']}")

# 목표
print("\n목표:")
for objective in quest['objectives']:
    print(f"  - {objective}")

# 보상
print(f"\n보상:")
print(f"  경험치: {quest['rewards']['exp']}")
print(f"  골드: {quest['rewards']['gold']}")
```

### NPC 생성

```python
from modules.game.quest_generator import NPCGenerator

# NPC 생성기 초기화
npc_gen = NPCGenerator()

# 상인 NPC 생성
npc = npc_gen.generate_npc("상인")

print(f"이름: {npc['name']}")
print(f"직업: {npc['type']}")
print(f"성격: {npc['personality']}")

# 대화
print("\n대화:")
for key, value in npc['dialogue'].items():
    print(f"  {key}: {value}")
```

### 던전 디자인

```python
from modules.game.quest_generator import DungeonDesigner

# 던전 디자이너 초기화
dungeon_gen = DungeonDesigner()

# 던전 생성
dungeon = dungeon_gen.generate_dungeon("어둠의 성", floors=5)

print(f"던전명: {dungeon['name']}")
print(f"타입: {dungeon['type']}")
print(f"난이도: {dungeon['difficulty']}")

# 각 층 정보
for floor in dungeon['floor_details']:
    print(f"\n{floor['floor']}층:")
    print(f"  구조: {floor['layout']}")
    print(f"  몬스터: {len(floor['monsters'])}종")
    print(f"  함정: {floor['traps']}")

# 보스 정보
boss = dungeon['boss']
print(f"\n보스: {boss['name']} (Lv.{boss['level']})")
print(f"HP: {boss['hp']}")
```

## 아이디어 생성 예제

### 제목 생성

```python
from modules.ideas.title_generator import TitleGenerator

# 제목 생성기 초기화
title_gen = TitleGenerator()

# 판타지 제목 5개 생성
titles = title_gen.generate_title(genre="판타지", count=5)

print("생성된 제목들:")
for i, title in enumerate(titles, 1):
    print(f"{i}. {title}")

# 클릭베이트 제목 생성
clickbait = title_gen.generate_clickbait_title(genre="판타지")
print(f"\n클릭베이트: {clickbait}")

# A/B 테스트용 제목
ab_titles = title_gen.generate_ab_test_titles(genre="로맨스")
print(f"\nA안: {ab_titles['version_a']}")
print(f"B안: {ab_titles['version_b']}")
print(f"C안: {ab_titles['version_c']}")
```

### 플롯 트위스트 생성

```python
from modules.ideas.title_generator import TwistGenerator

# 트위스트 생성기 초기화
twist_gen = TwistGenerator()

# 반전 생성
twist = twist_gen.generate_plot_twist("배신")

print(f"반전 유형: {twist['type']}")
print(f"반전 내용: {twist['twist']}")
print("\n복선:")
for foreshadow in twist['foreshadowing']:
    print(f"  - {foreshadow}")
```

### 랜덤 아이디어 생성

```python
from modules.ideas.title_generator import IdeaGenerator

# 아이디어 생성기 초기화
idea_gen = IdeaGenerator()

# 랜덤 아이디어 생성
idea = idea_gen.generate_random_idea()

print(f"컨셉: {idea['concept']}")
print(f"테마: {', '.join(idea['themes'])}")
print(f"세팅: {', '.join(idea['settings'])}")
print(f"주인공: {idea['protagonist']}")
print(f"훅: {idea['hook']}")

# 여러 아이디어 생성
ideas = idea_gen.generate_idea_batch(count=5)
print(f"\n총 {len(ideas)}개의 아이디어 생성됨")
```

## 데이터베이스 사용 예제

```python
from modules.database import DatabaseHandler

# 데이터베이스 초기화
db = DatabaseHandler("my_projects.db")

# 프로젝트 저장
project_id = db.save_project(
    name="나의 첫 소설",
    project_type="plot",
    content=plot  # 위에서 생성한 플롯
)

print(f"프로젝트 저장됨 (ID: {project_id})")

# 캐릭터 저장
char_id = db.save_character(project_id, character)
print(f"캐릭터 저장됨 (ID: {char_id})")

# 모든 프로젝트 조회
projects = db.get_projects()
for proj in projects:
    print(f"- {proj[1]} ({proj[2]})")

# 특정 프로젝트 조회
project = db.get_project(project_id)
print(f"\n프로젝트: {project[1]}")
```

## 통합 예제: 완전한 소설 설정 생성

```python
# 모든 모듈 임포트
from modules.webnovel.plot_generator import PlotGenerator
from modules.webnovel.character_generator import CharacterGenerator
from modules.webnovel.worldbuilding import WorldbuildingGenerator
from modules.ideas.title_generator import TitleGenerator
from modules.database import DatabaseHandler

# 1. 제목 생성
title_gen = TitleGenerator()
titles = title_gen.generate_title("판타지", 5)
selected_title = titles[0]
print(f"소설 제목: {selected_title}\n")

# 2. 세계관 구축
world_gen = WorldbuildingGenerator()
world = world_gen.generate_fantasy_world("신세계")
print(f"세계관: {world['name']}")
print(f"마법 시스템: {world['magic_system']['type']}\n")

# 3. 주인공 생성
char_gen = CharacterGenerator()
protagonist = char_gen.generate_character("한국어", "남성", 20, "판타지")
print(f"주인공: {protagonist['name']}")
print(f"성격: {protagonist['personality']['mbti']}\n")

# 4. 조연 생성
supporting = char_gen.generate_character("판타지", "여성", 22, "판타지")
print(f"조연: {supporting['name']}\n")

# 5. 플롯 생성
plot_gen = PlotGenerator()
plot = plot_gen.generate_plot("판타지")
print(f"플롯 주제: {plot['theme']}")
print(f"갈등: {plot['conflict']}\n")

# 6. 모두 데이터베이스에 저장
db = DatabaseHandler("my_novel.db")
project_id = db.save_project(
    name=selected_title,
    project_type="webnovel",
    content={
        "title": selected_title,
        "world": world,
        "plot": plot
    }
)

db.save_character(project_id, protagonist)
db.save_character(project_id, supporting)

print(f"모든 설정이 데이터베이스에 저장되었습니다! (프로젝트 ID: {project_id})")
```

## GUI 사용법

GUI를 사용하려면 디스플레이 서버가 있는 환경에서 다음 명령을 실행하세요:

```bash
python main.py
```

GUI에서는:
1. 좌측 메뉴에서 기능 선택
2. 필요한 옵션 설정
3. "생성" 버튼 클릭
4. 결과 확인 및 편집
5. "저장" 또는 "내보내기" 버튼으로 결과 저장

## 주의사항

- GUI는 Windows, macOS, Linux(X11/Wayland)에서만 작동합니다
- 헤드리스 환경에서는 위의 Python 코드 예제를 사용하세요
- 모든 기능은 오프라인에서 작동합니다 (AI API 불필요)
