import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.ingestion.market_data import MarketDataCollector
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.ingestion.news_scraper import NewsScraper

st.set_page_config(page_title="FinIntel Dashboard", layout="wide")

st.title("📈 Financial Intelligence & Sentiment Platform")
st.sidebar.header("Settings")

# User Input
ticker = st.sidebar.selectbox("Select Asset", ["SIVR", "BCS", "GNPX", "AAPL", "TSLA"])
days_to_plot = st.sidebar.slider("Days of History", 30, 365, 90)

# Data Loading
st.subheader(f"Analysis for {ticker}")
col1, col2 = st.columns([2, 1])

with col1:
    # 1. Price Chart
    collector = MarketDataCollector([ticker])
    data = collector.fetch_history(period=f"{days_to_plot}d")
    df = data[ticker]
    
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'])])
    fig.update_layout(title=f"{ticker} Price Action", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # 2. Sentiment Gauge
    st.write("🔍 **Real-Time Sentiment**")
    scraper = NewsScraper()
    analyzer = SentimentAnalyzer()
    
    headlines = scraper.get_sentiment_text(ticker)
    score = analyzer.get_sentiment(headlines)
    
    # Color coding the sentiment
    color = "green" if score > 0.1 else "red" if score < -0.1 else "gray"
    st.metric(label="FinBERT Score", value=round(score, 2), delta_color="normal")
    st.markdown(f"<h1 style='text-align: center; color: {color};'>{round(score*100, 1)}%</h1>", unsafe_allow_html=True)
    
    st.write("**Top Headlines:**")
    for h in headlines[:5]:
        st.write(f"- {h}")
