"""
메인 GUI 윈도우
CustomTkinter 기반 금융 데이터 분석 시스템
"""
import customtkinter as ctk
from typing import Dict, Any
import json
import os
import sys

# 상대 경로 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.crypto.upbit_api import UpbitAPI
from modules.crypto.analyzer import CryptoAnalyzer
from modules.forex.exchange_rate import ExchangeRateAPI
from modules.forex.predictor import ForexPredictor
from modules.stocks.stock_api import StockAPI
from modules.alert.telegram_bot import TelegramAlert
from modules.alert.email_sender import EmailAlert
from modules.alert.popup import PopupAlert
from database.db_manager import DatabaseManager


class FinancialAnalysisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 윈도우 설정
        self.title("금융 데이터 분석 & 알림 시스템")
        self.geometry("1400x900")
        
        # 테마 설정
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # 설정 로드
        self.config = self.load_config()
        
        # 모듈 초기화
        self.init_modules()
        
        # UI 구성
        self.create_ui()
    
    def load_config(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"설정 파일 로드 실패: {e}")
        
        # 기본 설정 반환
        return {
            "api_keys": {},
            "settings": {"language": "ko", "theme": "dark"},
            "alerts": {}
        }
    
    def save_config(self):
        """설정 파일 저장"""
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print("설정이 저장되었습니다.")
        except Exception as e:
            print(f"설정 파일 저장 실패: {e}")
    
    def init_modules(self):
        """모듈 초기화"""
        try:
            self.db = DatabaseManager()
            self.crypto_analyzer = CryptoAnalyzer()
            self.forex_api = ExchangeRateAPI(
                self.config.get("api_keys", {}).get("exchange_rate_api", {}).get("api_key", "")
            )
            self.forex_predictor = ForexPredictor()
            self.stock_api = StockAPI()
            
            # 알림 모듈
            telegram_config = self.config.get("api_keys", {}).get("telegram", {})
            self.telegram = TelegramAlert(
                telegram_config.get("bot_token", ""),
                telegram_config.get("chat_id", "")
            )
            
            email_config = self.config.get("api_keys", {}).get("email", {})
            self.email = EmailAlert(
                email_config.get("smtp_server", "smtp.gmail.com"),
                email_config.get("smtp_port", 587),
                email_config.get("sender_email", ""),
                email_config.get("sender_password", "")
            )
            
            self.popup = PopupAlert()
            
            print("모듈 초기화 완료")
        except Exception as e:
            print(f"모듈 초기화 실패: {e}")
    
    def create_ui(self):
        """UI 생성"""
        # 탭뷰 생성
        self.tabview = ctk.CTkTabview(self, width=1380, height=860)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)
        
        # 탭 추가
        self.tabview.add("암호화폐")
        self.tabview.add("환율")
        self.tabview.add("부동산")
        self.tabview.add("주식")
        self.tabview.add("설정")
        
        # 각 탭 구성
        self.create_crypto_tab()
        self.create_forex_tab()
        self.create_real_estate_tab()
        self.create_stocks_tab()
        self.create_settings_tab()
    
    def create_crypto_tab(self):
        """암호화폐 탭"""
        tab = self.tabview.tab("암호화폐")
        
        # 프레임 구성
        left_frame = ctk.CTkFrame(tab, width=300)
        left_frame.pack(side="left", fill="both", padx=10, pady=10)
        
        right_frame = ctk.CTkFrame(tab)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # 좌측: 코인 목록
        ctk.CTkLabel(left_frame, text="실시간 코인 시세", font=("Arial", 20, "bold")).pack(pady=10)
        
        self.crypto_listbox = ctk.CTkTextbox(left_frame, width=280, height=600)
        self.crypto_listbox.pack(pady=5, padx=10)
        
        ctk.CTkButton(left_frame, text="시세 조회", command=self.load_crypto_prices).pack(pady=5)
        ctk.CTkButton(left_frame, text="급등/급락 코인", command=self.load_top_movers).pack(pady=5)
        
        # 우측: 정보 표시
        ctk.CTkLabel(right_frame, text="코인 상세 정보", font=("Arial", 20, "bold")).pack(pady=10)
        
        self.crypto_info_text = ctk.CTkTextbox(right_frame, width=800, height=600)
        self.crypto_info_text.pack(pady=10, padx=10, fill="both", expand=True)
        
        # 알림 설정 프레임
        alert_frame = ctk.CTkFrame(right_frame)
        alert_frame.pack(pady=10, fill="x", padx=10)
        
        ctk.CTkLabel(alert_frame, text="가격 알림 설정:").pack(side="left", padx=5)
        
        self.crypto_alert_market = ctk.CTkEntry(alert_frame, width=150, placeholder_text="KRW-BTC")
        self.crypto_alert_market.pack(side="left", padx=5)
        
        self.crypto_alert_price = ctk.CTkEntry(alert_frame, width=150, placeholder_text="목표가 (원)")
        self.crypto_alert_price.pack(side="left", padx=5)
        
        ctk.CTkButton(alert_frame, text="알림 설정", command=self.set_crypto_alert).pack(side="left", padx=5)
    
    def create_forex_tab(self):
        """환율 탭"""
        tab = self.tabview.tab("환율")
        
        # 상단: 주요 환율
        top_frame = ctk.CTkFrame(tab)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(top_frame, text="주요 통화 환율 (KRW 기준)", font=("Arial", 20, "bold")).pack(pady=10)
        
        self.forex_rates_text = ctk.CTkTextbox(top_frame, width=1300, height=200)
        self.forex_rates_text.pack(pady=10, padx=10)
        
        ctk.CTkButton(top_frame, text="환율 조회", command=self.load_forex_rates).pack(pady=5)
        
        # 하단: 환차익 계산기
        bottom_frame = ctk.CTkFrame(tab)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(bottom_frame, text="환차익 계산기", font=("Arial", 18, "bold")).pack(pady=10)
        
        calc_frame = ctk.CTkFrame(bottom_frame)
        calc_frame.pack(pady=10)
        
        ctk.CTkLabel(calc_frame, text="금액:").grid(row=0, column=0, padx=5, pady=5)
        self.forex_amount = ctk.CTkEntry(calc_frame, width=150)
        self.forex_amount.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(calc_frame, text="출발 통화:").grid(row=1, column=0, padx=5, pady=5)
        self.forex_from = ctk.CTkEntry(calc_frame, width=150, placeholder_text="USD")
        self.forex_from.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(calc_frame, text="도착 통화:").grid(row=2, column=0, padx=5, pady=5)
        self.forex_to = ctk.CTkEntry(calc_frame, width=150, placeholder_text="KRW")
        self.forex_to.grid(row=2, column=1, padx=5, pady=5)
        
        ctk.CTkButton(calc_frame, text="계산", command=self.calculate_exchange_profit).grid(row=3, column=0, columnspan=2, pady=10)
        
        self.forex_result_text = ctk.CTkTextbox(bottom_frame, width=1300, height=300)
        self.forex_result_text.pack(pady=10, padx=10)
    
    def create_real_estate_tab(self):
        """부동산 탭"""
        tab = self.tabview.tab("부동산")
        
        ctk.CTkLabel(tab, text="아파트 실거래가 조회", font=("Arial", 20, "bold")).pack(pady=10)
        
        # 지역 선택
        region_frame = ctk.CTkFrame(tab)
        region_frame.pack(pady=10)
        
        ctk.CTkLabel(region_frame, text="지역 코드:").pack(side="left", padx=5)
        self.region_code = ctk.CTkEntry(region_frame, width=150, placeholder_text="11680 (강남구)")
        self.region_code.pack(side="left", padx=5)
        
        ctk.CTkButton(region_frame, text="조회", command=self.load_real_estate_data).pack(side="left", padx=5)
        
        # 결과 표시
        self.real_estate_text = ctk.CTkTextbox(tab, width=1300, height=700)
        self.real_estate_text.pack(pady=10, padx=10, fill="both", expand=True)
    
    def create_stocks_tab(self):
        """주식 탭"""
        tab = self.tabview.tab("주식")
        
        ctk.CTkLabel(tab, text="주식 정보 조회", font=("Arial", 20, "bold")).pack(pady=10)
        
        # 검색
        search_frame = ctk.CTkFrame(tab)
        search_frame.pack(pady=10)
        
        ctk.CTkLabel(search_frame, text="종목 코드:").pack(side="left", padx=5)
        self.stock_symbol = ctk.CTkEntry(search_frame, width=200, placeholder_text="005930.KS (삼성전자)")
        self.stock_symbol.pack(side="left", padx=5)
        
        ctk.CTkButton(search_frame, text="조회", command=self.load_stock_info).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="기술적 분석", command=self.analyze_stock_technical).pack(side="left", padx=5)
        
        # 결과 표시
        self.stock_info_text = ctk.CTkTextbox(tab, width=1300, height=700)
        self.stock_info_text.pack(pady=10, padx=10, fill="both", expand=True)
    
    def create_settings_tab(self):
        """설정 탭"""
        tab = self.tabview.tab("설정")
        
        ctk.CTkLabel(tab, text="API 키 및 알림 설정", font=("Arial", 20, "bold")).pack(pady=10)
        
        # 스크롤 가능한 프레임
        settings_frame = ctk.CTkScrollableFrame(tab, width=1300, height=750)
        settings_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # 텔레그램 설정
        ctk.CTkLabel(settings_frame, text="텔레그램 봇 설정", font=("Arial", 16, "bold")).pack(pady=10, anchor="w")
        
        telegram_frame = ctk.CTkFrame(settings_frame)
        telegram_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(telegram_frame, text="Bot Token:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.telegram_token = ctk.CTkEntry(telegram_frame, width=400)
        self.telegram_token.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(telegram_frame, text="Chat ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.telegram_chat_id = ctk.CTkEntry(telegram_frame, width=400)
        self.telegram_chat_id.grid(row=1, column=1, padx=5, pady=5)
        
        # 이메일 설정
        ctk.CTkLabel(settings_frame, text="이메일 설정", font=("Arial", 16, "bold")).pack(pady=10, anchor="w")
        
        email_frame = ctk.CTkFrame(settings_frame)
        email_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(email_frame, text="발신 이메일:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.email_sender = ctk.CTkEntry(email_frame, width=400)
        self.email_sender.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(email_frame, text="비밀번호:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.email_password = ctk.CTkEntry(email_frame, width=400, show="*")
        self.email_password.grid(row=1, column=1, padx=5, pady=5)
        
        # 저장 버튼
        ctk.CTkButton(settings_frame, text="설정 저장", command=self.save_settings, 
                     width=200, height=40).pack(pady=20)
        
        ctk.CTkButton(settings_frame, text="테스트 알림 전송", command=self.test_alerts,
                     width=200, height=40).pack(pady=5)
        
        # 기존 설정 로드
        self.load_settings_to_ui()
    
    def load_crypto_prices(self):
        """암호화폐 시세 조회"""
        self.crypto_listbox.delete("0.0", "end")
        self.crypto_listbox.insert("0.0", "조회 중...\n")
        
        try:
            markets = self.crypto_analyzer.upbit.get_market_all()
            krw_markets = [m['market'] for m in markets if m['market'].startswith('KRW-')][:20]
            
            tickers = self.crypto_analyzer.upbit.get_ticker(krw_markets)
            
            self.crypto_listbox.delete("0.0", "end")
            self.crypto_listbox.insert("0.0", "=== 실시간 시세 (업비트) ===\n\n")
            
            for ticker in tickers:
                market = ticker['market']
                name = ticker.get('korean_name', market)
                price = ticker['trade_price']
                change = ticker.get('signed_change_rate', 0) * 100
                
                text = f"{name} ({market})\n"
                text += f"  가격: {price:,.0f}원\n"
                text += f"  변동: {change:+.2f}%\n\n"
                
                self.crypto_listbox.insert("end", text)
            
        except Exception as e:
            self.crypto_listbox.delete("0.0", "end")
            self.crypto_listbox.insert("0.0", f"오류 발생: {e}")
    
    def load_top_movers(self):
        """급등/급락 코인 조회"""
        self.crypto_info_text.delete("0.0", "end")
        self.crypto_info_text.insert("0.0", "조회 중...\n")
        
        try:
            movers = self.crypto_analyzer.upbit.get_top_movers(20)
            
            self.crypto_info_text.delete("0.0", "end")
            self.crypto_info_text.insert("0.0", "=== 급등/급락 코인 ===\n\n")
            
            for mover in movers:
                text = f"{mover['korean_name']} ({mover['market']})\n"
                text += f"  현재가: {mover['trade_price']:,.0f}원\n"
                text += f"  변동률: {mover['change_rate']:+.2f}%\n"
                text += f"  거래대금: {mover['acc_trade_price_24h']/100000000:.2f}억원\n\n"
                
                self.crypto_info_text.insert("end", text)
            
        except Exception as e:
            self.crypto_info_text.delete("0.0", "end")
            self.crypto_info_text.insert("0.0", f"오류 발생: {e}")
    
    def set_crypto_alert(self):
        """암호화폐 가격 알림 설정"""
        market = self.crypto_alert_market.get().strip()
        try:
            target_price = float(self.crypto_alert_price.get().strip())
        except ValueError:
            self.show_message("오류", "유효한 가격을 입력하세요.")
            return
        
        if not market or target_price <= 0:
            self.show_message("오류", "마켓과 가격을 입력하세요.")
            return
        
        # 설정에 저장
        if "crypto" not in self.config["alerts"]:
            self.config["alerts"]["crypto"] = []
        
        self.config["alerts"]["crypto"].append({
            "market": market,
            "target_price": target_price
        })
        
        self.save_config()
        self.show_message("성공", f"{market} 알림이 설정되었습니다.\n목표가: {target_price:,.0f}원")
    
    def load_forex_rates(self):
        """환율 조회"""
        self.forex_rates_text.delete("0.0", "end")
        self.forex_rates_text.insert("0.0", "조회 중...\n")
        
        try:
            rates = self.forex_api.get_major_currencies_krw()
            
            self.forex_rates_text.delete("0.0", "end")
            self.forex_rates_text.insert("0.0", "=== 주요 통화 환율 (KRW) ===\n\n")
            
            currency_names = {
                "USD": "미국 달러",
                "JPY": "일본 엔 (100엔)",
                "EUR": "유로",
                "CNY": "중국 위안",
                "GBP": "영국 파운드"
            }
            
            for currency, rate in rates.items():
                name = currency_names.get(currency, currency)
                self.forex_rates_text.insert("end", f"{name} ({currency}): {rate:,.2f}원\n")
            
        except Exception as e:
            self.forex_rates_text.delete("0.0", "end")
            self.forex_rates_text.insert("0.0", f"오류 발생: {e}")
    
    def calculate_exchange_profit(self):
        """환차익 계산"""
        try:
            amount = float(self.forex_amount.get().strip())
            from_currency = self.forex_from.get().strip().upper()
            to_currency = self.forex_to.get().strip().upper()
            
            result = self.forex_api.calculate_exchange_profit(amount, from_currency, to_currency)
            
            if not result:
                self.forex_result_text.delete("0.0", "end")
                self.forex_result_text.insert("0.0", "환차익 계산 실패")
                return
            
            self.forex_result_text.delete("0.0", "end")
            self.forex_result_text.insert("0.0", "=== 환차익 계산 결과 ===\n\n")
            self.forex_result_text.insert("end", f"원래 금액: {result['original_amount']:,.2f} {from_currency}\n")
            self.forex_result_text.insert("end", f"환전 금액: {result['exchanged_amount']:,.2f} {to_currency}\n")
            self.forex_result_text.insert("end", f"재환전 금액: {result['final_amount']:,.2f} {from_currency}\n")
            self.forex_result_text.insert("end", f"손익: {result['profit']:,.2f} {from_currency} ({result['profit_percent']:+.2f}%)\n")
            self.forex_result_text.insert("end", f"수수료: {result['fee_percent']}%\n")
            
        except Exception as e:
            self.forex_result_text.delete("0.0", "end")
            self.forex_result_text.insert("0.0", f"오류 발생: {e}")
    
    def load_real_estate_data(self):
        """부동산 데이터 조회"""
        from modules.real_estate.molit_api import MOLITApi
        
        region_code = self.region_code.get().strip()
        if not region_code:
            region_code = "11680"  # 기본값: 강남구
        
        self.real_estate_text.delete("0.0", "end")
        self.real_estate_text.insert("0.0", "조회 중...\n")
        
        try:
            molit = MOLITApi()
            data = molit.get_apt_trade(region_code, "202401")
            
            self.real_estate_text.delete("0.0", "end")
            self.real_estate_text.insert("0.0", f"=== 아파트 실거래가 ({region_code}) ===\n\n")
            
            for apt in data:
                price_per_pyeong = molit.calculate_price_per_pyeong(apt['area'], apt['price'])
                
                text = f"{apt['apartment_name']} ({apt['dong']})\n"
                text += f"  거래금액: {apt['price']:,}만원\n"
                text += f"  전용면적: {apt['area']:.2f}㎡\n"
                text += f"  평당가격: {price_per_pyeong:,.0f}만원\n"
                text += f"  층: {apt['floor']}층\n"
                text += f"  건축년도: {apt['built_year']}년\n\n"
                
                self.real_estate_text.insert("end", text)
            
        except Exception as e:
            self.real_estate_text.delete("0.0", "end")
            self.real_estate_text.insert("0.0", f"오류 발생: {e}")
    
    def load_stock_info(self):
        """주식 정보 조회"""
        symbol = self.stock_symbol.get().strip()
        if not symbol:
            self.show_message("오류", "종목 코드를 입력하세요.")
            return
        
        self.stock_info_text.delete("0.0", "end")
        self.stock_info_text.insert("0.0", "조회 중...\n")
        
        try:
            info = self.stock_api.get_stock_info(symbol)
            
            if not info:
                self.stock_info_text.delete("0.0", "end")
                self.stock_info_text.insert("0.0", "종목 정보를 찾을 수 없습니다.")
                return
            
            self.stock_info_text.delete("0.0", "end")
            self.stock_info_text.insert("0.0", f"=== {info['name']} ({info['symbol']}) ===\n\n")
            self.stock_info_text.insert("end", f"현재가: ${info['price']:,.2f}\n")
            self.stock_info_text.insert("end", f"전일종가: ${info['previous_close']:,.2f}\n")
            self.stock_info_text.insert("end", f"시가총액: ${info['market_cap']:,}\n")
            self.stock_info_text.insert("end", f"PER: {info['pe_ratio']:.2f}\n")
            self.stock_info_text.insert("end", f"PBR: {info['pb_ratio']:.2f}\n")
            self.stock_info_text.insert("end", f"배당수익률: {info['dividend_yield']*100:.2f}%\n")
            self.stock_info_text.insert("end", f"52주 최고: ${info['52w_high']:,.2f}\n")
            self.stock_info_text.insert("end", f"52주 최저: ${info['52w_low']:,.2f}\n")
            
        except Exception as e:
            self.stock_info_text.delete("0.0", "end")
            self.stock_info_text.insert("0.0", f"오류 발생: {e}")
    
    def analyze_stock_technical(self):
        """주식 기술적 분석"""
        from modules.technical.ma import analyze_ma_signals
        from modules.technical.rsi import analyze_rsi
        
        symbol = self.stock_symbol.get().strip()
        if not symbol:
            self.show_message("오류", "종목 코드를 입력하세요.")
            return
        
        self.stock_info_text.delete("0.0", "end")
        self.stock_info_text.insert("0.0", "분석 중...\n")
        
        try:
            # 과거 데이터 조회
            df = self.stock_api.get_historical_data(symbol, period="1y", interval="1d")
            
            if df.empty:
                self.stock_info_text.delete("0.0", "end")
                self.stock_info_text.insert("0.0", "데이터를 가져올 수 없습니다.")
                return
            
            prices = df['Close'].tolist()
            
            # 이동평균선 분석
            ma_analysis = analyze_ma_signals(prices)
            
            # RSI 분석
            rsi_analysis = analyze_rsi(prices)
            
            self.stock_info_text.delete("0.0", "end")
            self.stock_info_text.insert("0.0", f"=== {symbol} 기술적 분석 ===\n\n")
            
            if "error" not in ma_analysis:
                self.stock_info_text.insert("end", "[ 이동평균선 분석 ]\n")
                self.stock_info_text.insert("end", f"현재가: ${ma_analysis['current_price']:,.2f}\n")
                self.stock_info_text.insert("end", f"5일 이평: ${ma_analysis['ma5']:,.2f}\n")
                self.stock_info_text.insert("end", f"20일 이평: ${ma_analysis['ma20']:,.2f}\n")
                self.stock_info_text.insert("end", f"60일 이평: ${ma_analysis['ma60']:,.2f}\n")
                self.stock_info_text.insert("end", f"120일 이평: ${ma_analysis['ma120']:,.2f}\n\n")
                
                if ma_analysis['signals']:
                    self.stock_info_text.insert("end", "신호:\n")
                    for signal in ma_analysis['signals']:
                        self.stock_info_text.insert("end", f"  - {signal}\n")
                    self.stock_info_text.insert("end", "\n")
            
            if "error" not in rsi_analysis:
                self.stock_info_text.insert("end", "[ RSI 분석 ]\n")
                self.stock_info_text.insert("end", f"RSI(14): {rsi_analysis['current_rsi']:.2f}\n")
                self.stock_info_text.insert("end", f"신호: {rsi_analysis['signal']}\n")
                self.stock_info_text.insert("end", f"추천: {rsi_analysis['recommendation']}\n")
                if rsi_analysis['divergence']:
                    self.stock_info_text.insert("end", f"다이버전스: {rsi_analysis['divergence']}\n")
            
        except Exception as e:
            self.stock_info_text.delete("0.0", "end")
            self.stock_info_text.insert("0.0", f"오류 발생: {e}")
    
    def load_settings_to_ui(self):
        """설정을 UI에 로드"""
        try:
            telegram_config = self.config.get("api_keys", {}).get("telegram", {})
            self.telegram_token.insert(0, telegram_config.get("bot_token", ""))
            self.telegram_chat_id.insert(0, telegram_config.get("chat_id", ""))
            
            email_config = self.config.get("api_keys", {}).get("email", {})
            self.email_sender.insert(0, email_config.get("sender_email", ""))
            self.email_password.insert(0, email_config.get("sender_password", ""))
        except Exception as e:
            print(f"설정 로드 실패: {e}")
    
    def save_settings(self):
        """설정 저장"""
        try:
            # 텔레그램 설정
            if "api_keys" not in self.config:
                self.config["api_keys"] = {}
            if "telegram" not in self.config["api_keys"]:
                self.config["api_keys"]["telegram"] = {}
            
            self.config["api_keys"]["telegram"]["bot_token"] = self.telegram_token.get().strip()
            self.config["api_keys"]["telegram"]["chat_id"] = self.telegram_chat_id.get().strip()
            
            # 이메일 설정
            if "email" not in self.config["api_keys"]:
                self.config["api_keys"]["email"] = {}
            
            self.config["api_keys"]["email"]["sender_email"] = self.email_sender.get().strip()
            self.config["api_keys"]["email"]["sender_password"] = self.email_password.get().strip()
            
            self.save_config()
            
            # 모듈 재초기화
            self.init_modules()
            
            self.show_message("성공", "설정이 저장되었습니다.")
        except Exception as e:
            self.show_message("오류", f"설정 저장 실패: {e}")
    
    def test_alerts(self):
        """테스트 알림 전송"""
        try:
            # 팝업 알림
            self.popup.show_alert("테스트 알림", "팝업 알림이 정상 작동합니다!")
            
            # 텔레그램 알림
            if self.telegram.enabled:
                self.telegram.send_alert("테스트 알림", "텔레그램 알림이 정상 작동합니다!", "INFO")
            
            # 이메일 알림
            if self.email.enabled:
                self.email.send_alert(
                    self.email.sender_email,
                    "테스트 알림",
                    "이메일 알림이 정상 작동합니다!",
                    "INFO"
                )
            
            self.show_message("성공", "테스트 알림이 전송되었습니다.")
        except Exception as e:
            self.show_message("오류", f"알림 전송 실패: {e}")
    
    def show_message(self, title: str, message: str):
        """메시지 다이얼로그 표시"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        
        ctk.CTkLabel(dialog, text=message, wraplength=350).pack(pady=30)
        ctk.CTkButton(dialog, text="확인", command=dialog.destroy).pack(pady=10)
        
        dialog.transient(self)
        dialog.grab_set()


if __name__ == "__main__":
    app = FinancialAnalysisApp()
    app.mainloop()
