"""
메인 GUI 윈도우
customtkinter 기반 모던 UI
"""

import customtkinter as ctk
from datetime import datetime
import threading


class MainWindow:
    """메인 윈도우 클래스"""
    
    def __init__(self, app_controller):
        """
        초기화
        Args:
            app_controller: 앱 컨트롤러 인스턴스
        """
        self.app = app_controller
        
        # 메인 윈도우 생성
        self.window = ctk.CTk()
        self.window.title("Streamer Automation Suite")
        self.window.geometry("1200x800")
        
        # 테마 설정
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # 탭뷰 생성
        self.tabview = ctk.CTkTabview(self.window)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 탭 추가
        self.tab_dashboard = self.tabview.add("대시보드")
        self.tab_chat = self.tabview.add("채팅 관리")
        self.tab_clip = self.tabview.add("클립 관리")
        self.tab_upload = self.tabview.add("업로드")
        self.tab_settings = self.tabview.add("설정")
        
        # 각 탭 초기화
        self._init_dashboard_tab()
        self._init_chat_tab()
        self._init_clip_tab()
        self._init_upload_tab()
        self._init_settings_tab()
        
        print("[GUI] 메인 윈도우 초기화 완료")
    
    def _init_dashboard_tab(self):
        """대시보드 탭 초기화"""
        # 제목
        title = ctk.CTkLabel(
            self.tab_dashboard,
            text="실시간 모니터링",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        # 통계 프레임
        stats_frame = ctk.CTkFrame(self.tab_dashboard)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # 시청자 수
        self.viewer_label = ctk.CTkLabel(
            stats_frame,
            text="현재 시청자: 0명",
            font=("Arial", 18)
        )
        self.viewer_label.pack(pady=10)
        
        # 채팅 활성도
        self.chat_activity_label = ctk.CTkLabel(
            stats_frame,
            text="채팅 활성도: 0 msg/min",
            font=("Arial", 16)
        )
        self.chat_activity_label.pack(pady=5)
        
        # 하이라이트 목록
        highlight_label = ctk.CTkLabel(
            self.tab_dashboard,
            text="감지된 하이라이트",
            font=("Arial", 18, "bold")
        )
        highlight_label.pack(pady=10)
        
        self.highlight_textbox = ctk.CTkTextbox(
            self.tab_dashboard,
            height=200
        )
        self.highlight_textbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 방송 제어 버튼
        control_frame = ctk.CTkFrame(self.tab_dashboard)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        self.start_button = ctk.CTkButton(
            control_frame,
            text="모니터링 시작",
            command=self.start_monitoring,
            width=150,
            height=40,
            font=("Arial", 14)
        )
        self.start_button.pack(side="left", padx=10, pady=10)
        
        self.stop_button = ctk.CTkButton(
            control_frame,
            text="모니터링 중지",
            command=self.stop_monitoring,
            width=150,
            height=40,
            font=("Arial", 14),
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=10, pady=10)
    
    def _init_chat_tab(self):
        """채팅 관리 탭 초기화"""
        # 제목
        title = ctk.CTkLabel(
            self.tab_chat,
            text="채팅 모더레이션",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        # 설정 프레임
        settings_frame = ctk.CTkFrame(self.tab_chat)
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        # 욕설 필터 토글
        self.profanity_filter_var = ctk.BooleanVar(value=True)
        profanity_switch = ctk.CTkSwitch(
            settings_frame,
            text="욕설 필터",
            variable=self.profanity_filter_var,
            font=("Arial", 14)
        )
        profanity_switch.pack(pady=5, anchor="w", padx=20)
        
        # 스팸 감지 토글
        self.spam_detection_var = ctk.BooleanVar(value=True)
        spam_switch = ctk.CTkSwitch(
            settings_frame,
            text="스팸 감지",
            variable=self.spam_detection_var,
            font=("Arial", 14)
        )
        spam_switch.pack(pady=5, anchor="w", padx=20)
        
        # 번역 토글
        self.translation_var = ctk.BooleanVar(value=True)
        translation_switch = ctk.CTkSwitch(
            settings_frame,
            text="실시간 번역",
            variable=self.translation_var,
            font=("Arial", 14)
        )
        translation_switch.pack(pady=5, anchor="w", padx=20)
        
        # 차단된 메시지 로그
        log_label = ctk.CTkLabel(
            self.tab_chat,
            text="차단된 메시지",
            font=("Arial", 18, "bold")
        )
        log_label.pack(pady=10)
        
        self.blocked_messages_textbox = ctk.CTkTextbox(
            self.tab_chat,
            height=300
        )
        self.blocked_messages_textbox.pack(fill="both", expand=True, padx=20, pady=10)
    
    def _init_clip_tab(self):
        """클립 관리 탭 초기화"""
        # 제목
        title = ctk.CTkLabel(
            self.tab_clip,
            text="클립 & 하이라이트",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        # 감지 설정
        detection_frame = ctk.CTkFrame(self.tab_clip)
        detection_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            detection_frame,
            text="하이라이트 감지 설정",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # 킬 감지
        self.kill_detection_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(
            detection_frame,
            text="킬 감지",
            variable=self.kill_detection_var
        ).pack(pady=5, anchor="w", padx=20)
        
        # 웃음 감지
        self.laugh_detection_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(
            detection_frame,
            text="웃음 감지",
            variable=self.laugh_detection_var
        ).pack(pady=5, anchor="w", padx=20)
        
        # 채팅 폭발 감지
        self.chat_burst_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(
            detection_frame,
            text="채팅 폭발 감지",
            variable=self.chat_burst_var
        ).pack(pady=5, anchor="w", padx=20)
        
        # 클립 목록
        clip_label = ctk.CTkLabel(
            self.tab_clip,
            text="생성된 클립",
            font=("Arial", 18, "bold")
        )
        clip_label.pack(pady=10)
        
        self.clip_listbox = ctk.CTkTextbox(
            self.tab_clip,
            height=250
        )
        self.clip_listbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 클립 생성 버튼
        clip_button = ctk.CTkButton(
            self.tab_clip,
            text="수동 클립 생성",
            command=self.create_manual_clip,
            width=200,
            height=40
        )
        clip_button.pack(pady=10)
    
    def _init_upload_tab(self):
        """업로드 탭 초기화"""
        # 제목
        title = ctk.CTkLabel(
            self.tab_upload,
            text="영상 업로드",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        # 업로드 설정
        upload_frame = ctk.CTkFrame(self.tab_upload)
        upload_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 제목 입력
        ctk.CTkLabel(upload_frame, text="제목:", font=("Arial", 14)).pack(pady=5)
        self.title_entry = ctk.CTkEntry(upload_frame, width=500)
        self.title_entry.pack(pady=5)
        
        # 설명 입력
        ctk.CTkLabel(upload_frame, text="설명:", font=("Arial", 14)).pack(pady=5)
        self.description_textbox = ctk.CTkTextbox(upload_frame, height=150)
        self.description_textbox.pack(pady=5, fill="x", padx=20)
        
        # 업로드 버튼
        button_frame = ctk.CTkFrame(upload_frame)
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="YouTube 업로드",
            command=self.upload_youtube,
            width=150
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="쇼츠 업로드",
            command=self.upload_shorts,
            width=150
        ).pack(side="left", padx=10)
    
    def _init_settings_tab(self):
        """설정 탭 초기화"""
        # 제목
        title = ctk.CTkLabel(
            self.tab_settings,
            text="설정",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        # 설정 프레임
        settings_frame = ctk.CTkFrame(self.tab_settings)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            settings_frame,
            text="Twitch OAuth Token:",
            font=("Arial", 14)
        ).pack(pady=10)
        
        self.twitch_token_entry = ctk.CTkEntry(settings_frame, width=400)
        self.twitch_token_entry.pack(pady=5)
        
        ctk.CTkButton(
            settings_frame,
            text="설정 저장",
            command=self.save_settings,
            width=150
        ).pack(pady=20)
    
    # 이벤트 핸들러
    def start_monitoring(self):
        """모니터링 시작"""
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        print("[GUI] 모니터링 시작됨")
        
        # 별도 스레드에서 앱 시작
        threading.Thread(target=self.app.start, daemon=True).start()
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        print("[GUI] 모니터링 중지됨")
        self.app.stop()
    
    def create_manual_clip(self):
        """수동 클립 생성"""
        print("[GUI] 수동 클립 생성 요청")
    
    def upload_youtube(self):
        """YouTube 업로드"""
        title = self.title_entry.get()
        description = self.description_textbox.get("1.0", "end")
        print(f"[GUI] YouTube 업로드: {title}")
    
    def upload_shorts(self):
        """쇼츠 업로드"""
        print("[GUI] 쇼츠 업로드 요청")
    
    def save_settings(self):
        """설정 저장"""
        print("[GUI] 설정 저장됨")
    
    def update_viewer_count(self, count):
        """시청자 수 업데이트"""
        self.viewer_label.configure(text=f"현재 시청자: {count}명")
    
    def add_highlight_log(self, message):
        """하이라이트 로그 추가"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.highlight_textbox.insert("end", f"[{timestamp}] {message}\n")
    
    def add_blocked_message_log(self, message):
        """차단 메시지 로그 추가"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.blocked_messages_textbox.insert("end", f"[{timestamp}] {message}\n")
    
    def run(self):
        """윈도우 실행"""
        self.window.mainloop()
