#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
테스트 스크립트
핵심 기능을 테스트합니다.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """모듈 임포트 테스트"""
    print("=" * 50)
    print("모듈 임포트 테스트")
    print("=" * 50)
    
    modules_to_test = [
        ('modules.crawler.news_crawler', 'NewsCrawler'),
        ('modules.crawler.wiki_crawler', 'WikiCrawler'),
        ('modules.crawler.coupang_crawler', 'CoupangCrawler'),
        ('modules.generator.content_generator', 'ContentGenerator'),
        ('modules.generator.template_manager', 'TemplateManager'),
        ('modules.generator.keyword_extractor', 'KeywordExtractor'),
        ('modules.optimizer.seo_optimizer', 'SEOOptimizer'),
        ('modules.optimizer.meta_generator', 'MetaGenerator'),
        ('modules.publisher.tistory_publisher', 'TistoryPublisher'),
        ('modules.publisher.wordpress_publisher', 'WordPressPublisher'),
        ('modules.translator.multi_translator', 'MultiTranslator'),
    ]
    
    success_count = 0
    fail_count = 0
    
    for module_path, class_name in modules_to_test:
        try:
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✓ {class_name:30} - OK")
            success_count += 1
        except Exception as e:
            print(f"✗ {class_name:30} - FAIL: {str(e)[:50]}")
            fail_count += 1
    
    print(f"\n결과: {success_count} 성공, {fail_count} 실패")
    return fail_count == 0


def test_template_manager():
    """템플릿 매니저 테스트 (의존성 없음)"""
    print("\n" + "=" * 50)
    print("템플릿 매니저 테스트")
    print("=" * 50)
    
    try:
        from modules.generator.template_manager import TemplateManager
        
        manager = TemplateManager(template_dir='templates')
        
        # 인트로 생성
        intro = manager.get_intro('인공지능')
        print(f"✓ 인트로 생성: {intro}")
        
        # 아웃트로 생성
        outro = manager.get_outro('인공지능')
        print(f"✓ 아웃트로 생성: {outro}")
        
        # 구조 생성
        sections = [
            {'title': '개요', 'content': '인공지능에 대한 개요입니다.'},
            {'title': '역사', 'content': '인공지능의 역사입니다.'}
        ]
        structure = manager.create_blog_structure('인공지능', sections)
        print(f"✓ 블로그 구조 생성: 제목 '{structure['title']}'")
        
        return True
        
    except Exception as e:
        print(f"✗ 템플릿 매니저 테스트 실패: {e}")
        return False


def test_seo_optimizer():
    """SEO 최적화기 테스트 (의존성 없음)"""
    print("\n" + "=" * 50)
    print("SEO 최적화기 테스트")
    print("=" * 50)
    
    try:
        from modules.optimizer.seo_optimizer import SEOOptimizer
        
        optimizer = SEOOptimizer()
        
        # 키워드 밀도 분석
        sample_text = "인공지능은 중요합니다. 인공지능 기술이 발전하고 있습니다. " * 10
        result = optimizer.analyze_keyword_density(sample_text, '인공지능')
        print(f"✓ 키워드 밀도: {result['density']}% (상태: {result['status']})")
        
        # SEO 점수 계산
        content = {
            'title': '인공지능 가이드',
            'intro': '인공지능에 대해 알아봅니다.',
            'sections': [
                {'title': '섹션1', 'content': '내용1 ' * 50},
                {'title': '섹션2', 'content': '내용2 ' * 50}
            ]
        }
        score_result = optimizer.calculate_seo_score(content, '인공지능')
        print(f"✓ SEO 점수: {score_result['percentage']}%")
        
        return True
        
    except Exception as e:
        print(f"✗ SEO 최적화기 테스트 실패: {e}")
        return False


def test_meta_generator():
    """메타 생성기 테스트"""
    print("\n" + "=" * 50)
    print("메타 생성기 테스트")
    print("=" * 50)
    
    try:
        from modules.optimizer.meta_generator import MetaGenerator
        
        generator = MetaGenerator()
        
        # 메타 디스크립션 생성
        content = "인공지능은 현대 기술의 핵심입니다. 다양한 분야에서 활용됩니다."
        description = generator.generate_meta_description(content, max_length=100)
        print(f"✓ 메타 디스크립션: {description}")
        
        # 메타 키워드 생성
        keywords = ['인공지능', '머신러닝', '딥러닝']
        meta_keywords = generator.generate_meta_keywords(keywords)
        print(f"✓ 메타 키워드: {meta_keywords}")
        
        return True
        
    except Exception as e:
        print(f"✗ 메타 생성기 테스트 실패: {e}")
        return False


def test_config_loading():
    """설정 파일 로딩 테스트"""
    print("\n" + "=" * 50)
    print("설정 파일 로딩 테스트")
    print("=" * 50)
    
    try:
        import json
        
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"✓ config.json 로드 성공")
        print(f"  - 티스토리 설정: {bool(config.get('tistory'))}")
        print(f"  - 네이버 설정: {bool(config.get('naver'))}")
        print(f"  - 워드프레스 설정: {bool(config.get('wordpress'))}")
        print(f"  - 쿠팡 설정: {bool(config.get('coupang'))}")
        
        return True
        
    except Exception as e:
        print(f"✗ 설정 파일 로딩 실패: {e}")
        return False


def main():
    """메인 테스트 함수"""
    print("\n")
    print("╔" + "═" * 48 + "╗")
    print("║" + " " * 10 + "Auto Blog Master 테스트" + " " * 14 + "║")
    print("╚" + "═" * 48 + "╝")
    print("\n")
    
    tests = [
        ("모듈 임포트", test_imports),
        ("설정 파일", test_config_loading),
        ("템플릿 매니저", test_template_manager),
        ("SEO 최적화기", test_seo_optimizer),
        ("메타 생성기", test_meta_generator),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} 테스트 중 예외 발생: {e}")
            results.append((test_name, False))
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("테스트 결과 요약")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 통과" if result else "✗ 실패"
        print(f"{test_name:20} : {status}")
    
    print(f"\n총 {passed}/{total} 테스트 통과")
    
    if passed == total:
        print("\n🎉 모든 테스트 통과!")
        return 0
    else:
        print(f"\n⚠️  {total - passed}개 테스트 실패")
        print("\n참고: 일부 테스트는 외부 라이브러리 설치 후 통과됩니다.")
        print("설치: pip install -r requirements.txt")
        return 1


if __name__ == '__main__':
    sys.exit(main())
