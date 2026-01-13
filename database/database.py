"""
Database Module
Manages post history and scheduling database
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, List


class Database:
    """Database manager for post history"""
    
    def __init__(self, db_path: str = 'database/posts.db'):
        self.db_path = db_path
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                content_path TEXT,
                caption TEXT,
                hashtags TEXT,
                post_url TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                published_at TIMESTAMP,
                error_message TEXT
            )
        ''')
        
        # Scheduled posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platforms TEXT NOT NULL,
                content_path TEXT NOT NULL,
                caption TEXT,
                hashtags TEXT,
                scheduled_time TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP
            )
        ''')
        
        # Platform accounts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS platform_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT UNIQUE NOT NULL,
                username TEXT,
                enabled INTEGER DEFAULT 0,
                last_used TIMESTAMP,
                post_count INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_post(self, platform: str, content_path: str, caption: str,
                 hashtags: str, post_url: str = None, status: str = 'success') -> int:
        """Add a post record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO posts (platform, content_path, caption, hashtags, post_url, status, published_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (platform, content_path, caption, hashtags, post_url, status, datetime.now()))
        
        post_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return post_id
    
    def add_scheduled_post(self, platforms: List[str], content_path: str,
                          caption: str, hashtags: str, scheduled_time: datetime) -> int:
        """Add a scheduled post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        platforms_str = json.dumps(platforms)
        
        cursor.execute('''
            INSERT INTO scheduled_posts (platforms, content_path, caption, hashtags, scheduled_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (platforms_str, content_path, caption, hashtags, scheduled_time))
        
        post_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return post_id
    
    def get_pending_scheduled_posts(self) -> List[Dict]:
        """Get pending scheduled posts that are ready to publish"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, platforms, content_path, caption, hashtags, scheduled_time
            FROM scheduled_posts
            WHERE status = 'pending' AND scheduled_time <= ?
        ''', (datetime.now(),))
        
        rows = cursor.fetchall()
        conn.close()
        
        posts = []
        for row in rows:
            posts.append({
                'id': row[0],
                'platforms': json.loads(row[1]),
                'content_path': row[2],
                'caption': row[3],
                'hashtags': row[4],
                'scheduled_time': row[5]
            })
        
        return posts
    
    def update_scheduled_post_status(self, post_id: int, status: str):
        """Update scheduled post status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE scheduled_posts
            SET status = ?, processed_at = ?
            WHERE id = ?
        ''', (status, datetime.now(), post_id))
        
        conn.commit()
        conn.close()
    
    def get_post_history(self, platform: str = None, limit: int = 50) -> List[Dict]:
        """Get post history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if platform:
            cursor.execute('''
                SELECT id, platform, content_path, caption, status, published_at, post_url
                FROM posts
                WHERE platform = ?
                ORDER BY published_at DESC
                LIMIT ?
            ''', (platform, limit))
        else:
            cursor.execute('''
                SELECT id, platform, content_path, caption, status, published_at, post_url
                FROM posts
                ORDER BY published_at DESC
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        posts = []
        for row in rows:
            posts.append({
                'id': row[0],
                'platform': row[1],
                'content_path': row[2],
                'caption': row[3],
                'status': row[4],
                'published_at': row[5],
                'post_url': row[6]
            })
        
        return posts
    
    def get_statistics(self) -> Dict:
        """Get posting statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total posts
        cursor.execute('SELECT COUNT(*) FROM posts')
        total_posts = cursor.fetchone()[0]
        
        # Successful posts
        cursor.execute("SELECT COUNT(*) FROM posts WHERE status = 'success'")
        successful_posts = cursor.fetchone()[0]
        
        # Failed posts
        cursor.execute("SELECT COUNT(*) FROM posts WHERE status = 'failed'")
        failed_posts = cursor.fetchone()[0]
        
        # Posts by platform
        cursor.execute('SELECT platform, COUNT(*) FROM posts GROUP BY platform')
        by_platform = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Scheduled posts
        cursor.execute("SELECT COUNT(*) FROM scheduled_posts WHERE status = 'pending'")
        scheduled_posts = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_posts': total_posts,
            'successful_posts': successful_posts,
            'failed_posts': failed_posts,
            'by_platform': by_platform,
            'scheduled_posts': scheduled_posts
        }
    
    def update_platform_account(self, platform: str, username: str, enabled: bool):
        """Update platform account info"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO platform_accounts (platform, username, enabled, last_used)
            VALUES (?, ?, ?, ?)
        ''', (platform, username, 1 if enabled else 0, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def increment_post_count(self, platform: str):
        """Increment post count for platform"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE platform_accounts
            SET post_count = post_count + 1, last_used = ?
            WHERE platform = ?
        ''', (datetime.now(), platform))
        
        conn.commit()
        conn.close()
