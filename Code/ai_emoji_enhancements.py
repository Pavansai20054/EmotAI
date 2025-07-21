"""
🚀 AI Emoji Enhancement Features
Advanced AI-powered emoji suggestion improvements for EmotAI

This module contains enhanced AI features for better emoji suggestions:
- Multi-modal emotion detection
- Context-aware emoji clustering
- Personalized emoji recommendations
- Advanced sentiment intensity analysis
"""

import json
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmotionContext:
    """Enhanced emotion context with multiple dimensions"""
    primary_emotion: str
    secondary_emotions: List[str]
    intensity: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    cultural_context: str
    temporal_context: str  # time-based context
    user_personality: Dict[str, float]

@dataclass
class EmojiSuggestion:
    """Enhanced emoji suggestion with metadata"""
    emoji: str
    relevance_score: float
    emotion_match: str
    cultural_appropriateness: float
    usage_frequency: float
    explanation: str

class AdvancedEmojiAnalyzer:
    """
    🧠 Advanced AI-powered emoji analyzer with enhanced features
    """
    
    def __init__(self):
        self.emotion_clusters = self._initialize_emotion_clusters()
        self.cultural_mappings = self._initialize_cultural_mappings()
        self.personality_weights = self._initialize_personality_weights()
        
    def _initialize_emotion_clusters(self) -> Dict[str, List[str]]:
        """Initialize advanced emotion clustering"""
        return {
            "joy_cluster": ["😊", "😄", "🎉", "✨", "🌟", "🥳", "😁", "🤗"],
            "love_cluster": ["❤️", "💕", "💖", "😍", "🥰", "💝", "💘", "💗"],
            "excitement_cluster": ["🚀", "⚡", "🔥", "💥", "🎯", "🌈", "🎊", "🎈"],
            "gratitude_cluster": ["🙏", "💝", "🤝", "👏", "🌺", "🌸", "💐", "🎁"],
            "sadness_cluster": ["😢", "😭", "💔", "😞", "😔", "🥺", "😿", "💧"],
            "anger_cluster": ["😠", "😡", "🤬", "💢", "🔥", "⚡", "👿", "😤"],
            "surprise_cluster": ["😲", "😱", "🤯", "😮", "🙀", "😯", "🤩", "✨"],
            "fear_cluster": ["😨", "😰", "😱", "🙈", "😬", "😟", "😧", "💀"]
        }
    
    def _initialize_cultural_mappings(self) -> Dict[str, Dict[str, float]]:
        """Initialize cultural appropriateness mappings"""
        return {
            "professional": {
                "😊": 0.9, "👍": 0.95, "🙏": 0.9, "✅": 0.95,
                "🎉": 0.7, "💪": 0.8, "🚀": 0.85, "⭐": 0.9
            },
            "casual": {
                "😂": 0.95, "🤣": 0.9, "😎": 0.85, "🔥": 0.9,
                "💯": 0.85, "🤪": 0.8, "🥳": 0.9, "✨": 0.85
            },
            "formal": {
                "😊": 0.8, "🙏": 0.9, "👍": 0.85, "✅": 0.9,
                "📝": 0.95, "📊": 0.9, "💼": 0.85, "🤝": 0.9
            }
        }
    
    def _initialize_personality_weights(self) -> Dict[str, Dict[str, float]]:
        """Initialize personality-based emoji weights"""
        return {
            "extrovert": {"🎉": 1.2, "🥳": 1.3, "😄": 1.1, "🚀": 1.2},
            "introvert": {"😊": 1.2, "🙏": 1.1, "💭": 1.3, "📚": 1.2},
            "optimistic": {"✨": 1.3, "🌟": 1.2, "🌈": 1.2, "☀️": 1.1},
            "analytical": {"🤔": 1.3, "📊": 1.2, "🔍": 1.2, "💡": 1.1}
        }

    def analyze_enhanced_emotion(self, text: str, user_context: Optional[Dict] = None) -> EmotionContext:
        """
        🎯 Enhanced emotion analysis with multi-dimensional context
        """
        # Simulate advanced emotion detection
        emotions = self._detect_multi_emotions(text)
        intensity = self._calculate_intensity(text, emotions)
        confidence = self._calculate_confidence(text, emotions)
        
        # Get user context
        user_personality = user_context.get('personality', {}) if user_context else {}
        cultural_context = user_context.get('culture', 'casual') if user_context else 'casual'
        
        return EmotionContext(
            primary_emotion=emotions[0] if emotions else 'neutral',
            secondary_emotions=emotions[1:3] if len(emotions) > 1 else [],
            intensity=intensity,
            confidence=confidence,
            cultural_context=cultural_context,
            temporal_context=self._get_temporal_context(),
            user_personality=user_personality
        )
    
    def _detect_multi_emotions(self, text: str) -> List[str]:
        """Detect multiple emotions in text"""
        # Simplified emotion detection (in real implementation, use advanced NLP)
        emotion_keywords = {
            'joy': ['happy', 'excited', 'great', 'awesome', 'wonderful', 'amazing'],
            'love': ['love', 'adore', 'cherish', 'heart', 'dear', 'sweet'],
            'sadness': ['sad', 'disappointed', 'upset', 'down', 'blue', 'crying'],
            'anger': ['angry', 'mad', 'furious', 'annoyed', 'frustrated', 'rage'],
            'surprise': ['wow', 'amazing', 'incredible', 'unbelievable', 'shocking'],
            'fear': ['scared', 'afraid', 'worried', 'nervous', 'anxious', 'terrified']
        }
        
        detected_emotions = []
        text_lower = text.lower()
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_emotions.append(emotion)
        
        return detected_emotions or ['neutral']
    
    def _calculate_intensity(self, text: str, emotions: List[str]) -> float:
        """Calculate emotional intensity"""
        # Intensity indicators
        intensity_words = ['very', 'extremely', 'super', 'really', 'so', 'totally']
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        exclamation_count = text.count('!')
        
        base_intensity = 0.5
        if any(word in text.lower() for word in intensity_words):
            base_intensity += 0.2
        if caps_ratio > 0.3:
            base_intensity += 0.2
        if exclamation_count > 0:
            base_intensity += min(exclamation_count * 0.1, 0.3)
            
        return min(base_intensity, 1.0)
    
    def _calculate_confidence(self, text: str, emotions: List[str]) -> float:
        """Calculate confidence in emotion detection"""
        # Simple confidence calculation based on text length and emotion clarity
        base_confidence = 0.7
        if len(text) > 50:
            base_confidence += 0.1
        if len(emotions) == 1:
            base_confidence += 0.1
        return min(base_confidence, 1.0)
    
    def _get_temporal_context(self) -> str:
        """Get time-based context"""
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 17:
            return 'afternoon'
        elif 17 <= hour < 21:
            return 'evening'
        else:
            return 'night'

    def generate_enhanced_suggestions(self, emotion_context: EmotionContext, limit: int = 10) -> List[EmojiSuggestion]:
        """
        ✨ Generate enhanced emoji suggestions with advanced scoring
        """
        suggestions = []
        
        # Get relevant emoji clusters
        primary_cluster = self.emotion_clusters.get(f"{emotion_context.primary_emotion}_cluster", [])
        
        # Score each emoji
        for emoji in primary_cluster[:limit]:
            relevance_score = self._calculate_relevance_score(emoji, emotion_context)
            cultural_score = self._get_cultural_appropriateness(emoji, emotion_context.cultural_context)
            
            suggestion = EmojiSuggestion(
                emoji=emoji,
                relevance_score=relevance_score,
                emotion_match=emotion_context.primary_emotion,
                cultural_appropriateness=cultural_score,
                usage_frequency=0.8,  # Placeholder
                explanation=f"Matches {emotion_context.primary_emotion} with {relevance_score:.1%} relevance"
            )
            suggestions.append(suggestion)
        
        # Sort by relevance score
        suggestions.sort(key=lambda x: x.relevance_score, reverse=True)
        return suggestions[:limit]
    
    def _calculate_relevance_score(self, emoji: str, context: EmotionContext) -> float:
        """Calculate emoji relevance score"""
        base_score = 0.7
        
        # Intensity matching
        if context.intensity > 0.8:
            base_score += 0.1
        
        # Personality matching
        for trait, weight in context.user_personality.items():
            if trait in self.personality_weights and emoji in self.personality_weights[trait]:
                base_score *= self.personality_weights[trait][emoji]
        
        # Confidence adjustment
        base_score *= context.confidence
        
        return min(base_score, 1.0)
    
    def _get_cultural_appropriateness(self, emoji: str, cultural_context: str) -> float:
        """Get cultural appropriateness score"""
        if cultural_context in self.cultural_mappings:
            return self.cultural_mappings[cultural_context].get(emoji, 0.5)
        return 0.7  # Default score

class PersonalizedEmojiRecommender:
    """
    🎯 Personalized emoji recommendation system
    """
    
    def __init__(self):
        self.user_preferences = {}
        self.usage_history = {}
        
    def learn_from_feedback(self, user_id: str, emoji: str, rating: int, context: str):
        """Learn from user feedback to improve recommendations"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        
        if emoji not in self.user_preferences[user_id]:
            self.user_preferences[user_id][emoji] = {'total_rating': 0, 'count': 0}
        
        self.user_preferences[user_id][emoji]['total_rating'] += rating
        self.user_preferences[user_id][emoji]['count'] += 1
        
        logger.info(f"Updated preferences for user {user_id}: {emoji} -> {rating}")
    
    def get_personalized_suggestions(self, user_id: str, base_suggestions: List[EmojiSuggestion]) -> List[EmojiSuggestion]:
        """Get personalized emoji suggestions based on user history"""
        if user_id not in self.user_preferences:
            return base_suggestions
        
        user_prefs = self.user_preferences[user_id]
        
        # Adjust scores based on user preferences
        for suggestion in base_suggestions:
            if suggestion.emoji in user_prefs:
                pref_data = user_prefs[suggestion.emoji]
                avg_rating = pref_data['total_rating'] / pref_data['count']
                # Adjust relevance score based on user preference (1-5 scale to 0.2-1.0 multiplier)
                multiplier = 0.2 + (avg_rating - 1) * 0.2
                suggestion.relevance_score *= multiplier
        
        # Re-sort by adjusted scores
        base_suggestions.sort(key=lambda x: x.relevance_score, reverse=True)
        return base_suggestions

# Example usage and testing
if __name__ == "__main__":
    # Initialize the enhanced analyzer
    analyzer = AdvancedEmojiAnalyzer()
    recommender = PersonalizedEmojiRecommender()
    
    # Test enhanced emotion analysis
    test_messages = [
        "I'm so excited about this new project! It's going to be amazing!",
        "Feeling a bit sad today, missing my family",
        "Thank you so much for your help, really appreciate it",
        "This is absolutely incredible! I can't believe it!"
    ]
    
    print("🚀 AI Emoji Enhancement Demo")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test Message {i}: '{message}'")
        
        # Analyze emotion with context
        user_context = {
            'personality': {'extrovert': 0.8, 'optimistic': 0.9},
            'culture': 'casual'
        }
        
        emotion_context = analyzer.analyze_enhanced_emotion(message, user_context)
        
        print(f"🎭 Primary Emotion: {emotion_context.primary_emotion}")
        print(f"📊 Intensity: {emotion_context.intensity:.2f}")
        print(f"🎯 Confidence: {emotion_context.confidence:.2f}")
        
        # Generate enhanced suggestions
        suggestions = analyzer.generate_enhanced_suggestions(emotion_context, limit=5)
        
        print("✨ Enhanced Emoji Suggestions:")
        for j, suggestion in enumerate(suggestions, 1):
            print(f"  {j}. {suggestion.emoji} (Score: {suggestion.relevance_score:.2f}) - {suggestion.explanation}")
    
    print("\n🎉 AI Emoji Enhancement Demo Complete!")