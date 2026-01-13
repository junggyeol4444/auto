"""
Structure generator for manuals
"""


class StructureGenerator:
    """Generate manual structure"""
    
    def __init__(self, template_manager):
        self.template_manager = template_manager
    
    def generate_product_manual(self, product_name, product_type, features, instructions):
        """Generate product manual structure"""
        sections = []
        
        # 1. Product Introduction
        intro_section = {
            'title': '제품 소개',
            'subsections': [
                {
                    'title': '제품 개요',
                    'content': f"{product_name}은(는) {product_type}입니다.\n\n이 제품은 사용자의 편의를 위해 설계되었습니다."
                },
                {
                    'title': '주요 특징',
                    'content': self._format_features(features)
                },
                {
                    'title': '사양',
                    'content': '제품 사양:\n- 제조사: [제조사명]\n- 모델명: ' + product_name
                }
            ]
        }
        sections.append(intro_section)
        
        # 2. Package Contents
        package_section = {
            'title': '구성품 확인',
            'content': '제품 구성품을 확인하세요:\n- 본체 1개\n- 사용 설명서 1부\n- 보증서 1부'
        }
        sections.append(package_section)
        
        # 3. Installation
        install_section = {
            'title': '설치 방법',
            'content': self._generate_installation_steps(instructions)
        }
        sections.append(install_section)
        
        # 4. Usage
        usage_section = {
            'title': '사용 방법',
            'content': self._generate_usage_instructions(instructions)
        }
        sections.append(usage_section)
        
        # 5. Precautions
        precaution_section = {
            'title': '주의사항',
            'content': '⚠️ 안전을 위해 다음 사항을 준수하세요:\n\n- 제품을 분해하지 마세요.\n- 물기가 있는 곳에서 사용하지 마세요.\n- 직사광선을 피해 보관하세요.'
        }
        sections.append(precaution_section)
        
        # 6. Troubleshooting
        faq_section = {
            'title': '문제 해결',
            'subsections': [
                {
                    'title': 'FAQ',
                    'content': self._generate_faq()
                }
            ]
        }
        sections.append(faq_section)
        
        # 7. Glossary
        glossary_section = {
            'title': '용어집',
            'content': '주요 용어 설명:\n- 전원: 제품을 작동시키는 에너지\n- 모드: 제품의 동작 방식'
        }
        sections.append(glossary_section)
        
        return {
            'title': f'{product_name} 사용 설명서',
            'type': 'product',
            'sections': sections
        }
    
    def generate_software_manual(self, software_name, version, features, functions):
        """Generate software manual structure"""
        sections = []
        
        # 1. Introduction
        intro_section = {
            'title': '소개',
            'subsections': [
                {
                    'title': '프로그램 개요',
                    'content': f"{software_name}은(는) 사용자를 위한 소프트웨어입니다.\n버전: {version}"
                },
                {
                    'title': '주요 기능',
                    'content': self._format_features(features)
                },
                {
                    'title': '시스템 요구사항',
                    'content': '• OS: Windows 10 이상\n• RAM: 4GB 이상\n• 저장 공간: 500MB 이상'
                }
            ]
        }
        sections.append(intro_section)
        
        # 2. Installation
        install_section = {
            'title': '설치',
            'subsections': [
                {
                    'title': '다운로드',
                    'content': '공식 웹사이트에서 설치 파일을 다운로드하세요.'
                },
                {
                    'title': '설치 과정',
                    'content': '1. 다운로드한 파일을 실행하세요.\n2. 설치 마법사의 지시를 따르세요.\n3. 설치 완료 후 프로그램을 실행하세요.'
                }
            ]
        }
        sections.append(install_section)
        
        # 3. User Interface
        ui_section = {
            'title': '사용자 인터페이스',
            'content': '메인 화면에서 모든 기능에 접근할 수 있습니다.\n\n주요 메뉴:\n- 파일: 파일 작업\n- 편집: 편집 기능\n- 보기: 화면 설정\n- 도구: 추가 도구'
        }
        sections.append(ui_section)
        
        # 4. Features
        features_section = {
            'title': '기능 설명',
            'content': self._format_software_functions(functions)
        }
        sections.append(features_section)
        
        # 5. Tutorial
        tutorial_section = {
            'title': '튜토리얼',
            'content': '시작하기:\n1. 프로그램을 실행하세요.\n2. 새 프로젝트를 생성하세요.\n3. 작업을 시작하세요.'
        }
        sections.append(tutorial_section)
        
        # 6. Troubleshooting
        trouble_section = {
            'title': '문제 해결',
            'content': self._generate_software_faq()
        }
        sections.append(trouble_section)
        
        # 7. Appendix
        appendix_section = {
            'title': '부록',
            'subsections': [
                {
                    'title': '용어집',
                    'content': '주요 용어 설명'
                },
                {
                    'title': '업데이트 기록',
                    'content': f'버전 {version}: 최초 릴리즈'
                }
            ]
        }
        sections.append(appendix_section)
        
        return {
            'title': f'{software_name} 사용자 매뉴얼',
            'type': 'software',
            'sections': sections
        }
    
    def _format_features(self, features):
        """Format features list"""
        if not features:
            return '주요 특징이 여기에 표시됩니다.'
        
        if isinstance(features, str):
            features = [f.strip() for f in features.split('\n') if f.strip()]
        
        formatted = []
        for i, feature in enumerate(features, 1):
            formatted.append(f"{i}. {feature}")
        
        return '\n'.join(formatted)
    
    def _format_software_functions(self, functions):
        """Format software functions"""
        if not functions:
            return '기능 설명이 여기에 표시됩니다.'
        
        if isinstance(functions, str):
            functions = [f.strip() for f in functions.split('\n') if f.strip()]
        
        formatted = []
        for func in functions:
            formatted.append(f"• {func}")
        
        return '\n'.join(formatted)
    
    def _generate_installation_steps(self, instructions):
        """Generate installation steps"""
        if instructions:
            return f"설치 순서:\n\n{instructions}"
        
        return "1. 제품을 포장에서 꺼내세요.\n2. 모든 구성품을 확인하세요.\n3. 설치 위치를 선정하세요.\n4. 제품을 설치하세요."
    
    def _generate_usage_instructions(self, instructions):
        """Generate usage instructions"""
        if instructions:
            return f"사용 방법:\n\n{instructions}"
        
        return "기본 사용 방법:\n1. 전원을 켜세요.\n2. 원하는 기능을 선택하세요.\n3. 작업을 완료한 후 전원을 끄세요."
    
    def _generate_faq(self):
        """Generate FAQ section"""
        faq = [
            "Q: 제품이 작동하지 않습니다.\nA: 전원 연결을 확인하세요.",
            "\nQ: 소음이 발생합니다.\nA: 정상적인 작동음일 수 있습니다. 지속되면 A/S 센터에 문의하세요.",
            "\nQ: A/S는 어디서 받나요?\nA: 고객센터(1234-5678)로 문의하세요."
        ]
        return ''.join(faq)
    
    def _generate_software_faq(self):
        """Generate software FAQ"""
        faq = [
            "Q: 프로그램이 실행되지 않습니다.\nA: 시스템 요구사항을 확인하고 재설치를 시도하세요.",
            "\nQ: 데이터가 저장되지 않습니다.\nA: 저장 경로의 쓰기 권한을 확인하세요.",
            "\nQ: 업데이트는 어떻게 하나요?\nA: 도움말 메뉴에서 '업데이트 확인'을 선택하세요."
        ]
        return ''.join(faq)
