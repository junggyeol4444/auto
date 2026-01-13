"""
환율 예측 모듈
선형 회귀 기반 환율 예측
"""
import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression


class ForexPredictor:
    def __init__(self):
        """환율 예측기 초기화"""
        self.model = LinearRegression()
    
    def predict_rate(self, historical_data: List[Dict[str, Any]], 
                    days_ahead: int = 7) -> List[Dict[str, Any]]:
        """환율 예측 (선형 회귀)"""
        try:
            if len(historical_data) < 5:
                return []
            
            # 데이터 준비
            dates = []
            rates = []
            
            for data in historical_data:
                if 'date' in data and 'rate' in data:
                    dates.append(data['date'])
                    rates.append(data['rate'])
            
            if len(rates) < 5:
                return []
            
            # X: 일수 (0, 1, 2, ...)
            X = np.array(range(len(rates))).reshape(-1, 1)
            y = np.array(rates)
            
            # 모델 학습
            self.model.fit(X, y)
            
            # 미래 예측
            predictions = []
            last_date = datetime.strptime(dates[-1], "%Y-%m-%d")
            
            for i in range(1, days_ahead + 1):
                future_x = np.array([[len(rates) + i - 1]])
                predicted_rate = self.model.predict(future_x)[0]
                
                future_date = last_date + timedelta(days=i)
                predictions.append({
                    "date": future_date.strftime("%Y-%m-%d"),
                    "predicted_rate": predicted_rate
                })
            
            return predictions
            
        except Exception as e:
            print(f"환율 예측 실패: {e}")
            return []
    
    def calculate_trend(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """환율 추세 분석"""
        try:
            if len(historical_data) < 2:
                return {}
            
            rates = [d['rate'] for d in historical_data if 'rate' in d]
            if len(rates) < 2:
                return {}
            
            # 첫 환율과 마지막 환율 비교
            first_rate = rates[0]
            last_rate = rates[-1]
            
            change = last_rate - first_rate
            change_pct = (change / first_rate * 100) if first_rate != 0 else 0
            
            # 추세 판단
            if change_pct > 2:
                trend = "상승"
            elif change_pct < -2:
                trend = "하락"
            else:
                trend = "횡보"
            
            # 변동성 계산 (표준편차)
            volatility = np.std(rates) if len(rates) > 1 else 0
            
            return {
                "first_rate": first_rate,
                "last_rate": last_rate,
                "change": change,
                "change_pct": change_pct,
                "trend": trend,
                "volatility": volatility,
                "period_days": len(rates)
            }
            
        except Exception as e:
            print(f"추세 분석 실패: {e}")
            return {}
    
    def calculate_moving_average(self, historical_data: List[Dict[str, Any]], 
                                window: int = 7) -> List[Dict[str, Any]]:
        """이동평균 계산"""
        try:
            if len(historical_data) < window:
                return []
            
            rates = [d['rate'] for d in historical_data if 'rate' in d]
            dates = [d['date'] for d in historical_data if 'date' in d]
            
            if len(rates) < window:
                return []
            
            result = []
            for i in range(window - 1, len(rates)):
                window_rates = rates[i - window + 1:i + 1]
                ma = sum(window_rates) / len(window_rates)
                
                result.append({
                    "date": dates[i],
                    "rate": rates[i],
                    "ma": ma
                })
            
            return result
            
        except Exception as e:
            print(f"이동평균 계산 실패: {e}")
            return []
    
    def detect_support_resistance(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """지지선/저항선 탐지"""
        try:
            if len(historical_data) < 10:
                return {}
            
            rates = [d['rate'] for d in historical_data if 'rate' in d]
            if len(rates) < 10:
                return {}
            
            # 최근 30일 기준
            recent_rates = rates[-30:] if len(rates) > 30 else rates
            
            # 지지선: 최근 최저가
            support = min(recent_rates)
            
            # 저항선: 최근 최고가
            resistance = max(recent_rates)
            
            # 현재가
            current_rate = rates[-1]
            
            # 현재가가 지지선/저항선에 얼마나 가까운지
            support_distance = ((current_rate - support) / support * 100) if support != 0 else 0
            resistance_distance = ((resistance - current_rate) / current_rate * 100) if current_rate != 0 else 0
            
            return {
                "support": support,
                "resistance": resistance,
                "current_rate": current_rate,
                "support_distance_pct": support_distance,
                "resistance_distance_pct": resistance_distance,
                "near_support": support_distance < 2,  # 2% 이내
                "near_resistance": resistance_distance < 2  # 2% 이내
            }
            
        except Exception as e:
            print(f"지지선/저항선 탐지 실패: {e}")
            return {}
