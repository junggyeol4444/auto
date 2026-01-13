"""
기술적 분석 - 볼린저 밴드
"""
from typing import List, Dict, Any
import math


def calculate_bollinger_bands(prices: List[float], period: int = 20, std_dev: int = 2) -> Dict[str, List[float]]:
    """볼린저 밴드 계산"""
    if len(prices) < period:
        return {"upper": [], "middle": [], "lower": []}
    
    upper = []
    middle = []
    lower = []
    
    for i in range(len(prices)):
        if i < period - 1:
            upper.append(None)
            middle.append(None)
            lower.append(None)
        else:
            # 중간선 (SMA)
            window = prices[i - period + 1:i + 1]
            sma = sum(window) / period
            
            # 표준편차
            variance = sum((x - sma) ** 2 for x in window) / period
            std = math.sqrt(variance)
            
            # 상단선/하단선
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            upper.append(upper_band)
            middle.append(sma)
            lower.append(lower_band)
    
    return {
        "upper": upper,
        "middle": middle,
        "lower": lower
    }


def analyze_bollinger_bands(prices: List[float], period: int = 20, std_dev: int = 2) -> Dict[str, Any]:
    """볼린저 밴드 분석"""
    bands = calculate_bollinger_bands(prices, period, std_dev)
    
    if not bands["upper"] or bands["upper"][-1] is None:
        return {"error": "볼린저 밴드 계산 실패"}
    
    current_price = prices[-1]
    upper = bands["upper"][-1]
    middle = bands["middle"][-1]
    lower = bands["lower"][-1]
    
    # 밴드 폭
    band_width = upper - lower
    band_width_pct = (band_width / middle * 100) if middle != 0 else 0
    
    # 가격 위치
    if current_price >= upper:
        position = "상단 돌파"
        signal = "과매수"
        recommendation = "매도 고려"
    elif current_price <= lower:
        position = "하단 돌파"
        signal = "과매도"
        recommendation = "매수 고려"
    elif current_price > middle:
        position = "상단 영역"
        signal = "강세"
        recommendation = "보유"
    elif current_price < middle:
        position = "하단 영역"
        signal = "약세"
        recommendation = "관망"
    else:
        position = "중간선"
        signal = "중립"
        recommendation = "관망"
    
    # %B 계산 (볼린저 밴드 내 가격 위치)
    percent_b = ((current_price - lower) / (upper - lower)) if (upper - lower) != 0 else 0.5
    
    return {
        "current_price": current_price,
        "upper_band": upper,
        "middle_band": middle,
        "lower_band": lower,
        "band_width": band_width,
        "band_width_pct": band_width_pct,
        "position": position,
        "signal": signal,
        "recommendation": recommendation,
        "percent_b": percent_b
    }
