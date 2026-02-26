import sqlite3

DB_NAME = "candidates.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Candidates table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        location TEXT,
        s3_url TEXT,
        skills TEXT,
        category TEXT,
        status TEXT DEFAULT 'pending'
    )
    """)

    # Prompts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prompts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT UNIQUE,
        content TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_candidate(name, email, phone, location, s3_url):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidates (name, email, phone, location, s3_url)
    VALUES (?, ?, ?, ?, ?)
    """, (name, email, phone, location, s3_url))

    conn.commit()
    conn.close()


def update_prompt(prompt_type, content):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO prompts (type, content)
    VALUES (?, ?)
    ON CONFLICT(type)
    DO UPDATE SET content=excluded.content
    """, (prompt_type, content))

    conn.commit()
    conn.close()


def get_prompt(prompt_type):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT content FROM prompts WHERE type=?
    """, (prompt_type,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None