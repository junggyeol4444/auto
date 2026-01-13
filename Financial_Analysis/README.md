# 금융 데이터 분석 & 알림 시스템

Windows EXE로 빌드 가능한 금융 데이터 분석 및 자동 알림 프로그램입니다.
CustomTkinter 기반 모던 GUI를 포함하며, 암호화폐, 환율, 부동산, 주식 등 다양한 금융 데이터를 실시간으로 분석하고 알림을 제공합니다.

## 주요 기능

### 1. 암호화폐 (코인)
- ✅ 실시간 시세 조회 (업비트, 바이낸스, CoinGecko API)
- ✅ 급등/급락 코인 탐지 (변동률 기준)
- ✅ 거래량 분석 및 시가총액 순위
- ✅ 가격 알림 설정 (목표가 도달 시 알림)

### 2. 환율
- ✅ 주요 통화 환율 조회 (USD, JPY, EUR, CNY, GBP)
- ✅ 실시간 환율 추이
- ✅ 환율 예측 (선형 회귀 기반)
- ✅ 환차익 계산기
- ✅ 환율 알림 설정

### 3. 부동산
- ✅ 아파트 실거래가 조회 (국토교통부 API)
- ✅ 지역별 가격 추이
- ✅ 평당 가격 자동 계산
- ✅ 급등 지역 탐지

### 4. 주식
- ✅ 실시간 시세 조회 (한국, 미국 주식)
- ✅ 종목 상세 정보 (PER, PBR, 배당수익률 등)
- ✅ 기술적 분석 (이동평균선, RSI, 볼린저 밴드, MACD, 스토캐스틱)
- ✅ 매수/매도 신호 자동 생성

### 5. 알림 시스템
- ✅ 텔레그램 봇 알림
- ✅ 이메일 알림 (SMTP)
- ✅ 윈도우 팝업 알림

## 빠른 시작 (간편 실행)

### Windows 사용자
**더블클릭으로 실행**: `run.bat` 파일을 더블클릭하면 자동으로 프로그램이 실행됩니다.
```cmd
run.bat
```

### Mac/Linux 사용자  
**터미널에서 실행**:
```bash
./run.sh
```

**참고**: `run.bat` / `run.sh` 스크립트는 자동으로 Python 확인 및 패키지 설치를 수행합니다.

---

## 수동 설치 및 실행 (선택사항)

### 1. Python 설치
Python 3.8 이상이 필요합니다. [Python 공식 사이트](https://www.python.org/downloads/)에서 다운로드하세요.

### 2. 의존성 설치
```bash
cd Financial_Analysis
pip install -r requirements.txt
```

### 3. 실행
```bash
python main.py
```

## 설정 방법

### config.json 설정
프로그램 실행 시 `config.json` 파일이 자동 생성됩니다. GUI의 "설정" 탭에서 API 키를 입력할 수 있습니다.

#### 텔레그램 봇 설정
1. [@BotFather](https://t.me/botfather)에서 봇 생성
2. Bot Token 받기
3. [@userinfobot](https://t.me/userinfobot)에서 Chat ID 확인
4. 설정 탭에 입력

#### 이메일 설정 (Gmail 예시)
1. Gmail 계정의 "2단계 인증" 활성화
2. "앱 비밀번호" 생성
3. 설정 탭에 이메일과 앱 비밀번호 입력

#### API 키 (선택사항)
- **업비트**: https://upbit.com/mypage/open_api_management
- **환율 API**: https://www.exchangerate-api.com/
- **국토교통부**: https://www.data.go.kr/
- **한국은행**: https://ecos.bok.or.kr/

## 사용 방법

### 암호화폐 탭
1. "시세 조회" 버튼으로 실시간 코인 가격 확인
2. "급등/급락 코인" 버튼으로 변동성 높은 코인 조회
3. 가격 알림 설정: 마켓 코드(예: KRW-BTC)와 목표가 입력

### 환율 탭
1. "환율 조회" 버튼으로 주요 통화 환율 확인
2. 환차익 계산기: 금액, 출발/도착 통화 입력 후 계산

### 부동산 탭
1. 지역 코드 입력 (예: 11680 - 강남구)
2. "조회" 버튼으로 실거래가 확인
3. 평당 가격 자동 계산됨

### 주식 탭
1. 종목 코드 입력 (예: 005930.KS - 삼성전자, AAPL - 애플)
2. "조회" 버튼으로 주식 정보 확인
3. "기술적 분석" 버튼으로 이동평균선, RSI 분석

### 설정 탭
1. API 키 및 알림 설정 입력
2. "설정 저장" 버튼으로 저장
3. "테스트 알림 전송" 버튼으로 알림 테스트

## Windows EXE 빌드 (독립 실행 파일 생성)

Windows에서 Python 설치 없이 실행 가능한 EXE 파일을 만들 수 있습니다.

### 간편 빌드 방법
**더블클릭으로 빌드**: `build_exe.bat` 파일을 더블클릭하면 자동으로 EXE를 생성합니다.
```cmd
build_exe.bat
```

**Mac/Linux에서 빌드**:
```bash
./build_exe.sh
```

빌드된 EXE 파일은 `dist` 폴더에 생성됩니다: `dist\금융분석시스템.exe`

### 수동 빌드 방법 (선택사항)
```bash
cd Financial_Analysis
pyinstaller --onefile --windowed --name "금융분석시스템" main.py
```

### 주의사항
- `config.json` 파일은 EXE 파일과 같은 폴더에 위치해야 합니다.
- `data` 폴더도 함께 배포해야 합니다.

## 디렉토리 구조

```
Financial_Analysis/
├── main.py                    # 메인 진입점
├── config.json                # 설정 파일
├── requirements.txt           # 의존성 목록
├── README.md                  # 사용 설명서
│
├── modules/                   # 기능 모듈
│   ├── crypto/               # 암호화폐
│   │   ├── upbit_api.py
│   │   ├── binance_api.py
│   │   ├── coingecko_api.py
│   │   └── analyzer.py
│   │
│   ├── forex/                # 환율
│   │   ├── exchange_rate.py
│   │   └── predictor.py
│   │
│   ├── real_estate/          # 부동산
│   │   ├── molit_api.py
│   │   └── analyzer.py
│   │
│   ├── stocks/               # 주식
│   │   ├── stock_api.py
│   │   └── dividend_analyzer.py
│   │
│   ├── technical/            # 기술적 분석
│   │   ├── ma.py
│   │   ├── rsi.py
│   │   ├── bollinger.py
│   │   ├── macd.py
│   │   └── stochastic.py
│   │
│   └── alert/                # 알림
│       ├── telegram_bot.py
│       ├── email_sender.py
│       └── popup.py
│
├── database/                  # 데이터베이스
│   └── db_manager.py
│
├── gui/                       # GUI
│   └── main_window.py
│
└── data/                      # 데이터 저장
    └── prices.db
```

## 기술 스택

- **GUI**: CustomTkinter 5.2.1
- **데이터 처리**: pandas, numpy
- **기술적 분석**: ta, scikit-learn
- **시각화**: matplotlib, plotly
- **데이터베이스**: SQLite
- **HTTP 요청**: requests, aiohttp
- **알림**: python-telegram-bot, smtplib, plyer

## 문제 해결

### 모듈을 찾을 수 없음
```bash
pip install -r requirements.txt
```

### 텔레그램 알림이 작동하지 않음
1. Bot Token과 Chat ID가 올바른지 확인
2. 봇과 대화를 한 번 시작해야 합니다 (`/start` 명령)

### 이메일 알림이 작동하지 않음
1. Gmail의 경우 "앱 비밀번호"를 사용해야 합니다
2. "보안 수준이 낮은 앱 액세스"는 더 이상 지원되지 않습니다

### API 호출 제한
- 업비트: 초당 10회 제한 (자동 처리됨)
- CoinGecko: 분당 50회 제한 (무료 버전)
- 과도한 호출 시 잠시 대기 후 재시도하세요

## 라이선스

이 프로젝트는 교육 및 개인 사용 목적으로 제공됩니다.

## 주의사항

- 실제 투자 결정에 이 프로그램의 분석 결과만 의존하지 마세요.
- API 키는 안전하게 보관하고 공개하지 마세요.
- 과도한 API 호출은 서비스 제한을 초래할 수 있습니다.
- 알림 기능은 네트워크 상태에 따라 지연될 수 있습니다.

## 업데이트 예정

- [ ] 실시간 차트 표시 (mplfinance)
- [ ] 포트폴리오 관리 기능
- [ ] 자동 매매 시스템 (모의 투자)
- [ ] 더 많은 기술적 지표
- [ ] 뉴스 크롤링 및 감성 분석
- [ ] 백테스팅 기능

## 연락처

문의사항이나 버그 리포트는 GitHub Issues를 이용해주세요.

---

**Version**: 1.0.0  
**Last Updated**: 2024-01
