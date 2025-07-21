import random
import re
from pydantic import BaseModel
from typing import List, Tuple, Optional
from textblob import TextBlob

class EmojiSuggestion(BaseModel):
    emojis: List[str]
    message: str
    explanation: Optional[str] = None
    sentences: Optional[List[dict]] = None  # Per-sentence results

class SentimentAnalyzer:
    def __init__(self):
        self.emoji_library = {
            "happy": {
                "mild": ["😊", "🙂", "😄", "😀"],
                "moderate": ["😃", "😁", "😆"],
                "strong": ["🤩", "🥳", "😻", "🎉", "🎊"],
            },
            "sad": {
                "mild": ["😔", "😞", "🥺", "😟"],
                "moderate": ["😢", "😥", "😭"],
                "strong": ["😩", "😣", "😿", "💔"],
            },
            "love": {
                "mild": ["🥰", "😍", "❤️", "😘"],
                "moderate": ["💖", "💕", "💞", "💓"],
                "strong": ["💘", "💝", "💟"],
            },
            "excited": {
                "mild": ["😎", "😏", "😺", "🤩"],
                "moderate": ["🤩", "🥳", "😻", "🙌"],
                "strong": ["🚀", "🔥", "🎉", "🎊"],
            },
            "greeting": {
                "mild": ["👋", "🤚", "🖐️", "🤝"],
                "moderate": ["✌️", "🤞", "👌", "🤙"],
                "strong": ["🤟", "🖖", "✋", "🙏"],
            },
            "angry": {
                "mild": ["😠", "😒", "😤"],
                "moderate": ["😡", "🤬"],
                "strong": ["👿"],
            },
            "danger": {
                "mild": ["⚠️", "🚨", "🆘", "🛑"],
                "moderate": ["😰", "😨", "😬", "😱"],
                "strong": ["🔥", "💣", "💥"],
            },
            "confused": {
                "mild": ["😕", "🤔", "🧐", "🤷"],
                "moderate": ["😖", "😣", "🤨", "😟"],
                "strong": ["😵", "😓", "🤯", "❓"],
            },
            "neutral": {
                "mild": ["😐", "😑", "😶", "😌"],
                "moderate": ["😒", "🙄", "😏", "😶"],
                "strong": ["🤨", "🧐", "🗿", "🧊"],
            },
            "mixed": {
                "happy_sad": ["😊😢", "😄😔", "🥲"],
                "excited_nervous": ["🤩😬", "😃😅", "😁😰"],
                "love_hate": ["🥰😒", "😍🙄"],
                "angry_confused": ["😡😕", "🤬🤔"],
            },
            "sarcasm": {
                "strong": ["🙃", "😏", "😒"]
            }
        }
        self.sentiment_map = {
            "happy": ["happy", "joy", "good", "great", "awesome", "cheerful"],
            "sad": ["sad", "bad", "upset", "unhappy", "depressed"],
            "love": ["love", "heart", "adore", "cherish"],
            "excited": ["excited", "wow", "amazing", "thrilled"],
            "greeting": ["hello", "hi", "hey", "greetings"],
            "angry": ["angry", "furious", "mad", "irritated"],
            "danger": ["danger", "warning", "alert", "emergency"],
            "confused": ["confused", "why", "huh", "what"],
            "nervous": ["nervous", "anxious", "worried", "apprehensive"],
        }
        self.mixed_patterns = [
            ({"happy", "sad"}, "happy_sad"),
            ({"excited", "nervous"}, "excited_nervous"),
            ({"love", "angry"}, "love_hate"),
            ({"angry", "confused"}, "angry_confused"),
        ]
        self.strong_keywords = {
            "marvelous", "amazing", "wonderful", "terrible", "horrible",
            "furious", "enraged", "urgent",
        }
        self.intensity_words = {
            "slightly": 1, "a little": 1, "very": 2, "really": 2,
            "extremely": 3, "seriously": 3, "so": 2, "completely": 3,
        }
        self.intensity_levels = {1: "mild", 2: "moderate", 3: "strong"}
        self.sentiment_priority = {
            "excited": 1, "love": 2, "happy": 3, "angry": 4, "danger": 5,
            "sad": 6, "nervous": 7, "greeting": 8, "confused": 9, "neutral": 10, "sarcasm": 11,
        }

    def detect_sentiment(self, message: str) -> List[Tuple[str, int]]:
        lower_msg = message.lower()
        words = re.findall(r"\b\w+\b|[^\w\s]", lower_msg)
        sentiment_intensities = {}

        # Sarcasm detection
        if "yeah right" in lower_msg or "as if" in lower_msg or "sure..." in lower_msg:
            sentiment_intensities["sarcasm"] = 3

        # TextBlob polarity
        blob = TextBlob(message)
        polarity = blob.sentiment.polarity
        if polarity > 0.6:
            sentiment_intensities["happy"] = max(sentiment_intensities.get("happy", 0), 3)
        elif polarity > 0.2:
            sentiment_intensities["happy"] = max(sentiment_intensities.get("happy", 0), 2)
        elif polarity < -0.6:
            sentiment_intensities["sad"] = max(sentiment_intensities.get("sad", 0), 3)
        elif polarity < -0.2:
            sentiment_intensities["sad"] = max(sentiment_intensities.get("sad", 0), 2)

        for sent, keywords in self.sentiment_map.items():
            for keyword in keywords:
                if re.search(r"\b" + re.escape(keyword) + r"\b", lower_msg):
                    base_intensity = 3 if keyword in self.strong_keywords else 1
                    if sent not in sentiment_intensities or base_intensity > sentiment_intensities[sent]:
                        sentiment_intensities[sent] = base_intensity

        for sent, current_intensity in list(sentiment_intensities.items()):
            for keyword in self.sentiment_map.get(sent, []):
                keyword_indices = [i for i, word in enumerate(words) if word == keyword]
                for idx in keyword_indices:
                    for i in range(max(0, idx - 3), idx):
                        if words[i] in self.intensity_words:
                            sentiment_intensities[sent] = max(
                                current_intensity, self.intensity_words[words[i]]
                            )

        if "?" in message and "confused" not in sentiment_intensities:
            sentiment_intensities["confused"] = 1

        if not sentiment_intensities:
            sentiment_intensities["neutral"] = 1

        detected_sentiments = sorted(
            sentiment_intensities.items(),
            key=lambda x: self.sentiment_priority.get(x[0], 99),
        )
        return detected_sentiments

    def get_mixed_emotion(self, sentiments: List[Tuple[str, int]]) -> Optional[str]:
        sentiment_set = {s[0] for s in sentiments}
        for pattern, mixed_type in self.mixed_patterns:
            if pattern.issubset(sentiment_set):
                intensities = {s[0]: s[1] for s in sentiments}
                if all(intensities.get(sent, 0) >= 1 for sent in pattern):
                    return mixed_type
        return None

    def get_emojis(self, sentiments: List[Tuple[str, int]], username: Optional[str] = None) -> Tuple[List[str], Optional[str]]:
        if not sentiments:
            neutral_msg = "No sentiment detected, defaulting to neutral."
            return ([random.choice(self.emoji_library["neutral"]["mild"])], neutral_msg)

        mixed_type = self.get_mixed_emotion(sentiments)
        if mixed_type:
            mixed_emojis = self.emoji_library["mixed"].get(mixed_type, [])
            if mixed_emojis:
                explanation = f"Mixed emotions detected: {mixed_type.replace('_', ' + ')}."
                return [random.choice(mixed_emojis)], explanation

        primary_sentiment, primary_intensity = sentiments[0]
        intensity_level = self.intensity_levels.get(primary_intensity, "mild")
        emoji_options = self.emoji_library.get(primary_sentiment, {}).get(
            intensity_level, self.emoji_library["neutral"]["mild"]
        )
        primary_emoji = random.choice(emoji_options)
        secondary_emoji = None
        explanation = f"Primary sentiment: {primary_sentiment} ({intensity_level})."
        if len(sentiments) > 1 and sentiments[1][1] >= 2:
            secondary_sentiment, secondary_intensity = sentiments[1]
            sec_intensity_level = self.intensity_levels.get(
                secondary_intensity, "mild"
            )
            secondary_options = self.emoji_library.get(
                secondary_sentiment, {}
            ).get(sec_intensity_level, [])
            if secondary_options:
                secondary_emoji = random.choice(secondary_options)
                explanation += f" Secondary sentiment: {secondary_sentiment} ({sec_intensity_level})."
        elif len(sentiments) > 1:
            explanation += f" Secondary sentiment ({sentiments[1][0]}) not strong enough for emoji."

        emojis = [primary_emoji]
        if secondary_emoji:
            emojis.append(secondary_emoji)
        return emojis, explanation

class AIAgent:
    def __init__(self):
        self.sentiment = SentimentAnalyzer()

    def suggest_emojis(self, message: str, username: Optional[str] = None) -> EmojiSuggestion:
        # Split message into sentences (simple split, use nltk for better results if you want)
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', message.strip()) if s.strip()]
        sentence_results = []
        all_emojis = []
        explanations = []
        for sent in sentences:
            sentiments = self.sentiment.detect_sentiment(sent)
            emojis, explanation = self.sentiment.get_emojis(sentiments, username)
            # Scale number of emojis with sentence length (1 emoji per 5 words, min 1)
            n_emoji = max(1, len(sent.split()) // 5)
            chosen_emojis = (emojis * ((n_emoji + len(emojis) - 1) // len(emojis)))[:n_emoji]
            all_emojis.extend(chosen_emojis)
            sentence_results.append({
                "sentence": sent,
                "emojis": chosen_emojis,
                "explanation": explanation
            })
            explanations.append(f'"{sent}": {explanation}')
        return EmojiSuggestion(
            emojis=all_emojis,
            message=message,
            explanation="\n".join(explanations),
            sentences=sentence_results
        )