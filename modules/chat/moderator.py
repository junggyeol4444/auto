"""
채팅 모더레이션 모듈
욕설 필터, 스팸 감지, 자동 타임아웃/밴 기능
"""

import re
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
import json
import os


class ChatModerator:
    """채팅 모더레이션 클래스"""
    
    def __init__(self, config_path="config.json", badwords_path="data/badwords.txt"):
        """
        초기화
        Args:
            config_path: 설정 파일 경로
            badwords_path: 금지어 파일 경로
        """
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.moderation_config = self.config.get('moderation', {})
        
        # 금지어 목록 로드
        self.badwords = self._load_badwords(badwords_path)
        
        # 사용자별 경고 카운트
        self.user_warnings = defaultdict(int)
        
        # 사용자별 메시지 히스토리 (스팸 감지용)
        self.user_messages = defaultdict(lambda: deque(maxlen=100))
        
        # 차단된 메시지 로그
        self.blocked_messages = []
        
        # 타임아웃/밴된 사용자
        self.timed_out_users = {}
        self.banned_users = set()
        
        print("[ChatModerator] 초기화 완료")
    
    def _load_badwords(self, path):
        """
        금지어 목록 로드
        Args:
            path: 금지어 파일 경로
        Returns:
            list: 금지어 목록
        """
        if not os.path.exists(path):
            print(f"[Warning] 금지어 파일을 찾을 수 없습니다: {path}")
            return []
        
        with open(path, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"[ChatModerator] {len(words)}개의 금지어 로드됨")
        return words
    
    def check_profanity(self, message):
        """
        욕설 검사
        Args:
            message: 검사할 메시지
        Returns:
            tuple: (욕설 포함 여부, 감지된 욕설 목록)
        """
        if not self.moderation_config.get('enable_profanity_filter', True):
            return False, []
        
        message_lower = message.lower()
        detected = []
        
        for word in self.badwords:
            # 정규식으로 변형 감지
            pattern = re.escape(word)
            # 특수문자/공백 사이에 있어도 감지
            pattern = pattern.replace(r'\ ', r'[\s\*\-_]*')
            
            if re.search(pattern, message_lower, re.IGNORECASE):
                detected.append(word)
        
        return len(detected) > 0, detected
    
    def check_spam(self, user_id, message):
        """
        스팸 검사
        Args:
            user_id: 사용자 ID
            message: 메시지
        Returns:
            tuple: (스팸 여부, 스팸 타입)
        """
        if not self.moderation_config.get('enable_spam_detection', True):
            return False, None
        
        current_time = time.time()
        user_msgs = self.user_messages[user_id]
        
        # 메시지 히스토리에 추가
        user_msgs.append({
            'message': message,
            'time': current_time
        })
        
        # 시간 윈도우 내의 메시지만 필터링
        time_window = self.moderation_config.get('spam_time_window', 60)
        recent_msgs = [m for m in user_msgs if current_time - m['time'] <= time_window]
        
        # 1. 동일 메시지 반복
        spam_threshold = self.moderation_config.get('spam_message_threshold', 5)
        same_message_count = sum(1 for m in recent_msgs if m['message'] == message)
        if same_message_count >= spam_threshold:
            return True, "동일 메시지 반복"
        
        # 2. 초당 메시지 수
        if len(recent_msgs) >= spam_threshold * 2:
            return True, "과도한 메시지 속도"
        
        # 3. 링크 스팸
        link_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        links = re.findall(link_pattern, message)
        link_limit = self.moderation_config.get('link_limit', 3)
        if len(links) >= link_limit:
            return True, "과도한 링크"
        
        return False, None
    
    def moderate_message(self, user_id, username, message):
        """
        메시지 모더레이션 처리
        Args:
            user_id: 사용자 ID
            username: 사용자명
            message: 메시지
        Returns:
            dict: 모더레이션 결과
        """
        result = {
            'allowed': True,
            'action': None,
            'reason': None,
            'warnings': 0
        }
        
        # 이미 밴된 사용자
        if user_id in self.banned_users:
            result['allowed'] = False
            result['action'] = 'banned'
            result['reason'] = '밴된 사용자'
            return result
        
        # 타임아웃 확인
        if user_id in self.timed_out_users:
            timeout_until = self.timed_out_users[user_id]
            if datetime.now() < timeout_until:
                result['allowed'] = False
                result['action'] = 'timeout'
                result['reason'] = f'타임아웃 중 (해제: {timeout_until.strftime("%H:%M:%S")})'
                return result
            else:
                # 타임아웃 해제
                del self.timed_out_users[user_id]
        
        # 욕설 검사
        has_profanity, detected_words = self.check_profanity(message)
        if has_profanity:
            result['allowed'] = False
            result['reason'] = f'욕설 감지: {", ".join(detected_words[:3])}'
            self._apply_warning(user_id, username, result)
            return result
        
        # 스팸 검사
        is_spam, spam_type = self.check_spam(user_id, message)
        if is_spam:
            result['allowed'] = False
            result['reason'] = f'스팸 감지: {spam_type}'
            self._apply_warning(user_id, username, result)
            return result
        
        return result
    
    def _apply_warning(self, user_id, username, result):
        """
        경고 적용 및 처벌 결정
        Args:
            user_id: 사용자 ID
            username: 사용자명
            result: 결과 딕셔너리 (수정됨)
        """
        self.user_warnings[user_id] += 1
        warnings = self.user_warnings[user_id]
        result['warnings'] = warnings
        
        warning_threshold = self.moderation_config.get('warning_threshold', 3)
        ban_threshold = self.moderation_config.get('ban_threshold', 5)
        timeout_duration = self.moderation_config.get('timeout_duration', 600)
        
        if warnings >= ban_threshold:
            # 영구 밴
            self.banned_users.add(user_id)
            result['action'] = 'ban'
            print(f"[ChatModerator] {username} 영구 밴 (경고 {warnings}회)")
            
        elif warnings >= warning_threshold:
            # 타임아웃
            timeout_until = datetime.now() + timedelta(seconds=timeout_duration)
            self.timed_out_users[user_id] = timeout_until
            result['action'] = 'timeout'
            result['timeout_duration'] = timeout_duration
            print(f"[ChatModerator] {username} 타임아웃 {timeout_duration}초 (경고 {warnings}회)")
            
        else:
            # 경고만
            result['action'] = 'warning'
            print(f"[ChatModerator] {username} 경고 {warnings}회")
        
        # 로그 저장
        self.blocked_messages.append({
            'time': datetime.now().isoformat(),
            'user_id': user_id,
            'username': username,
            'action': result['action'],
            'reason': result['reason'],
            'warnings': warnings
        })
    
    def add_badword(self, word):
        """금지어 추가"""
        if word not in self.badwords:
            self.badwords.append(word)
            print(f"[ChatModerator] 금지어 추가: {word}")
    
    def remove_badword(self, word):
        """금지어 제거"""
        if word in self.badwords:
            self.badwords.remove(word)
            print(f"[ChatModerator] 금지어 제거: {word}")
    
    def unban_user(self, user_id):
        """사용자 밴 해제"""
        if user_id in self.banned_users:
            self.banned_users.remove(user_id)
            self.user_warnings[user_id] = 0
            print(f"[ChatModerator] 사용자 밴 해제: {user_id}")
    
    def reset_warnings(self, user_id):
        """사용자 경고 초기화"""
        self.user_warnings[user_id] = 0
        print(f"[ChatModerator] 경고 초기화: {user_id}")
    
    def get_stats(self):
        """통계 조회"""
        return {
            'total_warnings': sum(self.user_warnings.values()),
            'users_with_warnings': len(self.user_warnings),
            'banned_users': len(self.banned_users),
            'timed_out_users': len(self.timed_out_users),
            'blocked_messages': len(self.blocked_messages)
        }
