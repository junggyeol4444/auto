"""
설정 윈도우
Settings Window
"""
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class SettingsWindow:
    """설정 윈도우 클래스"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        
        self.window = tk.Toplevel(parent)
        self.window.title("설정")
        self.window.geometry("600x700")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_ui()
    
    def create_ui(self):
        """UI 생성"""
        # 노트북 (탭)
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # API 설정 탭
        self.create_api_tab(notebook)
        
        # 알림 설정 탭
        self.create_notification_tab(notebook)
        
        # 일반 설정 탭
        self.create_general_tab(notebook)
        
        # 저장/취소 버튼
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(
            btn_frame,
            text='저장',
            command=self.save_settings
        ).pack(side='right', padx=5)
        
        ttk.Button(
            btn_frame,
            text='취소',
            command=self.window.destroy
        ).pack(side='right', padx=5)
    
    def create_api_tab(self, notebook):
        """API 설정 탭"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text='API 설정')
        
        # 스크롤 프레임
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        row = 0
        
        # Discord
        ttk.Label(scrollable_frame, text='Discord Bot Token:', font=('', 10, 'bold')).grid(
            row=row, column=0, sticky='w', padx=10, pady=(10, 5)
        )
        row += 1
        self.discord_token = ttk.Entry(scrollable_frame, width=50, show='*')
        self.discord_token.insert(0, self.config.get('discord', {}).get('token', ''))
        self.discord_token.grid(row=row, column=0, sticky='w', padx=10, pady=5)
        row += 1
        
        # Telegram
        ttk.Label(scrollable_frame, text='Telegram Bot Token:', font=('', 10, 'bold')).grid(
            row=row, column=0, sticky='w', padx=10, pady=(10, 5)
        )
        row += 1
        self.telegram_token = ttk.Entry(scrollable_frame, width=50, show='*')
        self.telegram_token.insert(0, self.config.get('telegram', {}).get('token', ''))
        self.telegram_token.grid(row=row, column=0, sticky='w', padx=10, pady=5)
        row += 1
        
        # LINE
        ttk.Label(scrollable_frame, text='LINE Channel Access Token:', font=('', 10, 'bold')).grid(
            row=row, column=0, sticky='w', padx=10, pady=(10, 5)
        )
        row += 1
        self.line_token = ttk.Entry(scrollable_frame, width=50, show='*')
        self.line_token.insert(0, self.config.get('line', {}).get('channel_access_token', ''))
        self.line_token.grid(row=row, column=0, sticky='w', padx=10, pady=5)
        row += 1
        
        ttk.Label(scrollable_frame, text='LINE Channel Secret:', font=('', 10, 'bold')).grid(
            row=row, column=0, sticky='w', padx=10, pady=(10, 5)
        )
        row += 1
        self.line_secret = ttk.Entry(scrollable_frame, width=50, show='*')
        self.line_secret.insert(0, self.config.get('line', {}).get('channel_secret', ''))
        self.line_secret.grid(row=row, column=0, sticky='w', padx=10, pady=5)
        row += 1
        
        # Google Analytics
        ttk.Label(scrollable_frame, text='Google Analytics Property ID:', font=('', 10, 'bold')).grid(
            row=row, column=0, sticky='w', padx=10, pady=(10, 5)
        )
        row += 1
        self.ga_property_id = ttk.Entry(scrollable_frame, width=50)
        self.ga_property_id.insert(0, self.config.get('analytics', {}).get('ga_property_id', ''))
        self.ga_property_id.grid(row=row, column=0, sticky='w', padx=10, pady=5)
        row += 1
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_notification_tab(self, notebook):
        """알림 설정 탭"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text='알림 설정')
        
        # 이메일 설정
        email_frame = ttk.LabelFrame(tab, text='이메일 설정', padding=10)
        email_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(email_frame, text='SMTP 호스트:').grid(row=0, column=0, sticky='w', pady=5)
        self.email_host = ttk.Entry(email_frame, width=40)
        self.email_host.insert(0, self.config.get('email', {}).get('host', 'smtp.gmail.com'))
        self.email_host.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(email_frame, text='포트:').grid(row=1, column=0, sticky='w', pady=5)
        self.email_port = ttk.Entry(email_frame, width=10)
        self.email_port.insert(0, str(self.config.get('email', {}).get('port', 587)))
        self.email_port.grid(row=1, column=1, sticky='w', padx=10, pady=5)
        
        ttk.Label(email_frame, text='사용자:').grid(row=2, column=0, sticky='w', pady=5)
        self.email_user = ttk.Entry(email_frame, width=40)
        self.email_user.insert(0, self.config.get('email', {}).get('user', ''))
        self.email_user.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(email_frame, text='비밀번호:').grid(row=3, column=0, sticky='w', pady=5)
        self.email_password = ttk.Entry(email_frame, width=40, show='*')
        self.email_password.insert(0, self.config.get('email', {}).get('password', ''))
        self.email_password.grid(row=3, column=1, padx=10, pady=5)
        
        # 텔레그램 알림 설정
        telegram_frame = ttk.LabelFrame(tab, text='텔레그램 알림', padding=10)
        telegram_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(telegram_frame, text='채팅 ID (쉼표로 구분):').grid(row=0, column=0, sticky='w', pady=5)
        self.telegram_chat_ids = ttk.Entry(telegram_frame, width=40)
        chat_ids = self.config.get('telegram', {}).get('chat_ids', [])
        self.telegram_chat_ids.insert(0, ','.join(map(str, chat_ids)))
        self.telegram_chat_ids.grid(row=0, column=1, padx=10, pady=5)
    
    def create_general_tab(self, notebook):
        """일반 설정 탭"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text='일반 설정')
        
        # 크롤링 설정
        crawl_frame = ttk.LabelFrame(tab, text='크롤링 설정', padding=10)
        crawl_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(crawl_frame, text='크롤링 주기 (분):').grid(row=0, column=0, sticky='w', pady=5)
        self.crawl_interval = ttk.Entry(crawl_frame, width=10)
        self.crawl_interval.insert(0, str(self.config.get('crawling', {}).get('interval', 60)))
        self.crawl_interval.grid(row=0, column=1, sticky='w', padx=10, pady=5)
        
        # 로그 설정
        log_frame = ttk.LabelFrame(tab, text='로그 설정', padding=10)
        log_frame.pack(fill='x', padx=10, pady=10)
        
        self.enable_logging = tk.BooleanVar(value=self.config.get('logging', {}).get('enabled', True))
        ttk.Checkbutton(
            log_frame,
            text='로깅 활성화',
            variable=self.enable_logging
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        ttk.Label(log_frame, text='로그 레벨:').grid(row=1, column=0, sticky='w', pady=5)
        self.log_level = ttk.Combobox(
            log_frame,
            values=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
            state='readonly',
            width=15
        )
        self.log_level.set(self.config.get('logging', {}).get('level', 'INFO'))
        self.log_level.grid(row=1, column=1, sticky='w', padx=10, pady=5)
    
    def save_settings(self):
        """설정 저장"""
        # API 설정
        self.config['discord'] = {'token': self.discord_token.get()}
        self.config['telegram'] = {'token': self.telegram_token.get()}
        self.config['line'] = {
            'channel_access_token': self.line_token.get(),
            'channel_secret': self.line_secret.get()
        }
        self.config['analytics'] = {'ga_property_id': self.ga_property_id.get()}
        
        # 알림 설정
        self.config['email'] = {
            'host': self.email_host.get(),
            'port': int(self.email_port.get() or 587),
            'user': self.email_user.get(),
            'password': self.email_password.get()
        }
        
        chat_ids_str = self.telegram_chat_ids.get()
        if chat_ids_str:
            self.config['telegram']['chat_ids'] = [
                int(cid.strip()) for cid in chat_ids_str.split(',') if cid.strip()
            ]
        
        # 일반 설정
        self.config['crawling'] = {'interval': int(self.crawl_interval.get() or 60)}
        self.config['logging'] = {
            'enabled': self.enable_logging.get(),
            'level': self.log_level.get()
        }
        
        # 파일에 저장
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo('성공', '설정이 저장되었습니다.')
            self.window.destroy()
        except Exception as e:
            messagebox.showerror('오류', f'설정 저장 실패: {str(e)}')


if __name__ == '__main__':
    # 테스트
    root = tk.Tk()
    root.withdraw()
    
    config = {}
    settings = SettingsWindow(root, config)
    root.mainloop()
