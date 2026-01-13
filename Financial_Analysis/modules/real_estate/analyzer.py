"""
부동산 분석 모듈
"""
from typing import List, Dict, Any


class RealEstateAnalyzer:
    def __init__(self):
        """부동산 분석기 초기화"""
        pass
    
    def analyze_price_trend(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """가격 추이 분석"""
        if not data:
            return {}
        
        try:
            # 평당 가격 계산
            for item in data:
                area = item.get("area", 0)
                price = item.get("price", 0)
                if area > 0:
                    area_pyeong = area / 3.3058
                    price_per_pyeong = (price * 10000) / area_pyeong / 10000
                    item["price_per_pyeong"] = price_per_pyeong
            
            # 평균 가격
            avg_price = sum(d["price"] for d in data) / len(data)
            
            # 평균 평당 가격
            pyeong_prices = [d.get("price_per_pyeong", 0) for d in data if "price_per_pyeong" in d]
            avg_price_per_pyeong = sum(pyeong_prices) / len(pyeong_prices) if pyeong_prices else 0
            
            return {
                "region": data[0].get("region", ""),
                "total_count": len(data),
                "avg_price_10k": avg_price,
                "avg_price_per_pyeong": avg_price_per_pyeong,
                "min_price": min(d["price"] for d in data),
                "max_price": max(d["price"] for d in data)
            }
            
        except Exception as e:
            print(f"가격 추이 분석 실패: {e}")
            return {}
    
    def detect_hot_regions(self, data_by_region: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """급등 지역 탐지 (샘플)"""
        # 실제로는 시계열 데이터로 3개월 대비 분석 필요
        hot_regions = [
            {"region": "강남구", "change_pct": 12.5, "avg_price": 180000},
            {"region": "서초구", "change_pct": 10.2, "avg_price": 170000},
            {"region": "용산구", "change_pct": 8.5, "avg_price": 150000}
        ]
        return sorted(hot_regions, key=lambda x: x['change_pct'], reverse=True)
