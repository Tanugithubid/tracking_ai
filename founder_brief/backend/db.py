
import sqlite3
from datetime import datetime
import os

DB_PATH = "founder_brief.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS thoughts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_input TEXT,
            mini_insight TEXT,
            full_brief TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daybreak (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_json TEXT,
            day_string TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_thought(raw, mini, full_json):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO thoughts (raw_input, mini_insight, full_brief) VALUES (?, ?, ?)", (raw, mini, full_json))
    conn.commit()
    conn.close()

def save_journal(content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO journal (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()

def save_daybreak(json_data, day_str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO daybreak (content_json, day_string) VALUES (?, ?)", (json_data, day_str))
    conn.commit()
    conn.close()

def get_today_daybreak(day_str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content_json FROM daybreak WHERE day_string = ?", (day_str,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_all_daybreaks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content_json, day_string FROM daybreak ORDER BY day_string DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_thoughts():
    if not os.path.exists(DB_PATH):
        init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM thoughts ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_journal():
    if not os.path.exists(DB_PATH):
        init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content, created_at FROM journal ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Always call init on import to ensure the vault is ready
init_db()
