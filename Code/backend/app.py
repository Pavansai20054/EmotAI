import os
import json
import uuid
from datetime import datetime, timezone

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from emotai import AIAgent

# --- Load .env file if present ---
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecret"
CORS(app)

# --- SQLite database setup ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emotiai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- SQLAlchemy Models ---
class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    text = db.Column(db.Text)
    suggestion = db.Column(db.Text)  # JSON: {"emojis":[], "explanation":"", ...}
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)  # 1=bad, 2=ok, 3=good
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

with app.app_context():
    db.create_all()

agent = AIAgent()

def get_user_id():
    if "user_id" not in session:
        user_id = str(uuid.uuid4())
        session["user_id"] = user_id
        if not User.query.get(user_id):
            db.session.add(User(id=user_id))
            db.session.commit()
    return session["user_id"]

@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.get_json()
    message = data.get("message", "")
    user_id = get_user_id()
    suggestion = agent.suggest_emojis(message, username=user_id)
    msg_obj = Message(
        user_id=user_id,
        text=message,
        suggestion=json.dumps(suggestion.dict())
    )
    db.session.add(msg_obj)
    db.session.commit()
    result = suggestion.dict()
    result["created_at"] = msg_obj.created_at.isoformat()
    result["message_id"] = msg_obj.id
    return jsonify(result)

@app.route("/history", methods=["GET"])
def history():
    user_id = get_user_id()
    messages = Message.query.filter_by(user_id=user_id).order_by(Message.created_at.desc()).all()
    history = []
    for msg in messages:
        item = json.loads(msg.suggestion)
        item["message"] = msg.text
        item["created_at"] = msg.created_at.isoformat()
        item["message_id"] = msg.id
        feedback = Feedback.query.filter_by(message_id=msg.id, user_id=user_id).first()
        if feedback:
            item["feedback"] = {"rating": feedback.rating, "comment": feedback.comment}
        history.append(item)
    return jsonify({"history": history})

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    user_id = get_user_id()
    message_id = data.get("message_id")
    rating = data.get("rating")
    comment = data.get("comment", "")
    if not message_id or not rating:
        return jsonify({"error": "message_id and rating required"}), 400
    fb = Feedback.query.filter_by(message_id=message_id, user_id=user_id).first()
    if fb:
        fb.rating = rating
        fb.comment = comment
        fb.created_at = datetime.now(timezone.utc)
    else:
        fb = Feedback(
            message_id=message_id, user_id=user_id,
            rating=rating, comment=comment
        )
        db.session.add(fb)
    db.session.commit()
    return jsonify({"msg": "Feedback recorded"})

@app.route("/analytics", methods=["GET"])
def analytics():
    emoji_counter = {}
    sentiment_counter = {"positive": 0, "negative": 0, "neutral": 0, "other": 0}
    feedback_counter = {1: 0, 2: 0, 3: 0}
    messages = Message.query.all()
    for msg in messages:
        s = json.loads(msg.suggestion)
        for emoji in s.get("emojis", []):
            emoji_counter[emoji] = emoji_counter.get(emoji, 0) + 1
        explanation = s.get("explanation", "")
        if "positive" in explanation:
            sentiment_counter["positive"] += 1
        elif "negative" in explanation:
            sentiment_counter["negative"] += 1
        elif "neutral" in explanation:
            sentiment_counter["neutral"] += 1
        else:
            sentiment_counter["other"] += 1
    for fb in Feedback.query.all():
        feedback_counter[fb.rating] = feedback_counter.get(fb.rating, 0) + 1
    return jsonify({
        "emoji_usage": [{"emoji": k, "count": v} for k, v in emoji_counter.items()],
        "sentiment_stats": sentiment_counter,
        "feedback_stats": feedback_counter,
        "message_count": len(messages)
    })

@app.route("/delete_user_data", methods=["POST"])
def delete_user_data():
    user_id = get_user_id()
    Feedback.query.filter_by(user_id=user_id).delete()
    Message.query.filter_by(user_id=user_id).delete()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    session.pop("user_id", None)
    return jsonify({"msg": "All your data has been deleted."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)