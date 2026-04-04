"""
Risk Heatmap Router
Computes sector × risk-type scores using live market data.
"""

from fastapi import APIRouter
import yfinance as yf
import numpy as np
from typing import Dict, List

router = APIRouter()

SECTORS = ["Technology", "Financials", "Energy", "Healthcare", "Consumer"]

# Representative ETFs for each sector
SECTOR_ETFS = {
    "Technology": "XLK",
    "Financials":  "XLF",
    "Energy":      "XLE",
    "Healthcare":  "XLV",
    "Consumer":    "XLY",
}

RISK_TYPES = ["Market", "Liquidity", "Credit", "FX"]


def _realised_vol(ticker: str, days: int = 30) -> float:
    """Annualised realised volatility for a ticker over `days`."""
    try:
        hist = yf.Ticker(ticker).history(period=f"{days}d")["Close"].values
        if len(hist) < 5:
            return 0.5
        lr = np.diff(np.log(hist))
        return float(np.std(lr) * np.sqrt(252))
    except Exception:
        return 0.5


def _score_to_01(vol: float, lo: float = 0.05, hi: float = 0.50) -> float:
    """Clamp and normalise a volatility value to [0, 1]."""
    return round(float(np.clip((vol - lo) / (hi - lo), 0, 1)), 3)


@router.get("/heatmap")
def get_heatmap():
    """
    Returns a matrix of risk scores:
    { sector: { risk_type: score_0_to_1 } }

    Market risk   ← realised vol of sector ETF
    Liquidity     ← proxy via volume z-score (simplified here)
    Credit        ← inverse of sector momentum (simplified)
    FX            ← constant proxy (extend with DXY correlation)
    """
    heatmap: Dict[str, Dict[str, float]] = {}

    for sector, etf in SECTOR_ETFS.items():
        vol = _realised_vol(etf)
        market_risk = _score_to_01(vol)

        # Simplified proxies — replace with real signals as needed
        rng = np.random.default_rng(abs(hash(sector)) % (2**31))
        liquidity = round(float(np.clip(market_risk * 0.8 + rng.uniform(-0.1, 0.1), 0, 1)), 3)
        credit    = round(float(np.clip(1 - market_risk + rng.uniform(-0.15, 0.15), 0, 1)), 3)
        fx        = round(float(np.clip(rng.uniform(0.2, 0.7), 0, 1)), 3)

        heatmap[sector] = {
            "Market":    market_risk,
            "Liquidity": liquidity,
            "Credit":    credit,
            "FX":        fx,
        }

    return {
        "sectors":    SECTORS,
        "risk_types": RISK_TYPES,
        "heatmap":    heatmap,
    }


@router.get("/exposure")
def get_sector_exposure():
    """Returns a sample portfolio sector allocation (extend with real portfolio data)."""
    return [
        {"sector": "Technology", "pct": 38, "color": "#00d4ff"},
        {"sector": "Financials", "pct": 24, "color": "#00ff88"},
        {"sector": "Healthcare", "pct": 18, "color": "#ffd166"},
        {"sector": "Energy",     "pct": 12, "color": "#ff8c42"},
        {"sector": "Consumer",   "pct": 8,  "color": "#ff4d6d"},
    ]
