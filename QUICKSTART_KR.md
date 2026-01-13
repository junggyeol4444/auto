# 빠른 시작 가이드 - Smart Video Editor Pro

## 5분 설정

### 사전 요구 사항 확인

시작하기 전에 다음 사항을 확인하세요:
- ✓ Windows 10/11, macOS 또는 Linux
- ✓ Python 3.8 이상
- ✓ 최소 4GB RAM
- ✓ 2GB 여유 디스크 공간

### 1단계: Python 설치 (필요한 경우)

**Windows:**
1. https://python.org 에서 Python 다운로드
2. 설치 프로그램을 실행하고 "Add Python to PATH" 체크
3. 확인: 명령 프롬프트를 열고 `python --version` 입력

**macOS:**
```bash
# Homebrew 사용
brew install python3
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### 2단계: FFmpeg 설치

**Windows:**
1. https://ffmpeg.org/download.html 에서 다운로드
2. `C:\ffmpeg`에 압축 해제
3. 시스템 PATH에 `C:\ffmpeg\bin` 추가
4. 확인: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### 3단계: 애플리케이션 받기

```bash
# 저장소 복제
git clone https://github.com/junggyeol4444/auto.git
cd auto

# 또는 GitHub에서 ZIP 파일 다운로드 및 압축 해제
```

### 4단계: 종속성 설치

**Windows:**
```cmd
# 가상 환경 생성
python -m venv venv
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
# 가상 환경 생성
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 5단계: 애플리케이션 실행

```bash
python main.py
```

GUI 창이 열립니다!

## 첫 번째 사용 튜토리얼

### 파트 1: 편집 스타일 학습 (5분)

1. **YouTube 동영상 찾기**
   - 동영상 선택 (10-20분 권장)
   - 명확한 편집 스타일이 있는 것 선택
   - 예: 기술 리뷰, 브이로그, 튜토리얼

2. **애플리케이션에서:**
   - "Learn Style" 탭 클릭
   - YouTube URL 붙여넣기
   - "Download Video" 클릭
   - 다운로드 완료 대기 (~2-5분)

3. **프로필 생성:**
   - 프로필 이름 입력 (예: "Tech Review Style")
   - "Learn Style" 클릭
   - 분석 완료 대기 (~3-5분)
   - 성공 메시지 나타남!

### 파트 2: 비디오 편집 (10분)

1. **비디오 준비:**
   - 비디오 파일 준비 (MP4, AVI, MOV 등)
   - 첫 테스트는 5분 이내로 유지

2. **애플리케이션에서:**
   - "Edit Video" 탭 클릭
   - "Browse..." 클릭하고 비디오 선택
   - 드롭다운에서 학습된 프로필 선택
   - "Remove Silence" 체크 (권장)
   - 출력 위치 선택
   - "Edit Video" 클릭

3. **처리 대기:**
   - 처리 시간은 비디오 길이의 ~2-3배
   - 진행률 표시줄 확인
   - 세부 정보는 로그 확인

4. **결과:**
   - 편집된 비디오가 출력 위치에 저장됨
   - 원본과 비교!

## 일반적인 첫 사용 문제

### 문제: "Python not found"
**해결책:** Python을 재설치하고 설치 중 "Add to PATH" 체크

### 문제: "FFmpeg not found"
**해결책:** FFmpeg를 설치하고 시스템 PATH에 추가 (위의 2단계 참조)

### 문제: "Module not found"
**해결책:** 
```bash
# 먼저 가상 환경 활성화
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 그런 다음 종속성 설치
pip install -r requirements.txt
```

### 문제: GUI가 열리지 않음
**해결책:**
```bash
# PyQt5를 특별히 설치
pip install PyQt5

# 다시 실행 시도
python main.py
```

### 문제: 다운로드 실패
**해결책:**
- 인터넷 연결 확인
- 다른 YouTube 동영상 시도
- 일부 동영상은 제한될 수 있음

## 최상의 결과를 위한 팁

### 학습을 위해:
1. ✓ 동일한 크리에이터의 동영상 사용
2. ✓ 10-20분 길이의 동영상 선택
3. ✓ 명확한 편집 스타일이 있는 동영상 선택
4. ✗ 음악이 많은 동영상 피하기
5. ✗ 라이브 스트림이나 편집되지 않은 콘텐츠 피하기

### 편집을 위해:
1. ✓ 먼저 짧은 클립으로 테스트 (2-3분)
2. ✓ 원본 파일을 백업으로 유지
3. ✓ 콘텐츠 유형에 적합한 프로필 사용
4. ✓ 긴 비디오 처리 전 출력 확인
5. ✗ 원본 파일을 덮어쓰지 않기

## 다음 단계

1. **여러 프로필 생성:**
   - 다른 YouTuber에서 학습
   - 다양한 편집 스타일 시도
   - 결과 비교

2. **실험:**
   - 같은 프로필로 다른 비디오 시도
   - 다양한 프로필 조합 테스트
   - 콘텐츠에 가장 적합한 것 찾기

3. **문서 읽기:**
   - 자세한 가이드는 USAGE.md 확인
   - 기술 세부 사항은 ARCHITECTURE.md 읽기
   - 전체 기능은 README.md 검토

## 도움 받기

- **GitHub Issues**: 버그 보고 또는 질문하기
- **README.md**: 전체 문서
- **USAGE.md**: 자세한 사용 가이드
- **ARCHITECTURE.md**: 기술 문서

## 빠른 명령 참조

```bash
# 환경 활성화
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 애플리케이션 실행
python main.py

# 실행 파일 빌드 (Windows)
build.bat

# 데모 실행
python demo.py

# 테스트 실행
python test_basic.py
```

---

**축하합니다!** 비디오 편집 자동화를 시작할 준비가 되었습니다! 🎉
