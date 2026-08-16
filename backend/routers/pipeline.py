"""
Pipeline Status Router
Tracks the state of the data ingestion and inference pipeline.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

STEPS = [
    {"id": "scrape",    "label": "Scrape Feeds",     "icon": "🌐", "description": "1,000+ financial news sources"},
    {"id": "parse",     "label": "Parse & Clean",    "icon": "🔧", "description": "Deduplicate, tokenise, normalise"},
    {"id": "finbert",   "label": "FinBERT Inference","icon": "🧠", "description": "Classify POS / NEG / NEU"},
    {"id": "risk",      "label": "Risk Scoring",     "icon": "📊", "description": "Sector × risk-type matrix"},
    {"id": "dashboard", "label": "Dashboard Update", "icon": "📡", "description": "Push to frontend"},
]

# In a real system this would be stored in Redis or a DB
_pipeline_state = {
    "scrape":    "done",
    "parse":     "done",
    "finbert":   "done",
    "risk":      "active",
    "dashboard": "pending",
}


@router.get("/status")
def get_pipeline_status():
    return {
        "steps": [
            {**step, "status": _pipeline_state.get(step["id"], "pending")}
            for step in STEPS
        ],
        "last_run": datetime.utcnow().isoformat() + "Z",
        "headlines_processed": 1247,
        "next_run_seconds": 300,
    }
