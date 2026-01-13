"""
CoinGecko API 연동 모듈
"""
import requests
import time
from typing import List, Dict, Any


class CoinGeckoAPI:
    def __init__(self):
        """CoinGecko API 초기화"""
        self.base_url = "https://api.coingecko.com/api/v3"
        self.last_request_time = 0
        self.request_interval = 1.5  # 무료 API는 분당 50회 제한
    
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
                    raise Exception(f"CoinGecko API 요청 실패: {e}")
                time.sleep(2 * (attempt + 1))
        
        return None
    
    def get_coins_markets(self, vs_currency: str = "krw", order: str = "market_cap_desc",
                         per_page: int = 100, page: int = 1) -> List[Dict[str, Any]]:
        """코인 시장 정보 조회"""
        try:
            return self._request("/coins/markets", {
                "vs_currency": vs_currency,
                "order": order,
                "per_page": per_page,
                "page": page,
                "sparkline": False
            })
        except Exception as e:
            print(f"코인 시장 정보 조회 실패: {e}")
            return []
    
    def get_coin_by_id(self, coin_id: str) -> Dict[str, Any]:
        """특정 코인 상세 정보 조회"""
        try:
            return self._request(f"/coins/{coin_id}", {
                "localization": False,
                "tickers": False,
                "market_data": True,
                "community_data": False,
                "developer_data": False
            })
        except Exception as e:
            print(f"코인 상세 정보 조회 실패: {e}")
            return {}
    
    def get_coin_market_chart(self, coin_id: str, vs_currency: str = "krw",
                             days: int = 30) -> Dict[str, Any]:
        """코인 가격 차트 데이터 조회"""
        try:
            return self._request(f"/coins/{coin_id}/market_chart", {
                "vs_currency": vs_currency,
                "days": days
            })
        except Exception as e:
            print(f"코인 차트 데이터 조회 실패: {e}")
            return {}
    
    def get_top_gainers_losers(self, vs_currency: str = "krw", 
                              limit: int = 20) -> Dict[str, List[Dict[str, Any]]]:
        """급등/급락 코인 조회"""
        try:
            coins = self.get_coins_markets(vs_currency=vs_currency, per_page=250)
            if not coins:
                return {"gainers": [], "losers": []}
            
            gainers = []
            losers = []
            
            for coin in coins:
                change_24h = coin.get('price_change_percentage_24h', 0)
                if change_24h is None:
                    continue
                
                coin_data = {
                    'id': coin['id'],
                    'symbol': coin['symbol'],
                    'name': coin['name'],
                    'current_price': coin['current_price'],
                    'change_24h': change_24h,
                    'market_cap': coin.get('market_cap', 0),
                    'volume_24h': coin.get('total_volume', 0)
                }
                
                if change_24h >= 10:  # 10% 이상 상승
                    gainers.append(coin_data)
                elif change_24h <= -10:  # 10% 이상 하락
                    losers.append(coin_data)
            
            gainers.sort(key=lambda x: x['change_24h'], reverse=True)
            losers.sort(key=lambda x: x['change_24h'])
            
            return {
                "gainers": gainers[:limit],
                "losers": losers[:limit]
            }
            
        except Exception as e:
            print(f"급등/급락 코인 조회 실패: {e}")
            return {"gainers": [], "losers": []}
    
    def get_top_by_market_cap(self, vs_currency: str = "krw", 
                             limit: int = 50) -> List[Dict[str, Any]]:
        """시가총액 상위 코인 조회"""
        try:
            coins = self.get_coins_markets(vs_currency=vs_currency, 
                                          order="market_cap_desc",
                                          per_page=limit)
            
            result = []
            for coin in coins:
                result.append({
                    'rank': coin.get('market_cap_rank', 0),
                    'id': coin['id'],
                    'symbol': coin['symbol'],
                    'name': coin['name'],
                    'current_price': coin['current_price'],
                    'market_cap': coin.get('market_cap', 0),
                    'volume_24h': coin.get('total_volume', 0),
                    'change_24h': coin.get('price_change_percentage_24h', 0)
                })
            
            return result
            
        except Exception as e:
            print(f"시가총액 상위 코인 조회 실패: {e}")
            return []
    
    def search_coins(self, query: str) -> List[Dict[str, Any]]:
        """코인 검색"""
        try:
            result = self._request("/search", {"query": query})
            return result.get('coins', []) if result else []
        except Exception as e:
            print(f"코인 검색 실패: {e}")
            return []
