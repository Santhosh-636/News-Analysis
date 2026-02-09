"""
Quick test script to verify the sentiment analysis system
"""

from news_scraper import NewsHeadlineScraper
from sentiment_analyzer import MultiLanguageSentimentAnalyzer
import pandas as pd

def test_system():
    print("=" * 70)
    print("TESTING INDIAN NEWS SENTIMENT ANALYSIS SYSTEM")
    print("=" * 70)
    
    # Test 1: News Scraper
    print("\n[1/2] Testing News Scraper...")
    print("-" * 70)
    
    scraper = NewsHeadlineScraper()
    headlines_df = scraper.scrape_all_sources()
    
    if not headlines_df.empty:
        print(f"✓ Successfully scraped {len(headlines_df)} headlines")
        print(f"✓ Sources: {headlines_df['source'].nunique()}")
        print(f"✓ Languages detected: {headlines_df['language'].unique().tolist()}")
        print("\nSample headlines:")
        for idx, row in headlines_df.head(3).iterrows():
            print(f"  • {row['title'][:80]}... [{row['source']}]")
    else:
        print("✗ No headlines scraped. Check internet connection.")
        return False
    
    # Test 2: Sentiment Analyzer
    print("\n[2/2] Testing Sentiment Analyzer...")
    print("-" * 70)
    
    analyzer = MultiLanguageSentimentAnalyzer()
    analyzed_df = analyzer.analyze_batch(headlines_df.head(5))
    
    if not analyzed_df.empty:
        print(f"✓ Successfully analyzed {len(analyzed_df)} headlines")
        print("\nSentiment Analysis Results:")
        for idx, row in analyzed_df.iterrows():
            print(f"\n  {row['emoji']} {row['title'][:60]}...")
            print(f"     Sentiment: {row['sentiment']}")
            print(f"     Emotions: {row['emotions']}")
            print(f"     Score: {row['compound_score']}")
    else:
        print("✗ Sentiment analysis failed")
        return False
    
    print("\n" + "=" * 70)
    print("✓ ALL TESTS PASSED!")
    print("=" * 70)
    print("\n🚀 Ready to launch dashboard!")
    print("   Run: streamlit run dashboard.py")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    test_system()
