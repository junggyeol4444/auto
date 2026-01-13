"""
주식 API 모듈 (yfinance 기반)
"""
import yfinance as yf
from typing import Dict, List, Any
import pandas as pd


class StockAPI:
    def __init__(self):
        """주식 API 초기화"""
        pass
    
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """주식 정보 조회"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            return {
                "symbol": symbol,
                "name": info.get("longName", symbol),
                "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
                "previous_close": info.get("previousClose", 0),
                "open": info.get("open", 0),
                "high": info.get("dayHigh", 0),
                "low": info.get("dayLow", 0),
                "volume": info.get("volume", 0),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "pb_ratio": info.get("priceToBook", 0),
                "dividend_yield": info.get("dividendYield", 0),
                "52w_high": info.get("fiftyTwoWeekHigh", 0),
                "52w_low": info.get("fiftyTwoWeekLow", 0)
            }
        except Exception as e:
            print(f"주식 정보 조회 실패: {e}")
            return {}
    
    def get_historical_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
        """과거 가격 데이터 조회"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period, interval=interval)
            return data
        except Exception as e:
            print(f"과거 데이터 조회 실패: {e}")
            return pd.DataFrame()
    
    def search_stock(self, query: str) -> List[Dict[str, Any]]:
        """주식 검색 (간단 버전)"""
        # 실제로는 더 정교한 검색 API가 필요
        common_stocks = {
            "삼성전자": "005930.KS",
            "SK하이닉스": "000660.KS",
            "NAVER": "035420.KS",
            "카카오": "035720.KS",
            "LG에너지솔루션": "373220.KS",
            "Apple": "AAPL",
            "Microsoft": "MSFT",
            "Tesla": "TSLA",
            "Amazon": "AMZN",
            "Google": "GOOGL"
        }
        
        results = []
        query_lower = query.lower()
        for name, symbol in common_stocks.items():
            if query_lower in name.lower() or query_lower in symbol.lower():
                results.append({"name": name, "symbol": symbol})
        
        return results
    
    def get_dividends(self, symbol: str) -> pd.DataFrame:
        """배당 정보 조회"""
        try:
            stock = yf.Ticker(symbol)
            dividends = stock.dividends
            return dividends
        except Exception as e:
            print(f"배당 정보 조회 실패: {e}")
            return pd.DataFrame()
