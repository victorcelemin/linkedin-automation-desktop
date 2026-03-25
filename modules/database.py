"""
Database Module - SQLite Database Management
"""

import sqlite3
import os
from datetime import datetime
import json


class Database:
    """SQLite Database Manager"""
    
    def __init__(self, db_path='data/linkedin_automation.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                tone TEXT,
                style TEXT,
                word_count INTEGER,
                hashtags TEXT,
                image_url TEXT,
                image_query TEXT,
                status TEXT DEFAULT 'GENERATED',
                scheduled_time TEXT,
                published_time TEXT,
                linkedin_post_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_post(self, content_data, image_url=None, status='GENERATED', 
                  scheduled_time=None):
        """Save a post to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        hashtags = json.dumps(content_data.get('hashtags', []))
        
        cursor.execute('''
            INSERT INTO posts (content, tone, style, word_count, hashtags,
                             image_url, image_query, status, scheduled_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            content_data.get('content', ''),
            content_data.get('tone', ''),
            content_data.get('style', ''),
            content_data.get('wordCount', 0),
            hashtags,
            image_url,
            content_data.get('image_query', ''),
            status,
            scheduled_time
        ))
        
        post_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return post_id
    
    def get_posts(self, status=None, limit=50):
        """Get posts from database"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT * FROM posts WHERE status = ?
                ORDER BY created_at DESC LIMIT ?
            ''', (status, limit))
        else:
            cursor.execute('''
                SELECT * FROM posts
                ORDER BY created_at DESC LIMIT ?
            ''', (limit,))
        
        posts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        # Parse hashtags
        for post in posts:
            if post.get('hashtags'):
                try:
                    post['hashtags'] = json.loads(post['hashtags'])
                except:
                    post['hashtags'] = []
        
        return posts
    
    def get_recent_posts(self, limit=5):
        """Get recent posts"""
        return self.get_posts(limit=limit)
    
    def update_post_status(self, post_id, status, linkedin_post_id=None):
        """Update post status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if status == 'PUBLISHED':
            cursor.execute('''
                UPDATE posts 
                SET status = ?, published_time = ?, linkedin_post_id = ?, updated_at = ?
                WHERE id = ?
            ''', (status, datetime.now().isoformat(), linkedin_post_id, 
                  datetime.now().isoformat(), post_id))
        else:
            cursor.execute('''
                UPDATE posts 
                SET status = ?, updated_at = ?
                WHERE id = ?
            ''', (status, datetime.now().isoformat(), post_id))
        
        conn.commit()
        conn.close()
    
    def delete_post(self, post_id):
        """Delete a post"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """Get statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total posts
        cursor.execute('SELECT COUNT(*) FROM posts')
        stats['total'] = cursor.fetchone()[0]
        
        # By status
        for status in ['GENERATED', 'SCHEDULED', 'PUBLISHED', 'FAILED']:
            cursor.execute('SELECT COUNT(*) FROM posts WHERE status = ?', (status,))
            stats[status.lower()] = cursor.fetchone()[0]
        
        # This week
        week_ago = (datetime.now() - __import__('datetime').timedelta(days=7)).isoformat()
        cursor.execute('SELECT COUNT(*) FROM posts WHERE published_time >= ?', (week_ago,))
        stats['published_this_week'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def save_setting(self, key, value):
        """Save a setting"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value, updated_at)
            VALUES (?, ?, ?)
        ''', (key, json.dumps(value), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_setting(self, key, default=None):
        """Get a setting"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            try:
                return json.loads(result[0])
            except:
                return result[0]
        return default