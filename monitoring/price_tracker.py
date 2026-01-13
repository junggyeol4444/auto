"""
가격 모니터링 시스템 - 메인 트래커
Price Tracking System
"""
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import os

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('price_tracker.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('price_tracker')


class PriceTracker:
    """가격 추적 메인 클래스"""
    
    def __init__(self, db_path='database/prices.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """데이터베이스 초기화"""
        # 디렉토리 생성
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 상품 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                name TEXT,
                site TEXT,
                target_price REAL,
                alert_enabled INTEGER DEFAULT 1,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # 가격 히스토리 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                price REAL NOT NULL,
                in_stock INTEGER DEFAULT 1,
                timestamp TEXT,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # 알림 설정 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                alert_type TEXT,
                alert_value TEXT,
                enabled INTEGER DEFAULT 1,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info('데이터베이스 초기화 완료')
    
    def add_product(self, url: str, name: str = None, site: str = None, 
                   target_price: float = None) -> int:
        """상품 추가"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        try:
            cursor.execute('''
                INSERT INTO products (url, name, site, target_price, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (url, name, site, target_price, now, now))
            
            product_id = cursor.lastrowid
            conn.commit()
            logger.info(f'상품 추가: {name} (ID: {product_id})')
            return product_id
        
        except sqlite3.IntegrityError:
            logger.warning(f'이미 등록된 상품: {url}')
            cursor.execute('SELECT id FROM products WHERE url = ?', (url,))
            return cursor.fetchone()[0]
        
        finally:
            conn.close()
    
    def update_price(self, product_id: int, price: float, in_stock: bool = True):
        """가격 업데이트"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO price_history (product_id, price, in_stock, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (product_id, price, 1 if in_stock else 0, timestamp))
        
        cursor.execute('''
            UPDATE products SET updated_at = ? WHERE id = ?
        ''', (timestamp, product_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f'가격 업데이트: 상품 {product_id}, 가격 {price}원')
    
    def get_product(self, product_id: int) -> Optional[Dict]:
        """상품 정보 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'url': row[1],
                'name': row[2],
                'site': row[3],
                'target_price': row[4],
                'alert_enabled': bool(row[5]),
                'created_at': row[6],
                'updated_at': row[7]
            }
        return None
    
    def get_all_products(self) -> List[Dict]:
        """모든 상품 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()
        
        conn.close()
        
        products = []
        for row in rows:
            products.append({
                'id': row[0],
                'url': row[1],
                'name': row[2],
                'site': row[3],
                'target_price': row[4],
                'alert_enabled': bool(row[5]),
                'created_at': row[6],
                'updated_at': row[7]
            })
        
        return products
    
    def get_price_history(self, product_id: int, days: int = 30) -> List[Dict]:
        """가격 히스토리 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute('''
            SELECT price, in_stock, timestamp 
            FROM price_history 
            WHERE product_id = ? AND timestamp >= ?
            ORDER BY timestamp ASC
        ''', (product_id, since))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                'price': row[0],
                'in_stock': bool(row[1]),
                'timestamp': row[2]
            })
        
        return history
    
    def get_current_price(self, product_id: int) -> Optional[float]:
        """현재 가격 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT price FROM price_history 
            WHERE product_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''', (product_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else None
    
    def get_price_statistics(self, product_id: int, days: int = 30) -> Dict:
        """가격 통계"""
        history = self.get_price_history(product_id, days)
        
        if not history:
            return {}
        
        prices = [h['price'] for h in history]
        
        return {
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_price': sum(prices) / len(prices),
            'current_price': prices[-1],
            'price_change': prices[-1] - prices[0] if len(prices) > 1 else 0
        }
    
    def check_price_alerts(self) -> List[Dict]:
        """가격 알림 체크"""
        alerts = []
        products = self.get_all_products()
        
        for product in products:
            if not product['alert_enabled'] or not product['target_price']:
                continue
            
            current_price = self.get_current_price(product['id'])
            
            if current_price and current_price <= product['target_price']:
                alerts.append({
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'current_price': current_price,
                    'target_price': product['target_price'],
                    'url': product['url']
                })
                logger.info(f'가격 알림: {product["name"]} - {current_price}원')
        
        return alerts
    
    def delete_product(self, product_id: int):
        """상품 삭제"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM price_history WHERE product_id = ?', (product_id,))
        cursor.execute('DELETE FROM alert_settings WHERE product_id = ?', (product_id,))
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f'상품 삭제: ID {product_id}')
    
    def update_target_price(self, product_id: int, target_price: float):
        """목표가 업데이트"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE products SET target_price = ?, updated_at = ? 
            WHERE id = ?
        ''', (target_price, datetime.now().isoformat(), product_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f'목표가 업데이트: 상품 {product_id}, 목표가 {target_price}원')


if __name__ == '__main__':
    # 테스트
    tracker = PriceTracker()
    print("가격 트래커가 초기화되었습니다.")
