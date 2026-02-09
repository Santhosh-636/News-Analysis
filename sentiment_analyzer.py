"""
Multi-language Sentiment Analysis Engine
Supports Indian languages with advanced sentiment classification
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import re

# Try to import translator, but make it optional
try:
    from googletrans import Translator
    TRANSLATOR_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    TRANSLATOR_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Translation library not available. Will analyze in original language.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultiLanguageSentimentAnalyzer:
    """Analyzes sentiment of news headlines across multiple languages"""
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.translator = Translator() if TRANSLATOR_AVAILABLE else None
        
        # Enhanced emotion keywords for Indian context
        self.emotion_keywords = {
            'joy': ['win', 'victory', 'celebration', 'success', 'achievement', 
                   'happy', 'joy', 'delight', 'triumph', 'champion', 'award',
                   'festival', 'wedding', 'birth', 'growth', 'profit'],
            
            'sadness': ['death', 'dead', 'died', 'loss', 'tragedy', 'accident',
                       'crash', 'collapse', 'fail', 'victim', 'mourning', 'grief',
                       'crisis', 'recession', 'layoff', 'unemployment'],
            
            'anger': ['protest', 'clash', 'violence', 'attack', 'rage', 'fury',
                     'outrage', 'riot', 'strike', 'controversy', 'scandal',
                     'corruption', 'fraud', 'scam', 'betrayal'],
            
            'fear': ['threat', 'danger', 'warning', 'alert', 'terror', 'panic',
                    'crisis', 'emergency', 'disaster', 'epidemic', 'disease',
                    'concern', 'worry', 'anxiety', 'risk'],
            
            'surprise': ['shock', 'stunned', 'unexpected', 'sudden', 'amazing',
                        'astonishing', 'dramatic', 'breakthrough', 'revelation',
                        'unprecedented', 'historic'],
            
            'neutral': ['meeting', 'conference', 'discussion', 'announce',
                       'report', 'statement', 'plan', 'project', 'visit', 'review']
        }
        
    def translate_to_english(self, text: str, detected_lang: str) -> str:
        """Translate non-English text to English"""
        # If translator is not available or language is English, return original
        if not self.translator or detected_lang == 'English' or detected_lang == 'Unknown':
            return text
        
        try:
            translation = self.translator.translate(text, dest='en')
            return translation.text
        except Exception as e:
            logger.warning(f"Translation error: {e}. Using original text.")
            return text
    
    def analyze_vader_sentiment(self, text: str) -> Dict:
        """Analyze sentiment using VADER"""
        scores = self.vader_analyzer.polarity_scores(text)
        return {
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'compound': scores['compound']
        }
    
    def analyze_textblob_sentiment(self, text: str) -> Dict:
        """Analyze sentiment using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            return {
                'polarity': polarity,
                'subjectivity': subjectivity
            }
        except:
            return {'polarity': 0, 'subjectivity': 0}
    
    def detect_emotions(self, text: str) -> List[str]:
        """Detect specific emotions based on keywords"""
        text_lower = text.lower()
        detected_emotions = []
        
        for emotion, keywords in self.emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_emotions.append(emotion)
        
        return detected_emotions if detected_emotions else ['neutral']
    
    def classify_sentiment(self, compound_score: float, polarity: float) -> str:
        """Classify overall sentiment"""
        # Combined scoring approach
        avg_score = (compound_score + polarity) / 2
        
        if avg_score >= 0.3:
            return 'Happy/Positive'
        elif avg_score <= -0.3:
            return 'Sad/Negative'
        elif avg_score > 0.05:
            return 'Slightly Positive'
        elif avg_score < -0.05:
            return 'Slightly Negative'
        else:
            return 'Neutral'
    
    def get_sentiment_emoji(self, sentiment: str) -> str:
        """Get emoji representation of sentiment"""
        emoji_map = {
            'Happy/Positive': '😊',
            'Sad/Negative': '😢',
            'Neutral': '😐',
            'Slightly Positive': '🙂',
            'Slightly Negative': '😕'
        }
        return emoji_map.get(sentiment, '😐')
    
    def analyze_headline(self, headline: str, language: str = 'English') -> Dict:
        """Comprehensive sentiment analysis of a single headline"""
        
        # Translate if needed
        english_text = self.translate_to_english(headline, language)
        
        # Get VADER sentiment
        vader_scores = self.analyze_vader_sentiment(english_text)
        
        # Get TextBlob sentiment
        textblob_scores = self.analyze_textblob_sentiment(english_text)
        
        # Detect emotions
        emotions = self.detect_emotions(english_text)
        
        # Classify overall sentiment
        sentiment_class = self.classify_sentiment(
            vader_scores['compound'], 
            textblob_scores['polarity']
        )
        
        # Get emoji
        emoji = self.get_sentiment_emoji(sentiment_class)
        
        return {
            'original_headline': headline,
            'english_translation': english_text,
            'language': language,
            'sentiment': sentiment_class,
            'emoji': emoji,
            'compound_score': round(vader_scores['compound'], 3),
            'polarity': round(textblob_scores['polarity'], 3),
            'subjectivity': round(textblob_scores['subjectivity'], 3),
            'emotions': ', '.join(emotions),
            'positive_score': round(vader_scores['positive'], 3),
            'negative_score': round(vader_scores['negative'], 3),
            'neutral_score': round(vader_scores['neutral'], 3)
        }
    
    def analyze_batch(self, headlines_df: pd.DataFrame) -> pd.DataFrame:
        """Analyze sentiment for a batch of headlines"""
        logger.info(f"Analyzing sentiment for {len(headlines_df)} headlines...")
        
        results = []
        for idx, row in headlines_df.iterrows():
            try:
                analysis = self.analyze_headline(
                    row['title'], 
                    row.get('language', 'English')
                )
                
                # Merge with original data
                result = {**row.to_dict(), **analysis}
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error analyzing headline: {e}")
                continue
        
        analyzed_df = pd.DataFrame(results)
        logger.info("Sentiment analysis complete!")
        
        return analyzed_df


if __name__ == "__main__":
    # Test the analyzer
    analyzer = MultiLanguageSentimentAnalyzer()
    
    test_headlines = [
        "India wins Cricket World Cup",
        "Tragic accident claims 20 lives",
        "Stock market reaches all-time high",
        "Government announces new policy"
    ]
    
    for headline in test_headlines:
        result = analyzer.analyze_headline(headline)
        print(f"\nHeadline: {headline}")
        print(f"Sentiment: {result['sentiment']} {result['emoji']}")
        print(f"Emotions: {result['emotions']}")
