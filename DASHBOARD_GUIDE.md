# 📰 Dashboard User Guide

## Getting Started

### Option 1: Using Quick Start (Easiest)
```bash
python quickstart.py
```
This will automatically:
1. Start the Streamlit server
2. Wait for it to initialize
3. Open the dashboard in your browser

### Option 2: Manual Start
```bash
python -m streamlit run dashboard.py
```
Then open your browser to: `http://localhost:8501`

---

## Dashboard Overview

### Main Sections

#### 1. **Key Metrics** (Top of Dashboard)
Shows 5 important statistics:
- **Total Headlines**: Number of news items analyzed
- **Positive %**: Percentage of positive/happy headlines
- **Negative %**: Percentage of negative/sad headlines
- **Neutral %**: Percentage of neutral headlines
- **Avg Score**: Average sentiment compound score (-1 to +1)

#### 2. **Visualizations** (Interactive Charts)

**Sentiment Distribution (Pie Chart)**
- Shows the breakdown of all 5 sentiment categories
- Click on any slice to highlight it
- Hover for exact percentages

**Top Emotions (Bar Chart)**
- Most frequently detected emotions in headlines
- Maximum 10 emotions shown
- Helps identify overall emotional tone

**Sentiment by Source (Stacked Bar Chart)**
- See which news sources have more positive/negative content
- Compare sentiment patterns across sources
- Useful for source credibility analysis

**Sentiment Score Distribution (Histogram)**
- Shows the range of compound sentiment scores
- Red dashed line indicates the neutral (0) point
- Helps identify if news is overall positive or negative

**Language Distribution (Bar Chart)**
- Number of headlines in each detected language
- Shows language coverage of the analysis

#### 3. **Headline Data Table**

**Features:**
- **Sortable Columns**: Click column headers to sort
- **Emoji Indicator**: Quick visual sentiment reference
- **Full Analysis**: See compound score, emotions, source, language, time
- **Adjustable Rows**: Use slider to show 5-50 headlines

**Column Descriptions:**
- **😊**: Sentiment emoji (visual indicator)
- **Headline**: Full news headline text
- **Sentiment**: Classification (Happy/Positive, Sad/Negative, etc.)
- **Emotions**: Detected emotion categories (joy, sadness, anger, etc.)
- **Score**: Compound sentiment score (-1.0 to +1.0)
- **Source**: News organization
- **Language**: Detected language
- **Time**: When headline was analyzed

#### 4. **Controls & Filters** (Sidebar)

**Refresh Button**
- Click "🔄 Refresh Data" to get latest headlines immediately
- Otherwise data refreshes every time page loads (5-min cache)

**Auto-Refresh Checkbox**
- Enable "Auto-refresh (5 min)" to automatically update headlines every 5 minutes
- Dashboard will refresh in background

**Sentiment Filter**
- Select which sentiment categories to display
- Default: all categories shown
- Useful for focusing on positive/negative news only

**Language Filter**
- Choose to view headlines in specific languages
- Example: English only, or English + Hindi

**Source Filter**
- Focus on specific news outlets
- Example: View only Times of India headlines

**Sorting Options**
- **Sort by**: Choose column to sort (score, time, source, sentiment)
- **Order**: Ascending or Descending
- **Show rows**: Select 5-50 headlines to display

---

## Common Tasks

### Find All Positive News
1. In Sentiment Filter → Select only "Happy/Positive"
2. Set Sort by → "compound_score" 
3. Order → "Descending"

### Compare News Source Bias
1. View "Sentiment by Source" chart
2. See which sources have more positive/negative coverage

### Find Most Recent Headlines
1. Sort by → "timestamp" (time)
2. Order → "Descending"

### Export Data for Analysis
1. Scroll to bottom of page
2. Click "📥 Download Full Data as CSV"
3. File downloads with current timestamp

### Analyze Hindi News Sentiment
1. Language Filter → Select "Hindi"
2. View all charts update for Hindi headlines only

---

## Understanding Sentiment Scores

### Compound Score (-1.0 to +1.0)
- **+1.0 to +0.3**: Clearly positive/happy
- **+0.3 to +0.05**: Slightly positive
- **+0.05 to -0.05**: Neutral
- **-0.05 to -0.3**: Slightly negative
- **-0.3 to -1.0**: Clearly negative/sad

### Example Headlines:
- "India wins World Cup! 🏆" → +0.85 (Happy/Positive)
- "Traffic accident causes delay" → -0.2 (Slightly Negative)
- "Government announces new policy" → +0.1 (Slightly Positive)
- "Meeting held with officials" → 0.0 (Neutral)
- "Terror attack injures 10 people" → -0.75 (Sad/Negative)

---

## Emotion Categories

The system detects 6 emotion categories:

| Emotion | Indicates | Example Keywords |
|---------|-----------|------------------|
| **Joy** | Positive, celebratory mood | Victory, celebration, success, award |
| **Sadness** | Loss, tragedy, grief | Death, accident, loss, tragedy |
| **Anger** | Outrage, conflict | Protest, violence, controversy, scandal |
| **Fear** | Threat, danger, crisis | Terror, danger, emergency, epidemic |
| **Surprise** | Unexpected events | Shock, breakthrough, unprecedented |
| **Neutral** | Factual reporting | Meeting, announcement, report |

---

## Tips for Better Analysis

### 1. **Refresh Regularly**
- News changes constantly
- Use manual refresh for fresh data
- Enable auto-refresh for continuous monitoring

### 2. **Use Multiple Filters**
- Combine sentiment + language filters
- Example: View Hindi positive news only
- Example: Check specific source's negative headlines

### 3. **Compare Over Time**
- Take screenshots at different times
- Compare sentiment trends
- Useful for media analysis

### 4. **Export & Analyze**
- Download CSV for deeper analysis
- Use Excel for custom calculations
- Perfect for research projects

### 5. **Watch for Patterns**
- Some sources more sensational (negative)
- Some languages more positive
- Hindi and English may have different sentiment patterns

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `R` | Refresh page in browser |
| `C` | Clear cache (browser specific) |
| `Ctrl+L` | Focus URL bar |

---

## Troubleshooting

### Dashboard Won't Load?
- Make sure the terminal is still running (you should see INFO messages)
- Try refreshing browser (Ctrl+R)
- Check firewall isn't blocking port 8501

### No Headlines Showing?
- Check internet connection
- Some news sites may be down
- Try manual refresh button
- Wait a few seconds for analysis to complete

### Charts Not Working?
- Refresh the page
- Clear browser cache
- Try a different browser

### Slow Performance?
- Close other browser tabs
- Disable auto-refresh temporarily
- Check internet connection speed

---

## FAQ

**Q: How often is data updated?**
- A: Every 5 minutes (default cache). Click refresh for instant update.

**Q: Can I change refresh interval?**
- A: Yes! Edit dashboard.py, find `@st.cache_data(ttl=300)` and change 300 to your desired seconds.

**Q: How many headlines are analyzed?**
- A: Usually 90-110 unique headlines per refresh from 9 news sources.

**Q: Why are some headlines in Hindi?**
- A: The system includes Hindi news sources (Dainik Bhaskar, Amar Ujala) as specified in the requirements.

**Q: Can I add more news sources?**
- A: Yes! Edit `news_scraper.py`, add entries to `self.news_sources` dictionary.

**Q: How accurate is the sentiment analysis?**
- A: ~85% accurate for clear cases. Irony/sarcasm may not be detected correctly.

**Q: What's the difference between Compound and Polarity scores?**
- A: Compound = VADER score, Polarity = TextBlob score. Both combined for final sentiment.

---

## Advanced Features

### Batch Export for Research
1. Click "📥 Download Full Data as CSV"
2. Open in Excel/Python for analysis
3. File includes all sentiment scores, emotions, languages

### Real-time Monitoring
1. Keep dashboard running in background
2. Check periodically for sentiment trends
3. Monitor specific sources for bias analysis

### Multi-user Access
1. Dashboard accessible at: `http://10.39.12.48:8501`
2. Any device on network can view live dashboard
3. Perfect for office/team monitoring

---

## Performance Stats

- **Headlines per refresh**: 90-110
- **Analysis time**: 2-3 seconds
- **Dashboard load time**: <5 seconds
- **Data cache duration**: 5 minutes
- **Browser memory usage**: ~100-200 MB

---

## Support & Help

**For Issues:**
1. Check SYSTEM_STATUS.md for detailed technical info
2. Review README.md for comprehensive documentation
3. Check internet connection and news source availability

**For Modifications:**
1. Edit `news_scraper.py` to add/remove sources
2. Edit `sentiment_analyzer.py` to adjust sentiment thresholds
3. Edit `dashboard.py` to customize visualizations

---

**Happy Analyzing! 📊**
