# Smart Video Editor Pro

**Smart Video Editor Pro**는 YouTube 동영상에서 편집 스타일을 학습하고 자동으로 비디오 편집 작업을 오프라인으로 수행하는 Windows 데스크톱 애플리케이션입니다.

## 주요 기능

### Phase 1 (MVP) - 구현 완료
- ✅ **YouTube 동영상 다운로더**: yt-dlp를 사용한 편집 스타일 학습용 동영상 다운로드
- ✅ **장면 전환 감지**: 자동으로 장면 전환을 감지하고 컷 타이밍 분석
- ✅ **음성 구간 감지**: 비디오에서 음성 구간과 타이밍 식별
- ✅ **무음 제거**: 동영상에서 자동으로 무음 부분 제거
- ✅ **패턴 학습**: 비디오를 분석하고 편집 패턴을 데이터베이스에 저장
- ✅ **프로필 관리**: 다양한 스타일을 위한 편집 프로필 저장 및 불러오기
- ✅ **비디오 편집**: 학습된 패턴을 적용하여 새로운 비디오 편집
- ✅ **사용자 친화적 GUI**: 학습 및 편집을 위한 직관적인 탭 인터페이스

### 향후 개선 사항
- OCR 기반 자막 생성 및 분석
- 고급 효과 패턴 인식
- 일괄 비디오 처리
- 커뮤니티 프로필 공유
- 썸네일 생성
- 추가 편집 스타일

## 기술 스택

- **Python 3.8+**: 핵심 프로그래밍 언어
- **PyQt5**: GUI 프레임워크
- **moviepy**: 비디오 처리 및 편집
- **OpenCV**: 장면 전환 감지
- **pydub**: 오디오 분석 및 처리
- **yt-dlp**: YouTube 동영상 다운로드
- **SQLAlchemy**: 데이터베이스 관리
- **PyInstaller**: Windows 실행 파일 생성

## 설치 방법

### 옵션 1: 소스에서 실행

1. **필수 요구 사항**:
   - Python 3.8 이상
   - FFmpeg (moviepy에 필요)

2. **저장소 복제**:
   ```bash
   git clone https://github.com/junggyeol4444/auto.git
   cd auto
   ```

3. **가상 환경 생성**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

4. **종속성 설치**:
   ```bash
   pip install -r requirements.txt
   ```

5. **애플리케이션 실행**:
   ```bash
   python main.py
   ```

### 옵션 2: Windows 실행 파일 빌드

1. **옵션 1의 1-4단계 수행**

2. **실행 파일 빌드**:
   ```bash
   # Windows에서
   build.bat
   
   # 또는 수동으로
   pyinstaller build.spec
   ```

3. **실행 파일 실행**:
   ```
   dist\SmartVideoEditorPro.exe
   ```

## 사용 가이드

### YouTube 동영상에서 학습하기

1. **"Learn Style" 탭 열기**
2. **YouTube URL 입력** - 학습하고 싶은 편집 스타일의 동영상
3. **"Download Video" 클릭** - 동영상 다운로드 대기
4. **프로필 이름 입력** (예: "MrBeast 스타일", "MKBHD 스타일")
5. **"Learn Style" 클릭** - 비디오 분석 및 패턴 저장
6. 애플리케이션이 수행하는 작업:
   - 장면 전환 감지 및 타이밍 패턴 계산
   - 음성 구간과 무음 식별을 위한 오디오 분석
   - 학습된 패턴을 데이터베이스에 저장

### 비디오 편집하기

1. **"Edit Video" 탭 열기**
2. **입력 비디오 선택** - "Browse..." 클릭
3. **학습된 프로필 선택** - 드롭다운에서 선택
4. **편집 옵션 선택**:
   - ☑️ **Remove Silence**: 자동으로 무음 부분 잘라내기
5. **출력 위치 지정** (또는 기본값 사용)
6. **"Edit Video" 클릭**
7. 처리 완료 대기

### 프로필 관리

- 동영상에서 학습하면 프로필이 자동으로 저장됩니다
- "Refresh Profiles" 버튼으로 프로필 목록 업데이트
- 각 프로필에는 다음이 포함됩니다:
  - 장면 전환 패턴 (타이밍, 지속 시간, 임계값)
  - 오디오 패턴 (무음 감지, 음성 패딩)

## 프로젝트 구조

```
auto/
├── main.py                          # 애플리케이션 진입점
├── requirements.txt                 # Python 종속성
├── build.spec                       # PyInstaller 구성
├── build.bat                        # Windows 빌드 스크립트
├── src/
│   ├── core/                        # 핵심 기능
│   │   ├── video_downloader.py      # YouTube 다운로더
│   │   ├── scene_detector.py        # 장면 전환 감지
│   │   ├── audio_analyzer.py        # 오디오/음성 분석
│   │   ├── style_learner.py         # 패턴 학습
│   │   └── video_editor.py          # 비디오 편집 엔진
│   ├── database/                    # 데이터베이스 레이어
│   │   └── models.py                # SQLAlchemy 모델
│   └── gui/                         # 사용자 인터페이스
│       └── main_window.py           # 메인 GUI 창
├── data/                            # 데이터 디렉토리
│   ├── profiles/                    # 저장된 프로필
│   └── temp/                        # 임시 파일
└── README.md                        # 이 파일
```

## 작동 방식

### 학습 단계
1. **다운로드**: yt-dlp를 사용하여 YouTube 동영상 다운로드
2. **장면 분석**: OpenCV로 프레임 처리하여 장면 전환 감지
3. **오디오 분석**: Pydub로 오디오를 분석하여 음성 및 무음 구간 찾기
4. **패턴 추출**: 타이밍, 지속 시간, 임계값에 대한 통계 계산
5. **저장**: SQLite 데이터베이스에 패턴 저장하여 나중에 사용

### 편집 단계
1. **프로필 로드**: 데이터베이스에서 학습된 패턴 검색
2. **입력 분석**: 동일한 알고리즘으로 비디오 처리
3. **패턴 적용**: 학습된 임계값과 타이밍을 사용하여 컷 생성
4. **무음 제거**: 음성을 보존하면서 조용한 구간 지능적으로 제거
5. **내보내기**: 편집된 세그먼트를 최종 비디오로 결합

## 요구 사항

- **운영 체제**: Windows 10/11 (주요 대상), macOS/Linux에서도 작동
- **Python**: 3.8 이상
- **RAM**: 최소 4GB, 권장 8GB
- **저장 공간**: 애플리케이션용 500MB + 비디오용 공간
- **FFmpeg**: 비디오 처리에 필요

## 문제 해결

### FFmpeg를 찾을 수 없음
"FFmpeg not found" 오류가 발생하면:
- **Windows**: https://ffmpeg.org 에서 다운로드하고 PATH에 추가
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

### PyQt5 문제
GUI가 시작되지 않으면:
```bash
pip install --upgrade PyQt5
```

### 비디오 처리 오류
- 입력 비디오가 지원되는 형식(MP4, AVI, MKV, MOV)인지 확인
- 출력을 위한 충분한 디스크 공간이 있는지 확인
- 먼저 짧은 비디오로 시도

## 개발

### 테스트 실행
```bash
# 단위 테스트 (구현 시)
pytest tests/
```

### 기여하기
기여를 환영합니다! 다음 단계를 따르세요:
1. 저장소 포크
2. 기능 브랜치 생성
3. 변경 사항 작성
4. 풀 리퀘스트 제출

## 라이선스

이 프로젝트는 오픈 소스입니다. 자세한 내용은 LICENSE 파일을 참조하세요.

## 감사의 말

- **yt-dlp**: YouTube 동영상 다운로드
- **moviepy**: 비디오 편집 기능
- **OpenCV**: 컴퓨터 비전 도구
- **PyQt5**: GUI 프레임워크
- 모든 오픈 소스 기여자

## 연락처

문제, 질문 또는 제안 사항이 있으면 GitHub에서 이슈를 열어주세요.

---

**참고**: 이 애플리케이션은 교육 및 개인 용도입니다. 동영상을 다운로드할 때는 항상 저작권법과 YouTube 서비스 약관을 준수하세요.
