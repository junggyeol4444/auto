# AI Design Automation Suite

**AI 기반 디자인 자동화 도구** - 유튜브 썸네일 제작 및 사진 합성 자동화

## 📋 프로그램 개요

AI Design Automation Suite는 유튜브 크리에이터와 디자이너를 위한 올인원 자동화 도구입니다.

### 주요 기능
1. **유튜브 썸네일 자동 제작**
   - 장르별 템플릿 (게임, 브이로그, 리뷰, 먹방, 교육)
   - 자동 텍스트 삽입 및 강조 효과
   - 얼굴 인식 자동 크롭
   - A/B 테스트용 9가지 버전 자동 생성
   - 눈에 띄는 색상 조합

2. **사진 합성**
   - AI 기반 배경 제거
   - 배경 교체 (단색, 그라데이션, 이미지)
   - 얼굴 합성 (Face Swap)
   - 콜라주 생성
   - 색감 통일 및 필터 적용
   - 그림자/반사 효과

## 🚀 설치 방법

### 필수 요구사항
- Python 3.8 이상
- Windows / macOS / Linux

### 설치 단계

1. **저장소 클론**
```bash
git clone https://github.com/junggyeol4444/auto.git
cd auto
```

2. **가상환경 생성 (권장)**
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

**참고**: 일부 라이브러리(dlib, face-recognition)는 설치가 복잡할 수 있습니다. 설치 실패 시에도 기본 기능은 동작합니다.

## 💻 사용 방법

### 프로그램 실행

```bash
python main.py
```

### 유튜브 썸네일 제작

1. **"유튜브 썸네일"** 탭 선택
2. 썸네일 제목 입력
3. 강조할 키워드 입력 (선택사항)
4. 이미지 업로드
5. 장르 선택
6. 색상 조합 선택
7. **"생성 시작"** 클릭
8. 9가지 버전 확인 및 저장

### 사진 합성

1. **"사진 합성"** 탭 선택
2. 기능 선택:
   - **배경 제거**: 이미지 배경 자동 제거
   - **배경 교체**: 새로운 배경으로 교체
   - **얼굴 합성**: 두 사진의 얼굴 교체
   - **콜라주**: 여러 이미지를 그리드로 배치
   - **색감 통일**: 여러 이미지에 동일한 필터 적용
3. 이미지 업로드
4. 옵션 설정
5. **"처리 시작"** 클릭
6. 결과 확인 및 저장

## 📁 출력 파일

생성된 파일은 다음 위치에 저장됩니다:
- 썸네일: `output/thumbnails/`
- 사진 합성: `output/synthesis/`

## 🔧 설정 변경

`config.json` 파일을 편집하여 설정을 변경할 수 있습니다:
- 색상 조합 추가/수정
- 장르 설정
- 출력 크기
- 기타 옵션

## 🏗️ EXE 파일 빌드 (Windows)

Windows에서 실행 파일로 빌드하려면:

```bash
build.bat
```

빌드된 EXE 파일은 `dist/` 폴더에 생성됩니다.

## 📦 기술 스택

### 이미지 처리
- **Pillow (PIL)**: 이미지 편집 및 합성
- **OpenCV**: 얼굴 인식 및 이미지 처리
- **rembg**: AI 기반 배경 제거
- **numpy**: 배열 연산

### 얼굴 인식/합성
- **dlib**: 얼굴 랜드마크 감지
- **face_recognition**: 얼굴 인식
- **OpenCV Haar Cascade**: 기본 얼굴 감지

### AI 이미지 생성 (선택사항)
- **Stable Diffusion**: 배경 생성
- **diffusers**: Stable Diffusion 라이브러리

### GUI
- **customtkinter**: 모던 UI

## 📝 프로젝트 구조

```
auto/
├── main.py                    # 메인 진입점
├── config.json                # 설정 파일
├── requirements.txt           # 의존성
├── README.md                  # 사용 설명서
├── build.bat                  # EXE 빌드 스크립트
│
├── modules/
│   ├── thumbnail/             # 썸네일 생성 모듈
│   ├── photo_synthesis/       # 사진 합성 모듈
│   ├── ai_generation/         # AI 생성 모듈 (선택)
│   └── utils/                 # 유틸리티
│
├── gui/                       # GUI 컴포넌트
│   ├── main_window.py
│   ├── thumbnail_tab.py
│   ├── synthesis_tab.py
│   └── preview_window.py
│
├── assets/                    # 에셋 (폰트, 효과 등)
└── output/                    # 출력 파일
```

## ⚠️ 문제 해결

### 일부 라이브러리 설치 실패
- **dlib**, **face-recognition** 설치 실패 시에도 기본 기능은 동작합니다
- 얼굴 합성 기능은 OpenCV의 기본 얼굴 감지를 사용합니다

### 한글 폰트 문제
- 시스템에 한글 폰트가 설치되어 있는지 확인하세요
- Windows: 맑은 고딕, 나눔고딕
- macOS: Apple SD Gothic Neo
- Linux: Noto Sans CJK

### rembg 배경 제거가 느린 경우
- 첫 실행 시 모델 다운로드로 시간이 걸릴 수 있습니다
- GPU가 없는 경우 CPU에서 실행되어 느릴 수 있습니다
- 대체 방법으로 간단한 배경 제거를 사용합니다

## 🤝 기여

이슈 및 풀 리퀘스트를 환영합니다!

## 📄 라이선스

이 프로젝트는 오픈소스이며 자유롭게 사용할 수 있습니다.

## 👨‍💻 개발자

junggyeol4444

## 📧 문의

문제나 제안사항이 있으시면 GitHub Issues를 통해 연락주세요.