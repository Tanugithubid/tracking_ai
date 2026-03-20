
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
        CREATE TABLE IF NOT EXISTS mastery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_input TEXT,
            corrected_output TEXT,
            stanford_rating INTEGER,
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

def get_all_thoughts():
    if not os.path.exists(DB_PATH):
        init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM thoughts ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Always call init on import to ensure the vault is ready
init_db()
