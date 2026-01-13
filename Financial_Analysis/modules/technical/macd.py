"""
기술적 분석 - MACD
"""
from typing import List, Dict, Any


def calculate_ema_for_macd(prices: List[float], period: int) -> List[float]:
    """MACD용 EMA 계산"""
    if len(prices) < period:
        return []
    
    multiplier = 2 / (period + 1)
    ema = [sum(prices[:period]) / period]
    
    for i in range(period, len(prices)):
        ema_value = (prices[i] - ema[-1]) * multiplier + ema[-1]
        ema.append(ema_value)
    
    return ema


def calculate_macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, List[float]]:
    """MACD 계산"""
    if len(prices) < slow:
        return {"macd": [], "signal": [], "histogram": []}
    
    # EMA 계산
    ema_fast = calculate_ema_for_macd(prices, fast)
    ema_slow = calculate_ema_for_macd(prices, slow)
    
    if not ema_fast or not ema_slow:
        return {"macd": [], "signal": [], "histogram": []}
    
    # MACD 라인 계산 (빠른 EMA - 느린 EMA)
    offset = slow - fast
    macd_line = [ema_fast[i + offset] - ema_slow[i] for i in range(len(ema_slow))]
    
    # 시그널 라인 계산 (MACD의 EMA)
    if len(macd_line) < signal:
        return {"macd": macd_line, "signal": [], "histogram": []}
    
    signal_line = calculate_ema_for_macd(macd_line, signal)
    
    # 히스토그램 계산
    histogram = []
    for i in range(len(signal_line)):
        idx = i + (len(macd_line) - len(signal_line))
        histogram.append(macd_line[idx] - signal_line[i])
    
    return {
        "macd": macd_line,
        "signal": signal_line,
        "histogram": histogram
    }


def analyze_macd(prices: List[float], fast: int = 12, slow: int = 26, signal_period: int = 9) -> Dict[str, Any]:
    """MACD 분석"""
    macd_data = calculate_macd(prices, fast, slow, signal_period)
    
    if not macd_data["macd"] or not macd_data["signal"]:
        return {"error": "MACD 계산 실패"}
    
    macd_line = macd_data["macd"]
    signal_line = macd_data["signal"]
    histogram = macd_data["histogram"]
    
    if not histogram or len(histogram) < 2:
        return {"error": "히스토그램 데이터 부족"}
    
    current_macd = macd_line[-1]
    current_signal = signal_line[-1]
    current_histogram = histogram[-1]
    prev_histogram = histogram[-2]
    
    # 신호 판단
    signals = []
    
    # 골든크로스/데드크로스
    if prev_histogram < 0 and current_histogram > 0:
        signals.append("골든크로스 (매수 신호)")
        recommendation = "매수 고려"
    elif prev_histogram > 0 and current_histogram < 0:
        signals.append("데드크로스 (매도 신호)")
        recommendation = "매도 고려"
    else:
        recommendation = "관망"
    
    # MACD 방향
    if current_macd > 0:
        signals.append("MACD 양수 (상승 모멘텀)")
    else:
        signals.append("MACD 음수 (하락 모멘텀)")
    
    # 히스토그램 방향
    if current_histogram > prev_histogram:
        signals.append("히스토그램 증가 (모멘텀 강화)")
    else:
        signals.append("히스토그램 감소 (모멘텀 약화)")
    
    return {
        "macd": current_macd,
        "signal": current_signal,
        "histogram": current_histogram,
        "signals": signals,
        "recommendation": recommendation
    }
