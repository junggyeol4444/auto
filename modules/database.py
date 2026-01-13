import sqlite3
import json
from datetime import datetime

class DatabaseHandler:
    def __init__(self, db_name="creative_writing.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize database with necessary tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                content TEXT
            )
        ''')
        
        # Characters table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                name TEXT NOT NULL,
                gender TEXT,
                age INTEGER,
                personality TEXT,
                appearance TEXT,
                background TEXT,
                abilities TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        ''')
        
        # Worldbuilding table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS worldbuilding (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                category TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_project(self, name, project_type, content):
        """Save a new project"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projects (name, type, content, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (name, project_type, json.dumps(content), datetime.now()))
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return project_id
    
    def update_project(self, project_id, content):
        """Update existing project"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE projects SET content = ?, updated_at = ?
            WHERE id = ?
        ''', (json.dumps(content), datetime.now(), project_id))
        conn.commit()
        conn.close()
    
    def get_projects(self):
        """Get all projects"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, type, created_at, updated_at FROM projects ORDER BY updated_at DESC')
        projects = cursor.fetchall()
        conn.close()
        return projects
    
    def get_project(self, project_id):
        """Get a specific project"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        project = cursor.fetchone()
        conn.close()
        return project
    
    def save_character(self, project_id, character_data):
        """Save a character"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO characters 
            (project_id, name, gender, age, personality, appearance, background, abilities)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_id,
            character_data.get('name', ''),
            character_data.get('gender', ''),
            character_data.get('age', 0),
            json.dumps(character_data.get('personality', {})),
            character_data.get('appearance', ''),
            character_data.get('background', ''),
            json.dumps(character_data.get('abilities', []))
        ))
        character_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return character_id
    
    def get_characters(self, project_id=None):
        """Get characters for a project or all characters"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        if project_id:
            cursor.execute('SELECT * FROM characters WHERE project_id = ?', (project_id,))
        else:
            cursor.execute('SELECT * FROM characters')
        characters = cursor.fetchall()
        conn.close()
        return characters
