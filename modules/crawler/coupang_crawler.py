# -*- coding: utf-8 -*-
"""
쿠팡 크롤러
쿠팡 검색 결과를 크롤링하여 제품 정보를 수집합니다.
"""

import requests
from bs4 import BeautifulSoup
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CoupangCrawler:
    """쿠팡 크롤링 클래스"""
    
    def __init__(self, partner_id=""):
        """
        Args:
            partner_id (str): 쿠팡 파트너스 ID
        """
        self.partner_id = partner_id
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        self.base_url = 'https://www.coupang.com/np/search'
    
    def search_products(self, keyword, max_results=10):
        """
        쿠팡에서 제품 검색
        
        Args:
            keyword (str): 검색 키워드
            max_results (int): 최대 결과 수
            
        Returns:
            list: 제품 정보 리스트
        """
        try:
            params = {
                'q': keyword,
                'channel': 'user'
            }
            
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            product_items = soup.select('li.search-product')
            
            products = []
            for item in product_items[:max_results]:
                try:
                    product = self._parse_product(item)
                    if product:
                        products.append(product)
                except Exception as e:
                    logger.warning(f"제품 파싱 실패: {e}")
                    continue
            
            logger.info(f"{len(products)}개의 제품 검색 완료")
            return products
            
        except Exception as e:
            logger.error(f"제품 검색 실패: {e}")
            return []
    
    def _parse_product(self, item):
        """
        제품 정보 파싱
        
        Args:
            item: BeautifulSoup 엘리먼트
            
        Returns:
            dict: 제품 정보
        """
        try:
            # 제품명
            name_elem = item.select_one('.name')
            name = name_elem.get_text(strip=True) if name_elem else ''
            
            # 가격
            price_elem = item.select_one('.price-value')
            price = price_elem.get_text(strip=True) if price_elem else '0'
            
            # 이미지
            img_elem = item.select_one('img.search-product-wrap-img')
            image_url = img_elem.get('src', '') if img_elem else ''
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            
            # 제품 링크
            link_elem = item.select_one('a.search-product-link')
            product_id = link_elem.get('href', '').split('/')[-1] if link_elem else ''
            product_url = f"https://www.coupang.com{link_elem.get('href', '')}" if link_elem else ''
            
            # 파트너스 링크 생성
            if self.partner_id and product_id:
                partner_url = f"https://link.coupang.com/a/{self.partner_id}?url={product_url}"
            else:
                partner_url = product_url
            
            # 평점
            rating_elem = item.select_one('.rating')
            rating = rating_elem.get_text(strip=True) if rating_elem else 'N/A'
            
            # 리뷰 수
            review_elem = item.select_one('.rating-total-count')
            review_count = review_elem.get_text(strip=True).strip('()') if review_elem else '0'
            
            return {
                'name': name,
                'price': price,
                'image_url': image_url,
                'product_url': product_url,
                'partner_url': partner_url,
                'rating': rating,
                'review_count': review_count
            }
            
        except Exception as e:
            logger.error(f"제품 정보 파싱 오류: {e}")
            return None
    
    def create_product_table(self, products, top_n=5):
        """
        제품 비교 테이블 HTML 생성
        
        Args:
            products (list): 제품 정보 리스트
            top_n (int): 상위 n개 제품
            
        Returns:
            str: HTML 테이블
        """
        if not products:
            return ""
        
        html = '<table style="border-collapse: collapse; width: 100%;">\n'
        html += '  <thead>\n'
        html += '    <tr style="background-color: #f2f2f2;">\n'
        html += '      <th style="border: 1px solid #ddd; padding: 8px;">제품명</th>\n'
        html += '      <th style="border: 1px solid #ddd; padding: 8px;">가격</th>\n'
        html += '      <th style="border: 1px solid #ddd; padding: 8px;">평점</th>\n'
        html += '      <th style="border: 1px solid #ddd; padding: 8px;">리뷰</th>\n'
        html += '      <th style="border: 1px solid #ddd; padding: 8px;">링크</th>\n'
        html += '    </tr>\n'
        html += '  </thead>\n'
        html += '  <tbody>\n'
        
        for product in products[:top_n]:
            html += '    <tr>\n'
            html += f'      <td style="border: 1px solid #ddd; padding: 8px;">{product["name"][:50]}</td>\n'
            html += f'      <td style="border: 1px solid #ddd; padding: 8px;">{product["price"]}원</td>\n'
            html += f'      <td style="border: 1px solid #ddd; padding: 8px;">{product["rating"]}</td>\n'
            html += f'      <td style="border: 1px solid #ddd; padding: 8px;">{product["review_count"]}</td>\n'
            html += f'      <td style="border: 1px solid #ddd; padding: 8px;"><a href="{product["partner_url"]}" target="_blank">보기</a></td>\n'
            html += '    </tr>\n'
        
        html += '  </tbody>\n'
        html += '</table>\n'
        html += '<p style="font-size: 0.9em; color: #666;">* 이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</p>\n'
        
        return html


if __name__ == '__main__':
    # 테스트 코드
    crawler = CoupangCrawler()
    products = crawler.search_products('노트북', max_results=5)
    
    print(f"\n총 {len(products)}개의 제품 검색됨\n")
    
    for i, product in enumerate(products, 1):
        print(f"=== 제품 {i} ===")
        print(f"제품명: {product['name'][:50]}")
        print(f"가격: {product['price']}원")
        print(f"평점: {product['rating']}")
        print(f"리뷰: {product['review_count']}\n")
    
    # 테이블 생성 테스트
    table = crawler.create_product_table(products, top_n=3)
    print("\n=== 생성된 HTML 테이블 ===")
    print(table)
