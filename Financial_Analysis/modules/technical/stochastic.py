"""
기술적 분석 - 스토캐스틱
"""
from typing import List, Dict, Any


def calculate_stochastic(highs: List[float], lows: List[float], closes: List[float], 
                        period: int = 14, k_smooth: int = 3, d_period: int = 3) -> Dict[str, List[float]]:
    """스토캐스틱 계산"""
    if len(closes) < period:
        return {"%K": [], "%D": []}
    
    # Fast %K 계산
    fast_k = []
    for i in range(len(closes)):
        if i < period - 1:
            fast_k.append(None)
        else:
            window_high = max(highs[i - period + 1:i + 1])
            window_low = min(lows[i - period + 1:i + 1])
            
            if window_high == window_low:
                fast_k.append(50)
            else:
                k = ((closes[i] - window_low) / (window_high - window_low)) * 100
                fast_k.append(k)
    
    # Slow %K (Fast %K의 이동평균)
    slow_k = []
    for i in range(len(fast_k)):
        if i < k_smooth - 1 or fast_k[i] is None:
            slow_k.append(None)
        else:
            window = [k for k in fast_k[i - k_smooth + 1:i + 1] if k is not None]
            if window:
                slow_k.append(sum(window) / len(window))
            else:
                slow_k.append(None)
    
    # %D (Slow %K의 이동평균)
    d_line = []
    for i in range(len(slow_k)):
        if i < d_period - 1 or slow_k[i] is None:
            d_line.append(None)
        else:
            window = [k for k in slow_k[i - d_period + 1:i + 1] if k is not None]
            if window:
                d_line.append(sum(window) / len(window))
            else:
                d_line.append(None)
    
    return {
        "%K": slow_k,
        "%D": d_line
    }


def analyze_stochastic(highs: List[float], lows: List[float], closes: List[float], 
                       period: int = 14) -> Dict[str, Any]:
    """스토캐스틱 분석"""
    stoch = calculate_stochastic(highs, lows, closes, period)
    
    k_line = stoch["%K"]
    d_line = stoch["%D"]
    
    if not k_line or k_line[-1] is None or not d_line or d_line[-1] is None:
        return {"error": "스토캐스틱 계산 실패"}
    
    current_k = k_line[-1]
    current_d = d_line[-1]
    
    # 신호 판단
    signals = []
    
    # 과매수/과매도
    if current_k >= 80:
        signals.append("과매수 (80 이상)")
        recommendation = "매도 고려"
    elif current_k <= 20:
        signals.append("과매도 (20 이하)")
        recommendation = "매수 고려"
    else:
        recommendation = "관망"
    
    # %K와 %D 크로스
    if len(k_line) >= 2 and len(d_line) >= 2:
        prev_k = k_line[-2]
        prev_d = d_line[-2]
        
        if prev_k is not None and prev_d is not None:
            # 골든크로스
            if prev_k < prev_d and current_k > current_d:
                signals.append("골든크로스 (매수 신호)")
                if current_k < 50:
                    recommendation = "매수 고려"
            # 데드크로스
            elif prev_k > prev_d and current_k < current_d:
                signals.append("데드크로스 (매도 신호)")
                if current_k > 50:
                    recommendation = "매도 고려"
    
    # 위치
    if current_k > 50:
        signals.append("강세 영역 (50 이상)")
    else:
        signals.append("약세 영역 (50 이하)")
    
    return {
        "%K": current_k,
        "%D": current_d,
        "signals": signals,
        "recommendation": recommendation,
        "overbought": current_k >= 80,
        "oversold": current_k <= 20
    }
