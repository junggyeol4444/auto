"""
기술적 분석 - 이동평균선 (MA, EMA)
"""
from typing import List, Dict, Any


def calculate_sma(prices: List[float], period: int = 20) -> List[float]:
    """단순 이동평균선 (SMA) 계산"""
    if len(prices) < period:
        return []
    
    sma = []
    for i in range(len(prices)):
        if i < period - 1:
            sma.append(None)
        else:
            avg = sum(prices[i - period + 1:i + 1]) / period
            sma.append(avg)
    
    return sma


def calculate_ema(prices: List[float], period: int = 20) -> List[float]:
    """지수 이동평균선 (EMA) 계산"""
    if len(prices) < period:
        return []
    
    ema = []
    multiplier = 2 / (period + 1)
    
    # 첫 EMA는 SMA로 계산
    sma = sum(prices[:period]) / period
    ema.append(sma)
    
    # 나머지 EMA 계산
    for i in range(period, len(prices)):
        ema_value = (prices[i] - ema[-1]) * multiplier + ema[-1]
        ema.append(ema_value)
    
    # 앞부분은 None으로 채우기
    result = [None] * (period - 1) + ema
    return result


def calculate_multiple_ma(prices: List[float], periods: List[int] = [5, 20, 60, 120]) -> Dict[str, List[float]]:
    """여러 기간의 이동평균선 계산"""
    result = {}
    for period in periods:
        result[f'SMA_{period}'] = calculate_sma(prices, period)
        result[f'EMA_{period}'] = calculate_ema(prices, period)
    return result


def detect_golden_cross(short_ma: List[float], long_ma: List[float]) -> Dict[str, Any]:
    """골든크로스 탐지 (단기 이평선이 장기 이평선을 상향 돌파)"""
    if len(short_ma) < 2 or len(long_ma) < 2:
        return {"detected": False}
    
    # 유효한 값만 확인
    if short_ma[-1] is None or short_ma[-2] is None:
        return {"detected": False}
    if long_ma[-1] is None or long_ma[-2] is None:
        return {"detected": False}
    
    # 이전에는 단기 < 장기, 현재는 단기 > 장기
    if short_ma[-2] < long_ma[-2] and short_ma[-1] > long_ma[-1]:
        return {
            "detected": True,
            "type": "golden_cross",
            "signal": "buy",
            "short_ma": short_ma[-1],
            "long_ma": long_ma[-1]
        }
    
    return {"detected": False}


def detect_dead_cross(short_ma: List[float], long_ma: List[float]) -> Dict[str, Any]:
    """데드크로스 탐지 (단기 이평선이 장기 이평선을 하향 돌파)"""
    if len(short_ma) < 2 or len(long_ma) < 2:
        return {"detected": False}
    
    # 유효한 값만 확인
    if short_ma[-1] is None or short_ma[-2] is None:
        return {"detected": False}
    if long_ma[-1] is None or long_ma[-2] is None:
        return {"detected": False}
    
    # 이전에는 단기 > 장기, 현재는 단기 < 장기
    if short_ma[-2] > long_ma[-2] and short_ma[-1] < long_ma[-1]:
        return {
            "detected": True,
            "type": "dead_cross",
            "signal": "sell",
            "short_ma": short_ma[-1],
            "long_ma": long_ma[-1]
        }
    
    return {"detected": False}


def analyze_ma_signals(prices: List[float]) -> Dict[str, Any]:
    """이동평균선 종합 분석"""
    if len(prices) < 120:
        return {"error": "데이터 부족 (최소 120개 필요)"}
    
    # 이동평균선 계산
    ma5 = calculate_sma(prices, 5)
    ma20 = calculate_sma(prices, 20)
    ma60 = calculate_sma(prices, 60)
    ma120 = calculate_sma(prices, 120)
    
    # 골든크로스/데드크로스 탐지
    gc_5_20 = detect_golden_cross(ma5, ma20)
    dc_5_20 = detect_dead_cross(ma5, ma20)
    gc_20_60 = detect_golden_cross(ma20, ma60)
    dc_20_60 = detect_dead_cross(ma20, ma60)
    
    # 현재 가격과 이평선 비교
    current_price = prices[-1]
    
    signals = []
    if gc_5_20["detected"]:
        signals.append("단기 골든크로스 (5일선이 20일선 돌파)")
    if dc_5_20["detected"]:
        signals.append("단기 데드크로스 (5일선이 20일선 하향)")
    if gc_20_60["detected"]:
        signals.append("중기 골든크로스 (20일선이 60일선 돌파)")
    if dc_20_60["detected"]:
        signals.append("중기 데드크로스 (20일선이 60일선 하향)")
    
    # 정배열/역배열 판단
    if (ma5[-1] and ma20[-1] and ma60[-1] and ma120[-1]):
        if ma5[-1] > ma20[-1] > ma60[-1] > ma120[-1]:
            signals.append("정배열 (강한 상승 추세)")
        elif ma5[-1] < ma20[-1] < ma60[-1] < ma120[-1]:
            signals.append("역배열 (강한 하락 추세)")
    
    return {
        "current_price": current_price,
        "ma5": ma5[-1] if ma5[-1] else None,
        "ma20": ma20[-1] if ma20[-1] else None,
        "ma60": ma60[-1] if ma60[-1] else None,
        "ma120": ma120[-1] if ma120[-1] else None,
        "signals": signals,
        "golden_cross_5_20": gc_5_20,
        "dead_cross_5_20": dc_5_20,
        "golden_cross_20_60": gc_20_60,
        "dead_cross_20_60": dc_20_60
    }
