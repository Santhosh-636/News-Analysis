# 📰 Indian News Sentiment Analysis Dashboard

A comprehensive real-time sentiment analysis application for Indian news headlines across multiple languages.

## 🌟 Features

### 1. Live News Scraping
- Scrapes headlines from **9+ major Indian news sources**
- Supports both RSS feeds and direct web scraping
- Coverage of English and Hindi news sources:
  - Times of India
  - NDTV
  - The Hindu
  - Indian Express
  - News18
  - Zee News
  - Hindustan Times
  - Dainik Bhaskar (Hindi)
  - Amar Ujala (Hindi)

### 2. Multi-Language Sentiment Analysis
- **Automatic language detection** for Indian languages
- **Translation support** for non-English headlines
- **Dual sentiment analysis** using:
  - VADER (Valence Aware Dictionary and sEntiment Reasoner)
  - TextBlob
- **6 emotion categories**: Joy, Sadness, Anger, Fear, Surprise, Neutral
- **5 sentiment classifications**: Happy/Positive, Sad/Negative, Neutral, Slightly Positive, Slightly Negative

### 3. Interactive Dashboard
- **Real-time visualization** with Streamlit
- **Auto-refresh** capability (5-minute intervals)
- **Multiple interactive charts**:
  - Sentiment distribution pie chart
  - Emotion analysis bar chart
  - Source-wise sentiment comparison
  - Sentiment score distribution
  - Language distribution
- **Advanced filtering** by sentiment, language, and source
- **Sortable data table** with all analyzed headlines
- **CSV export** functionality
- **Key metrics dashboard** with statistics

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Internet connection (for live scraping)

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data (optional, for enhanced analysis):
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
```

## 💻 Usage

### Running the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

### Individual Components

**Test News Scraper:**
```bash
python news_scraper.py
```

**Test Sentiment Analyzer:**
```bash
python sentiment_analyzer.py
```

## 📊 Dashboard Features Guide

### Main Dashboard
- **Total Headlines**: Number of headlines currently analyzed
- **Positive/Negative/Neutral**: Percentage distribution
- **Average Score**: Overall sentiment trend

### Visualizations
1. **Sentiment Distribution**: Pie chart showing sentiment breakdown
2. **Top Emotions**: Bar chart of detected emotions
3. **Sentiment Score Distribution**: Histogram of compound scores
4. **Language Distribution**: Headlines by language
5. **Source Analysis**: Stacked bar chart of sentiment by news source

### Filters (Sidebar)
- **Sentiment Filter**: Show specific sentiment categories
- **Language Filter**: Filter by language
- **Source Filter**: Select specific news sources

### Data Table
- Sort by score, time, source, or sentiment
- Adjustable number of rows
- Displays emoji indicators for quick visual reference

## 🔧 Customization

### Adding More News Sources

Edit `news_scraper.py` and add to `self.news_sources`:

```python
self.news_sources = {
    'Your Source Name': 'RSS_FEED_URL',
    # ... more sources
}
```

### Custom Emotion Keywords

Edit `sentiment_analyzer.py` in the `self.emotion_keywords` dictionary:

```python
'your_emotion': ['keyword1', 'keyword2', ...],
```

### Adjusting Sentiment Thresholds

Modify the `classify_sentiment` method in `sentiment_analyzer.py`:

```python
def classify_sentiment(self, compound_score: float, polarity: float) -> str:
    avg_score = (compound_score + polarity) / 2
    
    # Adjust these thresholds
    if avg_score >= 0.3:  # More positive
        return 'Happy/Positive'
    # ... etc
```

## 📝 Technical Details

### Architecture
```
┌─────────────────────┐
│  News Sources       │
│  (RSS + Direct)     │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  News Scraper       │
│  (BeautifulSoup,    │
│   Feedparser)       │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  Sentiment Analyzer │
│  (VADER, TextBlob,  │
│   GoogleTrans)      │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  Dashboard          │
│  (Streamlit,        │
│   Plotly)           │
└─────────────────────┘
```

### Sentiment Scoring
- **Compound Score**: -1 (most negative) to +1 (most positive)
- **Polarity**: -1 to +1
- **Subjectivity**: 0 (objective) to 1 (subjective)

### Caching
- Dashboard caches data for 5 minutes to improve performance
- Manual refresh available via sidebar button

## 🛠️ Troubleshooting

### No headlines appearing
- Check internet connection
- Some news sites may block scrapers (use VPN if needed)
- RSS feeds might be temporarily down

### Translation errors
- `googletrans` uses Google Translate API which can be rate-limited
- Consider implementing delays or using alternative translation APIs

### Slow performance
- Reduce number of sources in `news_scraper.py`
- Adjust cache TTL in dashboard (default: 300 seconds)
- Limit number of headlines per source

## 📜 License

This project is for educational purposes. Please respect the terms of service of news websites when scraping.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

## 📧 Support

For issues and questions, please check:
1. Internet connectivity
2. Python package versions
3. News source availability

---

**Built with ❤️ for analyzing Indian news sentiment**
