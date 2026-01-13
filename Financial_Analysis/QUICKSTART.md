# 빠른 시작 가이드

## 1. 설치 (5분)

### Windows
```cmd
cd Financial_Analysis
pip install -r requirements.txt
```

### Mac/Linux
```bash
cd Financial_Analysis
pip3 install -r requirements.txt
```

## 2. 설정 (3분)

### 기본 설정
프로그램을 처음 실행하면 `config.json` 파일이 자동 생성됩니다.

### API 키 설정 (선택사항)
GUI의 "설정" 탭에서 다음을 입력할 수 있습니다:
- 텔레그램 봇 토큰 & Chat ID
- 이메일 (Gmail 앱 비밀번호)

**참고**: API 키 없이도 대부분의 기능이 작동합니다 (샘플 데이터 사용)

## 3. 실행

```bash
python main.py
```

## 4. 주요 기능 사용법

### 암호화폐 탭
1. "시세 조회" 클릭 → 실시간 코인 가격 확인
2. "급등/급락 코인" 클릭 → 변동성 높은 코인 조회

### 환율 탭
1. "환율 조회" 클릭 → 주요 통화 환율 확인
2. 환차익 계산: 금액과 통화 입력 후 "계산" 클릭

### 주식 탭
1. 종목 코드 입력 (예: 005930.KS, AAPL)
2. "조회" → 주식 정보 확인
3. "기술적 분석" → 이동평균선, RSI 분석

### 설정 탭
1. API 키 입력
2. "설정 저장" 클릭
3. "테스트 알림 전송"으로 확인

## 5. 알림 설정

### 텔레그램 봇 만들기
1. Telegram에서 @BotFather 검색
2. `/newbot` 명령으로 봇 생성
3. Bot Token 받기
4. 생성한 봇과 대화 시작 (`/start`)
5. @userinfobot에서 Chat ID 확인
6. 설정 탭에 입력

### Gmail 설정
1. Google 계정 → 보안 → 2단계 인증 활성화
2. 앱 비밀번호 생성
3. 설정 탭에 이메일과 앱 비밀번호 입력

## 6. Windows EXE 빌드

```cmd
build_exe.bat
```

빌드된 파일: `dist\금융분석시스템.exe`

## 문제 해결

### "customtkinter를 찾을 수 없음"
```bash
pip install customtkinter
```

### "API 호출 실패"
- 인터넷 연결 확인
- API 키가 없어도 샘플 데이터로 작동합니다

### "텔레그램 알림 실패"
- Bot Token과 Chat ID 확인
- 봇과 대화를 시작했는지 확인 (`/start`)

## 더 많은 정보

자세한 내용은 `README.md`를 참조하세요.
