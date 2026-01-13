# AI Writing Assistant Suite - 아키텍처 문서

## 시스템 개요

AI Writing Assistant Suite는 모듈식 아키텍처로 설계된 Python 기반 데스크톱 애플리케이션입니다.

## 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────┐
│                     GUI Layer (customtkinter)            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ WebNovel Tab │  │Proofread Tab │  │  Manual Tab  │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
┌─────────┼──────────────────┼──────────────────┼─────────┐
│         ▼                  ▼                  ▼         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   WebNovel   │  │ Proofreading │  │    Manual    │  │
│  │   Generator  │  │    Checker   │  │  Generator   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                  │                  │         │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐  │
│  │  Character   │  │   Grammar    │  │   Template   │  │
│  │    Plot      │  │    Style     │  │  Structure   │  │
│  │  Dialogue    │  │ Consistency  │  │     FAQ      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                    Core Modules Layer                   │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────┐
│                   Utility Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │FileHandler   │  │ APIManager   │  │   Crawler    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────┐
│              External Dependencies                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │python-docx   │  │  OpenAI API  │  │  BeautifulS  │  │
│  │   PyPDF2     │  │Anthropic API │  │   oup4       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 디렉토리 구조

```
Writing_Assistant/
│
├── main.py                      # 애플리케이션 엔트리 포인트
├── config.json                  # 설정 파일
├── requirements.txt             # Python 의존성
├── README.md                    # 프로젝트 문서
├── USER_GUIDE.md               # 사용자 가이드
├── ARCHITECTURE.md             # 아키텍처 문서
├── test_basic.py               # 기본 테스트 스크립트
│
├── modules/                    # 핵심 기능 모듈
│   ├── webnovel/              # 웹소설 생성 모듈
│   │   ├── __init__.py
│   │   ├── generator.py       # 메인 생성기
│   │   ├── character.py       # 캐릭터 생성
│   │   ├── plot.py            # 플롯 구성
│   │   └── dialogue.py        # 대화 생성
│   │
│   ├── proofreading/          # 교정 모듈
│   │   ├── __init__.py
│   │   ├── grammar_check.py   # 문법 검사
│   │   ├── style_check.py     # 스타일 검사
│   │   └── consistency.py     # 일관성 검사
│   │
│   └── manual/                # 매뉴얼 생성 모듈
│       ├── __init__.py
│       ├── template_manager.py    # 템플릿 관리
│       ├── structure_generator.py # 구조 생성
│       └── faq_generator.py       # FAQ 생성
│
├── templates/                 # JSON 템플릿
│   ├── webnovel/             # 장르별 템플릿
│   │   ├── fantasy.json      # 판타지
│   │   ├── romance.json      # 로맨스
│   │   ├── martial_arts.json # 무협
│   │   └── modern.json       # 현대물
│   │
│   └── manual/               # 매뉴얼 템플릿
│       ├── product.json      # 제품 설명서
│       └── software.json     # 소프트웨어 매뉴얼
│
├── gui/                      # GUI 컴포넌트
│   ├── __init__.py
│   ├── main_window.py        # 메인 윈도우
│   ├── webnovel_tab.py       # 웹소설 탭
│   ├── proofreading_tab.py   # 교정 탭
│   ├── manual_tab.py         # 매뉴얼 탭
│   ├── editor_window.py      # 에디터 윈도우
│   └── settings_window.py    # 설정 윈도우
│
├── utils/                    # 유틸리티
│   ├── __init__.py
│   ├── file_handler.py       # 파일 I/O
│   ├── api_manager.py        # AI API 관리
│   └── crawler.py            # 웹 크롤링
│
└── output/                   # 생성된 파일
    ├── novels/               # 소설 파일
    ├── proofread/            # 교정된 파일
    └── manuals/              # 매뉴얼 파일
```

## 주요 컴포넌트 설명

### 1. GUI Layer

#### MainWindow (`gui/main_window.py`)
- 애플리케이션의 메인 윈도우
- 탭 뷰 관리 (웹소설, 교정, 매뉴얼)
- 설정 및 정보 메뉴

#### WebNovelTab (`gui/webnovel_tab.py`)
- 웹소설 생성 인터페이스
- 장르 선택, 파라미터 설정
- 생성 결과 표시 및 저장

#### ProofreadingTab (`gui/proofreading_tab.py`)
- 교정 인터페이스
- 원본/수정본 비교 뷰
- 오류 목록 표시

#### ManualTab (`gui/manual_tab.py`)
- 매뉴얼 생성 인터페이스
- 제품/소프트웨어 정보 입력
- 미리보기 및 저장

### 2. Core Modules Layer

#### WebNovel Module (`modules/webnovel/`)

**generator.py**
- 메인 생성 로직
- 템플릿 기반 생성
- AI API 통합 (선택)

**character.py**
- 캐릭터 자동 생성
- 이름, 성격, 능력 등
- 역할별 아키타입

**plot.py**
- 플롯 구조 생성
- 3막 구조
- 회차별 개요

**dialogue.py**
- 대화 생성
- 캐릭터 간 상호작용
- 감정 표현

#### Proofreading Module (`modules/proofreading/`)

**grammar_check.py**
- 맞춤법 검사
- 띄어쓰기 검사
- 문법 오류 감지

**style_check.py**
- 반복 표현 감지
- 문장 길이 검사
- 어색한 표현 제안

**consistency.py**
- 캐릭터 이름 일관성
- 시점 일관성
- 설정 모순 검사

#### Manual Module (`modules/manual/`)

**template_manager.py**
- 템플릿 로드 및 관리
- 템플릿 형식화

**structure_generator.py**
- 매뉴얼 구조 생성
- 섹션 자동 구성

**faq_generator.py**
- FAQ 자동 생성
- 일반적인 질문/답변

### 3. Utility Layer

#### FileHandler (`utils/file_handler.py`)
- TXT, DOCX 읽기/쓰기
- JSON 처리
- 파일 형식 변환

#### APIManager (`utils/api_manager.py`)
- OpenAI API 통합
- Anthropic API 통합
- API 키 관리

#### Crawler (`utils/crawler.py`)
- 웹 페이지 가져오기
- HTML 파싱
- 텍스트 추출

## 데이터 플로우

### 웹소설 생성 플로우

```
1. 사용자 입력 (제목, 장르, 파라미터)
   ↓
2. WebNovelTab → WebNovelGenerator
   ↓
3. 템플릿 로드 (JSON)
   ↓
4. 캐릭터 생성 (CharacterGenerator)
   ↓
5. 플롯 생성 (PlotGenerator)
   ↓
6. 회차별 내용 생성
   - 템플릿 기반 또는
   - AI API 사용 (선택)
   ↓
7. 결과 표시 및 저장
```

### 교정 플로우

```
1. 파일 업로드 또는 텍스트 입력
   ↓
2. ProofreadingTab → Checkers
   ↓
3. 선택된 검사 실행
   - GrammarChecker
   - StyleChecker
   - ConsistencyChecker
   ↓
4. 오류 수집
   ↓
5. 수정안 생성
   ↓
6. 결과 표시 (원본/수정본 비교)
```

### 매뉴얼 생성 플로우

```
1. 매뉴얼 정보 입력
   ↓
2. ManualTab → StructureGenerator
   ↓
3. 템플릿 로드
   ↓
4. 섹션별 내용 생성
   - 제품/소프트웨어 정보
   - FAQ 생성
   ↓
5. 미리보기 표시
   ↓
6. DOCX/TXT 저장
```

## 템플릿 시스템

### 구조

템플릿은 JSON 형식으로 저장되며 다음 요소를 포함합니다:

```json
{
  "genre": "장르명",
  "plot_templates": {
    "opening": ["도입부 템플릿..."],
    "development": ["전개부 템플릿..."],
    "climax": ["절정부 템플릿..."],
    "resolution": ["결말부 템플릿..."]
  },
  "character_archetypes": {
    "protagonist": {...},
    "heroine": {...}
  },
  "scene_templates": {...}
}
```

### 변수 치환

템플릿 내 변수는 `{변수명}` 형식으로 표시되며, 생성 시 실제 값으로 치환됩니다:

- `{protagonist}` → 주인공 이름
- `{event}` → 사건
- `{place}` → 장소
- 등등...

## AI API 통합

### OpenAI Integration

```python
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[...],
    max_tokens=2000
)
```

### Anthropic Integration

```python
response = anthropic.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=2000,
    messages=[...]
)
```

### Fallback 전략

1. AI API 사용 (활성화 시)
2. 템플릿 기반 생성 (백업)

## 확장성

### 새 장르 추가

1. `templates/webnovel/` 에 새 JSON 파일 생성
2. 플롯 템플릿, 캐릭터 아키타입 정의
3. GUI에 자동으로 표시됨

### 새 검사 추가

1. `modules/proofreading/` 에 새 체커 클래스 생성
2. `check_all()` 메서드 구현
3. ProofreadingTab에서 호출

### 새 매뉴얼 유형 추가

1. `templates/manual/` 에 새 템플릿 생성
2. StructureGenerator에 생성 메서드 추가
3. ManualTab에서 옵션 추가

## 성능 고려사항

- **템플릿 캐싱**: 템플릿은 한 번만 로드
- **비동기 생성**: GUI 응답성 유지 (향후 개선)
- **메모리 관리**: 대용량 텍스트 처리 시 청크 단위 처리

## 보안

- API 키는 config.json에 저장 (Git에서 제외)
- 민감 정보 암호화 (향후 개선)

## 테스트

- `test_basic.py`: 기본 기능 테스트
- 수동 테스트: GUI를 통한 통합 테스트

## 향후 계획

1. **플러그인 시스템**: 사용자 정의 모듈 추가
2. **클라우드 동기화**: 설정 및 템플릿 클라우드 저장
3. **협업 기능**: 여러 사용자 공동 작업
4. **AI 모델 통합**: 로컬 AI 모델 지원
5. **웹 버전**: 브라우저 기반 인터페이스

---

© 2024 AI Writing Assistant Suite
