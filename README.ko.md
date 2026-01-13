# YouTube 자동 콘텐츠 생성기

한국어 뉴스/위키 소스를 크롤링하고, 템플릿을 사용하여 스크립트로 재구성하고, 음성을 합성하고, 비디오를 생성하고, SEO 최적화된 메타데이터와 함께 YouTube에 업로드하는 완전한 자동화 파이프라인을 구축합니다.

## 아키텍처

**모듈식 아키텍처의 6개 핵심 모듈:**
- `crawler/` - 웹 스크래핑 (네이버/다음 뉴스, 위키백과/나무위키)
- `content/` - 3가지 템플릿 유형을 통한 스크립트 생성 (뉴스, 정보성, 스토리텔링)
- `tts/` - 다중 엔진 TTS (gTTS, pyttsx3, Coqui TTS 프레임워크)
- `video/` - MoviePy 기반 오디오 동기화 비디오 생성
- `youtube/` - OAuth 2.0을 사용한 YouTube Data API v3 업로드
- `gui/` - 실시간 진행 상황을 표시하는 CustomTkinter 인터페이스

## 사용법

**GUI 모드:**
```bash
python main.py
```

**프로그래밍 방식 API:**
```python
from crawler import ContentCrawler
from content import ContentRestructurer
from tts import TTSManager
from video import VideoCreator

crawler = ContentCrawler()
content = crawler.crawl_content("AI", include_news=True, include_wiki=True)

restructurer = ContentRestructurer()
script = restructurer.generate_script(content, template_type="informational")

tts = TTSManager(engine_type="gtts")
tts.text_to_speech(script, "audio.mp3")

video = VideoCreator()
video.create_simple_video("audio.mp3", "video.mp4")
```

## 구현 세부사항

- **URL 인코딩**: `urllib.parse.urlencode`를 통한 안전한 웹 요청
- **헬퍼 함수**: 중복 제거 (예: TTS의 `ensure_directory()`)
- **명명된 상수**: 매직 넘버 제거 (`UPLOAD_CHUNK_SIZE = 1024 * 1024`)
- **최상위 가져오기**: GUI에서 스레딩 오버헤드 방지
- **MoviePy 2.x 호환성**: 올바른 모듈 경로 사용

## 테스트 및 보안

- 통합 테스트: 6/6 통과
- CodeQL 스캔: 취약점 0개
- 모든 모듈 독립적으로 검증됨

## 문서

전체 문서 제공: README, 빠른 시작, 사용자 가이드, API 참조, 기여 가이드라인, 변경 로그, 구현 보고서.

## 주요 기능

### 1. 콘텐츠 수집 (웹 크롤링)
- 뉴스 사이트 크롤링 (네이버, 다음)
- 위키백과/나무위키 크롤링
- 구조화된 데이터 저장

### 2. 콘텐츠 재구성
- 템플릿 기반 스크립트 생성
- 3가지 스타일: 뉴스 리포트, 정보/교육, 스토리텔링
- 자연스러운 한국어 텍스트 구성

### 3. TTS 음성 생성
- 기본 로컬 TTS (gTTS, pyttsx3) 지원
- 사용자 맞춤형 TTS 모델 지원 (Coqui TTS)
- 음성 모델 저장 및 불러오기 기능

### 4. 영상 제작
- 스크립트 음성과 스톡 영상/이미지 결합
- MoviePy 라이브러리를 활용한 자동 편집
- 오디오-비디오 자동 동기화

### 5. YouTube API 연동
- 메타데이터 (제목, 설명, 태그) SEO 최적화
- OAuth 2.0 인증
- 자동 업로드 및 진행 상황 추적

### 6. GUI 제공
- 주제와 채널 유형을 선택할 수 있는 직관적인 사용자 인터페이스
- CustomTkinter 기반 현대적인 디자인
- 실시간 진행 상황 및 상태 업데이트

## 설치 방법

```bash
# 저장소 클론
git clone https://github.com/junggyeol4444/auto.git
cd auto

# 의존성 설치
pip install -r requirements.txt

# 설정 검증
python setup.py

# 애플리케이션 실행
python main.py
```

## 프로젝트 구조

```
auto/
├── src/                      # 소스 코드
│   ├── crawler/              # 웹 크롤링
│   ├── content/              # 콘텐츠 재구성
│   ├── tts/                  # 텍스트 음성 변환
│   ├── video/                # 비디오 생성
│   ├── youtube/              # YouTube API
│   └── gui/                  # 사용자 인터페이스
├── templates/                # 스크립트 템플릿
├── config/                   # 설정 파일
├── docs/                     # 문서
├── main.py                   # 애플리케이션 진입점
├── examples.py               # 사용 예제
├── setup.py                  # 설정 검증 도구
└── requirements.txt          # 의존성 목록
```

## 주요 종속성

- `requests`, `beautifulsoup4`, `lxml` - 웹 스크래핑
- `gTTS`, `pyttsx3` - 텍스트 음성 변환
- `moviepy` - 비디오 편집
- `google-api-python-client` - YouTube API
- `customtkinter` - GUI 프레임워크
- `pillow` - 이미지 처리

## 테스트 상태

✅ 모든 모듈 가져오기 성공  
✅ 콘텐츠 재구성기 테스트 완료  
✅ TTS 모듈 테스트 완료  
✅ 비디오 생성기 테스트 완료  
✅ YouTube 업로더 테스트 완료  
✅ GUI 모듈 테스트 완료  
✅ 통합 테스트: 6/6 통과  
✅ 보안 스캔: 취약점 0개  

## 라이선스

MIT License - 자세한 내용은 LICENSE 파일을 참조하세요.

## 기여

버그 리포트, 기능 제안, Pull Request를 환영합니다!

## 지원

- [이슈 제보](https://github.com/junggyeol4444/auto/issues)
- 문서는 `docs/` 디렉토리에서 확인하세요
