# AI Design Automation Suite - Architecture Documentation

## 프로젝트 개요

AI Design Automation Suite는 유튜브 크리에이터와 디자이너를 위한 자동화 도구입니다. 이 문서는 프로젝트의 아키텍처, 설계 결정, 그리고 각 모듈의 역할을 설명합니다.

## 아키텍처 설계

### 계층 구조

```
┌─────────────────────────────────────┐
│         GUI Layer (gui/)            │
│  - Main Window                      │
│  - Thumbnail Tab                    │
│  - Synthesis Tab                    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│     Business Logic (modules/)       │
│  - Thumbnail Generation             │
│  - Photo Synthesis                  │
│  - AI Generation (optional)         │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│      Utilities (modules/utils/)     │
│  - Image Processing                 │
│  - Font Management                  │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    External Libraries               │
│  - Pillow, OpenCV, rembg, etc.     │
└─────────────────────────────────────┘
```

## 모듈 설명

### 1. Thumbnail Generation (modules/thumbnail/)

#### template_manager.py
- **역할**: 장르별 템플릿 생성 및 관리
- **주요 기능**:
  - 5가지 장르 템플릿 (게임, 브이로그, 리뷰, 먹방, 교육)
  - 4가지 색상 조합
  - A/B 테스트용 9가지 버전 자동 생성
  - 그라데이션, 분할, 테두리 스타일 지원

#### text_overlay.py
- **역할**: 텍스트 삽입 및 강조 효과
- **주요 기능**:
  - 자동 텍스트 배치 (상단, 중앙, 하단)
  - 키워드 하이라이트
  - 외곽선 및 그림자 효과
  - 다중 라인 텍스트 지원
  - 자동 텍스트 줄바꿈

#### face_detect.py
- **역할**: 얼굴 인식 및 스마트 크롭
- **주요 기능**:
  - OpenCV Haar Cascade 기반 얼굴 감지
  - 얼굴 중심 자동 크롭
  - 여러 얼굴 처리
  - 썸네일 비율에 맞는 스마트 크롭

#### effects.py
- **역할**: 시각 효과 생성
- **주요 기능**:
  - 화살표, 원, 별, 반짝임 효과
  - 느낌표 추가
  - 다중 효과 자동 배치

### 2. Photo Synthesis (modules/photo_synthesis/)

#### background_remover.py
- **역할**: 배경 제거
- **주요 기능**:
  - rembg 라이브러리 사용 (AI 기반)
  - 폴백: 간단한 색상 임계값 방식
  - 배치 처리 지원
  - 투명 배경 PNG 저장

#### background_replacer.py
- **역할**: 배경 교체
- **주요 기능**:
  - 단색 배경
  - 그라데이션 배경
  - 이미지 배경 (fit, fill, stretch)
  - 블러 배경

#### face_swap.py
- **역할**: 얼굴 합성
- **주요 기능**:
  - face_recognition 라이브러리 사용 (우선)
  - 폴백: OpenCV Haar Cascade
  - 얼굴 랜드마크 감지
  - Seamless cloning
  - 자동 블렌딩

#### collage.py
- **역할**: 콜라주 생성
- **주요 기능**:
  - 그리드 레이아웃 (2x2, 3x3 등)
  - 자유 배치
  - 폴라로이드 스타일
  - 모자이크 스타일
  - 자동 크기 조정 및 정렬

#### color_grading.py
- **역할**: 색감 조정 및 필터
- **주요 기능**:
  - 5가지 프리셋 필터 (vintage, vivid, warm, cool, bw)
  - HSV 조정
  - 색상 매칭 (여러 이미지 통일)
  - LAB 색공간 기반 매칭

#### shadow_reflection.py
- **역할**: 그림자 및 반사 효과
- **주요 기능**:
  - 드롭 섀도우
  - 반사 효과 (그라데이션 페이드)
  - 원근 그림자
  - 캐스트 섀도우 (광원 방향 기반)

### 3. AI Generation (modules/ai_generation/)

#### stable_diffusion.py
- **역할**: AI 배경 생성 (선택사항)
- **주요 기능**:
  - Stable Diffusion 통합
  - 장르별 프롬프트 자동 생성
  - GPU/CPU 자동 감지
  - 폴백: 단순 배경 생성

### 4. Utilities (modules/utils/)

#### image_utils.py
- **역할**: 이미지 처리 유틸리티
- **주요 기능**:
  - 리사이즈, 크롭
  - PIL ↔ OpenCV 변환
  - 그라데이션 생성
  - 투명도 처리
  - 밝기/대비 조정

#### font_manager.py
- **역할**: 폰트 관리
- **주요 기능**:
  - 시스템 폰트 자동 감지
  - 한글 폰트 우선 처리
  - 폴백 메커니즘
  - 크기 및 스타일 지원

## 설계 결정

### 1. 오류 처리 전략

**원칙**: 선택적 의존성은 실패해도 프로그램이 계속 동작해야 함

- **rembg 없음**: 간단한 색상 기반 배경 제거 사용
- **face_recognition 없음**: OpenCV Haar Cascade 사용
- **Stable Diffusion 없음**: 간단한 그라데이션/패턴 생성

### 2. 성능 최적화

- **지연 로딩**: Stable Diffusion 등 무거운 모듈은 첫 사용시 로드
- **배치 처리**: 여러 이미지 동시 처리 지원
- **해상도 조정**: 미리보기는 낮은 해상도, 저장은 원본 해상도

### 3. 사용자 경험

- **한글 UI**: 모든 인터페이스 한글 지원
- **실시간 프로그레스**: 처리 중 진행상황 표시
- **미리보기**: 저장 전 결과 확인
- **A/B 테스트**: 여러 버전 자동 생성으로 선택권 제공

### 4. 확장성

- **모듈화**: 각 기능을 독립 모듈로 분리
- **설정 파일**: config.json으로 쉬운 커스터마이징
- **플러그인 구조**: 새로운 필터/효과 쉽게 추가 가능

## 데이터 흐름

### 썸네일 생성 흐름

```
1. 사용자 입력 (제목, 키워드, 이미지, 장르, 색상)
   ↓
2. 이미지 전처리
   - 얼굴 감지 (face_detect.py)
   - 스마트 크롭
   ↓
3. 템플릿 생성 (template_manager.py)
   - 9가지 버전 생성
   ↓
4. 텍스트 오버레이 (text_overlay.py)
   - 제목 추가
   - 키워드 하이라이트
   ↓
5. 효과 추가 (effects.py)
   - 화살표, 원, 별 등
   ↓
6. 출력
   - 미리보기 표시
   - PNG 저장
```

### 사진 합성 흐름

```
1. 기능 선택 (배경 제거, 교체, 얼굴 합성, 콜라주, 색감)
   ↓
2. 이미지 업로드
   ↓
3. 처리 (해당 모듈 호출)
   - background_remover.py
   - background_replacer.py
   - face_swap.py
   - collage.py
   - color_grading.py
   ↓
4. 출력
   - 미리보기 표시
   - PNG 저장
```

## 의존성 관리

### 필수 의존성
- **Pillow**: 이미지 처리
- **OpenCV**: 컴퓨터 비전
- **numpy**: 수치 연산
- **customtkinter**: GUI

### 선택적 의존성
- **rembg**: 고품질 배경 제거 (없으면 기본 방식 사용)
- **face-recognition**: 정밀 얼굴 인식 (없으면 Haar Cascade 사용)
- **diffusers/torch**: AI 배경 생성 (없으면 간단한 배경 생성)

## 파일 구조 규칙

### 출력 파일 명명
- 썸네일: `thumbnail_YYYYMMDD_HHMMSS_v{번호}.png`
- 합성: `{기능명}_YYYYMMDD_HHMMSS.png`

### 설정 파일
- `config.json`: 색상, 장르, 경로 등 설정
- 런타임에 변경 가능

## 테스트 전략

### 1. 단위 테스트
- 각 모듈의 핵심 기능 테스트
- `test_basic.py` 실행

### 2. 통합 테스트
- 전체 워크플로우 테스트
- `example_usage.py` 실행

### 3. GUI 테스트
- 수동 테스트 필요
- `python main.py` 실행

## 배포 전략

### Windows EXE
1. PyInstaller 사용
2. `build.bat` 실행
3. 의존성 자동 포함
4. 설정 파일 번들링

### 크기 최적화
- 선택적 의존성 제외 가능
- GPU 버전 vs CPU 버전 선택

## 향후 개선 사항

### 단기
- [ ] 더 많은 템플릿 추가
- [ ] 추가 효과 및 필터
- [ ] 사용자 정의 폰트 업로드

### 중기
- [ ] 배치 처리 UI
- [ ] 템플릿 편집기
- [ ] 히스토리 관리

### 장기
- [ ] 웹 버전
- [ ] 클라우드 저장
- [ ] 협업 기능

## 문제 해결 가이드

### 폰트 관련
- **문제**: 한글이 깨짐
- **해결**: 시스템에 한글 폰트 설치 또는 `assets/fonts/`에 추가

### 성능 문제
- **문제**: 처리가 느림
- **해결**: 이미지 크기 줄이기, GPU 사용, 선택적 의존성 최소화

### 의존성 설치 실패
- **문제**: dlib 설치 실패
- **해결**: 선택사항이므로 무시 가능, 기본 기능 사용

## 참고 자료

- [Pillow Documentation](https://pillow.readthedocs.io/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [rembg GitHub](https://github.com/danielgatis/rembg)

## 라이선스

이 프로젝트는 오픈소스이며 자유롭게 사용, 수정, 배포할 수 있습니다.
