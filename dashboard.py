"""
Interactive Dashboard for Sentiment Analysis of Indian News Headlines
Real-time visualization with Streamlit
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
import time
from news_scraper import NewsHeadlineScraper
from sentiment_analyzer import MultiLanguageSentimentAnalyzer

# Page configuration
st.set_page_config(
    page_title="Indian News Sentiment Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stAlert {
        background-color: #e8f4f8;
    }
    h1 {
        color: #1f4788;
        text-align: center;
        font-weight: bold;
    }
    h2, h3 {
        color: #2c5aa0;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_and_analyze_news():
    """Load news and perform sentiment analysis"""
    scraper = NewsHeadlineScraper()
    analyzer = MultiLanguageSentimentAnalyzer()
    
    # Scrape news
    headlines_df = scraper.scrape_all_sources()
    
    if headlines_df.empty:
        return pd.DataFrame()
    
    # Analyze sentiment
    analyzed_df = analyzer.analyze_batch(headlines_df)
    
    return analyzed_df


def create_sentiment_distribution_chart(df):
    """Create sentiment distribution pie chart"""
    sentiment_counts = df['sentiment'].value_counts()
    
    colors = {
        'Happy/Positive': '#2ecc71',
        'Sad/Negative': '#e74c3c',
        'Neutral': '#95a5a6',
        'Slightly Positive': '#3498db',
        'Slightly Negative': '#e67e22'
    }
    
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title='Sentiment Distribution of News Headlines',
        color=sentiment_counts.index,
        color_discrete_map=colors,
        hole=0.4
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400, showlegend=True)
    
    return fig


def create_emotion_distribution_chart(df):
    """Create emotion distribution bar chart"""
    # Extract all emotions
    all_emotions = []
    for emotions_str in df['emotions']:
        all_emotions.extend(emotions_str.split(', '))
    
    emotion_counts = pd.Series(all_emotions).value_counts().head(10)
    
    colors_map = {
        'joy': '#f1c40f',
        'sadness': '#3498db',
        'anger': '#e74c3c',
        'fear': '#9b59b6',
        'surprise': '#e67e22',
        'neutral': '#95a5a6'
    }
    
    colors = [colors_map.get(emotion, '#34495e') for emotion in emotion_counts.index]
    
    fig = px.bar(
        x=emotion_counts.index,
        y=emotion_counts.values,
        title='Top Emotions in News Headlines',
        labels={'x': 'Emotion', 'y': 'Count'},
        color=emotion_counts.index,
        color_discrete_sequence=colors
    )
    
    fig.update_layout(height=400, showlegend=False)
    fig.update_xaxes(tickangle=-45)
    
    return fig


def create_source_sentiment_chart(df):
    """Create sentiment by source chart"""
    source_sentiment = df.groupby(['source', 'sentiment']).size().reset_index(name='count')
    
    fig = px.bar(
        source_sentiment,
        x='source',
        y='count',
        color='sentiment',
        title='Sentiment Distribution by News Source',
        labels={'count': 'Number of Headlines', 'source': 'News Source'},
        barmode='stack',
        color_discrete_map={
            'Happy/Positive': '#2ecc71',
            'Sad/Negative': '#e74c3c',
            'Neutral': '#95a5a6',
            'Slightly Positive': '#3498db',
            'Slightly Negative': '#e67e22'
        }
    )
    
    fig.update_layout(height=500, xaxis_tickangle=-45)
    
    return fig


def create_sentiment_score_distribution(df):
    """Create compound score distribution"""
    fig = px.histogram(
        df,
        x='compound_score',
        nbins=30,
        title='Distribution of Sentiment Scores',
        labels={'compound_score': 'Compound Sentiment Score', 'count': 'Frequency'},
        color_discrete_sequence=['#3498db']
    )
    
    fig.add_vline(x=0, line_dash="dash", line_color="red", 
                  annotation_text="Neutral", annotation_position="top")
    fig.update_layout(height=400)
    
    return fig


def create_language_distribution_chart(df):
    """Create language distribution chart"""
    lang_counts = df['language'].value_counts()
    
    fig = px.bar(
        x=lang_counts.index,
        y=lang_counts.values,
        title='News Headlines by Language',
        labels={'x': 'Language', 'y': 'Count'},
        color=lang_counts.values,
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(height=400, showlegend=False)
    
    return fig


def display_sentiment_metrics(df):
    """Display key sentiment metrics"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_headlines = len(df)
    positive_pct = (df['sentiment'].str.contains('Positive').sum() / total_headlines * 100)
    negative_pct = (df['sentiment'].str.contains('Negative').sum() / total_headlines * 100)
    neutral_pct = (df['sentiment'] == 'Neutral').sum() / total_headlines * 100
    avg_compound = df['compound_score'].mean()
    
    with col1:
        st.metric("Total Headlines", total_headlines, "Live")
    
    with col2:
        st.metric("Positive", f"{positive_pct:.1f}%", delta=f"{positive_pct:.1f}%", 
                 delta_color="normal")
    
    with col3:
        st.metric("Negative", f"{negative_pct:.1f}%", delta=f"-{negative_pct:.1f}%",
                 delta_color="inverse")
    
    with col4:
        st.metric("Neutral", f"{neutral_pct:.1f}%")
    
    with col5:
        sentiment_indicator = "Positive 📈" if avg_compound > 0 else "Negative 📉" if avg_compound < 0 else "Neutral ➡️"
        st.metric("Avg Score", f"{avg_compound:.3f}", sentiment_indicator)


def main():
    """Main dashboard application"""
    
    # Header
    st.title("📰 Indian News Sentiment Analysis Dashboard")
    st.markdown("### Real-time Sentiment Analysis Across Multiple Indian Languages")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://www.flaticon.com/svg/static/icons/svg/3305/3305620.svg", width=100)
        st.title("Controls")
        
        # Refresh button
        if st.button("🔄 Refresh Data", width='stretch'):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Auto-refresh option
        auto_refresh = st.checkbox("Auto-refresh (5 min)", value=False)
        
        st.markdown("---")
        
        # Filters
        st.subheader("Filters")
        
    # Load data
    with st.spinner("🔍 Scraping live news and analyzing sentiment..."):
        df = load_and_analyze_news()
    
    if df.empty:
        st.error("⚠️ No headlines found. Please check your internet connection and try again.")
        return
    
    # Apply filters from sidebar
    with st.sidebar:
        sentiment_filter = st.multiselect(
            "Filter by Sentiment",
            options=df['sentiment'].unique().tolist(),
            default=df['sentiment'].unique().tolist()
        )
        
        language_filter = st.multiselect(
            "Filter by Language",
            options=df['language'].unique().tolist(),
            default=df['language'].unique().tolist()
        )
        
        source_filter = st.multiselect(
            "Filter by Source",
            options=df['source'].unique().tolist(),
            default=df['source'].unique().tolist()
        )
    
    # Apply filters
    filtered_df = df[
        (df['sentiment'].isin(sentiment_filter)) &
        (df['language'].isin(language_filter)) &
        (df['source'].isin(source_filter))
    ]
    
    if filtered_df.empty:
        st.warning("No headlines match the selected filters.")
        return
    
    # Display metrics
    st.subheader("📊 Key Metrics")
    display_sentiment_metrics(filtered_df)
    
    st.markdown("---")
    
    # Main visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_sentiment_distribution_chart(filtered_df), 
                       width='stretch')
    
    with col2:
        st.plotly_chart(create_emotion_distribution_chart(filtered_df), 
                       width='stretch')
    
    # Second row of visualizations
    col3, col4 = st.columns(2)
    
    with col3:
        st.plotly_chart(create_sentiment_score_distribution(filtered_df), 
                       width='stretch')
    
    with col4:
        st.plotly_chart(create_language_distribution_chart(filtered_df), 
                       width='stretch')
    
    # Source analysis
    st.plotly_chart(create_source_sentiment_chart(filtered_df), 
                   width='stretch')
    
    st.markdown("---")
    
    # Headlines table
    st.subheader("📋 News Headlines with Sentiment Analysis")
    
    # Display options
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        sort_by = st.selectbox(
            "Sort by",
            ['compound_score', 'timestamp', 'source', 'sentiment'],
            index=0
        )
    with col2:
        sort_order = st.radio("Order", ['Descending', 'Ascending'])
    with col3:
        show_rows = st.slider("Show rows", 5, 50, 20)
    
    # Sort and display
    display_df = filtered_df.sort_values(
        by=sort_by, 
        ascending=(sort_order == 'Ascending')
    ).head(show_rows)
    
    # Create display dataframe
    table_df = display_df[[
        'emoji', 'title', 'sentiment', 'emotions', 'compound_score', 
        'source', 'language', 'timestamp'
    ]].copy()
    
    table_df.columns = [
        '😊', 'Headline', 'Sentiment', 'Emotions', 'Score', 
        'Source', 'Language', 'Time'
    ]
    
    st.dataframe(
        table_df,
        width='stretch',
        height=600,
        hide_index=True
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Full Data as CSV",
        data=csv,
        file_name=f"news_sentiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<center>Last updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + 
        " | Data source: Live Indian News Websites</center>",
        unsafe_allow_html=True
    )
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(300)  # 5 minutes
        st.rerun()


if __name__ == "__main__":
    main()
