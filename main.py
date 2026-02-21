import os
from src.ingestion.market_data import MarketDataCollector
from src.ingestion.news_scraper import NewsScraper
from src.models.sentiment_analyzer import SentimentAnalyzer

def main():
    print("🚀 Starting Financial Intelligence Pipeline...")
    
    # 1. Setup
    tickers = ["SIVR", "BCS", "GNPX", "AAPL"]
    if not os.path.exists('data'):
        os.makedirs('data')

    # 2. Collect Market Data
    print("📊 Fetching market prices...")
    collector = MarketDataCollector(tickers)
    hist_data = collector.fetch_history()
    collector.save_to_csv(hist_data)

    # 3. Analyze Sentiment
    print("🧠 Running NLP Sentiment Analysis (FinBERT)...")
    scraper = NewsScraper()
    analyzer = SentimentAnalyzer()
    
    for ticker in tickers:
        headlines = scraper.get_sentiment_text(ticker)
        score = analyzer.get_sentiment(headlines)
        print(f"Ticker: {ticker} | Headlines Found: {len(headlines)} | Sentiment Score: {score:.2f}")

    print("✅ Pipeline execution complete.")

if __name__ == "__main__":
    main()
