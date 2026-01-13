# Bot Development Framework Suite

다양한 플랫폼 챗봇 및 자동화 봇 통합 개발 프레임워크

## 🚀 빠른 시작 (실행 파일)

### ⚡ Windows 사용자
1. `run.bat` 파일을 더블클릭
2. 자동으로 환경 설정 및 프로그램 실행
3. GUI에서 API 키 입력 후 사용 시작!

### ⚡ Linux/Mac 사용자
1. 터미널에서 `./run.sh` 실행
2. 자동으로 환경 설정 및 프로그램 실행
3. GUI에서 API 키 입력 후 사용 시작!

### 💎 Windows EXE 파일 생성
- `build_exe.bat` 실행 → `dist/BotFramework.exe` 생성
- 설치 없이 바로 실행 가능한 단일 실행 파일

---

## 🌟 주요 기능

### 1. 챗봇 플랫폼 지원
- **디스코드 봇**: 명령어 시스템, 음악 재생, 서버 관리, 자동 응답
- **텔레그램 봇**: 명령어, 인라인 키보드, 정기 알림, 파일 전송
- **라인 봇**: 메시지 응답, 푸시 알림, 리치 메뉴
- **카카오톡 봇**: 메신저봇R용 JavaScript 스크립트

### 2. 크롬 확장 프로그램
- 웹페이지 자동화 (폼 작성, 클릭, DOM 조작)
- 데이터 수집 (스크래핑)
- 자동 번역
- 가격 비교
- 광고 차단

### 3. 가격 모니터링
- 지원 쇼핑몰: 쿠팡, 네이버쇼핑, 11번가, 지마켓, 옥션
- 정기적 가격 크롤링 (1시간마다)
- 가격 변동 감지 및 알림
- 가격 히스토리 그래프
- SQLite 데이터베이스 저장

### 4. 데이터 분석
- **웹 트래픽 분석**: Google Analytics API 연동
- **키워드 트렌드 분석**: 네이버 데이터랩, Google Trends
- **리포트 자동 생성**: PDF 형식 (그래프, 표 포함)

### 5. GUI (tkinter)
- 봇 관리 탭
- 가격 모니터링 탭
- 데이터 분석 탭
- 설정 탭

## 📁 프로젝트 구조

```
Bot_Framework/
├── main.py                      # 프로그램 진입점
├── run.bat                      # ⭐ Windows 실행 스크립트
├── run.sh                       # ⭐ Linux/Mac 실행 스크립트
├── build_exe.bat                # ⭐ Windows EXE 빌드 스크립트
├── build_exe.sh                 # ⭐ Linux/Mac EXE 빌드 스크립트
├── BotFramework.spec            # ⭐ PyInstaller 설정 파일
├── config.json                  # 설정 파일
├── requirements.txt             # 의존성 목록
├── README.md                    # 사용 설명서
│
├── bots/                        # 봇 모듈
│   ├── discord/
│   │   ├── discord_bot.py      # 디스코드 봇 메인
│   │   ├── commands.py         # 명령어 시스템
│   │   └── music.py            # 음악 재생 봇
│   │
│   ├── telegram/
│   │   ├── telegram_bot.py     # 텔레그램 봇 메인
│   │   └── handlers.py         # 핸들러 및 스케줄러
│   │
│   ├── line/
│   │   └── line_bot.py         # 라인 봇
│   │
│   └── kakaotalk/
│       └── kakao_script.js     # 카카오톡 봇 스크립트
│
├── chrome_extension/            # 크롬 확장 프로그램
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   ├── popup.html
│   └── popup.js
│
├── monitoring/                  # 가격 모니터링
│   ├── price_tracker.py        # 가격 추적 메인
│   ├── crawlers.py             # 쇼핑몰 크롤러
│   └── notifier.py             # 알림 전송
│
├── analytics/                   # 데이터 분석
│   ├── web_analytics.py        # 웹 트래픽 분석
│   ├── trend_analyzer.py       # 트렌드 분석
│   └── report_generator.py     # 리포트 생성
│
├── gui/                         # GUI
│   ├── main_window.py          # 메인 윈도우
│   └── settings_window.py      # 설정 윈도우
│
├── database/                    # 데이터베이스
│   └── prices.db               # SQLite 데이터베이스
│
├── output/                      # 출력 폴더
│   ├── reports/                # PDF 리포트
│   └── graphs/                 # 그래프 이미지
│
└── logs/                        # 로그 파일
```

## 🚀 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/junggyeol4444/auto.git
cd auto
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 추가 설치 (선택사항)
- **Chrome Driver**: Selenium 웹 크롤링용
- **FFmpeg**: 디스코드 음악 봇용
  ```bash
  # Windows: https://ffmpeg.org/download.html
  # Ubuntu: sudo apt install ffmpeg
  ```

## 🎮 사용 방법

### 방법 1: 실행 스크립트 사용 (권장)

#### Windows 사용자:
```bash
# 더블클릭 또는 명령 프롬프트에서
run.bat
```

#### Linux/Mac 사용자:
```bash
# 터미널에서
./run.sh
```

**실행 스크립트의 장점:**
- ✅ 자동으로 가상환경 생성 및 활성화
- ✅ 필요한 패키지 자동 설치
- ✅ 한 번 클릭으로 프로그램 실행
- ✅ 의존성 관리 자동화

### 방법 2: 수동 실행
```bash
python main.py
```

### 2. API 키 설정
1. GUI에서 "설정" 탭으로 이동
2. 각 플랫폼의 API 키/토큰 입력
3. "모든 설정 저장" 클릭

### 3. 봇 시작
1. "봇 관리" 탭에서 플랫폼 선택 (디스코드/텔레그램/라인)
2. "봇 시작" 버튼 클릭
3. 로그에서 봇 상태 확인

### 4. 가격 모니터링
1. "가격 모니터링" 탭으로 이동
2. 상품 URL과 목표가 입력
3. "상품 등록" 클릭
4. "가격 체크" 버튼으로 수동 체크 또는 자동 주기적 체크

### 5. 데이터 분석
1. "데이터 분석" 탭으로 이동
2. 분석 유형 선택 (웹 트래픽/키워드 트렌드)
3. 분석 기간 설정
4. "분석 시작" 클릭
5. "PDF 리포트 생성" 클릭

## 🔑 API 키 발급 방법

### Discord Bot
1. [Discord Developer Portal](https://discord.com/developers/applications) 접속
2. "New Application" 클릭
3. Bot 섹션에서 Token 생성
4. Privileged Gateway Intents 활성화

### Telegram Bot
1. Telegram에서 [@BotFather](https://t.me/botfather) 검색
2. `/newbot` 명령어로 봇 생성
3. Bot Token 받기

### LINE Bot
1. [LINE Developers](https://developers.line.biz/) 접속
2. Provider 및 Channel 생성
3. Channel Access Token 및 Channel Secret 발급

### Google Analytics
1. [Google Analytics](https://analytics.google.com/) 접속
2. Property 생성
3. Property ID 확인

## 🔧 설정 파일 (config.json)

```json
{
  "discord": {
    "token": "YOUR_DISCORD_TOKEN"
  },
  "telegram": {
    "token": "YOUR_TELEGRAM_TOKEN",
    "chat_ids": [123456789]
  },
  "line": {
    "channel_access_token": "YOUR_LINE_TOKEN",
    "channel_secret": "YOUR_LINE_SECRET"
  },
  "email": {
    "host": "smtp.gmail.com",
    "port": 587,
    "user": "your-email@gmail.com",
    "password": "your-app-password"
  },
  "analytics": {
    "ga_property_id": "YOUR_GA_PROPERTY_ID"
  }
}
```

## 📦 Windows EXE 빌드

### 방법 1: 빌드 스크립트 사용 (권장)

#### Windows:
```bash
build_exe.bat
```

#### Linux/Mac (크로스 컴파일):
```bash
./build_exe.sh
```

**빌드 스크립트의 장점:**
- ✅ PyInstaller 자동 설치
- ✅ 이전 빌드 파일 자동 정리
- ✅ 최적화된 빌드 설정 적용
- ✅ 빌드 성공/실패 상태 확인

빌드 완료 후:
- 📁 `dist/BotFramework.exe` 파일이 생성됩니다
- 📋 `config.json` 파일을 함께 배포하세요
- 🚀 EXE 파일을 더블클릭하여 실행

### 방법 2: 수동 빌드

```bash
# PyInstaller 설치
pip install pyinstaller

# EXE 파일 생성 (Spec 파일 사용)
pyinstaller BotFramework.spec

# 또는 간단한 빌드
pyinstaller --onefile --windowed --name BotFramework main.py

# 생성된 파일: dist/BotFramework.exe
```

## 🤖 봇 명령어

### Discord Bot
- `!안녕` - 인사
- `!날씨 [도시]` - 날씨 정보
- `!주사위 [면수]` - 주사위 굴리기
- `!투표 [질문]` - 투표 생성
- `!핑` - 응답 속도 확인
- `!정보` - 서버 정보
- `!청소 [개수]` - 메시지 삭제 (관리자)
- `!join` - 음성 채널 입장
- `!play [URL]` - 음악 재생
- `!pause` - 일시정지
- `!resume` - 재개
- `!stop` - 정지
- `!skip` - 다음 곡

### Telegram Bot
- `/start` - 봇 시작
- `/help` - 도움말
- `/weather [도시]` - 날씨 정보
- `/news` - 최신 뉴스
- `/price [종목]` - 가격 정보
- `/button` - 인라인 버튼 예시
- `/menu` - 메뉴

### KakaoTalk Bot
- `날씨 [도시]` - 날씨 정보
- `번역 [텍스트]` - 번역
- `계산 [수식]` - 계산기
- `뉴스` - 최신 뉴스
- `시간` - 현재 시간
- `주사위` - 주사위 굴리기
- `도움말` - 사용 가능한 명령어

## 🌐 크롬 확장 프로그램 설치

1. Chrome에서 `chrome://extensions/` 접속
2. "개발자 모드" 활성화
3. "압축해제된 확장 프로그램을 로드합니다" 클릭
4. `chrome_extension` 폴더 선택

## 📊 지원하는 쇼핑몰

- 쿠팡 (coupang.com)
- 네이버 쇼핑 (shopping.naver.com)
- 11번가 (11st.co.kr)
- 지마켓 (gmarket.co.kr)
- 옥션 (auction.co.kr)

## 🔔 알림 설정

### 이메일 알림
Gmail 사용 시:
1. Google 계정 보안 설정
2. "앱 비밀번호" 생성
3. 설정 탭에서 입력

### 텔레그램 알림
1. Chat ID 확인: [@userinfobot](https://t.me/userinfobot)
2. 설정 탭에서 Chat ID 입력

## ⚠️ 주의사항

1. **API 키 보안**: config.json 파일을 절대 공개하지 마세요
2. **Rate Limiting**: API 호출 제한을 준수하세요
3. **크롤링**: 각 사이트의 robots.txt와 이용약관을 확인하세요
4. **봇 권한**: Discord/Telegram 봇에 적절한 권한을 부여하세요

## 🐛 문제 해결

### 봇이 시작되지 않을 때
- API 토큰이 올바른지 확인
- 인터넷 연결 확인
- 로그 파일 확인

### 크롤링이 실패할 때
- Chrome Driver 버전 확인
- 사이트 구조 변경 확인
- User-Agent 설정 확인

### GUI가 표시되지 않을 때
- tkinter 설치 확인: `sudo apt install python3-tk` (Linux)
- 디스플레이 환경 변수 확인

## 📝 라이선스

이 프로젝트는 개인 사용 및 학습 목적으로 제공됩니다.

## 👨‍💻 개발자

junggyeol4444

## 🤝 기여

이슈 및 풀 리퀘스트를 환영합니다!

## 📧 문의

GitHub Issues를 통해 문의해주세요.

---

**⚡ 개발 완료 및 테스트 준비 완료**

이 프로젝트는 다양한 봇 플랫폼과 자동화 기능을 통합한 종합 프레임워크입니다.
GUI를 통해 쉽게 관리하고, 가격 모니터링 및 데이터 분석 기능을 활용하세요!