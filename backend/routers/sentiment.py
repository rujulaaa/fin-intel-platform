"""
Sentiment Analysis Router
Scrapes financial headlines and classifies them with FinBERT
(ProsusAI/finbert from HuggingFace).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
import time

router = APIRouter()
logger = logging.getLogger(__name__)

# ── Lazy-load FinBERT so startup is fast ──────────────────────────────────────
_pipeline = None

def get_finbert():
    global _pipeline
    if _pipeline is None:
        try:
            from transformers import pipeline as hf_pipeline
            _pipeline = hf_pipeline(
                "text-classification",
                model="ProsusAI/finbert",
                tokenizer="ProsusAI/finbert",
                top_k=None,          # return all 3 scores
            )
            logger.info("FinBERT loaded successfully")
        except Exception as e:
            logger.error(f"FinBERT load failed: {e}")
            _pipeline = None
    return _pipeline


# ── Headline scraping ─────────────────────────────────────────────────────────
DEMO_HEADLINES = [
    {"text": "Fed signals potential rate pause amid cooling inflation data; markets rally", "source": "Reuters", "time": "2m ago"},
    {"text": "NVDA beats Q4 earnings by 18%, data center revenue surges to record high", "source": "Bloomberg", "time": "8m ago"},
    {"text": "China manufacturing PMI contracts for third consecutive month, export fears grow", "source": "FT", "time": "15m ago"},
    {"text": "Apple announces $110B share buyback program, largest in company history", "source": "WSJ", "time": "22m ago"},
    {"text": "Treasury yields hold steady as investors await key employment report", "source": "CNBC", "time": "31m ago"},
    {"text": "Regional banks face increasing pressure from commercial real estate exposure", "source": "Bloomberg", "time": "45m ago"},
    {"text": "S&P 500 achieves new all-time high as tech sector leads broad market gains", "source": "Reuters", "time": "1h ago"},
    {"text": "Oil prices slide 2.3% on demand concerns and rising US crude inventories", "source": "WSJ", "time": "1h ago"},
    {"text": "Microsoft Azure revenue growth decelerates slightly, guidance remains intact", "source": "FT", "time": "2h ago"},
    {"text": "Retail sales beat expectations, consumer spending remains resilient", "source": "CNBC", "time": "2h ago"},
]

def scrape_headlines(max_headlines: int = 20) -> List[dict]:
    """
    Scrape financial headlines.
    Real implementation: uses requests + BeautifulSoup on RSS feeds.
    Falls back to demo data if network is unavailable.
    """
    try:
        import requests
        from bs4 import BeautifulSoup

        feeds = [
            ("https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US", "Yahoo Finance"),
            ("https://www.investing.com/rss/news.rss", "Investing.com"),
        ]
        headlines = []
        for url, source in feeds:
            try:
                resp = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
                soup = BeautifulSoup(resp.content, "xml")
                for item in soup.find_all("item")[:10]:
                    title = item.find("title")
                    if title:
                        headlines.append({"text": title.text.strip(), "source": source, "time": "live"})
            except Exception as e:
                logger.warning(f"Feed {url} failed: {e}")

        return headlines[:max_headlines] if headlines else DEMO_HEADLINES
    except ImportError:
        return DEMO_HEADLINES


# ── Label mapping ─────────────────────────────────────────────────────────────
LABEL_MAP = {
    "positive": "POS",
    "negative": "NEG",
    "neutral":  "NEU",
}


def classify(texts: List[str]) -> List[dict]:
    """Run FinBERT inference; fall back to keyword heuristic if unavailable."""
    pipe = get_finbert()
    if pipe:
        try:
            results = pipe(texts, truncation=True, max_length=512)
            output = []
            for scores in results:
                best = max(scores, key=lambda x: x["score"])
                output.append({
                    "label": LABEL_MAP.get(best["label"].lower(), best["label"]),
                    "confidence": round(best["score"] * 100, 1),
                })
            return output
        except Exception as e:
            logger.warning(f"FinBERT inference error: {e}")

    # ── Keyword heuristic fallback ──
    pos_kw = ["beat", "surges", "rally", "gains", "record", "buyback", "resilient", "high"]
    neg_kw = ["contracts", "pressure", "slide", "exposure", "fears", "decelerates", "decline"]
    out = []
    for t in texts:
        tl = t.lower()
        if any(k in tl for k in pos_kw):
            out.append({"label": "POS", "confidence": 82.0})
        elif any(k in tl for k in neg_kw):
            out.append({"label": "NEG", "confidence": 79.0})
        else:
            out.append({"label": "NEU", "confidence": 74.0})
    return out


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/headlines")
def get_headlines(limit: int = 10):
    """Scrape + classify headlines. Returns up to `limit` results."""
    headlines = scrape_headlines(limit)
    texts = [h["text"] for h in headlines]
    sentiments = classify(texts)
    return [
        {**h, **s}
        for h, s in zip(headlines, sentiments)
    ]


class ClassifyRequest(BaseModel):
    texts: List[str]

@router.post("/classify")
def classify_texts(req: ClassifyRequest):
    """Classify arbitrary list of texts with FinBERT."""
    if not req.texts:
        raise HTTPException(status_code=400, detail="texts list is empty")
    results = classify(req.texts)
    return [{"text": t, **r} for t, r in zip(req.texts, results)]


@router.get("/summary")
def sentiment_summary(limit: int = 50):
    """Aggregate sentiment distribution over recent headlines."""
    headlines = scrape_headlines(limit)
    texts = [h["text"] for h in headlines]
    results = classify(texts)
    counts = {"POS": 0, "NEG": 0, "NEU": 0}
    for r in results:
        counts[r["label"]] = counts.get(r["label"], 0) + 1
    total = len(results) or 1
    return {
        "total": total,
        "distribution": {k: round(v/total*100, 1) for k, v in counts.items()},
        "raw_counts": counts,
    }
