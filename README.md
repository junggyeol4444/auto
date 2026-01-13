# YouTube Auto Content Generator

자동화된 YouTube 콘텐츠 생성 프로그램입니다. 웹 크롤링부터 영상 제작, YouTube 업로드까지 완전 자동화합니다.

## 주요 기능

### 1. 콘텐츠 수집 (웹 크롤링)
- **뉴스 사이트 크롤링**: 네이버 뉴스, 다음 뉴스
- **위키백과/나무위키 크롤링**: 정보성 콘텐츠 수집
- 구조화된 데이터 저장

### 2. 콘텐츠 재구성
- **템플릿 기반 스크립트 생성**:
  - 뉴스 리포트 스타일
  - 정보/교육 스타일
  - 스토리텔링 스타일
- 자연스러운 텍스트 구성

### 3. TTS (음성 생성)
- **로컬 TTS 엔진**:
  - gTTS (Google Text-to-Speech)
  - pyttsx3 (오프라인 TTS)
- **맞춤형 TTS**: Coqui TTS 등 커스텀 모델 지원
- 음성 모델 저장 및 불러오기

### 4. 영상 제작
- MoviePy를 활용한 자동 영상 편집
- 스크립트 음성과 배경 이미지/영상 결합
- 텍스트 오버레이 지원

### 5. YouTube API 연동
- 자동 업로드
- SEO 최적화된 메타데이터 생성
- 제목, 설명, 태그 자동 설정

### 6. GUI 인터페이스
- CustomTkinter 기반 직관적인 UI
- 주제 및 채널 유형 선택
- TTS 엔진 선택 (로컬/맞춤형)
- 실시간 진행 상황 표시

## 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/junggyeol4444/auto.git
cd auto
```

### 2. 가상 환경 생성 (권장)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 추가 설정

#### YouTube API 설정
1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트 생성
2. YouTube Data API v3 활성화
3. OAuth 2.0 클라이언트 ID 생성
4. `credentials.json` 파일을 프로젝트 루트에 저장

#### 맞춤형 TTS 사용 (선택사항)
```bash
# Coqui TTS 설치
pip install TTS
```

## 사용 방법

### GUI 모드 (권장)
```bash
python main.py
```

GUI에서:
1. 콘텐츠 주제 입력
2. 채널 유형 선택 (뉴스/정보/스토리텔링)
3. TTS 엔진 선택
4. 옵션 설정 (뉴스 크롤링, 위키 크롤링, YouTube 업로드)
5. "콘텐츠 생성 시작" 버튼 클릭

### 프로그래밍 방식

```python
from src.crawler import ContentCrawler
from src.content import ContentRestructurer
from src.tts import TTSManager
from src.video import VideoCreator
from src.youtube import YouTubeUploader

# 1. 콘텐츠 크롤링
crawler = ContentCrawler()
content = crawler.crawl_content("인공지능", include_news=True, include_wiki=True)

# 2. 스크립트 생성
restructurer = ContentRestructurer()
script = restructurer.generate_script(content, template_type="informational")
metadata = restructurer.generate_metadata(content, script)

# 3. TTS 음성 생성
tts = TTSManager(engine_type="gtts")
tts.text_to_speech(script, "output/audio.mp3")

# 4. 비디오 생성
video_creator = VideoCreator()
video_creator.create_simple_video("output/audio.mp3", "output/video.mp4")

# 5. YouTube 업로드
uploader = YouTubeUploader()
video_id = uploader.upload_video("output/video.mp4", metadata)
print(f"Video uploaded: https://www.youtube.com/watch?v={video_id}")
```

## 프로젝트 구조

```
auto/
├── main.py                    # 애플리케이션 진입점
├── requirements.txt           # 의존성 목록
├── README.md                  # 이 파일
├── .gitignore                # Git 제외 파일
├── config/                    # 설정 파일
│   └── default_config.json
├── templates/                 # 스크립트 템플릿
│   ├── news_report.txt
│   ├── informational.txt
│   └── storytelling.txt
└── src/                       # 소스 코드
    ├── crawler/               # 웹 크롤링 모듈
    │   ├── __init__.py
    │   └── web_crawler.py
    ├── content/               # 콘텐츠 재구성 모듈
    │   ├── __init__.py
    │   └── restructure.py
    ├── tts/                   # TTS 모듈
    │   ├── __init__.py
    │   └── tts_engine.py
    ├── video/                 # 비디오 생성 모듈
    │   ├── __init__.py
    │   └── video_creator.py
    ├── youtube/               # YouTube API 모듈
    │   ├── __init__.py
    │   └── uploader.py
    └── gui/                   # GUI 모듈
        ├── __init__.py
        └── main_window.py
```

## 출력 파일

생성된 콘텐츠는 `output/{topic}/` 디렉토리에 저장됩니다:
- `script.txt`: 생성된 스크립트
- `audio.mp3`: TTS로 생성된 음성
- `video.mp4`: 최종 비디오 파일

## 주의사항

1. **웹 크롤링**: 웹사이트 이용 약관을 준수하고, 적절한 딜레이를 두어 서버에 부담을 주지 않도록 합니다.
2. **YouTube API**: 일일 할당량 제한이 있으므로 주의하세요.
3. **저작권**: 크롤링한 콘텐츠의 저작권을 확인하고, 공정 이용 원칙을 준수하세요.
4. **TTS 라이선스**: 사용하는 TTS 엔진의 라이선스를 확인하세요.

## 문제 해결

### MoviePy 설치 오류
```bash
# ImageMagick 설치 (선택사항, 텍스트 오버레이에 필요)
# Windows: https://imagemagick.org/script/download.php
# macOS: brew install imagemagick
# Linux: sudo apt-get install imagemagick
```

### YouTube 업로드 오류
- `credentials.json` 파일이 올바른 위치에 있는지 확인
- OAuth 동의 화면 설정이 완료되었는지 확인
- 첫 실행 시 브라우저를 통한 인증 필요

### TTS 한글 음성 문제
- gTTS는 한국어를 지원합니다 (`lang='ko'`)
- pyttsx3는 시스템에 한국어 TTS 엔진이 설치되어 있어야 합니다

## 라이선스

이 프로젝트는 교육 목적으로 제공됩니다. 사용 시 관련 법규와 윤리를 준수해 주세요.

## 기여

버그 리포트, 기능 제안, Pull Request를 환영합니다!

## 연락처

문의사항이 있으시면 이슈를 등록해 주세요.