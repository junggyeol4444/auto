"""
GUI 메인 윈도우
Main Window with tkinter
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import logging
from datetime import datetime
import json
import os
import sys

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bots.discord.discord_bot import DiscordBot
from bots.telegram.telegram_bot import TelegramBot
from bots.line.line_bot import LineBot
from monitoring.price_tracker import PriceTracker
from monitoring.crawlers import CrawlerFactory
from monitoring.notifier import Notifier
from analytics.web_analytics import WebAnalytics
from analytics.trend_analyzer import TrendAnalyzer
from analytics.report_generator import ReportGenerator

logger = logging.getLogger('main_window')


class MainWindow:
    """메인 윈도우 클래스"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Bot Development Framework Suite")
        self.root.geometry("1200x800")
        
        # 봇 인스턴스
        self.discord_bot = None
        self.telegram_bot = None
        self.line_bot = None
        
        # 모니터링 시스템
        self.price_tracker = PriceTracker()
        self.notifier = None
        
        # 분석 도구
        self.web_analytics = WebAnalytics()
        self.trend_analyzer = TrendAnalyzer()
        self.report_generator = ReportGenerator()
        
        # 설정 로드
        self.config = self.load_config()
        
        # UI 생성
        self.create_ui()
    
    def load_config(self):
        """설정 파일 로드"""
        config_file = 'config.json'
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'discord': {'token': ''},
            'telegram': {'token': ''},
            'line': {'channel_access_token': '', 'channel_secret': ''},
            'email': {'host': '', 'port': 587, 'user': '', 'password': ''},
            'analytics': {'ga_property_id': ''}
        }
    
    def save_config(self):
        """설정 파일 저장"""
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f'설정 저장 실패: {str(e)}')
            return False
    
    def create_ui(self):
        """UI 생성"""
        # 탭 생성
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 각 탭 생성
        self.create_bot_tab()
        self.create_price_tab()
        self.create_analytics_tab()
        self.create_settings_tab()
    
    def create_bot_tab(self):
        """봇 관리 탭"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='봇 관리')
        
        # 플랫폼 선택
        platform_frame = ttk.LabelFrame(tab, text='플랫폼 선택', padding=10)
        platform_frame.pack(fill='x', padx=10, pady=10)
        
        self.platform_var = tk.StringVar(value='discord')
        platforms = [
            ('디스코드', 'discord'),
            ('텔레그램', 'telegram'),
            ('라인', 'line')
        ]
        
        for i, (text, value) in enumerate(platforms):
            ttk.Radiobutton(
                platform_frame,
                text=text,
                value=value,
                variable=self.platform_var,
                command=self.on_platform_change
            ).grid(row=0, column=i, padx=10)
        
        # API 토큰 입력
        token_frame = ttk.LabelFrame(tab, text='API 토큰', padding=10)
        token_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(token_frame, text='토큰:').grid(row=0, column=0, sticky='w')
        self.token_entry = ttk.Entry(token_frame, width=60, show='*')
        self.token_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Button(
            token_frame,
            text='저장',
            command=self.save_token
        ).grid(row=0, column=2)
        
        # 봇 컨트롤
        control_frame = ttk.Frame(tab)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        self.start_btn = ttk.Button(
            control_frame,
            text='봇 시작',
            command=self.start_bot,
            width=15
        )
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = ttk.Button(
            control_frame,
            text='봇 중지',
            command=self.stop_bot,
            width=15,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=5)
        
        # 로그 출력
        log_frame = ttk.LabelFrame(tab, text='로그', padding=10)
        log_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap='word')
        self.log_text.pack(fill='both', expand=True)
        
        # 로그 핸들러 추가
        self.setup_log_handler()
    
    def create_price_tab(self):
        """가격 모니터링 탭"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='가격 모니터링')
        
        # 상품 추가
        add_frame = ttk.LabelFrame(tab, text='상품 추가', padding=10)
        add_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(add_frame, text='상품 URL:').grid(row=0, column=0, sticky='w')
        self.url_entry = ttk.Entry(add_frame, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(add_frame, text='목표가:').grid(row=1, column=0, sticky='w')
        self.target_price_entry = ttk.Entry(add_frame, width=20)
        self.target_price_entry.grid(row=1, column=1, sticky='w', padx=10, pady=5)
        
        ttk.Button(
            add_frame,
            text='상품 등록',
            command=self.add_product
        ).grid(row=0, column=2, rowspan=2)
        
        # 상품 목록
        list_frame = ttk.LabelFrame(tab, text='등록된 상품', padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview
        columns = ('상품명', '현재가', '목표가', '상태')
        self.product_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings')
        
        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=200)
        
        self.product_tree.pack(fill='both', expand=True)
        
        # 버튼
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(
            btn_frame,
            text='새로고침',
            command=self.refresh_products
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text='가격 체크',
            command=self.check_prices
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text='삭제',
            command=self.delete_product
        ).pack(side='left', padx=5)
        
        # 초기 목록 로드
        self.refresh_products()
    
    def create_analytics_tab(self):
        """데이터 분석 탭"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='데이터 분석')
        
        # 분석 유형 선택
        type_frame = ttk.LabelFrame(tab, text='분석 유형', padding=10)
        type_frame.pack(fill='x', padx=10, pady=10)
        
        self.analysis_type = tk.StringVar(value='traffic')
        types = [
            ('웹 트래픽 분석', 'traffic'),
            ('키워드 트렌드 분석', 'trend')
        ]
        
        for i, (text, value) in enumerate(types):
            ttk.Radiobutton(
                type_frame,
                text=text,
                value=value,
                variable=self.analysis_type
            ).grid(row=0, column=i, padx=10)
        
        # 기간 설정
        period_frame = ttk.LabelFrame(tab, text='분석 기간', padding=10)
        period_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(period_frame, text='시작일:').grid(row=0, column=0, sticky='w')
        self.start_date_entry = ttk.Entry(period_frame, width=15)
        self.start_date_entry.insert(0, '2024-01-01')
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(period_frame, text='종료일:').grid(row=0, column=2, sticky='w', padx=(20, 0))
        self.end_date_entry = ttk.Entry(period_frame, width=15)
        self.end_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.end_date_entry.grid(row=0, column=3, padx=10, pady=5)
        
        # 실행 버튼
        ttk.Button(
            tab,
            text='분석 시작',
            command=self.start_analysis
        ).pack(pady=10)
        
        # 결과 표시
        result_frame = ttk.LabelFrame(tab, text='분석 결과', padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.analysis_text = scrolledtext.ScrolledText(result_frame, height=15, wrap='word')
        self.analysis_text.pack(fill='both', expand=True)
        
        # 리포트 생성 버튼
        ttk.Button(
            tab,
            text='PDF 리포트 생성',
            command=self.generate_report
        ).pack(pady=10)
    
    def create_settings_tab(self):
        """설정 탭"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='설정')
        
        # API 키 관리
        api_frame = ttk.LabelFrame(tab, text='API 키 관리', padding=10)
        api_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 스크롤 가능한 프레임
        canvas = tk.Canvas(api_frame)
        scrollbar = ttk.Scrollbar(api_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # API 설정 항목들
        row = 0
        
        # Discord
        ttk.Label(scrollable_frame, text='Discord Token:', font=('', 10, 'bold')).grid(
            row=row, column=0, sticky='w', pady=(10, 5)
        )
        row += 1
        self.discord_token_entry = ttk.Entry(scrollable_frame, width=60, show='*')
        self.discord_token_entry.insert(0, self.config.get('discord', {}).get('token', ''))
        self.discord_token_entry.grid(row=row, column=0, sticky='w', pady=5)
        row += 1
        
        # Telegram
        ttk.Label(scrollable_frame, text='Telegram Token:', font=('', 10, 'bold')).grid(
            row=row, column=0, sticky='w', pady=(10, 5)
        )
        row += 1
        self.telegram_token_entry = ttk.Entry(scrollable_frame, width=60, show='*')
        self.telegram_token_entry.insert(0, self.config.get('telegram', {}).get('token', ''))
        self.telegram_token_entry.grid(row=row, column=0, sticky='w', pady=5)
        row += 1
        
        # LINE
        ttk.Label(scrollable_frame, text='LINE Channel Access Token:', font=('', 10, 'bold')).grid(
            row=row, column=0, sticky='w', pady=(10, 5)
        )
        row += 1
        self.line_token_entry = ttk.Entry(scrollable_frame, width=60, show='*')
        self.line_token_entry.insert(0, self.config.get('line', {}).get('channel_access_token', ''))
        self.line_token_entry.grid(row=row, column=0, sticky='w', pady=5)
        row += 1
        
        # 저장 버튼
        ttk.Button(
            scrollable_frame,
            text='모든 설정 저장',
            command=self.save_all_settings
        ).grid(row=row, column=0, pady=20)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def setup_log_handler(self):
        """로그 핸들러 설정"""
        class TextHandler(logging.Handler):
            def __init__(self, text_widget):
                logging.Handler.__init__(self)
                self.text_widget = text_widget
            
            def emit(self, record):
                msg = self.format(record)
                def append():
                    self.text_widget.insert('end', msg + '\n')
                    self.text_widget.see('end')
                self.text_widget.after(0, append)
        
        text_handler = TextHandler(self.log_text)
        text_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(text_handler)
    
    def log(self, message):
        """로그 출력"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_text.insert('end', f'[{timestamp}] {message}\n')
        self.log_text.see('end')
    
    def on_platform_change(self):
        """플랫폼 변경 시"""
        platform = self.platform_var.get()
        token = ''
        
        if platform == 'discord':
            token = self.config.get('discord', {}).get('token', '')
        elif platform == 'telegram':
            token = self.config.get('telegram', {}).get('token', '')
        elif platform == 'line':
            token = self.config.get('line', {}).get('channel_access_token', '')
        
        self.token_entry.delete(0, 'end')
        self.token_entry.insert(0, token)
    
    def save_token(self):
        """토큰 저장"""
        platform = self.platform_var.get()
        token = self.token_entry.get()
        
        if platform == 'discord':
            self.config.setdefault('discord', {})['token'] = token
        elif platform == 'telegram':
            self.config.setdefault('telegram', {})['token'] = token
        elif platform == 'line':
            self.config.setdefault('line', {})['channel_access_token'] = token
        
        if self.save_config():
            messagebox.showinfo('성공', '토큰이 저장되었습니다.')
        else:
            messagebox.showerror('오류', '토큰 저장에 실패했습니다.')
    
    def start_bot(self):
        """봇 시작"""
        platform = self.platform_var.get()
        token = self.token_entry.get()
        
        if not token:
            messagebox.showwarning('경고', '토큰을 입력하세요.')
            return
        
        def run_bot():
            try:
                if platform == 'discord':
                    self.discord_bot = DiscordBot(token)
                    self.log('디스코드 봇 시작 중...')
                    self.discord_bot.run()
                
                elif platform == 'telegram':
                    self.telegram_bot = TelegramBot(token)
                    self.log('텔레그램 봇 시작 중...')
                    self.telegram_bot.run()
                
                elif platform == 'line':
                    self.line_bot = LineBot(token)
                    self.log('LINE 봇 시작 중...')
                    # LINE은 웹훅 서버가 필요
                    self.log('LINE 봇은 웹훅 서버 설정이 필요합니다.')
            
            except Exception as e:
                self.log(f'오류: {str(e)}')
        
        thread = threading.Thread(target=run_bot, daemon=True)
        thread.start()
        
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
    
    def stop_bot(self):
        """봇 중지"""
        self.log('봇 중지 중...')
        # 봇 중지 로직 (비동기 처리 필요)
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
    
    def add_product(self):
        """상품 추가"""
        url = self.url_entry.get()
        target_price_str = self.target_price_entry.get()
        
        if not url:
            messagebox.showwarning('경고', 'URL을 입력하세요.')
            return
        
        try:
            target_price = float(target_price_str) if target_price_str else None
        except ValueError:
            messagebox.showerror('오류', '올바른 가격을 입력하세요.')
            return
        
        # 크롤링으로 상품 정보 가져오기
        crawler = CrawlerFactory.get_crawler(url)
        product_info = crawler.crawl(url)
        
        if product_info:
            product_id = self.price_tracker.add_product(
                url=url,
                name=product_info['name'],
                site=product_info['site'],
                target_price=target_price
            )
            
            # 현재 가격 저장
            self.price_tracker.update_price(product_id, product_info['price'], product_info['in_stock'])
            
            self.log(f'상품 추가: {product_info["name"]}')
            self.refresh_products()
            
            messagebox.showinfo('성공', '상품이 등록되었습니다.')
        else:
            messagebox.showerror('오류', '상품 정보를 가져올 수 없습니다.')
    
    def refresh_products(self):
        """상품 목록 새로고침"""
        # 기존 항목 삭제
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # 상품 목록 가져오기
        products = self.price_tracker.get_all_products()
        
        for product in products:
            current_price = self.price_tracker.get_current_price(product['id'])
            target_price = product['target_price'] or 0
            
            if current_price and target_price and current_price <= target_price:
                status = '목표가 도달!'
            else:
                status = '추적 중'
            
            self.product_tree.insert('', 'end', iid=product['id'], values=(
                product['name'],
                f'{current_price:,.0f}원' if current_price else 'N/A',
                f'{target_price:,.0f}원' if target_price else 'N/A',
                status
            ))
    
    def check_prices(self):
        """가격 체크"""
        self.log('가격 체크 시작...')
        
        def check():
            products = self.price_tracker.get_all_products()
            
            for product in products:
                try:
                    crawler = CrawlerFactory.get_crawler(product['url'])
                    product_info = crawler.crawl(product['url'])
                    
                    if product_info:
                        self.price_tracker.update_price(
                            product['id'],
                            product_info['price'],
                            product_info['in_stock']
                        )
                        self.log(f'{product["name"]}: {product_info["price"]:,.0f}원')
                except Exception as e:
                    self.log(f'오류 ({product["name"]}): {str(e)}')
            
            self.log('가격 체크 완료')
            self.refresh_products()
        
        thread = threading.Thread(target=check, daemon=True)
        thread.start()
    
    def delete_product(self):
        """상품 삭제"""
        selection = self.product_tree.selection()
        if not selection:
            messagebox.showwarning('경고', '삭제할 상품을 선택하세요.')
            return
        
        if messagebox.askyesno('확인', '선택한 상품을 삭제하시겠습니까?'):
            for item in selection:
                product_id = int(item)
                self.price_tracker.delete_product(product_id)
            
            self.refresh_products()
            self.log('상품 삭제 완료')
    
    def start_analysis(self):
        """분석 시작"""
        analysis_type = self.analysis_type.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        
        self.analysis_text.delete('1.0', 'end')
        self.analysis_text.insert('end', f'분석 중...\n\n')
        
        def analyze():
            if analysis_type == 'traffic':
                data = self.web_analytics.get_traffic_overview('property_id', start_date, end_date)
                result = f"웹 트래픽 분석 결과 ({start_date} ~ {end_date})\n\n"
                result += f"총 사용자: {data['total_users']:,}명\n"
                result += f"총 세션: {data['total_sessions']:,}회\n"
                result += f"페이지뷰: {data['pageviews']:,}회\n"
                result += f"평균 세션 시간: {data['avg_session_duration']}초\n"
                result += f"이탈률: {data['bounce_rate']}%\n"
            
            elif analysis_type == 'trend':
                keywords = ['Python', 'JavaScript', 'React']
                data = self.trend_analyzer.analyze_keyword_trend(keywords, start_date, end_date)
                result = f"키워드 트렌드 분석 결과 ({start_date} ~ {end_date})\n\n"
                
                for keyword, info in data.items():
                    result += f"\n[{keyword}]\n"
                    result += f"평균 검색량 지수: {info['avg_ratio']}\n"
                    result += f"최대: {info['max_ratio']}, 최소: {info['min_ratio']}\n"
            
            self.analysis_text.delete('1.0', 'end')
            self.analysis_text.insert('end', result)
        
        thread = threading.Thread(target=analyze, daemon=True)
        thread.start()
    
    def generate_report(self):
        """리포트 생성"""
        self.log('PDF 리포트 생성 중...')
        
        def generate():
            try:
                # 더미 데이터로 리포트 생성
                data = {
                    '개요': {
                        '기간': f"{self.start_date_entry.get()} ~ {self.end_date_entry.get()}",
                        '총 사용자': '12,500명',
                        '페이지뷰': '45,600회'
                    }
                }
                
                output_file = self.report_generator.generate_pdf_report('분석 리포트', data)
                
                if output_file:
                    self.log(f'리포트 생성 완료: {output_file}')
                    messagebox.showinfo('성공', f'리포트가 생성되었습니다.\n{output_file}')
                else:
                    self.log('리포트 생성 실패')
            except Exception as e:
                self.log(f'오류: {str(e)}')
        
        thread = threading.Thread(target=generate, daemon=True)
        thread.start()
    
    def save_all_settings(self):
        """모든 설정 저장"""
        self.config['discord']['token'] = self.discord_token_entry.get()
        self.config['telegram']['token'] = self.telegram_token_entry.get()
        self.config['line']['channel_access_token'] = self.line_token_entry.get()
        
        if self.save_config():
            messagebox.showinfo('성공', '모든 설정이 저장되었습니다.')
        else:
            messagebox.showerror('오류', '설정 저장에 실패했습니다.')


if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
