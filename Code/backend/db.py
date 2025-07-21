import sqlite3
from contextlib import contextmanager
from pathlib import Path
import threading

DB_PATH = Path(__file__).parent / "instance" / "emotiai.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
_connection_lock = threading.Lock()

@contextmanager
def get_db():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                message TEXT,
                emojis TEXT,
                explanation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS emoji_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                emoji TEXT,
                sentiment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                message TEXT,
                feedback TEXT,
                rating INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                emoji TEXT,
                usage_count INTEGER DEFAULT 1,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        db.commit()

def store_suggestion(username, message, suggestion):
    with get_db() as db:
        db.execute(
            "INSERT INTO suggestions (username, message, emojis, explanation) VALUES (?, ?, ?, ?)",
            (
                username,
                message,
                ",".join(suggestion.emojis),
                suggestion.explanation or "",
            ),
        )
        db.commit()
        # Update user preferences
        for emoji in suggestion.emojis:
            db.execute("""
                INSERT INTO user_preferences (username, emoji, usage_count, last_used)
                VALUES (?, ?, 1, CURRENT_TIMESTAMP)
                ON CONFLICT(username, emoji) DO UPDATE SET
                  usage_count = usage_count + 1,
                  last_used = CURRENT_TIMESTAMP
            """, (username, emoji))
        db.commit()

def fetch_user_history(username):
    with get_db() as db:
        rows = db.execute(
            "SELECT message, emojis, explanation, created_at FROM suggestions WHERE username=? ORDER BY created_at DESC LIMIT 20",
            (username,),
        ).fetchall()
        return [
            {
                "message": row["message"],
                "emojis": row["emojis"].split(","),
                "explanation": row["explanation"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]

def record_emoji_usage(username, emoji, sentiment):
    with get_db() as db:
        db.execute(
            "INSERT INTO emoji_analytics (username, emoji, sentiment) VALUES (?, ?, ?)",
            (username, emoji, sentiment),
        )
        db.commit()

def get_usage_stats():
    with get_db() as db:
        rows = db.execute(
            "SELECT emoji, COUNT(*) as count FROM emoji_analytics GROUP BY emoji ORDER BY count DESC"
        ).fetchall()
        return [{"emoji": row["emoji"], "count": row["count"]} for row in rows]

def store_feedback(username, message, feedback, rating):
    with get_db() as db:
        db.execute(
            "INSERT INTO feedback (username, message, feedback, rating) VALUES (?, ?, ?, ?)",
            (username, message, feedback, rating),
        )
        db.commit()

def get_feedback():
    with get_db() as db:
        rows = db.execute(
            "SELECT username, message, feedback, rating, created_at FROM feedback ORDER BY created_at DESC"
        ).fetchall()
        return [
            {
                "username": row["username"],
                "message": row["message"],
                "feedback": row["feedback"],
                "rating": row["rating"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]

def fetch_user_preferences(username):
    with get_db() as db:
        rows = db.execute(
            "SELECT emoji FROM user_preferences WHERE username=? ORDER BY usage_count DESC, last_used DESC LIMIT 5",
            (username,),
        ).fetchall()
        return [row["emoji"] for row in rows]