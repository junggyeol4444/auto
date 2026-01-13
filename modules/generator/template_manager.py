# -*- coding: utf-8 -*-
"""
템플릿 관리자
콘텐츠 생성을 위한 템플릿을 관리합니다.
"""

import json
import random
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TemplateManager:
    """템플릿 관리 클래스"""
    
    def __init__(self, template_dir='templates'):
        """
        Args:
            template_dir (str): 템플릿 디렉토리 경로
        """
        self.template_dir = template_dir
        self.intro_templates = []
        self.outro_templates = []
        self.section_templates = []
        
        self.load_templates()
    
    def load_templates(self):
        """템플릿 파일 로드"""
        try:
            # Intro 템플릿
            intro_path = os.path.join(self.template_dir, 'intro_templates.json')
            if os.path.exists(intro_path):
                with open(intro_path, 'r', encoding='utf-8') as f:
                    self.intro_templates = json.load(f)
                logger.info(f"{len(self.intro_templates)}개의 인트로 템플릿 로드됨")
            
            # Outro 템플릿
            outro_path = os.path.join(self.template_dir, 'outro_templates.json')
            if os.path.exists(outro_path):
                with open(outro_path, 'r', encoding='utf-8') as f:
                    self.outro_templates = json.load(f)
                logger.info(f"{len(self.outro_templates)}개의 아웃트로 템플릿 로드됨")
            
            # Section 템플릿
            section_path = os.path.join(self.template_dir, 'section_templates.json')
            if os.path.exists(section_path):
                with open(section_path, 'r', encoding='utf-8') as f:
                    self.section_templates = json.load(f)
                logger.info(f"{len(self.section_templates)}개의 섹션 템플릿 로드됨")
            
        except Exception as e:
            logger.error(f"템플릿 로드 실패: {e}")
    
    def get_intro(self, topic):
        """
        인트로 생성
        
        Args:
            topic (str): 주제
            
        Returns:
            str: 인트로 텍스트
        """
        if not self.intro_templates:
            return f"{topic}에 대해 알아보겠습니다."
        
        template = random.choice(self.intro_templates)
        return template.format(주제=topic)
    
    def get_outro(self, topic):
        """
        아웃트로 생성
        
        Args:
            topic (str): 주제
            
        Returns:
            str: 아웃트로 텍스트
        """
        if not self.outro_templates:
            return "이상으로 마치겠습니다."
        
        template = random.choice(self.outro_templates)
        return template.format(주제=topic)
    
    def get_section_intro(self, subtitle):
        """
        섹션 인트로 생성
        
        Args:
            subtitle (str): 소제목
            
        Returns:
            str: 섹션 인트로 텍스트
        """
        if not self.section_templates:
            return f"{subtitle}"
        
        template = random.choice(self.section_templates)
        return template.format(소제목=subtitle)
    
    def create_blog_structure(self, topic, sections):
        """
        블로그 글 구조 생성
        
        Args:
            topic (str): 주제
            sections (list): 섹션 리스트 [{'title': '제목', 'content': '내용'}, ...]
            
        Returns:
            dict: 블로그 글 구조
        """
        structure = {
            'title': f"{topic}에 대한 완벽 가이드",
            'intro': self.get_intro(topic),
            'sections': [],
            'outro': self.get_outro(topic)
        }
        
        for section in sections:
            structure['sections'].append({
                'heading': section.get('title', ''),
                'intro': self.get_section_intro(section.get('title', '')),
                'content': section.get('content', '')
            })
        
        return structure
    
    def format_as_html(self, structure):
        """
        구조를 HTML로 변환
        
        Args:
            structure (dict): 블로그 글 구조
            
        Returns:
            str: HTML 텍스트
        """
        html = f"<h1>{structure['title']}</h1>\n\n"
        html += f"<p>{structure['intro']}</p>\n\n"
        
        for section in structure['sections']:
            html += f"<h2>{section['heading']}</h2>\n"
            html += f"<p>{section['intro']}</p>\n"
            html += f"<p>{section['content']}</p>\n\n"
        
        html += f"<p>{structure['outro']}</p>\n"
        
        return html
    
    def format_as_markdown(self, structure):
        """
        구조를 Markdown으로 변환
        
        Args:
            structure (dict): 블로그 글 구조
            
        Returns:
            str: Markdown 텍스트
        """
        md = f"# {structure['title']}\n\n"
        md += f"{structure['intro']}\n\n"
        
        for section in structure['sections']:
            md += f"## {section['heading']}\n\n"
            md += f"{section['intro']}\n\n"
            md += f"{section['content']}\n\n"
        
        md += f"{structure['outro']}\n"
        
        return md


if __name__ == '__main__':
    # 테스트 코드
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    manager = TemplateManager(template_dir='../../templates')
    
    # 샘플 섹션
    sections = [
        {'title': '인공지능이란', 'content': '인공지능은 인간의 지능을 모방한 기술입니다.'},
        {'title': '인공지능의 역사', 'content': '1950년대부터 연구가 시작되었습니다.'},
        {'title': '인공지능의 미래', 'content': '다양한 분야에서 활용될 것입니다.'}
    ]
    
    # 구조 생성
    structure = manager.create_blog_structure('인공지능', sections)
    
    # Markdown 출력
    markdown = manager.format_as_markdown(structure)
    print(markdown)
