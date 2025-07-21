from .db import get_db

def record_emoji_usage(username, emoji, sentiment):
    db = get_db()
    db.execute(
        "INSERT INTO emoji_analytics (username, emoji, sentiment) VALUES (?, ?, ?)",
        (username, emoji, sentiment),
    )
    db.commit()

def get_usage_stats():
    db = get_db()
    result = db.execute(
        "SELECT emoji, COUNT(*) as count FROM emoji_analytics GROUP BY emoji ORDER BY count DESC"
    )
    return [{"emoji": row[0], "count": row[1]} for row in result.fetchall()]