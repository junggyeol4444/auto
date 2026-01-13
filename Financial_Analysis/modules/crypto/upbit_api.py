"""
업비트 API 연동 모듈
"""
import requests
import time
from typing import List, Dict, Any


class UpbitAPI:
    def __init__(self):
        """업비트 API 초기화"""
        self.base_url = "https://api.upbit.com/v1"
        self.last_request_time = 0
        self.request_interval = 0.1  # 초당 10회 제한
    
    def _rate_limit(self):
        """API 호출 제한 준수"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.request_interval:
            time.sleep(self.request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _request(self, endpoint: str, params: Dict = None, max_retries: int = 3) -> Dict:
        """API 요청 (재시도 로직 포함)"""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(max_retries):
            try:
                self._rate_limit()
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise Exception(f"업비트 API 요청 실패: {e}")
                time.sleep(1 * (attempt + 1))  # 지수 백오프
        
        return {}
    
    def get_market_all(self) -> List[Dict[str, Any]]:
        """전체 마켓 코드 조회"""
        try:
            return self._request("/market/all")
        except Exception as e:
            print(f"마켓 코드 조회 실패: {e}")
            return []
    
    def get_ticker(self, markets: List[str]) -> List[Dict[str, Any]]:
        """현재가 정보 조회"""
        try:
            markets_str = ",".join(markets)
            return self._request("/ticker", {"markets": markets_str})
        except Exception as e:
            print(f"현재가 조회 실패: {e}")
            return []
    
    def get_candles_minutes(self, market: str, unit: int = 1, count: int = 200) -> List[Dict[str, Any]]:
        """분 캔들 조회"""
        try:
            return self._request(f"/candles/minutes/{unit}", {
                "market": market,
                "count": count
            })
        except Exception as e:
            print(f"분 캔들 조회 실패: {e}")
            return []
    
    def get_candles_days(self, market: str, count: int = 200) -> List[Dict[str, Any]]:
        """일 캔들 조회"""
        try:
            return self._request("/candles/days", {
                "market": market,
                "count": count
            })
        except Exception as e:
            print(f"일 캔들 조회 실패: {e}")
            return []
    
    def get_orderbook(self, markets: List[str]) -> List[Dict[str, Any]]:
        """호가 정보 조회"""
        try:
            markets_str = ",".join(markets)
            return self._request("/orderbook", {"markets": markets_str})
        except Exception as e:
            print(f"호가 정보 조회 실패: {e}")
            return []
    
    def get_top_movers(self, limit: int = 20) -> List[Dict[str, Any]]:
        """급등/급락 코인 조회 (1시간 변동률 기준)"""
        try:
            markets = self.get_market_all()
            krw_markets = [m['market'] for m in markets if m['market'].startswith('KRW-')]
            
            if not krw_markets:
                return []
            
            tickers = self.get_ticker(krw_markets)
            
            # 1시간 변동률 계산 및 정렬
            movers = []
            for ticker in tickers:
                change_rate = ticker.get('signed_change_rate', 0) * 100
                if abs(change_rate) >= 5:  # 5% 이상 변동
                    movers.append({
                        'market': ticker['market'],
                        'korean_name': ticker.get('korean_name', ''),
                        'trade_price': ticker['trade_price'],
                        'change_rate': change_rate,
                        'acc_trade_price_24h': ticker.get('acc_trade_price_24h', 0)
                    })
            
            # 변동률 절대값 기준 정렬
            movers.sort(key=lambda x: abs(x['change_rate']), reverse=True)
            return movers[:limit]
            
        except Exception as e:
            print(f"급등/급락 코인 조회 실패: {e}")
            return []
    
    def get_top_volume(self, limit: int = 20) -> List[Dict[str, Any]]:
        """거래량 상위 코인 조회"""
        try:
            markets = self.get_market_all()
            krw_markets = [m['market'] for m in markets if m['market'].startswith('KRW-')]
            
            if not krw_markets:
                return []
            
            tickers = self.get_ticker(krw_markets)
            
            # 거래대금 기준 정렬
            tickers.sort(key=lambda x: x.get('acc_trade_price_24h', 0), reverse=True)
            
            result = []
            for ticker in tickers[:limit]:
                result.append({
                    'market': ticker['market'],
                    'korean_name': ticker.get('korean_name', ''),
                    'trade_price': ticker['trade_price'],
                    'change_rate': ticker.get('signed_change_rate', 0) * 100,
                    'acc_trade_price_24h': ticker.get('acc_trade_price_24h', 0)
                })
            
            return result
            
        except Exception as e:
            print(f"거래량 상위 코인 조회 실패: {e}")
            return []
