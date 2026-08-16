# Finny Finance

I built this as a full-stack financial intelligence platform that combines real-time market data, NLP-powered sentiment analysis, sector risk heatmaps, and volatility forecasting into one live dashboard.

**Live dashboard:** [https://rujulaaa.github.io/fin-intel-platform](https://rujulaaa.github.io/fin-intel-platform)

## What it does

- **Real-time watchlist** tracking 10 major stocks (AAPL, NVDA, TSLA, MSFT, AMZN, GOOGL, META, JPM, SPY, QQQ) with live prices and daily change
- **Sentiment analysis feed** that classifies financial headlines as positive, negative, or neutral. The backend uses FinBERT (ProsusAI/finbert, fine-tuned to 85% accuracy). The static frontend runs a keyword-based NLP classifier in the browser for instant results
- **Sector risk heatmap** mapping Technology, Financials, Energy, Healthcare, and Consumer sectors against Market, Liquidity, Credit, and FX risk
- **Volatility forecasting** with historical realized volatility and a 10-day mean-reverting forecast model
- **Sentiment distribution ring** showing the live POS/NEG/NEU breakdown
- **Market movers panel** highlighting the top 5 biggest movers in the watchlist
- **Data pipeline tracker** showing the status of each processing step

## How the live data works

The dashboard can pull live data two ways:

1. **Finnhub API (free):** Sign up at [finnhub.io](https://finnhub.io) for a free API key (takes 30 seconds, 60 calls/min). Paste it in the `FINNHUB_KEY` constant in `frontend/index.html`. This gives you real-time stock quotes and live financial news headlines, all fetched directly in the browser with no backend needed.

2. **FastAPI backend:** When running locally or deployed on Render, the Python backend uses yfinance for market data and FinBERT for ML-powered sentiment classification.

Without either, the dashboard runs with smart demo data that randomizes slightly on each load and auto-refreshes every 5 minutes.

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

The repo has a GitHub Actions workflow that auto-deploys `frontend/` on every push to `main`.

1. Go to **Settings > Pages** in the repo
2. Under **Source**, select **GitHub Actions**
3. Push to `main`
4. Dashboard goes live at `https://rujulaaa.github.io/fin-intel-platform/`

For live stock data on GitHub Pages, add a free Finnhub API key (see "How the live data works" above).

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
