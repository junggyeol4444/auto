"""
포인트 시스템 모듈
시청 시간 기반 포인트 지급 및 관리
"""

import json
import sqlite3
from datetime import datetime
from collections import defaultdict


class PointsSystem:
    """포인트 시스템 클래스"""
    
    def __init__(self, config_path="config.json", db_path="data/points.db"):
        """
        초기화
        Args:
            config_path: 설정 파일 경로
            db_path: 데이터베이스 경로
        """
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.points_config = self.config.get('points', {})
        self.enabled = self.points_config.get('enabled', True)
        
        # 데이터베이스 초기화
        self.db_path = db_path
        self._init_database()
        
        # 활성 사용자 추적 (마지막 활동 시간)
        self.active_users = {}
        
        print("[PointsSystem] 초기화 완료")
    
    def _init_database(self):
        """데이터베이스 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 포인트 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS points (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                points INTEGER DEFAULT 0,
                is_subscriber INTEGER DEFAULT 0,
                is_follower INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # 포인트 히스토리 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS point_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                amount INTEGER NOT NULL,
                reason TEXT,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_user_points(self, user_id):
        """
        사용자 포인트 조회
        Args:
            user_id: 사용자 ID
        Returns:
            int: 포인트
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT points FROM points WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        return result[0] if result else 0
    
    def add_points(self, user_id, username, amount, reason=''):
        """
        포인트 추가
        Args:
            user_id: 사용자 ID
            username: 사용자명
            amount: 포인트 양
            reason: 사유
        Returns:
            int: 업데이트된 포인트
        """
        if not self.enabled or amount <= 0:
            return self.get_user_points(user_id)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 사용자 존재 확인
        cursor.execute('SELECT points FROM points WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        current_time = datetime.now().isoformat()
        
        if result:
            # 기존 사용자 - 포인트 추가
            new_points = result[0] + amount
            cursor.execute(
                'UPDATE points SET points = ?, username = ?, updated_at = ? WHERE user_id = ?',
                (new_points, username, current_time, user_id)
            )
        else:
            # 신규 사용자
            new_points = amount
            cursor.execute(
                'INSERT INTO points (user_id, username, points, created_at, updated_at) VALUES (?, ?, ?, ?, ?)',
                (user_id, username, new_points, current_time, current_time)
            )
        
        # 히스토리 저장
        cursor.execute(
            'INSERT INTO point_history (user_id, amount, reason, timestamp) VALUES (?, ?, ?, ?)',
            (user_id, amount, reason, current_time)
        )
        
        conn.commit()
        conn.close()
        
        print(f"[PointsSystem] {username} +{amount} 포인트 (사유: {reason})")
        return new_points
    
    def deduct_points(self, user_id, username, amount, reason=''):
        """
        포인트 차감
        Args:
            user_id: 사용자 ID
            username: 사용자명
            amount: 차감할 포인트
            reason: 사유
        Returns:
            tuple: (성공 여부, 업데이트된 포인트)
        """
        current_points = self.get_user_points(user_id)
        
        if current_points < amount:
            return False, current_points
        
        return True, self.add_points(user_id, username, -amount, reason)
    
    def award_watch_time_points(self, user_id, username, minutes, is_subscriber=False, is_follower=False):
        """
        시청 시간에 따른 포인트 지급
        Args:
            user_id: 사용자 ID
            username: 사용자명
            minutes: 시청 시간 (분)
            is_subscriber: 구독자 여부
            is_follower: 팔로워 여부
        Returns:
            int: 지급된 포인트
        """
        base_points = self.points_config.get('points_per_minute', 10) * minutes
        
        # 보너스 적용
        multiplier = 1.0
        if is_subscriber:
            multiplier *= self.points_config.get('bonus_subscriber', 2.0)
        elif is_follower:
            multiplier *= self.points_config.get('bonus_follower', 1.5)
        
        points_to_award = int(base_points * multiplier)
        
        # 포인트 지급
        self.add_points(user_id, username, points_to_award, f'시청 시간 {minutes}분')
        
        # 상태 업데이트
        self._update_user_status(user_id, is_subscriber, is_follower)
        
        return points_to_award
    
    def _update_user_status(self, user_id, is_subscriber, is_follower):
        """사용자 상태 업데이트"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE points SET is_subscriber = ?, is_follower = ? WHERE user_id = ?',
            (1 if is_subscriber else 0, 1 if is_follower else 0, user_id)
        )
        
        conn.commit()
        conn.close()
    
    def get_leaderboard(self, limit=10):
        """
        포인트 리더보드
        Args:
            limit: 순위 수
        Returns:
            list: 리더보드
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT username, points FROM points ORDER BY points DESC LIMIT ?',
            (limit,)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        return [{'rank': i+1, 'username': row[0], 'points': row[1]} for i, row in enumerate(results)]
    
    def get_user_rank(self, user_id):
        """
        사용자 순위 조회
        Args:
            user_id: 사용자 ID
        Returns:
            int: 순위
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT COUNT(*) + 1 FROM points WHERE points > (SELECT points FROM points WHERE user_id = ?)',
            (user_id,)
        )
        
        rank = cursor.fetchone()[0]
        conn.close()
        
        return rank
    
    def reset_all_points(self):
        """모든 포인트 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE points SET points = 0')
        cursor.execute('DELETE FROM point_history')
        
        conn.commit()
        conn.close()
        
        print("[PointsSystem] 모든 포인트 초기화됨")
    
    def export_points(self, filepath):
        """
        포인트 데이터 내보내기
        Args:
            filepath: 저장할 파일 경로
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM points ORDER BY points DESC')
        results = cursor.fetchall()
        
        conn.close()
        
        # JSON으로 저장
        data = [
            {
                'user_id': row[0],
                'username': row[1],
                'points': row[2],
                'is_subscriber': bool(row[3]),
                'is_follower': bool(row[4]),
                'created_at': row[5],
                'updated_at': row[6]
            }
            for row in results
        ]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"[PointsSystem] 포인트 데이터 저장됨: {filepath}")
