"""
SQLite Database Manager
데이터 저장 및 조회 관리
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any
import os


class DatabaseManager:
    def __init__(self, db_path: str = "data/prices.db"):
        """데이터베이스 매니저 초기화"""
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """데이터베이스 연결 생성"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """데이터베이스 테이블 초기화"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 암호화폐 가격 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                price REAL NOT NULL,
                volume REAL,
                market_cap REAL,
                change_24h REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 환율 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS forex_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency_pair TEXT NOT NULL,
                rate REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 부동산 실거래가 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS real_estate_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region TEXT NOT NULL,
                dong TEXT,
                apartment_name TEXT,
                area REAL,
                price INTEGER,
                floor INTEGER,
                built_year INTEGER,
                deal_date TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 주식 가격 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                name TEXT,
                price REAL NOT NULL,
                volume INTEGER,
                change_pct REAL,
                market TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 경제 지표 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS economic_indicators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                indicator_name TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT,
                country TEXT,
                date TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 알림 로그 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alert_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT NOT NULL,
                target TEXT NOT NULL,
                message TEXT,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def insert_crypto_price(self, symbol: str, price: float, volume: float = None, 
                           market_cap: float = None, change_24h: float = None):
        """암호화폐 가격 저장"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO crypto_prices (symbol, price, volume, market_cap, change_24h)
            VALUES (?, ?, ?, ?, ?)
        """, (symbol, price, volume, market_cap, change_24h))
        conn.commit()
        conn.close()
    
    def get_crypto_prices(self, symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
        """암호화폐 가격 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM crypto_prices 
            WHERE symbol = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (symbol, limit))
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def insert_forex_rate(self, currency_pair: str, rate: float):
        """환율 저장"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO forex_rates (currency_pair, rate)
            VALUES (?, ?)
        """, (currency_pair, rate))
        conn.commit()
        conn.close()
    
    def get_forex_rates(self, currency_pair: str, limit: int = 100) -> List[Dict[str, Any]]:
        """환율 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM forex_rates 
            WHERE currency_pair = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (currency_pair, limit))
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def insert_real_estate_price(self, region: str, dong: str, apartment_name: str,
                                 area: float, price: int, floor: int = None,
                                 built_year: int = None, deal_date: str = None):
        """부동산 실거래가 저장"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO real_estate_prices 
            (region, dong, apartment_name, area, price, floor, built_year, deal_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (region, dong, apartment_name, area, price, floor, built_year, deal_date))
        conn.commit()
        conn.close()
    
    def get_real_estate_prices(self, region: str, limit: int = 100) -> List[Dict[str, Any]]:
        """부동산 실거래가 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM real_estate_prices 
            WHERE region = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (region, limit))
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def insert_stock_price(self, symbol: str, name: str, price: float, 
                          volume: int = None, change_pct: float = None, 
                          market: str = "KR"):
        """주식 가격 저장"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO stock_prices (symbol, name, price, volume, change_pct, market)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (symbol, name, price, volume, change_pct, market))
        conn.commit()
        conn.close()
    
    def get_stock_prices(self, symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
        """주식 가격 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM stock_prices 
            WHERE symbol = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (symbol, limit))
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def insert_economic_indicator(self, indicator_name: str, value: float,
                                  unit: str = None, country: str = "KR",
                                  date: str = None):
        """경제 지표 저장"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO economic_indicators 
            (indicator_name, value, unit, country, date)
            VALUES (?, ?, ?, ?, ?)
        """, (indicator_name, value, unit, country, date))
        conn.commit()
        conn.close()
    
    def get_economic_indicators(self, indicator_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """경제 지표 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM economic_indicators 
            WHERE indicator_name = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (indicator_name, limit))
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def log_alert(self, alert_type: str, target: str, message: str, status: str = "sent"):
        """알림 로그 저장"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alert_logs (alert_type, target, message, status)
            VALUES (?, ?, ?, ?)
        """, (alert_type, target, message, status))
        conn.commit()
        conn.close()
    
    def get_alert_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """알림 로그 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM alert_logs 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results
