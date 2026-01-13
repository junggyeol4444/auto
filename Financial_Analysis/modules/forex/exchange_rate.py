"""
환율 API 연동 모듈
"""
import requests
import time
from typing import Dict, List, Any
from datetime import datetime, timedelta


class ExchangeRateAPI:
    def __init__(self, api_key: str = ""):
        """환율 API 초기화"""
        self.api_key = api_key
        self.base_url = "https://v6.exchangerate-api.com/v6"
        self.bok_url = "https://ecos.bok.or.kr/api"
        self.last_request_time = 0
        self.request_interval = 1.0
    
    def _rate_limit(self):
        """API 호출 제한 준수"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.request_interval:
            time.sleep(self.request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _request(self, url: str, max_retries: int = 3) -> Any:
        """API 요청 (재시도 로직 포함)"""
        for attempt in range(max_retries):
            try:
                self._rate_limit()
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise Exception(f"환율 API 요청 실패: {e}")
                time.sleep(1 * (attempt + 1))
        
        return None
    
    def get_latest_rates(self, base_currency: str = "USD") -> Dict[str, Any]:
        """최신 환율 조회"""
        try:
            if self.api_key:
                url = f"{self.base_url}/{self.api_key}/latest/{base_currency}"
                return self._request(url)
            else:
                # API 키가 없으면 무료 API 사용
                url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
                return self._request(url)
        except Exception as e:
            print(f"최신 환율 조회 실패: {e}")
            return {}
    
    def get_pair_rate(self, from_currency: str, to_currency: str) -> float:
        """통화 쌍 환율 조회"""
        try:
            if self.api_key:
                url = f"{self.base_url}/{self.api_key}/pair/{from_currency}/{to_currency}"
                data = self._request(url)
                if data and 'conversion_rate' in data:
                    return data['conversion_rate']
            else:
                # API 키가 없으면 USD 기준으로 계산
                rates = self.get_latest_rates("USD")
                if rates and 'rates' in rates:
                    from_rate = rates['rates'].get(from_currency, 1.0)
                    to_rate = rates['rates'].get(to_currency, 1.0)
                    return to_rate / from_rate if from_rate != 0 else 0
            
            return 0
        except Exception as e:
            print(f"통화 쌍 환율 조회 실패: {e}")
            return 0
    
    def get_major_currencies_krw(self) -> Dict[str, float]:
        """주요 통화 대 원화 환율 조회"""
        major_currencies = ['USD', 'JPY', 'EUR', 'CNY', 'GBP']
        rates = {}
        
        try:
            # USD 기준 환율 조회
            usd_rates = self.get_latest_rates("USD")
            if not usd_rates or 'rates' not in usd_rates:
                return self._get_fallback_rates()
            
            krw_rate = usd_rates['rates'].get('KRW', 1300)
            
            for currency in major_currencies:
                if currency == 'USD':
                    rates[currency] = krw_rate
                else:
                    currency_rate = usd_rates['rates'].get(currency, 1.0)
                    rates[currency] = krw_rate / currency_rate if currency_rate != 0 else 0
            
            # JPY는 100엔 기준으로 변환
            if 'JPY' in rates:
                rates['JPY'] = rates['JPY'] * 100
            
            return rates
            
        except Exception as e:
            print(f"주요 통화 환율 조회 실패: {e}")
            return self._get_fallback_rates()
    
    def _get_fallback_rates(self) -> Dict[str, float]:
        """대체 환율 (API 실패 시)"""
        return {
            'USD': 1300.0,
            'JPY': 900.0,  # 100엔 기준
            'EUR': 1400.0,
            'CNY': 180.0,
            'GBP': 1650.0
        }
    
    def calculate_exchange_profit(self, amount: float, from_currency: str, 
                                 to_currency: str, fee_percent: float = 1.0) -> Dict[str, Any]:
        """환차익 계산"""
        try:
            rate = self.get_pair_rate(from_currency, to_currency)
            if rate == 0:
                return {}
            
            # 환전 금액 계산 (수수료 차감)
            exchanged_amount = amount * rate * (1 - fee_percent / 100)
            
            # 다시 원래 통화로 환전
            reverse_rate = self.get_pair_rate(to_currency, from_currency)
            final_amount = exchanged_amount * reverse_rate * (1 - fee_percent / 100)
            
            # 손익 계산
            profit = final_amount - amount
            profit_percent = (profit / amount * 100) if amount > 0 else 0
            
            return {
                "original_amount": amount,
                "exchanged_amount": exchanged_amount,
                "final_amount": final_amount,
                "profit": profit,
                "profit_percent": profit_percent,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "fee_percent": fee_percent
            }
            
        except Exception as e:
            print(f"환차익 계산 실패: {e}")
            return {}
    
    def get_historical_rates_mock(self, currency: str = "USD", days: int = 30) -> List[Dict[str, Any]]:
        """과거 환율 데이터 (모의 데이터)"""
        # 실제로는 유료 API나 한국은행 API를 사용해야 함
        result = []
        current_rate = self.get_pair_rate(currency, "KRW")
        
        if current_rate == 0:
            current_rate = 1300.0  # 기본값
        
        for i in range(days, 0, -1):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            # 단순 랜덤 변동 (±2%)
            import random
            variation = random.uniform(-0.02, 0.02)
            rate = current_rate * (1 + variation * (i / days))
            
            result.append({
                "date": date,
                "currency": currency,
                "rate": rate
            })
        
        return result
    
    def check_rate_alert(self, currency: str, target_rate: float) -> Dict[str, Any]:
        """환율 알림 체크"""
        try:
            current_rate = self.get_pair_rate(currency, "KRW")
            
            if current_rate == 0:
                return {"triggered": False, "message": "환율 정보를 가져올 수 없습니다."}
            
            # 목표 환율 도달 여부 확인
            if current_rate >= target_rate:
                return {
                    "triggered": True,
                    "currency": currency,
                    "current_rate": current_rate,
                    "target_rate": target_rate,
                    "message": f"{currency}/KRW 환율이 목표 {target_rate:.2f}원에 도달했습니다. (현재: {current_rate:.2f}원)"
                }
            
            return {
                "triggered": False,
                "currency": currency,
                "current_rate": current_rate,
                "target_rate": target_rate,
                "diff_pct": ((target_rate - current_rate) / current_rate * 100)
            }
            
        except Exception as e:
            print(f"환율 알림 체크 실패: {e}")
            return {"triggered": False, "message": f"오류 발생: {e}"}
