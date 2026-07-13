import sqlite3

DATABASE_PATH = "database/chat.db"


def get_connection():
    return sqlite3.connect(
        DATABASE_PATH,
        timeout=10,
        check_same_thread=False
    )

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_conversation(
    session_id: str,
    question: str,
    answer: str
):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO conversations (
                session_id,
                question,
                answer
            )
            VALUES (?, ?, ?)
        """, (
            session_id,
            question,
            answer
        ))

        conn.commit()

    finally:
        conn.close()

def get_conversation_history(session_id: str, limit: int = 5):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT question, answer
            FROM conversations
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (session_id, limit),
        )

        rows = cursor.fetchall()
        rows.reverse()

        return rows

    finally:
        conn.close()