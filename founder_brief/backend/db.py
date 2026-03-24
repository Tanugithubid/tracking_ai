
import os
import json
import sqlite3
from datetime import datetime

# Driver for PostgreSQL
try:
    import psycopg2
    from psycopg2 import pool
except ImportError:
    psycopg2 = None

DATABASE_URL = os.environ.get("DATABASE_URL")
DB_PATH = "founder_brief.db"

# Connection Helper
def get_connection():
    if DATABASE_URL:
        # Connect to Supabase/PostgreSQL
        return psycopg2.connect(DATABASE_URL)
    else:
        # Fallback to local SQLite
        conn = sqlite3.connect(DB_PATH)
        return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tables for SQLite/Postgres compatibility
    # Postgres uses 'SERIAL' or 'SERIAL PRIMARY KEY'
    # SQLite uses 'INTEGER PRIMARY KEY AUTOINCREMENT'
    # We will use simple SQL that mostly works on both or handle specifically
    
    is_postgres = True if DATABASE_URL else False
    id_type = "SERIAL PRIMARY KEY" if is_postgres else "INTEGER PRIMARY KEY AUTOINCREMENT"
    text_type = "TEXT" # Works on both
    timestamp_type = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS thoughts (
            id {id_type},
            raw_input {text_type},
            mini_insight {text_type},
            full_brief {text_type},
            created_at {timestamp_type}
        )
    """)
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS journal (
            id {id_type},
            content {text_type},
            created_at {timestamp_type}
        )
    """)
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS daybreak (
            id {id_type},
            content_json {text_type},
            day_string VARCHAR(20) UNIQUE,
            created_at {timestamp_type}
        )
    """)
    
    conn.commit()
    conn.close()

def save_thought(raw, mini, full_json):
    conn = get_connection()
    cursor = conn.cursor()
    # Postgres uses %s placeholders, SQLite uses ?
    placeholder = "%s" if DATABASE_URL else "?"
    cursor.execute(f"INSERT INTO thoughts (raw_input, mini_insight, full_brief) VALUES ({placeholder}, {placeholder}, {placeholder})", (raw, mini, full_json))
    conn.commit()
    conn.close()

def save_journal(content):
    conn = get_connection()
    cursor = conn.cursor()
    placeholder = "%s" if DATABASE_URL else "?"
    cursor.execute(f"INSERT INTO journal (content) VALUES ({placeholder})", (content,))
    conn.commit()
    conn.close()

def save_daybreak(json_data, day_str):
    conn = get_connection()
    cursor = conn.cursor()
    if DATABASE_URL:
        # Upsert logic for Postgres
        cursor.execute("""
            INSERT INTO daybreak (content_json, day_string) VALUES (%s, %s)
            ON CONFLICT (day_string) DO UPDATE SET content_json = EXCLUDED.content_json
        """, (json_data, day_str))
    else:
        # Upsert logic for SQLite
        cursor.execute("INSERT OR REPLACE INTO daybreak (content_json, day_string) VALUES (?, ?)", (json_data, day_str))
    conn.commit()
    conn.close()

def get_today_daybreak(day_str):
    conn = get_connection()
    cursor = conn.cursor()
    placeholder = "%s" if DATABASE_URL else "?"
    cursor.execute(f"SELECT content_json FROM daybreak WHERE day_string = {placeholder}", (day_str,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_all_daybreaks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT content_json, day_string FROM daybreak ORDER BY day_string DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_thoughts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM thoughts ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_journal():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT content, created_at FROM journal ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Always call init on import to ensure the vault is ready
init_db()
