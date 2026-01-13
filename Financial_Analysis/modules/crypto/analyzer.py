"""
암호화폐 분석기 모듈
"""
from typing import Dict, List, Any
from .upbit_api import UpbitAPI
from .binance_api import BinanceAPI
from .coingecko_api import CoinGeckoAPI


class CryptoAnalyzer:
    def __init__(self):
        """암호화폐 분석기 초기화"""
        self.upbit = UpbitAPI()
        self.binance = BinanceAPI()
        self.coingecko = CoinGeckoAPI()
    
    def get_comprehensive_market_data(self) -> Dict[str, Any]:
        """종합 시장 데이터 조회"""
        data = {
            "upbit": {
                "top_volume": [],
                "top_movers": []
            },
            "binance": {
                "top_volume": [],
                "top_gainers": []
            },
            "coingecko": {
                "top_market_cap": [],
                "gainers_losers": {"gainers": [], "losers": []}
            }
        }
        
        try:
            # 업비트 데이터
            data["upbit"]["top_volume"] = self.upbit.get_top_volume(10)
            data["upbit"]["top_movers"] = self.upbit.get_top_movers(10)
        except Exception as e:
            print(f"업비트 데이터 조회 실패: {e}")
        
        try:
            # 바이낸스 데이터
            data["binance"]["top_volume"] = self.binance.get_top_volume(10)
            data["binance"]["top_gainers"] = self.binance.get_top_gainers(10)
        except Exception as e:
            print(f"바이낸스 데이터 조회 실패: {e}")
        
        try:
            # CoinGecko 데이터
            data["coingecko"]["top_market_cap"] = self.coingecko.get_top_by_market_cap(limit=20)
            data["coingecko"]["gainers_losers"] = self.coingecko.get_top_gainers_losers(limit=10)
        except Exception as e:
            print(f"CoinGecko 데이터 조회 실패: {e}")
        
        return data
    
    def detect_pump_dump(self, threshold_percent: float = 10.0) -> Dict[str, List[Dict[str, Any]]]:
        """급등/급락 코인 탐지"""
        result = {
            "pump": [],  # 급등
            "dump": []   # 급락
        }
        
        try:
            # 업비트에서 급등/급락 코인 조회
            movers = self.upbit.get_top_movers(30)
            for mover in movers:
                change_rate = mover['change_rate']
                if change_rate >= threshold_percent:
                    result["pump"].append(mover)
                elif change_rate <= -threshold_percent:
                    result["dump"].append(mover)
        except Exception as e:
            print(f"급등/급락 탐지 실패: {e}")
        
        return result
    
    def analyze_volume_spike(self, market: str = "KRW-BTC") -> Dict[str, Any]:
        """거래량 급증 분석"""
        try:
            # 일봉 데이터 조회
            candles = self.upbit.get_candles_days(market, count=30)
            if not candles:
                return {}
            
            # 평균 거래량 계산
            volumes = [c['candle_acc_trade_volume'] for c in candles[1:]]
            avg_volume = sum(volumes) / len(volumes) if volumes else 0
            
            # 현재 거래량
            current_volume = candles[0]['candle_acc_trade_volume']
            
            # 거래량 비율
            volume_ratio = (current_volume / avg_volume) if avg_volume > 0 else 0
            
            return {
                "market": market,
                "current_volume": current_volume,
                "avg_volume_30d": avg_volume,
                "volume_ratio": volume_ratio,
                "is_spike": volume_ratio > 2.0  # 평균 대비 2배 이상
            }
            
        except Exception as e:
            print(f"거래량 분석 실패: {e}")
            return {}
    
    def check_price_alert(self, market: str, target_price: float) -> Dict[str, Any]:
        """가격 알림 체크"""
        try:
            ticker = self.upbit.get_ticker([market])
            if not ticker:
                return {"triggered": False, "message": "가격 정보를 가져올 수 없습니다."}
            
            current_price = ticker[0]['trade_price']
            
            # 목표가 도달 여부 확인
            if current_price >= target_price:
                return {
                    "triggered": True,
                    "market": market,
                    "current_price": current_price,
                    "target_price": target_price,
                    "message": f"{market} 가격이 목표가 {target_price:,.0f}원에 도달했습니다. (현재가: {current_price:,.0f}원)"
                }
            
            return {
                "triggered": False,
                "market": market,
                "current_price": current_price,
                "target_price": target_price,
                "diff_pct": ((target_price - current_price) / current_price * 100)
            }
            
        except Exception as e:
            print(f"가격 알림 체크 실패: {e}")
            return {"triggered": False, "message": f"오류 발생: {e}"}
    
    def get_market_summary(self, market: str = "KRW-BTC") -> Dict[str, Any]:
        """시장 요약 정보"""
        try:
            ticker = self.upbit.get_ticker([market])
            if not ticker:
                return {}
            
            t = ticker[0]
            return {
                "market": market,
                "korean_name": t.get('korean_name', ''),
                "current_price": t['trade_price'],
                "change_rate": t.get('signed_change_rate', 0) * 100,
                "high_price": t.get('high_price', 0),
                "low_price": t.get('low_price', 0),
                "volume_24h": t.get('acc_trade_volume_24h', 0),
                "trade_value_24h": t.get('acc_trade_price_24h', 0),
                "prev_closing_price": t.get('prev_closing_price', 0)
            }
            
        except Exception as e:
            print(f"시장 요약 정보 조회 실패: {e}")
            return {}
