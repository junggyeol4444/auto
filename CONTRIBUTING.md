# Contributing to AI Design Automation Suite

AI Design Automation Suite 프로젝트에 기여해 주셔서 감사합니다!

## 개발 환경 설정

### 1. 저장소 포크 및 클론

```bash
# 저장소 포크
# GitHub에서 Fork 버튼 클릭

# 클론
git clone https://github.com/YOUR_USERNAME/auto.git
cd auto

# 원본 저장소 추가
git remote add upstream https://github.com/junggyeol4444/auto.git
```

### 2. 가상환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 활성화
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 의존성 설치

```bash
# 개발용 의존성 포함
pip install -r requirements.txt
pip install pytest flake8 black
```

## 개발 가이드라인

### 코드 스타일

#### Python 코드
- **PEP 8** 준수
- **Black** 포매터 사용 (라인 길이: 100)
- **Type hints** 사용 권장

```python
def process_image(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
    """
    Process an image
    
    Args:
        image: Input PIL Image
        size: Target size (width, height)
    
    Returns:
        Processed PIL Image
    """
    pass
```

#### 문서화
- 모든 공개 함수/클래스에 docstring 작성
- 한글 또는 영어 사용 가능
- Google 스타일 또는 NumPy 스타일 docstring

#### 네이밍 규칙
- 함수/변수: `snake_case`
- 클래스: `PascalCase`
- 상수: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`

### 프로젝트 구조

새로운 기능 추가 시 적절한 위치에 배치:

```
modules/
├── thumbnail/        # 썸네일 관련 기능
├── photo_synthesis/  # 사진 합성 관련 기능
├── ai_generation/    # AI 생성 관련 기능
└── utils/            # 공통 유틸리티
```

### 의존성 관리

#### 새로운 의존성 추가
1. 필수 의존성인지 선택사항인지 결정
2. `requirements.txt`에 추가
3. 선택적 의존성은 주석 처리하고 try-except로 처리

```python
try:
    import optional_library
    OPTIONAL_AVAILABLE = True
except ImportError:
    OPTIONAL_AVAILABLE = False
    print("Warning: optional_library not available")
```

#### 최소 의존성 원칙
- 무거운 라이브러리는 선택사항으로
- 가벼운 대안이 있다면 그것 사용
- GPU 전용 라이브러리는 CPU 폴백 제공

### 에러 처리

#### 사용자 친화적 에러 메시지
```python
try:
    result = process_image(image)
except FileNotFoundError:
    raise ValueError("이미지 파일을 찾을 수 없습니다. 경로를 확인하세요.")
except Exception as e:
    raise RuntimeError(f"이미지 처리 중 오류 발생: {e}")
```

#### 폴백 메커니즘
```python
def remove_background(image: Image.Image) -> Image.Image:
    if REMBG_AVAILABLE:
        return remove_with_rembg(image)
    else:
        print("rembg를 사용할 수 없어 기본 방식을 사용합니다")
        return remove_fallback(image)
```

## 기여 프로세스

### 1. 이슈 생성 또는 확인
- 버그 리포트
- 기능 요청
- 질문

### 2. 브랜치 생성
```bash
git checkout -b feature/new-feature
# 또는
git checkout -b fix/bug-fix
```

### 3. 개발
- 작은 단위로 커밋
- 명확한 커밋 메시지 작성

```bash
git add .
git commit -m "Add new thumbnail template for cooking genre"
```

### 4. 테스트
```bash
# 기본 테스트
python test_basic.py

# 예제 실행
python example_usage.py

# GUI 테스트
python main.py
```

### 5. 코드 정리
```bash
# 포매팅
black .

# 린팅
flake8 modules/ gui/
```

### 6. Pull Request
```bash
git push origin feature/new-feature
```

GitHub에서 Pull Request 생성

#### PR 체크리스트
- [ ] 테스트 통과
- [ ] 문서 업데이트
- [ ] 코드 스타일 준수
- [ ] 커밋 메시지 명확
- [ ] 변경사항 설명

## 기여 유형

### 버그 수정
1. 이슈에서 버그 확인
2. 재현 단계 문서화
3. 수정 및 테스트
4. PR 생성

### 새 기능 추가
1. 이슈에서 기능 논의
2. 설계 리뷰
3. 구현
4. 테스트 및 문서화
5. PR 생성

### 문서 개선
- README 개선
- ARCHITECTURE 업데이트
- 코드 주석 추가
- 예제 추가

### 번역
- UI 텍스트 다국어 지원
- 문서 번역

## 커밋 메시지 가이드

### 형식
```
<type>: <subject>

<body>

<footer>
```

### Type
- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 스타일 (포매팅)
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드/도구 변경

### 예제
```
feat: Add vintage filter to color grading

Implement a vintage filter that reduces saturation and 
adds warm tint to images.

Closes #123
```

## 리뷰 프로세스

1. PR 제출
2. 자동 테스트 실행
3. 코드 리뷰
4. 피드백 반영
5. 승인 및 머지

## 코드 리뷰 가이드라인

### 리뷰어
- 건설적인 피드백 제공
- 코드 스타일, 로직, 성능 확인
- 테스트 케이스 충분한지 확인

### 작성자
- 피드백 수용적으로 받아들이기
- 질문에 명확히 답변
- 필요시 코드 수정

## 버전 관리

### 버전 번호
- Semantic Versioning 사용
- MAJOR.MINOR.PATCH
  - MAJOR: 호환성 없는 변경
  - MINOR: 기능 추가 (호환)
  - PATCH: 버그 수정

## 릴리스 프로세스

1. 버전 번호 결정
2. CHANGELOG 업데이트
3. 태그 생성
4. GitHub Release 생성
5. (선택) PyPI 배포

## 질문이나 도움이 필요하신가요?

- GitHub Issues에 질문 올리기
- 기존 이슈/PR 검색
- 문서 확인

## 행동 강령

- 존중과 배려
- 건설적인 피드백
- 다양성 존중
- 협력적 태도

## 감사합니다!

여러분의 기여가 프로젝트를 더 좋게 만듭니다. 🎉
