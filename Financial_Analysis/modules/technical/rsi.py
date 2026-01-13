"""
기술적 분석 - RSI (상대강도지수)
"""
from typing import List, Dict, Any


def calculate_rsi(prices: List[float], period: int = 14) -> List[float]:
    """RSI 계산"""
    if len(prices) < period + 1:
        return []
    
    rsi_values = [None] * period
    
    # 가격 변동 계산
    changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    
    # 상승/하락 분리
    gains = [max(change, 0) for change in changes]
    losses = [abs(min(change, 0)) for change in changes]
    
    # 첫 평균 계산
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    # 첫 RSI 계산
    if avg_loss == 0:
        rsi_values.append(100)
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)
    
    # 나머지 RSI 계산 (smoothed)
    for i in range(period, len(changes)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
        if avg_loss == 0:
            rsi_values.append(100)
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)
    
    return rsi_values


def analyze_rsi(prices: List[float], period: int = 14) -> Dict[str, Any]:
    """RSI 분석"""
    rsi_values = calculate_rsi(prices, period)
    
    if not rsi_values or rsi_values[-1] is None:
        return {"error": "RSI 계산 실패"}
    
    current_rsi = rsi_values[-1]
    
    # 신호 판단
    if current_rsi >= 70:
        signal = "과매수"
        recommendation = "매도 고려"
    elif current_rsi <= 30:
        signal = "과매도"
        recommendation = "매수 고려"
    elif current_rsi >= 60:
        signal = "강세"
        recommendation = "보유"
    elif current_rsi <= 40:
        signal = "약세"
        recommendation = "관망"
    else:
        signal = "중립"
        recommendation = "관망"
    
    # 다이버전스 탐지 (간단 버전)
    divergence = None
    if len(prices) >= 20 and len(rsi_values) >= 20:
        # 가격은 상승하는데 RSI는 하락
        if prices[-1] > prices[-20] and rsi_values[-1] < rsi_values[-20]:
            divergence = "약세 다이버전스"
        # 가격은 하락하는데 RSI는 상승
        elif prices[-1] < prices[-20] and rsi_values[-1] > rsi_values[-20]:
            divergence = "강세 다이버전스"
    
    return {
        "current_rsi": current_rsi,
        "signal": signal,
        "recommendation": recommendation,
        "divergence": divergence,
        "overbought": current_rsi >= 70,
        "oversold": current_rsi <= 30
    }
