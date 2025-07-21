from Code.backend.emotai import store_suggestion, fetch_user_history, EmojiSuggestion
from Code.backend.db import init_db

def test_store_and_fetch_suggestion():
    init_db()
    username = "testuser"
    msg = "I love this!"
    suggestion = EmojiSuggestion(
        emojis=["❤️"],
        message=msg,
        explanation="Primary sentiment: love (mild)."
    )
    store_suggestion(username, msg, suggestion)
    history = fetch_user_history(username)
    assert any(msg in h["message"] for h in history)
    assert any("❤️" in h["emojis"] for h in history)