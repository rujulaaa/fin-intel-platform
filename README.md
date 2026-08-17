# Finny Finance

I built this as a full-stack financial intelligence platform that pulls together real-time market data, sentiment analysis on financial headlines, sector risk heatmaps, and volatility forecasting into one live dashboard.

**Live dashboard:** [https://rujulaaa.github.io/fin-intel-platform/](https://rujulaaa.github.io/fin-intel-platform/)

## What it does

The project has two layers: a live frontend dashboard deployed on GitHub Pages, and a Python backend that can be run locally or deployed separately for deeper ML-powered analysis.

### Live dashboard (GitHub Pages)

- **Real-time stock watchlist** tracking 10 major tickers (AAPL, NVDA, TSLA, MSFT, AMZN, GOOGL, META, JPM, SPY, QQQ) with live prices and daily change via Finnhub API
- **Live financial news feed** pulling real headlines from Finnhub, classified as positive, negative, or neutral using a keyword-based NLP classifier running in the browser
- **Sentiment distribution ring** showing the real-time POS/NEG/NEU breakdown across headlines
- **Market movers panel** highlighting the top 5 biggest movers in the watchlist
- **Sector risk heatmap** mapping Technology, Financials, Energy, Healthcare, and Consumer sectors against Market, Liquidity, Credit, and FX risk types
- **Volatility forecast chart** with historical realized volatility and a 10-day mean-reverting projection
- **Sector exposure bars** showing portfolio allocation across sectors
- **Data pipeline tracker** visualizing the end-to-end processing flow from scraping to dashboard

### Backend (local / Render)

When the FastAPI backend is running, it replaces the frontend data sources with:

- **yfinance** for live market data and historical OHLCV
- **FinBERT** (ProsusAI/finbert via HuggingFace Transformers) for ML-powered sentiment classification, fine-tuned to 85% accuracy
- **requests + BeautifulSoup4** for scraping 1,000+ financial headlines from RSS feeds
- **Real-time risk computation** using realized volatility from sector ETFs (XLK, XLF, XLE, XLV, XLY)
- **Volatility forecasting** using historical log returns with a mean-reverting AR(1) model

## Project structure

```
fin-intel-platform/
├── backend/
│   ├── main.py                  # FastAPI entry point
│   ├── __init__.py
│   └── routers/
│       ├── market.py            # yfinance market data + volatility
│       ├── sentiment.py         # headline scraping + FinBERT inference
│       ├── risk.py              # sector risk heatmap
│       ├── pipeline.py          # pipeline status tracker
│       └── __init__.py
├── frontend/
│   └── index.html               # self-contained live dashboard
├── .github/
│   └── workflows/
│       └── deploy.yml           # auto-deploys to GitHub Pages
├── Procfile
├── requirements.txt
├── .gitignore
└── README.md
```

## Running locally

```bash
git clone https://github.com/rujulaaa/fin-intel-platform.git
cd fin-intel-platform
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

Open [http://localhost:8000](http://localhost:8000) and the backend serves the dashboard with live yfinance data and FinBERT classification.

## Deploying to GitHub Pages

The repo includes a GitHub Actions workflow that auto-deploys `frontend/` on every push to `main`.

1. Go to **Settings > Pages** in the repo
2. Under **Source**, select **GitHub Actions**
3. Push to `main`
4. Dashboard goes live at [https://rujulaaa.github.io/fin-intel-platform/](https://rujulaaa.github.io/fin-intel-platform/)

The frontend uses the Finnhub API (free, 60 calls/min) for real-time stock quotes and live news. The API key is set in the `FINNHUB_KEY` constant in `frontend/index.html`.

## Tech stack

| Layer | Technology |
|-------|-----------|
| Market data | yfinance (backend), Finnhub API (frontend) |
| News scraping | requests + BeautifulSoup4 (backend), Finnhub news API (frontend) |
| Sentiment model | ProsusAI/finbert via HuggingFace Transformers (backend), keyword NLP classifier (frontend) |
| Backend | FastAPI + uvicorn |
| Frontend | vanilla HTML/CSS/JS, no build step |
| Deployment | GitHub Pages (frontend) + Render (backend, optional) |

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/market/watchlist` | live prices for the 10-stock watchlist |
| GET | `/api/market/volatility/{ticker}` | historical volatility + 10-day forecast |
| GET | `/api/market/kpis` | dashboard KPI metrics |
| GET | `/api/sentiment/headlines` | scraped + FinBERT-classified headlines |
| POST | `/api/sentiment/classify` | classify any list of text with FinBERT |
| GET | `/api/sentiment/summary` | sentiment distribution summary |
| GET | `/api/risk/heatmap` | sector x risk-type matrix |
| GET | `/api/risk/exposure` | portfolio sector allocation |
| GET | `/api/pipeline/status` | status of each pipeline step |
