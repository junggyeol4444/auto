# Troubleshooting - 문제 해결 가이드

## 일반적인 문제

### 1. 설치 관련

#### "Python 3.8 이상이 필요합니다"
**해결방법:**
```bash
# Python 버전 확인
python --version

# Python 3.8+ 다운로드
# https://www.python.org/downloads/
```

#### "pip install 실패"
**해결방법:**
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 개별 설치 시도
pip install customtkinter
pip install twitchio
```

#### "FFmpeg를 찾을 수 없습니다"
**해결방법:**
1. FFmpeg 다운로드: https://ffmpeg.org/download.html
2. 압축 해제
3. 환경 변수 PATH에 bin 폴더 추가
4. CMD 재시작 후 `ffmpeg -version` 확인

### 2. API 인증 문제

#### "Twitch 인증 실패"
**원인:**
- Client ID/Secret 오류
- OAuth Token 만료
- 권한 부족

**해결방법:**
```json
// config.json 확인
{
  "twitch": {
    "client_id": "정확한_ID",
    "oauth_token": "oauth:xxxxxxxxxxxx",  // "oauth:" 접두사 확인
    "channel": "채널명_정확히"
  }
}
```

#### "YouTube API 할당량 초과"
**원인:** 일일 API 할당량 10,000 유닛 초과

**해결방법:**
- 내일까지 대기
- 여러 프로젝트로 분산
- Quota 증가 신청

### 3. 실행 오류

#### "ModuleNotFoundError: No module named 'XXX'"
**해결방법:**
```bash
pip install -r requirements.txt --force-reinstall
```

#### "customtkinter 오류"
**해결방법:**
```bash
pip uninstall customtkinter
pip install customtkinter==5.2.1
```

#### "SQLite 오류"
**해결방법:**
- `data/points.db` 파일 삭제 후 재시작
- Python에 SQLite3 포함 여부 확인

### 4. 기능 오류

#### "채팅 모더레이션이 작동하지 않음"
**체크리스트:**
- [ ] Twitch OAuth에 `chat:read`, `chat:edit` 권한 있는지
- [ ] GUI에서 "모니터링 시작" 버튼 눌렀는지
- [ ] config.json에서 `enable_profanity_filter: true`인지

#### "클립이 생성되지 않음"
**원인:**
- FFmpeg 미설치
- 비디오 소스 경로 오류
- 디스크 공간 부족

**해결방법:**
```bash
# FFmpeg 테스트
ffmpeg -version

# 디스크 공간 확인
# output/clips/ 폴더 확인
```

#### "번역이 작동하지 않음"
**원인:** googletrans API 제한

**해결방법:**
```bash
# googletrans 재설치
pip uninstall googletrans
pip install googletrans==3.1.0a0
```

### 5. 성능 문제

#### "프로그램이 느립니다"
**최적화 방법:**
1. 하이라이트 감지 민감도 낮추기
2. 캐시 폴더 정리
3. 클립 자동 생성 끄기 (수동으로만)

#### "메모리 사용량이 높습니다"
**해결방법:**
```json
// config.json 수정
{
  "clip": {
    "auto_create": false  // 자동 클립 생성 끄기
  }
}
```

### 6. Windows EXE 빌드 문제

#### "PyInstaller 빌드 실패"
**해결방법:**
```bash
# PyInstaller 재설치
pip uninstall pyinstaller
pip install pyinstaller

# 빌드 재시도
python build.py
```

#### "EXE 실행 시 오류"
**해결방법:**
- FFmpeg를 EXE와 같은 폴더에 배치
- config.json 필수 (같은 폴더)
- data/ 폴더 필수

## 디버그 모드

문제 진단을 위해:

```python
# main.py 맨 위에 추가
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 로그 확인

```bash
# 실행 로그 저장
python main.py > output.log 2>&1
```

## 자주 묻는 질문 (FAQ)

**Q: 무료로 사용 가능한가요?**
A: 네, 오픈소스입니다. 단, API 사용량에 따라 클라우드 비용 발생 가능

**Q: 치지직(Chzzk)도 지원하나요?**
A: 현재 기본 구조만 있으며, 공식 API 부재로 제한적

**Q: 여러 채널 동시 모니터링 가능한가요?**
A: 현재는 단일 채널만 지원. 멀티 채널은 추후 업데이트 예정

**Q: Mac/Linux에서 실행 가능한가요?**
A: 네, Python 스크립트는 크로스 플랫폼. GUI는 테스트 필요

**Q: 방송 중에도 켜놔도 되나요?**
A: 네, 백그라운드에서 안전하게 실행됩니다

## 여전히 해결되지 않는 문제

GitHub Issues에 다음 정보와 함께 등록해주세요:

1. 에러 메시지 전체
2. Python 버전 (`python --version`)
3. OS 정보 (Windows 10/11, macOS, Linux)
4. 실행 명령어
5. config.json 설정 (API 키 제외)

## 연락처

- GitHub Issues: https://github.com/junggyeol4444/auto/issues
- 이메일: (프로젝트 관리자 이메일)
