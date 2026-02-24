"""
✨ Premium Interactive Dashboard for Sentiment Analysis of Indian News Headlines
Modern, Attractive Real-time Visualization with Streamlit
"""

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

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

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Indian News Sentiment Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PREMIUM CUSTOM CSS STYLING
# ============================================================================
st.markdown("""
    <style>
    /* Root Color Variables for Dark Theme */
    :root {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --success-color: #27AE60;
        --warning-color: #F39C12;
        --danger-color: #E74C3C;
        --dark-bg: #0f1419;
        --darker-bg: #0a0e13;
        --card-bg: #1a2332;
        --text-primary: #e8eef7;
        --text-secondary: #a8b8d8;
        --accent-1: #4ECDC4;
        --accent-2: #FF6B6B;
    }
    
    /* Main Container - Dark Theme */
    .main {
        background-color: #0f1419 !important;
        padding: 0;
        margin: 0;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #0a0e13 !important;
        min-height: 100vh;
        color: #e8eef7 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1a2332 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        color: #e8eef7 !important;
    }
    
    /* Headers - Dark Theme */
    h1 {
        color: #4ECDC4 !important;
        text-align: center;
        font-weight: bold;
        font-size: 2.5em;
        text-shadow: 0 4px 12px rgba(78, 205, 196, 0.3);
        margin-bottom: 10px;
    }
    
    h2 {
        color: #4ECDC4 !important;
        font-weight: bold;
        text-decoration: underline;
        text-decoration-color: #FF6B6B;
        text-decoration-thickness: 3px;
        text-underline-offset: 8px;
        margin-top: 30px;
        margin-bottom: 20px;
        text-shadow: 0 2px 8px rgba(78, 205, 196, 0.2);
    }
    
    h3 {
        color: #a8b8d8 !important;
        font-weight: 600;
        margin-top: 20px;
    }
    
    /* Paragraph Text - Dark Theme */
    p {
        color: #e8eef7 !important;
    }
    
    /* Main content area text */
    [data-testid="stAppViewContainer"] p {
        color: #a8b8d8 !important;
    }
    
    /* Metric Cards - Dark Theme */
    [data-testid="metric-container"] {
        background: #1a2332 !important;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        border-left: 5px solid #4ECDC4;
        transition: all 0.3s ease;
        border: 1px solid rgba(78, 205, 196, 0.2);
    }
    
    [data-testid="metric-container"] label {
        color: #a8b8d8 !important;
        font-weight: 500;
    }
    
    [data-testid="metric-container"] div {
        color: #e8eef7 !important;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(78, 205, 196, 0.2);
        border-color: rgba(78, 205, 196, 0.4);
    }
    
    /* Alerts and Messages - Dark Theme */
    .stAlert {
        background-color: rgba(78, 205, 196, 0.1) !important;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #4ECDC4;
        color: #e8eef7 !important;
        border: 1px solid rgba(78, 205, 196, 0.3);
    }
    
    /* Buttons - Dark Theme */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E72 100%) !important;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(255, 107, 107, 0.5);
    }
    
    /* Selectbox and Multiselect */
    .stSelectbox label,
    .stMultiSelect label {
        color: #e8eef7 !important;
        font-weight: 600;
    }
    
    .stSelectbox,
    .stMultiSelect,
    [data-baseweb="select"] {
        border-radius: 8px;
        border: 2px solid #4ECDC4 !important;
        background-color: #1a2332 !important;
    }
    
    [data-baseweb="select"] input {
        color: #e8eef7 !important;
        background-color: #1a2332 !important;
    }
    
    /* Radio Buttons */
    .stRadio label {
        color: #e8eef7 !important;
        font-weight: 500;
    }
    
    .stRadio {
        border-radius: 8px;
    }
    
    /* Checkbox */
    .stCheckbox label {
        color: #e8eef7 !important;
        font-weight: 500;
    }
    
    /* Slider */
    .stSlider label {
        color: #e8eef7 !important;
        font-weight: 600;
    }
    
    .stSlider {
        padding: 10px 0;
    }
    
    /* Dataframe - Dark Theme */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        background-color: #1a2332 !important;
    }
    
    [data-testid="stDataFrame"] th {
        background-color: #4ECDC4 !important;
        color: #0a0e13 !important;
        font-weight: bold;
    }
    
    [data-testid="stDataFrame"] td {
        color: #e8eef7 !important;
        background-color: #242f3f !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #95E1D3);
        margin: 30px 0;
        opacity: 0.5;
    }
    
    /* Sidebar Text - Explicit Colors */
    [data-testid="stSidebar"] h1 {
        color: #4ECDC4 !important;
        font-size: 1.5em;
        text-shadow: 0 2px 8px rgba(78, 205, 196, 0.2);
    }
    
    [data-testid="stSidebar"] h2 {
        color: #4ECDC4 !important;
        text-decoration: none;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #a8b8d8 !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #e8eef7 !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stCheckbox label {
        color: #e8eef7 !important;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #e8eef7 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label {
        color: #e8eef7 !important;
    }
    
    [data-testid="stSidebar"] .stInfo {
        background-color: rgba(78, 205, 196, 0.1) !important;
        border-left-color: #4ECDC4 !important;
        color: #a8b8d8 !important;
    }
    
    /* Info/Success/Warning boxes */
    .stInfo {
        background-color: rgba(78, 205, 196, 0.1) !important;
        color: #a8b8d8 !important;
        border-radius: 8px;
        border: 1px solid rgba(78, 205, 196, 0.3) !important;
    }
    
    .stSuccess {
        background-color: rgba(39, 174, 96, 0.1) !important;
        color: #27AE60 !important;
        border: 1px solid rgba(39, 174, 96, 0.3) !important;
    }
    
    .stWarning {
        background-color: rgba(243, 156, 18, 0.1) !important;
        color: #F39C12 !important;
        border: 1px solid rgba(243, 156, 18, 0.3) !important;
    }
    
    .stError {
        background-color: rgba(231, 76, 60, 0.1) !important;
        color: #E74C3C !important;
        border: 1px solid rgba(231, 76, 60, 0.3) !important;
    }
    
    /* Spinner text */
    .stSpinner {
        color: #4ECDC4 !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #27AE60 0%, #229954 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
    }
    
    .stDownloadButton > button:hover {
        box-shadow: 0 8px 20px rgba(39, 174, 96, 0.5);
    }
    
    /* Footer */
    footer {
        color: #a8b8d8 !important;
        text-align: center;
        font-size: 0.9em;
        margin-top: 50px;
        padding: 30px 20px;
        border-top: 2px solid rgba(78, 205, 196, 0.3);
        background: #1a2332 !important;
    }
    
    /* General text fixes */
    .element-container {
        color: #e8eef7 !important;
    }
    
    .stMarkdown {
        color: #a8b8d8 !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a2332;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4ECDC4;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #FF6B6B;
    }
    
    /* Smooth transitions */
    * {
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# CACHE DATA LOADING
# ============================================================================
@st.cache_data(ttl=300)
def load_and_analyze_news():
    """Load news and perform sentiment analysis"""
    scraper = NewsHeadlineScraper()
    analyzer = MultiLanguageSentimentAnalyzer()
    
    headlines_df = scraper.scrape_all_sources()
    
    if headlines_df.empty:
        return pd.DataFrame()
    
    analyzed_df = analyzer.analyze_batch(headlines_df)
    return analyzed_df

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================
def create_sentiment_distribution_chart(df):
    """Create sentiment distribution pie chart with animation"""
    sentiment_counts = df['sentiment'].value_counts()
    
    colors = {
        'Happy/Positive': '#27AE60',
        'Sad/Negative': '#E74C3C',
        'Neutral': '#95A5A6',
        'Slightly Positive': '#3498DB',
        'Slightly Negative': '#E67E22'
    }
    
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title='<b>📊 Sentiment Distribution</b>',
        color=sentiment_counts.index,
        color_discrete_map=colors,
        hole=0.4
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
        marker=dict(line=dict(color='white', width=2))
    )
    
    fig.update_layout(
        height=450,
        showlegend=True,
        title_font_size=16,
        title_x=0.5,
        font=dict(size=12, family="Arial", color='#e8eef7'),
        title_font_color='#4ECDC4',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_emotion_distribution_chart(df):
    """Create emotion distribution bar chart"""
    all_emotions = []
    for emotions_str in df['emotions']:
        all_emotions.extend(emotions_str.split(', '))
    
    emotion_counts = pd.Series(all_emotions).value_counts().head(10)
    
    colors_map = {
        'joy': '#F39C12',
        'sadness': '#3498DB',
        'anger': '#E74C3C',
        'fear': '#9B59B6',
        'surprise': '#E67E22',
        'neutral': '#95A5A6'
    }
    
    colors = [colors_map.get(emotion, '#34495E') for emotion in emotion_counts.index]
    
    fig = px.bar(
        x=emotion_counts.index,
        y=emotion_counts.values,
        title='<b>😊 Emotion Analysis</b>',
        labels={'x': 'Emotion', 'y': 'Frequency'},
        color=emotion_counts.index,
        color_discrete_sequence=colors
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>',
        marker=dict(line=dict(color='white', width=1))
    )
    
    fig.update_layout(
        height=450,
        showlegend=False,
        title_font_size=16,
        title_x=0.5,
        xaxis_tickangle=-45,
        font=dict(size=11, family="Arial", color='#e8eef7'),
        title_font_color='#4ECDC4',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_source_sentiment_chart(df):
    """Create sentiment by source stacked bar chart"""
    import warnings
    warnings.filterwarnings('ignore')
    
    source_sentiment = df.groupby(['source', 'sentiment'], observed=True).size().reset_index(name='count')
    
    fig = px.bar(
        source_sentiment,
        x='source',
        y='count',
        color='sentiment',
        title='<b>🏢 Sentiment by News Source</b>',
        labels={'count': 'Number of Headlines', 'source': 'News Source'},
        barmode='stack',
        color_discrete_map={
            'Happy/Positive': '#27AE60',
            'Sad/Negative': '#E74C3C',
            'Neutral': '#95A5A6',
            'Slightly Positive': '#3498DB',
            'Slightly Negative': '#E67E22'
        }
    )
    
    fig.update_traces(
        hovertemplate='<b>%{fullData.name}</b><br>Count: %{y}<extra></extra>'
    )
    
    fig.update_layout(
        height=500,
        xaxis_tickangle=-45,
        title_font_size=16,
        title_x=0.5,
        font=dict(size=10, family="Arial", color='#e8eef7'),
        title_font_color='#4ECDC4',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True
    )
    
    return fig

def create_sentiment_score_distribution(df):
    """Create compound score distribution histogram"""
    fig = px.histogram(
        df,
        x='compound_score',
        nbins=30,
        title='<b>📈 Sentiment Score Distribution</b>',
        labels={'compound_score': 'Compound Score', 'count': 'Frequency'},
        color_discrete_sequence=['#3498DB']
    )
    
    fig.add_vline(
        x=0,
        line_dash="dash",
        line_color="red",
        annotation_text="Neutral",
        annotation_position="top right"
    )
    
    fig.update_traces(
        hovertemplate='Score: %{x:.2f}<br>Count: %{y}<extra></extra>',
        marker=dict(line=dict(color='white', width=0.5))
    )
    
    fig.update_layout(
        height=450,
        title_font_size=16,
        title_x=0.5,
        font=dict(size=11, family="Arial", color='#e8eef7'),
        title_font_color='#4ECDC4',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_language_distribution_chart(df):
    """Create language distribution bar chart"""
    lang_counts = df['language'].value_counts()
    
    fig = px.bar(
        x=lang_counts.index,
        y=lang_counts.values,
        title='<b>🌍 Language Distribution</b>',
        labels={'x': 'Language', 'y': 'Number of Headlines'},
        color=lang_counts.values,
        color_continuous_scale='Viridis'
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Headlines: %{y}<extra></extra>',
        marker=dict(line=dict(color='white', width=1))
    )
    
    fig.update_layout(
        height=450,
        showlegend=False,
        title_font_size=16,
        title_x=0.5,
        xaxis_tickangle=-45,
        font=dict(size=11, family="Arial", color='#e8eef7'),
        title_font_color='#4ECDC4',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def display_sentiment_metrics(df):
    """Display key sentiment metrics in an attractive way"""
    total_headlines = len(df)
    positive_pct = (df['sentiment'].str.contains('Positive').sum() / total_headlines * 100)
    negative_pct = (df['sentiment'].str.contains('Negative').sum() / total_headlines * 100)
    neutral_pct = (df['sentiment'] == 'Neutral').sum() / total_headlines * 100
    avg_compound = df['compound_score'].mean()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "📰 Total Headlines",
            total_headlines,
            "Live",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            "😊 Positive",
            f"{positive_pct:.1f}%",
            f"+{positive_pct:.1f}%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "😢 Negative",
            f"{negative_pct:.1f}%",
            f"-{negative_pct:.1f}%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "😐 Neutral",
            f"{neutral_pct:.1f}%",
            "Neutral",
            delta_color="off"
        )
    
    with col5:
        sentiment_indicator = "Positive 📈" if avg_compound > 0.1 else "Negative 📉" if avg_compound < -0.1 else "Balanced ➡️"
        st.metric(
            "📊 Avg Score",
            f"{avg_compound:.3f}",
            sentiment_indicator,
            delta_color="off"
        )


# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    """Main dashboard application"""
    
    # Header Section
    st.markdown("""
        <div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #1a2332 0%, #2c3f52 100%); border-radius: 15px; margin-bottom: 30px; border: 2px solid #4ECDC4; box-shadow: 0 8px 24px rgba(78, 205, 196, 0.15);'>
            <h1 style='margin: 0; font-size: 3em; color: #4ECDC4; text-shadow: 0 4px 12px rgba(78, 205, 196, 0.3);'>📰 Indian News Sentiment Dashboard</h1>
            <p style='color: #a8b8d8; font-size: 1.2em; margin: 15px 0 10px 0; font-weight: 500;'>Real-time Sentiment Analysis Across All Indian Languages</p>
            <p style='color: #e8eef7; font-size: 0.95em;'>✨ Powered by Advanced NLP & Multi-Language Support ✨</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Configuration
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 20px; background-color: rgba(78, 205, 196, 0.1); border-radius: 10px; margin-bottom: 20px; border: 2px solid #4ECDC4;'>
                <h2 style='color: #4ECDC4; margin: 0; font-size: 1.3em; text-shadow: 0 2px 8px rgba(78, 205, 196, 0.2);'>⚙️ CONTROLS</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Refresh button
        st.markdown("<p style='color: #e8eef7; font-weight: bold; margin-bottom: 10px;'>Data Refresh</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Now", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        with col2:
            st.info("⏱️ Auto updates every 5 min")
        
        st.markdown("---")
        
        # Auto-refresh option
        st.markdown("<p style='color: #e8eef7; font-weight: bold; margin-bottom: 10px;'>Auto-Refresh Settings</p>", unsafe_allow_html=True)
        auto_refresh = st.checkbox("🔄 Enable Auto-Refresh (5 min)", value=False)
        
        st.markdown("---")
        
        # Filters
        st.markdown(
            "<div style='background-color: rgba(78, 205, 196, 0.15); padding: 15px; border-radius: 10px; margin: 20px 0; border: 1px solid rgba(78, 205, 196, 0.3);'>"
            "<p style='color: #4ECDC4; font-weight: bold; margin: 0;'>🎯 ADVANCED FILTERS</p>"
            "</div>",
            unsafe_allow_html=True
        )
        
        st.markdown("""<p style='color: #e8eef7; font-size: 0.9em; font-weight: bold; margin-top: 10px;'>Filter by Sentiment</p>""", unsafe_allow_html=True)
        
    # Load data
    with st.spinner("🔍 Scraping live news and analyzing sentiment..."):
        df = load_and_analyze_news()
    
    if df.empty:
        st.error("⚠️ No headlines found. Please check your internet connection and try again.")
        return
    
    # Apply filters from sidebar (continued)
    with st.sidebar:
        sentiment_options = df['sentiment'].unique().tolist()
        sentiment_filter = st.multiselect(
            "Sentiments",
            options=sentiment_options,
            default=sentiment_options,
            key="sentiment_filter"
        )
        
        st.markdown("""<p style='color: #e8eef7; font-size: 0.9em; font-weight: bold; margin-top: 15px;'>Filter by Language</p>""", unsafe_allow_html=True)
        language_options = df['language'].unique().tolist()
        language_filter = st.multiselect(
            "Languages",
            options=language_options,
            default=language_options,
            key="language_filter"
        )
        
        st.markdown("""<p style='color: #e8eef7; font-size: 0.9em; font-weight: bold; margin-top: 15px;'>Filter by Source</p>""", unsafe_allow_html=True)
        source_options = df['source'].unique().tolist()
        source_filter = st.multiselect(
            "News Sources",
            options=source_options,
            default=source_options,
            key="source_filter"
        )
    
    # Apply filters
    filtered_df = df[
        (df['sentiment'].isin(sentiment_filter)) &
        (df['language'].isin(language_filter)) &
        (df['source'].isin(source_filter))
    ]
    
    if filtered_df.empty:
        st.warning("⚠️ No headlines match the selected filters. Try adjusting your filters.")
        return
    
    # Display metrics
    st.markdown("## 📊 **Key Metrics**")
    display_sentiment_metrics(filtered_df)
    
    st.markdown("---")
    
    # Main visualizations - Row 1
    st.markdown("## 📈 **Visualizations**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_sentiment_distribution_chart(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_emotion_distribution_chart(filtered_df), use_container_width=True)
    
    # Secondary visualizations - Row 2
    col3, col4 = st.columns(2)
    
    with col3:
        st.plotly_chart(create_sentiment_score_distribution(filtered_df), use_container_width=True)
    
    with col4:
        st.plotly_chart(create_language_distribution_chart(filtered_df), use_container_width=True)
    
    # Source analysis - Full width
    st.plotly_chart(create_source_sentiment_chart(filtered_df), use_container_width=True)
    
    st.markdown("---")
    
    # Headlines table section
    st.markdown("## 📋 **Detailed News Analysis**")
    
    # Display options
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        sort_by = st.selectbox(
            "📊 Sort Headlines By",
            ['compound_score', 'timestamp', 'source', 'sentiment'],
            index=0
        )
    with col2:
        sort_order = st.radio("📍 Order", ['Desc ⬇️', 'Asc ⬆️'], horizontal=True)
    with col3:
        show_rows = st.slider("📈 Show Rows", 5, 100, 25)
    
    # Sort and display
    display_df = filtered_df.sort_values(
        by=sort_by,
        ascending=(sort_order == 'Asc ⬆️')
    ).head(show_rows)
    
    # Create display dataframe with better formatting
    table_df = display_df[[
        'emoji', 'title', 'sentiment', 'emotions', 'compound_score',
        'source', 'language', 'timestamp'
    ]].copy()
    
    table_df.columns = [
        '😊', 'Headline', 'Sentiment', 'Emotions', 'Score',
        'Source', 'Language', 'Time'
    ]
    
    # Style and display
    st.dataframe(
        table_df,
        height=600,
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Download section
    st.markdown("## 📥 **Export Data**")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Data as CSV",
            data=csv,
            file_name=f"news_sentiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        st.info(f"✅ {len(filtered_df)} headlines ready to download")
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
        <div style='text-align: center; padding: 30px 20px; background: linear-gradient(135deg, #1a2332 0%, #2c3f52 100%); border-radius: 10px; margin-top: 30px; border-top: 3px solid #4ECDC4; border: 2px solid rgba(78, 205, 196, 0.3); box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);'>
            <p style='color: #e8eef7; margin: 10px 0; font-weight: bold;'>
                <b>Last Updated:</b> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
            </p>
            <p style='color: #a8b8d8; margin: 5px 0; font-size: 0.9em;'>
                📊 Data Source: Live Indian News Websites | 🌐 Languages: All Major Indian Languages
            </p>
            <p style='color: #4ECDC4; margin: 10px 0; font-size: 0.85em;'>
                ✨ Built with ❤️ for analyzing Indian news sentiment across all languages ✨
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(300)  # 5 minutes
        st.rerun()

if __name__ == "__main__":
    main()
