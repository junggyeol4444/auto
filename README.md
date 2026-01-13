# AI Writing Assistant Suite

웹소설 대필, 소설 교정, 매뉴얼 작성을 지원하는 올인원 AI 작문 도우미입니다.

## 주요 기능

### 1. 웹소설 대필
- **장르별 스토리 생성**: 판타지, 로맨스, 무협, 현대물
- **캐릭터 자동 생성**: 이름, 나이, 직업, 외모, 성격, 능력, 배경, 목표
- **플롯 구성 자동화**: 기승전결, 3막 구조
- **회차별 집필**: 1회당 3000-5000자
- **대화 및 장면 묘사 자동 생성**

### 2. 소설/시나리오 교정
- **맞춤법 검사**: 한글 맞춤법 검사
- **띄어쓰기 교정**
- **문법 오류 감지**: 주어-서술어 호응, 시제 일관성
- **문장 다듬기**: 어색한 표현 수정
- **반복 표현 감지**
- **캐릭터 일관성 검사**: 이름, 설정 오류
- **시점 일관성 검사**: 1인칭/3인칭 혼용

### 3. 매뉴얼 작성
- **제품 사용 설명서** 자동 생성
- **소프트웨어 매뉴얼** 자동 생성
- **FAQ 자동 생성**
- **목차 자동 생성**
- **DOCX 및 TXT 형식 지원**

## 설치 방법

### 필수 요구사항
- Python 3.8 이상
- Windows 10 이상 (Linux/Mac도 지원)

### 설치 단계

1. 저장소 클론
```bash
git clone https://github.com/junggyeol4444/auto.git
cd auto
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 실행
```bash
python main.py
```

## 사용 방법

### 웹소설 대필

1. **웹소설 대필** 탭 선택
2. 장르 선택 (판타지, 로맨스, 무협, 현대물)
3. 제목 입력
4. 주인공 정보 입력 (선택)
5. 회차 수 및 분량 설정
6. 줄거리 개요 입력 (선택)
7. **생성 시작** 버튼 클릭
8. 생성된 소설 확인 및 저장

### 소설 교정

1. **소설 교정** 탭 선택
2. 파일 업로드 또는 텍스트 직접 입력
3. 교정 옵션 선택 (맞춤법, 문법, 스타일, 일관성)
4. **교정 시작** 버튼 클릭
5. 오류 목록 확인
6. 수정본 확인 및 저장

### 매뉴얼 작성

1. **매뉴얼 작성** 탭 선택
2. 유형 선택 (제품 / 소프트웨어)
3. 제품명 및 버전 입력
4. 주요 기능 입력
5. 사용 방법 입력
6. **매뉴얼 생성** 버튼 클릭
7. 미리보기 확인 후 DOCX 또는 TXT로 저장

## 설정

⚙️ 설정 버튼을 클릭하여:
- **AI API 설정**: OpenAI 또는 Anthropic API 키 입력 (고품질 생성)
- **출력 설정**: 기본 저장 형식 선택
- **웹소설 설정**: 기본 회당 분량 설정

## 기술 스택

- **GUI**: customtkinter (모던 UI)
- **자연어 처리**: konlpy, nltk
- **AI API**: OpenAI GPT-4, Anthropic Claude (선택)
- **문법 검사**: py-hanspell, language-tool-python
- **웹 크롤링**: requests, BeautifulSoup4
- **문서 처리**: python-docx, PyPDF2

## 디렉토리 구조

```
Writing_Assistant/
├── main.py                 # 메인 실행 파일
├── config.json            # 설정 파일
├── requirements.txt       # 의존성 목록
├── README.md             # 사용 설명서
│
├── modules/              # 핵심 기능 모듈
│   ├── webnovel/        # 웹소설 생성
│   ├── proofreading/    # 교정 기능
│   └── manual/          # 매뉴얼 생성
│
├── templates/           # 장르별 템플릿
│   ├── webnovel/
│   └── manual/
│
├── gui/                 # GUI 컴포넌트
│   ├── main_window.py
│   ├── webnovel_tab.py
│   ├── proofreading_tab.py
│   ├── manual_tab.py
│   └── settings_window.py
│
├── utils/               # 유틸리티
│   ├── file_handler.py
│   ├── api_manager.py
│   └── crawler.py
│
└── output/              # 생성된 파일
    ├── novels/
    ├── proofread/
    └── manuals/
```

## AI API 사용 (선택)

AI API를 사용하면 더욱 고품질의 컨텐츠를 생성할 수 있습니다.

### OpenAI API
1. [OpenAI 웹사이트](https://platform.openai.com/)에서 API 키 발급
2. 설정에서 API 키 입력
3. "AI API 사용" 체크

### Anthropic API
1. [Anthropic 웹사이트](https://www.anthropic.com/)에서 API 키 발급
2. 설정에서 API 키 입력
3. "AI API 사용" 체크

> 참고: AI API 없이도 템플릿 기반 생성이 가능합니다.

## 파일 형식

### 입력 지원
- TXT (텍스트 파일)
- DOCX (워드 문서)

### 출력 지원
- TXT (텍스트 파일)
- DOCX (워드 문서)

## 문제 해결

### 프로그램이 실행되지 않음
- Python 버전 확인 (3.8 이상)
- 의존성 재설치: `pip install -r requirements.txt`

### GUI가 표시되지 않음
- customtkinter 설치 확인: `pip install customtkinter`

### 맞춤법 검사 오류
- py-hanspell 설치 확인: `pip install py-hanspell`
- 인터넷 연결 확인 (API 사용 시)

## 라이선스

© 2024 All rights reserved.

## 기여

이슈 및 풀 리퀘스트를 환영합니다!

## 문의

문제가 발생하거나 제안 사항이 있으시면 이슈를 등록해주세요.