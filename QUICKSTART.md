# Quick Start Guide - 빠른 시작 가이드

## 5분 안에 시작하기

### 1단계: 설치 (2분)

```bash
# 저장소 클론
git clone https://github.com/junggyeol4444/auto.git
cd auto

# 자동 설치 스크립트 실행
python setup.py
```

### 2단계: API 키 설정 (2분)

#### Twitch 설정
1. https://dev.twitch.tv/console/apps 접속
2. "Register Your Application" 클릭
3. Name: "My Stream Bot"
4. OAuth Redirect URLs: http://localhost
5. Category: "Broadcasting Suite"
6. Client ID와 Secret 복사

#### OAuth Token 생성
1. https://twitchtokengenerator.com/ 접속
2. "Custom Scope Token" 선택
3. 필요한 권한 선택:
   - `chat:read`
   - `chat:edit`
   - `clips:edit`
4. Token 복사

#### config.json 수정
```json
{
  "twitch": {
    "client_id": "여기에_클라이언트_ID",
    "client_secret": "여기에_시크릿",
    "oauth_token": "여기에_토큰",
    "channel": "내_채널명"
  }
}
```

### 3단계: 실행 (1분)

```bash
python main.py
```

## GUI 기본 사용법

### 대시보드
1. "모니터링 시작" 버튼 클릭
2. 실시간 통계 확인
3. 하이라이트 자동 감지

### 채팅 관리
- 욕설 필터 ON/OFF
- 차단된 메시지 로그 확인

### 클립 관리
- 자동 생성된 클립 확인
- "수동 클립 생성" 버튼으로 즉시 클립 생성

## 채팅 명령어 테스트

방송 채팅창에서:
```
!가위바위보 가위
!주사위 2
!sr Dynamite
!포인트
```

## 문제 해결

### "FFmpeg를 찾을 수 없습니다"
→ FFmpeg 설치: https://ffmpeg.org/download.html

### "모듈을 찾을 수 없습니다"
→ `pip install -r requirements.txt` 실행

### "API 인증 실패"
→ config.json의 API 키 확인

## 다음 단계

✅ 금지어 목록 커스터마이징 (`data/badwords.txt`)
✅ 하이라이트 키워드 추가 (`data/keywords.txt`)
✅ Discord 웹훅 설정 (알림 자동화)
✅ YouTube API 설정 (자동 업로드)

## 도움말

- 전체 문서: `README.md`
- 이슈 리포트: GitHub Issues
- 설정 상세: `config.json` 주석 참고
