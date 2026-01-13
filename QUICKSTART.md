# 빠른 시작 가이드 (Quick Start Guide)

## 5분 안에 시작하기

### 1단계: 설치 (2분)

```bash
# 저장소 클론
git clone https://github.com/junggyeol4444/auto.git
cd auto

# 의존성 설치
pip install -r requirements.txt
```

### 2단계: 실행 (1분)

#### GUI 사용 (권장)
```bash
python main.py
```

#### 또는 Python 코드로 직접 사용
```python
from modules.webnovel.plot_generator import PlotGenerator
from modules.webnovel.character_generator import CharacterGenerator

# 플롯 생성
plot_gen = PlotGenerator()
plot = plot_gen.generate_plot("판타지")
print(f"테마: {plot['theme']}")

# 캐릭터 생성
char_gen = CharacterGenerator()
character = char_gen.generate_character()
print(f"캐릭터: {character['name']}")
```

### 3단계: 생성 시작 (2분)

1. 좌측 메뉴에서 "📖 웹소설" 클릭
2. "📖 플롯 생성" 클릭
3. 장르 선택 (예: 판타지)
4. "생성" 버튼 클릭
5. 결과 확인!

---

## 주요 기능 바로가기

### 웹소설 작가라면
```python
# 완전한 소설 설정 생성
from modules.webnovel.plot_generator import PlotGenerator
from modules.webnovel.character_generator import CharacterGenerator
from modules.ideas.title_generator import TitleGenerator

# 제목
title_gen = TitleGenerator()
title = title_gen.generate_title("판타지", 1)[0]

# 주인공
char_gen = CharacterGenerator()
hero = char_gen.generate_character("한국어", "남성", 20)

# 플롯
plot_gen = PlotGenerator()
plot = plot_gen.generate_plot("판타지")

print(f"제목: {title}")
print(f"주인공: {hero['name']} ({hero['personality']['mbti']})")
print(f"테마: {plot['theme']}")
```

### 시나리오 작가라면
```python
from modules.scenario.scenario_generator import ScenarioGenerator

scenario_gen = ScenarioGenerator()

# 영화 시나리오
movie = scenario_gen.generate_movie_scenario("액션", 120)
print(f"영화: {movie['title']} ({movie['duration']})")

# 드라마 시놉시스
drama = scenario_gen.generate_drama_synopsis(16)
print(f"드라마: {drama['title']} ({drama['episodes']}부작)")
```

### 게임 개발자라면
```python
from modules.game.quest_generator import QuestGenerator, NPCGenerator, DungeonDesigner

# 퀘스트
quest_gen = QuestGenerator()
quest = quest_gen.generate_main_quest(10)
print(f"퀘스트: {quest['name']}")

# NPC
npc_gen = NPCGenerator()
npc = npc_gen.generate_npc("상인")
print(f"NPC: {npc['name']} ({npc['type']})")

# 던전
dungeon_gen = DungeonDesigner()
dungeon = dungeon_gen.generate_dungeon("어둠의 던전", 5)
print(f"던전: {dungeon['name']} ({dungeon['difficulty']})")
```

### 아이디어가 필요하다면
```python
from modules.ideas.title_generator import TitleGenerator, IdeaGenerator

# 제목 10개 생성
title_gen = TitleGenerator()
titles = title_gen.generate_title("판타지", 10)
for i, title in enumerate(titles, 1):
    print(f"{i}. {title}")

# 랜덤 아이디어
idea_gen = IdeaGenerator()
idea = idea_gen.generate_random_idea()
print(f"\n아이디어: {idea['concept']}")
```

---

## 문제 해결

### GUI가 실행되지 않는다면?
GUI는 디스플레이 서버가 필요합니다. 헤드리스 환경이라면 Python 코드로 직접 사용하세요.

```bash
# 테스트 실행으로 확인
python test_modules.py
```

### 의존성 설치 오류
```bash
# pip 업그레이드
pip install --upgrade pip

# 다시 설치
pip install -r requirements.txt
```

### tkinter 오류 (Linux)
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

---

## 다음 단계

1. **더 많은 예제**: `EXAMPLES.md` 파일 참조
2. **전체 문서**: `README.md` 파일 참조
3. **프로젝트 상세**: `PROJECT_SUMMARY.md` 파일 참조

---

## 유용한 팁

### 여러 개 한번에 생성
```python
# 캐릭터 5명 생성
characters = [char_gen.generate_character() for _ in range(5)]

# 제목 20개 생성
titles = title_gen.generate_title("판타지", 20)

# 퀘스트 10개 생성
quests = [quest_gen.generate_main_quest(i) for i in range(1, 11)]
```

### 데이터베이스에 저장
```python
from modules.database import DatabaseHandler

db = DatabaseHandler("my_project.db")

# 프로젝트 저장
project_id = db.save_project("내 소설", "plot", plot)

# 캐릭터 저장
for char in characters:
    db.save_character(project_id, char)
```

### 파일로 내보내기
```python
# 텍스트 파일로 저장
with open("output/my_plot.txt", "w", encoding="utf-8") as f:
    f.write(f"제목: {title}\n\n")
    f.write(f"주인공: {hero['name']}\n\n")
    f.write(f"테마: {plot['theme']}\n")
```

---

## 도움말

- **버그 리포트**: GitHub Issues
- **기능 요청**: GitHub Issues
- **문서**: 프로젝트 폴더의 Markdown 파일들

---

**즐거운 창작 되세요! 🎉**
