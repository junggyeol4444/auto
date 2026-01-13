# Streamer Automation Suite

트위치, 유튜브, 치지직 스트리머를 위한 올인원 자동화 도구

## 🎯 주요 기능

### 📱 채팅 관리
- **욕설 필터**: 한국어, 영어, 일본어 욕설 자동 감지 및 차단
- **스팸 감지**: 반복 메시지, 과도한 링크 자동 차단
- **실시간 번역**: 다국어 채팅 자동 번역 (한/영/일/중)
- **채팅 통계**: 시청자 수, 채팅 활성도, 인기 단어 분석

### 🎬 클립 & 하이라이트
- **자동 하이라이트 감지**: 킬, 웃음, 채팅 폭발, 볼륨 급증 감지
- **자동 클립 생성**: 하이라이트 순간 자동 클립 생성 (로컬 저장 + Twitch API)
- **쇼츠 자동 변환**: 클립을 9:16 쇼츠 형식으로 자동 변환

### 🎮 인터랙션
- **미니게임 봇**: 가위바위보, 주사위, 예측 게임, 랜덤 뽑기
- **포인트 시스템**: 시청 시간 기반 포인트 지급, 리더보드
- **음악 요청**: !sr 명령어로 YouTube 음악 요청 및 재생

### 📊 최적화
- **제목 최적화**: SEO 친화적 + 클릭 유도 제목 자동 생성
- **태그 생성**: 자동 태그 및 해시태그 생성
- **썸네일 생성**: 영상에서 자동 썸네일 추출

### 📤 업로드 & 공유
- **YouTube 업로드**: 영상 자동 업로드 (예약 기능 포함)
- **쇼츠 업로드**: YouTube Shorts 자동 업로드
- **소셜 미디어**: Twitter, Discord 자동 알림 및 공유

## 🚀 설치 방법

### 1. 필수 요구사항
- Python 3.8 이상
- FFmpeg (영상 처리용)
- Windows 10/11 (권장)

### 2. Python 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. FFmpeg 설치
**Windows:**
1. https://ffmpeg.org/download.html 에서 다운로드
2. 환경 변수 PATH에 추가

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### 4. 설정 파일 수정
`config.json` 파일을 열어 다음 정보를 입력하세요:

```json
{
  "twitch": {
    "client_id": "YOUR_TWITCH_CLIENT_ID",
    "client_secret": "YOUR_TWITCH_CLIENT_SECRET",
    "oauth_token": "YOUR_TWITCH_OAUTH_TOKEN",
    "channel": "YOUR_CHANNEL_NAME"
  },
  "youtube": {
    "client_secrets_file": "client_secrets.json"
  }
}
```

#### Twitch 설정:
1. https://dev.twitch.tv/console/apps 접속
2. 새 애플리케이션 등록
3. Client ID와 Client Secret 복사
4. OAuth Token: https://twitchtokengenerator.com/ 에서 생성

#### YouTube 설정:
1. https://console.cloud.google.com/ 접속
2. YouTube Data API v3 활성화
3. OAuth 2.0 클라이언트 ID 생성
4. `client_secrets.json` 파일 다운로드

## 📖 사용 방법

### 기본 실행
```bash
python main.py
```

### GUI 사용법

#### 1. 대시보드 탭
- **모니터링 시작**: 실시간 채팅 모니터링 및 하이라이트 감지 시작
- **현재 시청자**: 실시간 시청자 수 표시
- **하이라이트 목록**: 감지된 하이라이트 실시간 표시

#### 2. 채팅 관리 탭
- **욕설 필터 ON/OFF**: 욕설 차단 기능 토글
- **스팸 감지 ON/OFF**: 스팸 감지 기능 토글
- **실시간 번역 ON/OFF**: 채팅 번역 기능 토글
- **차단된 메시지 로그**: 차단된 메시지 실시간 확인

#### 3. 클립 관리 탭
- **하이라이트 감지 설정**: 킬/웃음/채팅폭발 감지 ON/OFF
- **생성된 클립**: 자동 생성된 클립 목록
- **수동 클립 생성**: 버튼 클릭으로 현재 순간 클립 생성

#### 4. 업로드 탭
- **제목/설명 입력**: 업로드할 영상 정보 입력
- **YouTube 업로드**: 일반 영상 업로드
- **쇼츠 업로드**: 쇼츠 형식 업로드

#### 5. 설정 탭
- API 키 및 인증 정보 관리

### 채팅 명령어

#### 미니게임
- `!가위바위보 [가위/바위/보]` - 가위바위보 게임
- `!주사위 [개수]` - 주사위 굴리기 (1-5개)
- `!예측 [승리/패배]` - 게임 결과 예측

#### 음악
- `!sr [곡명]` - 음악 요청 (YouTube 검색)
- `!스킵` - 현재 곡 스킵 (관리자 전용)

#### 포인트
- `!포인트` - 내 포인트 확인
- `!순위` - 포인트 순위 확인

## 📁 프로젝트 구조

```
Streamer_Automation/
├── main.py                 # 메인 애플리케이션
├── config.json            # 설정 파일
├── requirements.txt       # 의존성 패키지
│
├── modules/
│   ├── chat/             # 채팅 모듈
│   │   ├── moderator.py      # 모더레이션
│   │   ├── translator.py     # 번역
│   │   └── stats.py          # 통계
│   │
│   ├── clip/             # 클립 모듈
│   │   ├── highlight_detector.py  # 하이라이트 감지
│   │   ├── clip_creator.py        # 클립 생성
│   │   └── shorts_generator.py    # 쇼츠 생성
│   │
│   ├── bot/              # 봇 모듈
│   │   ├── minigame.py       # 미니게임
│   │   ├── points.py         # 포인트 시스템
│   │   └── music_player.py   # 음악 플레이어
│   │
│   ├── optimization/     # 최적화 모듈
│   │   ├── title_optimizer.py   # 제목 최적화
│   │   ├── tag_generator.py     # 태그 생성
│   │   └── thumbnail_creator.py # 썸네일 생성
│   │
│   └── upload/           # 업로드 모듈
│       ├── youtube_uploader.py  # YouTube 업로드
│       ├── shorts_uploader.py   # 쇼츠 업로드
│       └── social_share.py      # 소셜 미디어
│
├── gui/
│   └── main_window.py    # GUI 메인 윈도우
│
├── data/
│   ├── badwords.txt      # 금지어 목록
│   ├── keywords.txt      # 하이라이트 키워드
│   └── points.db         # 포인트 데이터베이스
│
└── output/
    ├── clips/            # 클립 저장
    ├── shorts/           # 쇼츠 저장
    └── stats/            # 통계 저장
```

## 🔧 고급 설정

### 욕설 필터 커스터마이징
`data/badwords.txt` 파일에 금지어 추가:
```
새로운금지어
another_bad_word
```

### 하이라이트 키워드 추가
`data/keywords.txt` 파일에 감지할 키워드 추가:
```
# 킬 관련
penta kill
epic victory

# 반응 키워드
amazing
incredible
```

### 설정 파일 상세 옵션
```json
{
  "moderation": {
    "timeout_duration": 600,     # 타임아웃 시간 (초)
    "warning_threshold": 3,      # 경고 임계값
    "ban_threshold": 5           # 밴 임계값
  },
  "highlight_detection": {
    "chat_burst_threshold": 10,  # 채팅 폭발 기준 (초당 메시지)
    "volume_threshold": 1.5,     # 볼륨 급증 배율
    "laugh_sensitivity": 0.7     # 웃음 감지 민감도
  },
  "clip": {
    "before_seconds": 10,        # 클립 앞부분 (초)
    "after_seconds": 10          # 클립 뒷부분 (초)
  }
}
```

## 🎯 Windows EXE 빌드

### PyInstaller 사용
```bash
pip install pyinstaller

pyinstaller --name="StreamerAutomationSuite" \
            --windowed \
            --onefile \
            --icon=icon.ico \
            main.py
```

빌드된 EXE 파일은 `dist/` 폴더에 생성됩니다.

## 📝 라이선스
MIT License

## 🤝 기여하기
Pull Request는 언제나 환영합니다!

## ⚠️ 주의사항
- API 키는 절대 공개하지 마세요
- 스팸 방지를 위해 적절한 Rate Limiting 설정 필요
- YouTube/Twitch API 할당량 제한 확인

## 📞 문의
이슈가 있으시면 GitHub Issues에 등록해주세요.

---

**Streamer Automation Suite** - 스트리머를 위한 완벽한 자동화 솔루션 🎮✨