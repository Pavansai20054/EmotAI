from .db import get_db

def store_feedback(username, message, feedback, rating):
    db = get_db()
    db.execute(
        "INSERT INTO feedback (username, message, feedback, rating) VALUES (?, ?, ?, ?)",
        (username, message, feedback, rating),
    )
    db.commit()

def get_feedback():
    db = get_db()
    result = db.execute(
        "SELECT username, message, feedback, rating FROM feedback"
    )
    return [
        {
            "username": row[0],
            "message": row[1],
            "feedback": row[2],
            "rating": row[3]
        }
        for row in result.fetchall()
    ]