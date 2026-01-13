"""
배당 분석 모듈
"""
from typing import Dict, List, Any
import pandas as pd


class DividendAnalyzer:
    def __init__(self):
        """배당 분석기 초기화"""
        pass
    
    def analyze_dividend(self, symbol: str, stock_api) -> Dict[str, Any]:
        """배당 분석"""
        try:
            # 주식 정보 조회
            info = stock_api.get_stock_info(symbol)
            dividends = stock_api.get_dividends(symbol)
            
            if dividends.empty:
                return {
                    "symbol": symbol,
                    "has_dividend": False,
                    "message": "배당 정보가 없습니다."
                }
            
            # 최근 배당
            recent_dividend = dividends.iloc[-1] if not dividends.empty else 0
            
            # 연간 배당금 계산
            annual_dividend = dividends.tail(4).sum() if len(dividends) >= 4 else dividends.sum()
            
            # 배당수익률
            current_price = info.get("price", 0)
            dividend_yield = (annual_dividend / current_price * 100) if current_price > 0 else 0
            
            # 연속 배당 년수
            consecutive_years = len(dividends)
            
            return {
                "symbol": symbol,
                "name": info.get("name", symbol),
                "has_dividend": True,
                "current_price": current_price,
                "recent_dividend": recent_dividend,
                "annual_dividend": annual_dividend,
                "dividend_yield": dividend_yield,
                "consecutive_years": consecutive_years,
                "total_dividends": len(dividends)
            }
            
        except Exception as e:
            print(f"배당 분석 실패: {e}")
            return {}
    
    def get_top_dividend_stocks(self) -> List[Dict[str, Any]]:
        """배당수익률 상위 종목 (샘플 데이터)"""
        # 실제로는 API나 데이터베이스에서 조회
        sample_data = [
            {"symbol": "005930.KS", "name": "삼성전자", "dividend_yield": 2.5, "price": 71000},
            {"symbol": "000660.KS", "name": "SK하이닉스", "dividend_yield": 1.8, "price": 125000},
            {"symbol": "AAPL", "name": "Apple", "dividend_yield": 0.5, "price": 175.0},
            {"symbol": "MSFT", "name": "Microsoft", "dividend_yield": 0.8, "price": 380.0}
        ]
        return sorted(sample_data, key=lambda x: x['dividend_yield'], reverse=True)
