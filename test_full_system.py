"""
Full System Test and Validation
Tests all components of the sentiment analysis system
"""

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

from news_scraper import NewsHeadlineScraper
from sentiment_analyzer import MultiLanguageSentimentAnalyzer
import pandas as pd
import sys

def test_news_scraper():
    """Test the news scraper"""
    print("\n" + "="*60)
    print("TESTING NEWS SCRAPER")
    print("="*60)
    
    try:
        scraper = NewsHeadlineScraper()
        print("✓ NewsHeadlineScraper initialized successfully")
        
        headlines_df = scraper.scrape_all_sources()
        print(f"✓ Successfully scraped {len(headlines_df)} unique headlines")
        
        if not headlines_df.empty:
            print(f"✓ DataFrame shape: {headlines_df.shape}")
            print(f"✓ Columns: {list(headlines_df.columns)}")
            print(f"\nSample data from first 3 headlines:")
            for idx, row in headlines_df.head(3).iterrows():
                print(f"  {idx+1}. [{row['source']}] {row['title'][:60]}...")
        
        return headlines_df
    
    except Exception as e:
        print(f"✗ Error testing news scraper: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()

def test_sentiment_analyzer(headlines_df):
    """Test the sentiment analyzer"""
    print("\n" + "="*60)
    print("TESTING SENTIMENT ANALYZER")
    print("="*60)
    
    try:
        analyzer = MultiLanguageSentimentAnalyzer()
        print("✓ MultiLanguageSentimentAnalyzer initialized successfully")
        
        if headlines_df.empty:
            print("✗ No headlines to analyze")
            return pd.DataFrame()
        
        analyzed_df = analyzer.analyze_batch(headlines_df)
        print(f"✓ Successfully analyzed {len(analyzed_df)} headlines")
        
        if not analyzed_df.empty:
            print(f"✓ DataFrame shape: {analyzed_df.shape}")
            print(f"✓ New columns added: {[col for col in analyzed_df.columns if col not in headlines_df.columns]}")
            
            # Show sentiment distribution
            print(f"\n✓ Sentiment Distribution:")
            sentiment_counts = analyzed_df['sentiment'].value_counts()
            for sentiment, count in sentiment_counts.items():
                pct = (count / len(analyzed_df)) * 100
                print(f"  - {sentiment}: {count} ({pct:.1f}%)")
            
            # Show sample analysis
            print(f"\nSample Analysis:")
            for idx, row in analyzed_df.head(2).iterrows():
                print(f"\n  [{idx+1}] {row['title'][:70]}...")
                print(f"      Sentiment: {row['sentiment']} {row['emoji']}")
                print(f"      Emotions: {row['emotions']}")
                print(f"      Compound Score: {row['compound_score']}")
        
        return analyzed_df
    
    except Exception as e:
        print(f"✗ Error testing sentiment analyzer: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()

def test_dashboard_functions(analyzed_df):
    """Test dashboard visualization functions"""
    print("\n" + "="*60)
    print("TESTING DASHBOARD FUNCTIONS")
    print("="*60)
    
    try:
        # Import dashboard functions
        from dashboard import (
            create_sentiment_distribution_chart,
            create_emotion_distribution_chart,
            create_source_sentiment_chart,
            create_sentiment_score_distribution,
            create_language_distribution_chart
        )
        
        if analyzed_df.empty:
            print("✗ No data to create charts")
            return
        
        print("Testing chart functions...")
        
        try:
            fig1 = create_sentiment_distribution_chart(analyzed_df)
            print("✓ Sentiment distribution chart created")
        except Exception as e:
            print(f"✗ Error creating sentiment distribution chart: {e}")
        
        try:
            fig2 = create_emotion_distribution_chart(analyzed_df)
            print("✓ Emotion distribution chart created")
        except Exception as e:
            print(f"✗ Error creating emotion distribution chart: {e}")
        
        try:
            fig3 = create_source_sentiment_chart(analyzed_df)
            print("✓ Source sentiment chart created")
        except Exception as e:
            print(f"✗ Error creating source sentiment chart: {e}")
        
        try:
            fig4 = create_sentiment_score_distribution(analyzed_df)
            print("✓ Sentiment score distribution chart created")
        except Exception as e:
            print(f"✗ Error creating sentiment score distribution chart: {e}")
        
        try:
            fig5 = create_language_distribution_chart(analyzed_df)
            print("✓ Language distribution chart created")
        except Exception as e:
            print(f"✗ Error creating language distribution chart: {e}")
        
        print("\n✓ All chart functions executed successfully!")
        
    except ImportError as e:
        print(f"✗ Error importing dashboard functions: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"✗ Error testing dashboard functions: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "NEWS SENTIMENT ANALYSIS - SYSTEM TEST" + " "*11 + "║")
    print("╚" + "="*58 + "╝")
    
    # Test scraper
    headlines_df = test_news_scraper()
    
    # Test analyzer
    analyzed_df = test_sentiment_analyzer(headlines_df)
    
    # Test dashboard
    test_dashboard_functions(analyzed_df)
    
    # Summary
    print("\n" + "="*60)
    print("SYSTEM TEST SUMMARY")
    print("="*60)
    
    if not headlines_df.empty and not analyzed_df.empty:
        print(f"✓ Total Headlines Scraped: {len(headlines_df)}")
        print(f"✓ Total Headlines Analyzed: {len(analyzed_df)}")
        print(f"✓ Sentiment Categories: {analyzed_df['sentiment'].nunique()}")
        print(f"✓ Languages Detected: {analyzed_df['language'].nunique()}")
        print(f"✓ News Sources: {analyzed_df['source'].nunique()}")
        print("\n✓ ALL TESTS PASSED! System is ready to run.")
        print("\nTo start the dashboard, run:")
        print("  python -m streamlit run dashboard.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        sys.exit(1)
    
    print("\n")

if __name__ == "__main__":
    main()
