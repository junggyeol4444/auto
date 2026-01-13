# -*- coding: utf-8 -*-
"""
이미지 처리기
이미지 다운로드, 리사이즈, 최적화를 수행합니다.
"""

import requests
from PIL import Image
import io
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageProcessor:
    """이미지 처리 클래스"""
    
    def __init__(self, output_dir='output/images'):
        """
        Args:
            output_dir (str): 이미지 저장 디렉토리
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def download_image(self, url, filename):
        """
        이미지 다운로드
        
        Args:
            url (str): 이미지 URL
            filename (str): 저장할 파일명
            
        Returns:
            str: 저장된 파일 경로 또는 None
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"이미지 다운로드 완료: {filename}")
            return filepath
            
        except Exception as e:
            logger.error(f"이미지 다운로드 실패: {e}")
            return None
    
    def resize_image(self, filepath, max_width=1200, max_height=800):
        """
        이미지 리사이즈
        
        Args:
            filepath (str): 이미지 파일 경로
            max_width (int): 최대 너비
            max_height (int): 최대 높이
            
        Returns:
            bool: 성공 여부
        """
        try:
            with Image.open(filepath) as img:
                # 원본 비율 유지하며 리사이즈
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                img.save(filepath, optimize=True, quality=85)
            
            logger.info(f"이미지 리사이즈 완료: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"이미지 리사이즈 실패: {e}")
            return False
    
    def optimize_image(self, filepath, quality=85):
        """
        이미지 최적화 (압축)
        
        Args:
            filepath (str): 이미지 파일 경로
            quality (int): 품질 (1-100)
            
        Returns:
            bool: 성공 여부
        """
        try:
            with Image.open(filepath) as img:
                # RGB로 변환 (RGBA 등 다른 모드 처리)
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 최적화하여 저장
                img.save(filepath, 'JPEG', optimize=True, quality=quality)
            
            logger.info(f"이미지 최적화 완료: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"이미지 최적화 실패: {e}")
            return False
    
    def process_image(self, url, filename, max_width=1200, max_height=800, quality=85):
        """
        이미지 다운로드 및 처리 (통합)
        
        Args:
            url (str): 이미지 URL
            filename (str): 저장할 파일명
            max_width (int): 최대 너비
            max_height (int): 최대 높이
            quality (int): 압축 품질
            
        Returns:
            str: 처리된 파일 경로 또는 None
        """
        # 다운로드
        filepath = self.download_image(url, filename)
        if not filepath:
            return None
        
        # 리사이즈
        self.resize_image(filepath, max_width, max_height)
        
        # 최적화
        self.optimize_image(filepath, quality)
        
        return filepath
    
    def generate_alt_tag(self, keyword, index=0):
        """
        이미지 ALT 태그 생성
        
        Args:
            keyword (str): 키워드
            index (int): 이미지 순번
            
        Returns:
            str: ALT 태그 텍스트
        """
        templates = [
            f"{keyword} 관련 이미지",
            f"{keyword} 설명 이미지",
            f"{keyword} 예시 이미지",
            f"{keyword} 가이드 이미지"
        ]
        
        alt_text = templates[index % len(templates)]
        return alt_text
    
    def insert_images_into_content(self, html_content, image_paths, keyword):
        """
        HTML 콘텐츠에 이미지 자동 삽입
        
        Args:
            html_content (str): HTML 콘텐츠
            image_paths (list): 이미지 파일 경로 리스트
            keyword (str): 키워드 (ALT 태그용)
            
        Returns:
            str: 이미지가 삽입된 HTML
        """
        import re
        
        # H2 태그 찾기
        h2_pattern = re.compile(r'(<h2>.*?</h2>)', re.IGNORECASE)
        h2_tags = h2_pattern.findall(html_content)
        
        # 각 H2 뒤에 이미지 삽입
        modified_content = html_content
        for i, h2_tag in enumerate(h2_tags):
            if i < len(image_paths):
                img_path = image_paths[i]
                alt_text = self.generate_alt_tag(keyword, i)
                
                img_tag = f'\n<img src="{img_path}" alt="{alt_text}" style="max-width: 100%; height: auto;" />\n'
                
                # H2 태그 뒤에 이미지 삽입
                modified_content = modified_content.replace(
                    h2_tag,
                    h2_tag + img_tag,
                    1
                )
        
        logger.info(f"{min(len(h2_tags), len(image_paths))}개의 이미지 삽입 완료")
        return modified_content


if __name__ == '__main__':
    # 테스트 코드
    processor = ImageProcessor(output_dir='/tmp/test_images')
    
    # ALT 태그 생성 테스트
    alt_text = processor.generate_alt_tag('인공지능', 0)
    print(f"ALT 태그: {alt_text}")
    
    print("\n이미지 처리 테스트는 실제 URL이 필요합니다.")
