"""
DART API 모듈 (전자공시시스템)
"""
import requests
from typing import Dict, Any


class DartAPI:
    def __init__(self, api_key: str = ""):
        """DART API 초기화"""
        self.api_key = api_key
        self.base_url = "https://opendart.fss.or.kr/api"
    
    def get_company_info(self, corp_code: str) -> Dict[str, Any]:
        """기업 정보 조회"""
        if not self.api_key:
            return {}
        
        try:
            url = f"{self.base_url}/company.json"
            params = {
                "crtfc_key": self.api_key,
                "corp_code": corp_code
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"기업 정보 조회 실패: {e}")
            return {}
    
    def get_dividend_info(self, corp_code: str, bsns_year: str) -> Dict[str, Any]:
        """배당 정보 조회"""
        if not self.api_key:
            return {}
        
        try:
            url = f"{self.base_url}/alotMatter.json"
            params = {
                "crtfc_key": self.api_key,
                "corp_code": corp_code,
                "bsns_year": bsns_year
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"배당 정보 조회 실패: {e}")
            return {}
