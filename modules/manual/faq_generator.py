"""
FAQ generator for manuals
"""


class FAQGenerator:
    """Generate FAQ sections"""
    
    def __init__(self):
        self.common_questions = {
            'product': [
                {
                    'q': '제품이 작동하지 않아요.',
                    'a': '전원이 제대로 연결되어 있는지 확인하세요. 전원 버튼을 3초 이상 눌러보세요.'
                },
                {
                    'q': '초기화는 어떻게 하나요?',
                    'a': '설정 메뉴에서 "초기화" 또는 "공장 초기화"를 선택하세요. 주의: 모든 데이터가 삭제됩니다.'
                },
                {
                    'q': '보증 기간은 얼마나 되나요?',
                    'a': '제품 구매일로부터 1년간 무상 보증 서비스를 제공합니다.'
                },
                {
                    'q': 'A/S는 어디서 받을 수 있나요?',
                    'a': '가까운 서비스 센터를 방문하시거나 고객센터(1234-5678)로 문의하세요.'
                },
                {
                    'q': '소모품 구매는 어떻게 하나요?',
                    'a': '공식 온라인 쇼핑몰이나 대리점에서 구매 가능합니다.'
                }
            ],
            'software': [
                {
                    'q': '설치가 안 됩니다.',
                    'a': '관리자 권한으로 실행해보세요. 백신 프로그램을 일시적으로 비활성화하고 시도해보세요.'
                },
                {
                    'q': '프로그램이 느려요.',
                    'a': '불필요한 프로그램을 종료하세요. 메모리 부족일 수 있으니 시스템 요구사항을 확인하세요.'
                },
                {
                    'q': '업데이트는 어떻게 하나요?',
                    'a': '도움말 메뉴 > 업데이트 확인을 선택하시거나, 자동 업데이트 기능을 활성화하세요.'
                },
                {
                    'q': '라이선스 키를 잃어버렸어요.',
                    'a': '구매 확인 이메일을 확인하시거나 고객지원팀에 문의하세요.'
                },
                {
                    'q': '데이터를 복구할 수 있나요?',
                    'a': '자동 백업 기능이 활성화되어 있다면 파일 > 백업에서 복구할 수 있습니다.'
                },
                {
                    'q': '오류 코드의 의미는?',
                    'a': '매뉴얼의 "오류 코드" 섹션을 참고하시거나 고객지원팀에 오류 코드를 알려주세요.'
                }
            ]
        }
    
    def generate_faq(self, manual_type='product', custom_questions=None):
        """Generate FAQ section"""
        faqs = []
        
        # Add common questions
        if manual_type in self.common_questions:
            faqs.extend(self.common_questions[manual_type])
        
        # Add custom questions
        if custom_questions:
            for q in custom_questions:
                if isinstance(q, dict) and 'q' in q and 'a' in q:
                    faqs.append(q)
        
        return self._format_faq(faqs)
    
    def _format_faq(self, faqs):
        """Format FAQ list"""
        formatted = []
        
        for i, faq in enumerate(faqs, 1):
            formatted.append(f"**Q{i}: {faq['q']}**")
            formatted.append(f"A: {faq['a']}")
            formatted.append("")  # Empty line between FAQs
        
        return '\n'.join(formatted)
    
    def add_custom_faq(self, question, answer):
        """Add custom FAQ entry"""
        return {
            'q': question,
            'a': answer
        }
