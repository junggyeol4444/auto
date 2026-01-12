# YouTube Auto Content Generator - 사용 가이드

## 목차
1. [시작하기](#시작하기)
2. [GUI 사용법](#gui-사용법)
3. [프로그래밍 방식 사용](#프로그래밍-방식-사용)
4. [모듈별 사용법](#모듈별-사용법)
5. [문제 해결](#문제-해결)

## 시작하기

### 설치 및 설정

1. **저장소 클론**
   ```bash
   git clone https://github.com/junggyeol4444/auto.git
   cd auto
   ```

2. **가상 환경 생성 (권장)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **설정 검증**
   ```bash
   python setup.py
   ```

### YouTube API 설정 (선택사항)

YouTube 자동 업로드 기능을 사용하려면:

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성
3. YouTube Data API v3 활성화
4. OAuth 2.0 클라이언트 ID 생성
5. `credentials.json` 파일을 프로젝트 루트에 저장

## GUI 사용법

### 기본 사용

1. 애플리케이션 시작: `python main.py`
2. 콘텐츠 주제 입력
3. 채널 유형 선택 (뉴스/정보/스토리텔링)
4. TTS 엔진 선택
5. 옵션 설정
6. "콘텐츠 생성 시작" 클릭

### 출력 파일

`output/{주제명}/` 디렉토리에 저장:
- `script.txt`: 스크립트
- `audio.mp3`: 음성
- `video.mp4`: 비디오

## 프로그래밍 방식 사용

```python
from crawler import ContentCrawler
from content import ContentRestructurer
from tts import TTSManager
from video import VideoCreator

# 1. 크롤링
crawler = ContentCrawler()
content = crawler.crawl_content("AI", include_news=True, include_wiki=True)

# 2. 스크립트 생성
restructurer = ContentRestructurer()
script = restructurer.generate_script(content, "informational")

# 3. TTS 생성
tts = TTSManager(engine_type="gtts")
tts.text_to_speech(script, "audio.mp3")

# 4. 비디오 생성
video = VideoCreator()
video.create_simple_video("audio.mp3", "video.mp4")
```

자세한 내용은 전체 문서를 참조하세요.
