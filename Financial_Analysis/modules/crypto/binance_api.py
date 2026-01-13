"""
바이낸스 API 연동 모듈
"""
import requests
import time
from typing import List, Dict, Any


class BinanceAPI:
    def __init__(self):
        """바이낸스 API 초기화"""
        self.base_url = "https://api.binance.com/api/v3"
        self.last_request_time = 0
        self.request_interval = 0.1
    
    def _rate_limit(self):
        """API 호출 제한 준수"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.request_interval:
            time.sleep(self.request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _request(self, endpoint: str, params: Dict = None, max_retries: int = 3) -> Any:
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
                    raise Exception(f"바이낸스 API 요청 실패: {e}")
                time.sleep(1 * (attempt + 1))
        
        return None
    
    def get_ticker_24hr(self, symbol: str = None) -> Any:
        """24시간 가격 변동 정보"""
        try:
            params = {"symbol": symbol} if symbol else {}
            return self._request("/ticker/24hr", params)
        except Exception as e:
            print(f"24시간 가격 변동 조회 실패: {e}")
            return [] if not symbol else {}
    
    def get_price(self, symbol: str = None) -> Any:
        """현재 가격 조회"""
        try:
            params = {"symbol": symbol} if symbol else {}
            return self._request("/ticker/price", params)
        except Exception as e:
            print(f"현재 가격 조회 실패: {e}")
            return [] if not symbol else {}
    
    def get_klines(self, symbol: str, interval: str = "1d", limit: int = 500) -> List[List]:
        """캔들스틱 데이터 조회"""
        try:
            return self._request("/klines", {
                "symbol": symbol,
                "interval": interval,
                "limit": limit
            })
        except Exception as e:
            print(f"캔들스틱 조회 실패: {e}")
            return []
    
    def get_top_gainers(self, limit: int = 20) -> List[Dict[str, Any]]:
        """급등 코인 조회"""
        try:
            tickers = self.get_ticker_24hr()
            if not tickers:
                return []
            
            # USDT 마켓만 필터링
            usdt_tickers = [t for t in tickers if t['symbol'].endswith('USDT')]
            
            # 변동률 기준 정렬
            gainers = []
            for ticker in usdt_tickers:
                change_pct = float(ticker.get('priceChangePercent', 0))
                if change_pct >= 5:  # 5% 이상 상승
                    gainers.append({
                        'symbol': ticker['symbol'],
                        'price': float(ticker['lastPrice']),
                        'change_pct': change_pct,
                        'volume': float(ticker['volume']),
                        'quote_volume': float(ticker['quoteVolume'])
                    })
            
            gainers.sort(key=lambda x: x['change_pct'], reverse=True)
            return gainers[:limit]
            
        except Exception as e:
            print(f"급등 코인 조회 실패: {e}")
            return []
    
    def get_top_volume(self, limit: int = 20) -> List[Dict[str, Any]]:
        """거래량 상위 코인 조회"""
        try:
            tickers = self.get_ticker_24hr()
            if not tickers:
                return []
            
            # USDT 마켓만 필터링
            usdt_tickers = [t for t in tickers if t['symbol'].endswith('USDT')]
            
            # 거래대금 기준 정렬
            volume_list = []
            for ticker in usdt_tickers:
                volume_list.append({
                    'symbol': ticker['symbol'],
                    'price': float(ticker['lastPrice']),
                    'change_pct': float(ticker.get('priceChangePercent', 0)),
                    'volume': float(ticker['volume']),
                    'quote_volume': float(ticker['quoteVolume'])
                })
            
            volume_list.sort(key=lambda x: x['quote_volume'], reverse=True)
            return volume_list[:limit]
            
        except Exception as e:
            print(f"거래량 상위 코인 조회 실패: {e}")
            return []
