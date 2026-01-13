# 기여 가이드

Auto Blog Master 프로젝트에 기여해주셔서 감사합니다! 🎉

## 기여 방법

### 버그 리포트

버그를 발견하셨다면 다음 정보와 함께 Issue를 등록해주세요:

- 문제 설명
- 재현 방법
- 예상 동작
- 실제 동작
- 환경 정보 (OS, Python 버전)
- 에러 로그

### 기능 제안

새로운 기능을 제안하고 싶다면:

1. Issue에 제안 내용을 작성해주세요
2. 기능의 필요성과 사용 사례를 설명해주세요
3. 가능하다면 구현 방법도 제안해주세요

### Pull Request

1. **Fork** 저장소를 Fork 합니다
2. **Branch** 새 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature`)
3. **Commit** 변경사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`)
4. **Push** 브랜치에 푸시합니다 (`git push origin feature/AmazingFeature`)
5. **Pull Request** PR을 생성합니다

## 개발 가이드라인

### 코드 스타일

- PEP 8 스타일 가이드를 따릅니다
- 한국어 주석을 사용합니다
- Docstring을 작성합니다

```python
def example_function(param1, param2):
    """
    함수 설명
    
    Args:
        param1 (str): 파라미터 1 설명
        param2 (int): 파라미터 2 설명
        
    Returns:
        bool: 반환값 설명
    """
    pass
```

### 테스트

- 새로운 기능에는 테스트를 추가해주세요
- `python test_basic.py`로 기본 테스트를 실행하세요

### 커밋 메시지

명확하고 설명적인 커밋 메시지를 작성해주세요:

```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 스타일 변경
refactor: 리팩토링
test: 테스트 추가/수정
chore: 기타 변경사항
```

## 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/junggyeol4444/auto.git
cd auto

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 설정
python setup.py
```

## 프로젝트 구조

```
auto/
├── modules/          # 핵심 모듈
│   ├── crawler/      # 크롤러
│   ├── generator/    # 콘텐츠 생성
│   ├── optimizer/    # SEO 최적화
│   ├── image/        # 이미지 처리
│   ├── publisher/    # 발행
│   └── translator/   # 번역
├── gui/              # GUI 인터페이스
├── templates/        # 템플릿 파일
└── main.py           # 메인 실행 파일
```

## 질문이 있으신가요?

- Issue를 통해 질문해주세요
- 문서를 먼저 확인해보세요

감사합니다! 🙏
