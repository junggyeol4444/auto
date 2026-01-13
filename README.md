# Auto Blog Master 🤖

블로그 자동화 시스템 - 웹 크롤링과 템플릿 시스템으로 블로그 포스팅 자동 생성 및 발행

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 목차

- [개요](#개요)
- [주요 기능](#주요-기능)
- [지원 블로그 유형](#지원-블로그-유형)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [디렉토리 구조](#디렉토리-구조)
- [설정](#설정)
- [기술 스택](#기술-스택)
- [라이선스](#라이선스)

## 🎯 개요

Auto Blog Master는 웹 크롤링과 자연어 처리 기술을 활용하여 블로그 콘텐츠를 자동으로 생성하고 여러 플랫폼에 발행하는 시스템입니다. AI API 없이도 고품질의 SEO 최적화된 콘텐츠를 생성할 수 있습니다.

### 핵심 원리
1. 웹에서 정보 수집 (크롤링)
2. TextRank 알고리즘으로 핵심 내용 추출
3. 템플릿 시스템으로 자연스러운 글 재구성
4. SEO 최적화 적용
5. 다중 플랫폼 자동 발행

## ✨ 주요 기능

### 1. 콘텐츠 자동 생성
- 🌐 웹 크롤링을 통한 정보 수집 (뉴스, 위키피디아, SNS)
- 📝 TextRank 알고리즘으로 핵심 문장 추출
- 🎨 템플릿 시스템으로 자연스러운 글 재구성
- 🔑 자동 요약 및 키워드 추출

### 2. SEO 최적화
- ✅ 키워드 밀도 자동 분석 및 조정 (1-3% 권장)
- 📊 검색 친화적 제목 생성
- 🏷️ 메타 태그 자동 생성
- 📑 헤딩 구조(H1/H2/H3) 자동 구성
- 🖼️ 이미지 ALT 태그 생성
- 🔗 내부 링크 자동 삽입

### 3. 이미지 자동 처리
- 🔍 무료 스톡 이미지 자동 검색 (Unsplash, Pexels)
- 📥 주제에 맞는 이미지 자동 다운로드
- 📌 본문에 자동 삽입 (H2 제목마다 배치)
- 🎨 이미지 최적화 (리사이즈, 압축)

### 4. 쿠팡파트너스 연동
- 🛒 쿠팡 제품 자동 검색
- 💰 제품 정보 추출 (이름, 가격, 이미지, 링크)
- 📊 제품 비교 테이블 자동 생성
- 🔗 파트너스 링크 자동 삽입

### 5. 멀티 플랫폼 발행
- **티스토리**: API 자동 발행
- **네이버 블로그**: Selenium 웹 자동화 발행
- **워드프레스**: XML-RPC API 발행
- 여러 플랫폼 동시 발행 가능

### 6. 예약 발행 시스템
- ⏰ 날짜/시간 예약 발행
- 🔄 반복 발행 스케줄 (매일, 주 3회 등)

## 📚 지원 블로그 유형

1. **SEO 최적화 블로그**: 검색 상위 노출 목적의 정보성 블로그
2. **게임 공략 블로그**: 게임 가이드, 팁, 공략 정보
3. **웹툰/웹소설 리뷰**: 작품 리뷰, 줄거리 요약, 추천
4. **만화 리뷰 블로그**: 일본 만화, 한국 만화 리뷰, 추천
5. **드라마/영화 리뷰**: 작품 분석, 평론, 추천
6. **IT/테크 뉴스 블로그**: 최신 기술 뉴스 큐레이션
7. **쿠팡파트너스 블로그**: 제품 리뷰 + 수익화

## 🚀 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/junggyeol4444/auto.git
cd auto
```

### 2. 가상환경 생성 (권장)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. NLTK 데이터 다운로드

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 5. 설정 파일 편집

`config.json` 파일을 열어 API 키와 계정 정보를 입력합니다.

## 📖 사용 방법

### GUI 모드 실행

```bash
python main.py
```

### 기본 사용 흐름

1. **주제 입력**: 작성할 블로그의 주제나 키워드를 입력
2. **블로그 유형 선택**: 7가지 유형 중 선택
3. **발행 플랫폼 선택**: 티스토리, 네이버, 워드프레스 중 선택
4. **옵션 설정**: 이미지 자동 삽입, SEO 최적화, 쿠팡 제품 삽입
5. **생성 시작**: 자동으로 콘텐츠 생성
6. **미리보기 및 수정**: 생성된 글 확인 및 편집
7. **발행**: 선택한 플랫폼에 자동 발행

### 개별 모듈 사용 예제

#### 뉴스 크롤러

```python
from modules.crawler.news_crawler import NewsCrawler

crawler = NewsCrawler()
articles = crawler.crawl('인공지능', max_articles=5)
```

#### 콘텐츠 생성기

```python
from modules.generator.content_generator import ContentGenerator

generator = ContentGenerator()
summary = generator.summarize_text(text, ratio=0.3)
```

#### SEO 최적화

```python
from modules.optimizer.seo_optimizer import SEOOptimizer

optimizer = SEOOptimizer()
result = optimizer.analyze_keyword_density(text, '인공지능')
```

## 📁 디렉토리 구조

```
Auto_Blog_Master/
├── main.py                    # 메인 실행 파일
├── config.json                # 설정 파일
├── requirements.txt           # 의존성 목록
├── README.md                  # 사용 설명서
│
├── modules/
│   ├── crawler/               # 크롤러 모듈
│   │   ├── news_crawler.py
│   │   ├── wiki_crawler.py
│   │   ├── coupang_crawler.py
│   │   ├── twitter_crawler.py
│   │   ├── pixiv_crawler.py
│   │   ├── instagram_crawler.py
│   │   └── sns_aggregator.py
│   │
│   ├── generator/             # 콘텐츠 생성 모듈
│   │   ├── content_generator.py
│   │   ├── template_manager.py
│   │   └── keyword_extractor.py
│   │
│   ├── optimizer/             # SEO 최적화 모듈
│   │   ├── seo_optimizer.py
│   │   └── meta_generator.py
│   │
│   ├── image/                 # 이미지 처리 모듈
│   │   ├── image_searcher.py
│   │   └── image_processor.py
│   │
│   ├── publisher/             # 발행 모듈
│   │   ├── tistory_publisher.py
│   │   ├── naver_publisher.py
│   │   └── wordpress_publisher.py
│   │
│   └── translator/            # 번역 모듈
│       └── multi_translator.py
│
├── gui/                       # GUI 모듈
│   ├── main_window.py
│   ├── editor_window.py
│   └── settings_window.py
│
├── templates/                 # 템플릿 파일
│   ├── intro_templates.json
│   ├── outro_templates.json
│   └── section_templates.json
│
├── output/                    # 출력 디렉토리
│   ├── drafts/
│   └── images/
│
└── cache/                     # 캐시 디렉토리
    └── crawled_data/
```

## ⚙️ 설정

### config.json 구조

```json
{
  "tistory": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "access_token": "YOUR_ACCESS_TOKEN",
    "blog_name": "YOUR_BLOG_NAME"
  },
  "naver": {
    "id": "YOUR_NAVER_ID",
    "password": "YOUR_PASSWORD"
  },
  "wordpress": {
    "url": "https://your-wordpress-site.com",
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD"
  },
  "coupang": {
    "partner_id": "YOUR_PARTNER_ID",
    "access_key": "YOUR_ACCESS_KEY",
    "secret_key": "YOUR_SECRET_KEY"
  },
  "unsplash": {
    "access_key": "YOUR_UNSPLASH_KEY"
  },
  "pexels": {
    "api_key": "YOUR_PEXELS_KEY"
  }
}
```

### API 키 발급 방법

- **티스토리**: [Tistory 오픈 API](https://www.tistory.com/guide/api/manage/register)
- **Unsplash**: [Unsplash Developers](https://unsplash.com/developers)
- **Pexels**: [Pexels API](https://www.pexels.com/api/)
- **쿠팡파트너스**: [쿠팡 파트너스](https://partners.coupang.com/)

## 🛠️ 기술 스택

### 웹 크롤링
- requests, BeautifulSoup4, selenium, newspaper3k, wikipedia

### 자연어 처리
- nltk, konlpy, gensim, rake-nltk, scikit-learn

### 번역
- googletrans, langdetect

### 블로그 발행
- pytistory, python-wordpress-xmlrpc, selenium, webdriver-manager

### 이미지 처리
- Pillow

### GUI
- customtkinter

### 기타
- pandas, schedule

## 🚨 주의사항

1. **크롤링**: 대상 사이트의 robots.txt와 이용약관을 준수하세요
2. **자동화**: 네이버 블로그 자동 발행은 자동화 감지 시스템으로 제한될 수 있습니다
3. **저작권**: 크롤링한 콘텐츠는 반드시 재구성하여 사용하세요
4. **API 한도**: 각 API의 사용 한도를 확인하세요

## 🔧 문제 해결

### 크롤링 실패
- 네트워크 연결 확인
- User-Agent 헤더 확인
- 대상 사이트 구조 변경 여부 확인

### 발행 실패
- API 키/계정 정보 확인
- API 사용 한도 확인
- 네트워크 방화벽 설정 확인

### GUI 실행 오류
- customtkinter 설치 확인
- Python 버전 확인 (3.8 이상)

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 👨‍💻 기여

버그 리포트, 기능 제안, PR을 환영합니다!

## 📧 연락처

문의사항이 있으시면 Issue를 등록해주세요.

---

**주의**: 이 도구는 교육 목적으로 제작되었습니다. 웹 크롤링 시 해당 사이트의 이용약관을 반드시 확인하고 준수하세요.