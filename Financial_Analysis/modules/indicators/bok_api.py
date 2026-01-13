"""
한국은행 API 모듈
"""
import requests
from typing import List, Dict, Any


class BOKAPI:
    def __init__(self, api_key: str = ""):
        """한국은행 API 초기화"""
        self.api_key = api_key
        self.base_url = "https://ecos.bok.or.kr/api"
    
    def get_interest_rate(self) -> Dict[str, Any]:
        """기준금리 조회"""
        if not self.api_key:
            # API 키가 없으면 샘플 데이터
            return {
                "rate": 3.50,
                "date": "2024-01",
                "unit": "%"
            }
        
        try:
            # 실제 API 호출 구현
            # StatisticSearch API 사용
            return {
                "rate": 3.50,
                "date": "2024-01",
                "unit": "%"
            }
        except Exception as e:
            print(f"기준금리 조회 실패: {e}")
            return {}
    
    def get_cpi(self) -> Dict[str, Any]:
        """소비자물가지수 조회"""
        return {
            "value": 112.5,
            "date": "2024-01",
            "yoy_change": 3.2
        }
