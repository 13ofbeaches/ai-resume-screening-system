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


def insert_candidate(name, email, phone, location, s3_url, skills):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidates (
        name, email, phone, location, s3_url, skills, status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, email, phone, location, s3_url, skills, "pending"))

    conn.commit()

    candidate_id = cursor.lastrowid

    conn.close()

    return candidate_id


def update_candidate_category(candidate_id, category):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE candidates
    SET category = ?, status = ?
    WHERE id = ?
    """, (category, "processed", candidate_id))

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

    return result[0] if result else None


def get_all_candidates():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # 🔥 makes rows behave like dictionaries
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name, email, phone, location, s3_url, skills, category, status
    FROM candidates
    """)

    rows = cursor.fetchall()
    conn.close()

    # Convert sqlite Row objects to real dictionaries
    return [dict(row) for row in rows]