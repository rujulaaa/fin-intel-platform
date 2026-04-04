# 📊 FintelliQ – Financial Intelligence Platform

> End-to-end market intelligence: real-time data ingestion, FinBERT sentiment analysis, risk heatmaps, and volatility forecasts.

---

## 🗂️ Project Structure

```
fintelliq/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── requirements.txt
│   └── routers/
│       ├── market.py            # yfinance market data + volatility
│       ├── sentiment.py         # headline scraping + FinBERT inference
│       ├── risk.py              # sector risk heatmap
│       └── pipeline.py          # pipeline status tracker
├── frontend/
│   └── index.html               # Full dashboard (fetches from API)
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Pages auto-deploy
├── Procfile                     # For Render/Railway deployment
├── requirements.txt             # Root-level (for Render)
└── README.md
```

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/fintelliq.git
cd fintelliq
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the backend
```bash
uvicorn backend.main:app --reload --port 8000
```

### 4. Open the dashboard
Navigate to [http://localhost:8000](http://localhost:8000)

The FastAPI server automatically serves `frontend/index.html` at the root.

---

## 🌐 Deploy Frontend to GitHub Pages (free, static)

> The dashboard works standalone with fallback demo data when the backend is offline.

### Steps:
1. Push this repo to GitHub
2. Go to **Settings → Pages**
3. Under **Source**, select **GitHub Actions**
4. The workflow in `.github/workflows/deploy.yml` auto-deploys on every push to `main`
5. Your dashboard will be live at: `https://YOUR_USERNAME.github.io/fintelliq/`

> **Note:** When hosted on GitHub Pages, the frontend uses demo/fallback data since there's no backend. For live data, deploy the backend separately (see below).

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Market Data | `yfinance` — real-time prices, historical OHLCV |
| News Scraping | `requests` + `BeautifulSoup4` — 1,000+ daily headlines |
| Sentiment AI | `ProsusAI/finbert` (HuggingFace Transformers) |
| Backend API | `FastAPI` + `uvicorn` |
| Frontend | Vanilla HTML/CSS/JS — no build step needed |
| Deployment | GitHub Pages (frontend) + Render (backend) |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/market/watchlist` | Live prices for 10 stocks |
| GET | `/api/market/volatility/{ticker}` | Historical vol + 10-day forecast |
| GET | `/api/market/kpis` | Dashboard KPI metrics |
| GET | `/api/sentiment/headlines` | Scraped + FinBERT-classified headlines |
| POST | `/api/sentiment/classify` | Classify custom text list |
| GET | `/api/sentiment/summary` | Sentiment distribution summary |
| GET | `/api/risk/heatmap` | Sector × risk-type matrix |
| GET | `/api/risk/exposure` | Portfolio sector allocation |
| GET | `/api/pipeline/status` | Data pipeline step statuses |
