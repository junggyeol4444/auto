"""
모듈 임포트 테스트
설치된 패키지와 프로젝트 모듈 확인
"""
import sys
import os

# 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """모듈 임포트 테스트"""
    print("=" * 60)
    print("모듈 임포트 테스트 시작")
    print("=" * 60)
    print()
    
    # 필수 패키지 확인
    packages = [
        "customtkinter",
        "pandas",
        "numpy",
        "requests",
        "yfinance",
        "sklearn"
    ]
    
    print("[ 필수 패키지 확인 ]")
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package:20s} - 설치됨")
        except ImportError:
            print(f"✗ {package:20s} - 미설치 (pip install {package})")
    
    print()
    print("[ 프로젝트 모듈 확인 ]")
    
    # 프로젝트 모듈 확인
    modules_to_test = [
        ("database.db_manager", "DatabaseManager"),
        ("modules.crypto.upbit_api", "UpbitAPI"),
        ("modules.crypto.binance_api", "BinanceAPI"),
        ("modules.crypto.coingecko_api", "CoinGeckoAPI"),
        ("modules.crypto.analyzer", "CryptoAnalyzer"),
        ("modules.forex.exchange_rate", "ExchangeRateAPI"),
        ("modules.forex.predictor", "ForexPredictor"),
        ("modules.stocks.stock_api", "StockAPI"),
        ("modules.real_estate.molit_api", "MOLITApi"),
        ("modules.alert.telegram_bot", "TelegramAlert"),
        ("modules.alert.email_sender", "EmailAlert"),
        ("modules.alert.popup", "PopupAlert"),
        ("modules.technical.ma", "calculate_sma"),
        ("modules.technical.rsi", "calculate_rsi"),
        ("modules.technical.bollinger", "calculate_bollinger_bands"),
        ("modules.technical.macd", "calculate_macd"),
        ("modules.technical.stochastic", "calculate_stochastic")
    ]
    
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✓ {module_name:40s} - OK")
        except Exception as e:
            print(f"✗ {module_name:40s} - 오류: {e}")
    
    print()
    print("=" * 60)
    print("테스트 완료")
    print("=" * 60)


if __name__ == "__main__":
    test_imports()
