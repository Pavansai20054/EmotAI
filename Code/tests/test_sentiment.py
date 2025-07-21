from Code.backend.emotai import SentimentAnalyzer

def test_happy_sentiment():
    analyzer = SentimentAnalyzer()
    sentiments = analyzer.detect_sentiment("I am so happy today!")
    assert sentiments[0][0] == "happy"

def test_sad_sentiment():
    analyzer = SentimentAnalyzer()
    sentiments = analyzer.detect_sentiment("I feel really sad.")
    assert sentiments[0][0] == "sad"

def test_mixed_emotion():
    analyzer = SentimentAnalyzer()
    sentiments = analyzer.detect_sentiment("I'm happy but also a bit sad.")
    mixed = analyzer.get_mixed_emotion(sentiments)
    assert mixed == "happy_sad"