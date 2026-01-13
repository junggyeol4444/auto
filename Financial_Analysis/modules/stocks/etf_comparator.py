"""
ETF 비교 모듈
"""
from typing import List, Dict, Any


class ETFComparator:
    def __init__(self):
        """ETF 비교기 초기화"""
        pass
    
    def compare_etfs(self, symbols: List[str]) -> List[Dict[str, Any]]:
        """ETF 비교 (샘플 데이터)"""
        # 실제로는 yfinance나 다른 API 사용
        sample_data = [
            {
                "symbol": "SPY",
                "name": "SPDR S&P 500 ETF",
                "price": 450.0,
                "expense_ratio": 0.09,
                "aum": 400000000000,
                "ytd_return": 15.5
            },
            {
                "symbol": "QQQ",
                "name": "Invesco QQQ Trust",
                "price": 380.0,
                "expense_ratio": 0.20,
                "aum": 200000000000,
                "ytd_return": 25.3
            }
        ]
        
        return [etf for etf in sample_data if etf["symbol"] in symbols]
