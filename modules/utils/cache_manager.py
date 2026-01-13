"""Translation cache manager using SQLite"""
import sqlite3
import hashlib
from pathlib import Path
from typing import Optional


class CacheManager:
    """Manage translation cache to avoid redundant API calls"""
    
    def __init__(self, db_path: str = "data/database/translation_cache.db", max_size_mb: int = 100):
        self.db_path = Path(db_path)
        self.max_size_mb = max_size_mb
        self._init_database()
    
    def _init_database(self):
        """Initialize cache database"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text_hash TEXT UNIQUE NOT NULL,
                source_lang TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                engine TEXT NOT NULL,
                original_text TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_hash_langs 
            ON translations(text_hash, source_lang, target_lang, engine)
        ''')
        
        conn.commit()
        conn.close()
    
    def _get_hash(self, text: str, source_lang: str, target_lang: str, engine: str) -> str:
        """Generate hash for cache key"""
        key = f"{text}|{source_lang}|{target_lang}|{engine}"
        return hashlib.sha256(key.encode()).hexdigest()
    
    def get(self, text: str, source_lang: str, target_lang: str, engine: str) -> Optional[str]:
        """
        Get cached translation
        
        Args:
            text: Original text
            source_lang: Source language code
            target_lang: Target language code
            engine: Translation engine name
            
        Returns:
            Cached translation or None
        """
        text_hash = self._get_hash(text, source_lang, target_lang, engine)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT translated_text FROM translations
            WHERE text_hash = ? AND source_lang = ? AND target_lang = ? AND engine = ?
        ''', (text_hash, source_lang, target_lang, engine))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def set(self, text: str, source_lang: str, target_lang: str, engine: str, translation: str):
        """
        Cache translation
        
        Args:
            text: Original text
            source_lang: Source language code
            target_lang: Target language code
            engine: Translation engine name
            translation: Translated text
        """
        text_hash = self._get_hash(text, source_lang, target_lang, engine)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO translations 
                (text_hash, source_lang, target_lang, engine, original_text, translated_text)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (text_hash, source_lang, target_lang, engine, text, translation))
            
            conn.commit()
        except Exception as e:
            print(f"Cache error: {e}")
        finally:
            conn.close()
        
        # Check cache size and clean if needed
        self._check_size()
    
    def _check_size(self):
        """Check cache size and clean old entries if needed"""
        file_size_mb = self.db_path.stat().st_size / (1024 * 1024)
        
        if file_size_mb > self.max_size_mb:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete oldest 20% of entries
            cursor.execute('''
                DELETE FROM translations
                WHERE id IN (
                    SELECT id FROM translations
                    ORDER BY timestamp ASC
                    LIMIT (SELECT COUNT(*) * 0.2 FROM translations)
                )
            ''')
            
            conn.commit()
            conn.close()
            
            # Vacuum to reclaim space
            conn = sqlite3.connect(self.db_path)
            conn.execute('VACUUM')
            conn.close()
    
    def clear(self):
        """Clear all cached translations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM translations')
        conn.commit()
        conn.close()
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM translations')
        count = cursor.fetchone()[0]
        
        conn.close()
        
        file_size_mb = self.db_path.stat().st_size / (1024 * 1024) if self.db_path.exists() else 0
        
        return {
            'entries': count,
            'size_mb': round(file_size_mb, 2)
        }
