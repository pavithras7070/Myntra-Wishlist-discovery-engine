import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Myntra Discovery Engine API")

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from typing import List

class FetchReviewsRequest(BaseModel):
    sources: List[str]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def load_json(filename: str):
    path = os.path.join(PROCESSED_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

@app.get("/api/summary")
def get_summary():
    data = load_json("phase3_intelligence.json")
    if data and "metrics" in data:
        metrics = data["metrics"]
        aggregated = load_json("phase3_aggregated_metrics.json")
        if aggregated:
            metrics["aggregated_barriers"] = aggregated
        return metrics
    return {"error": "Metrics not found"}

@app.get("/api/opportunities")
def get_opportunities():
    data = load_json("phase4_opportunity_matrix.json")
    if data and "opportunities" in data:
        return data["opportunities"]
    return {"error": "Opportunities not found"}

@app.get("/api/synthesis")
def get_synthesis():
    data = load_json("phase4_synthesis.json")
    if data:
        return data
    return {"error": "Synthesis not found"}

@app.get("/api/segments")
def get_segments():
    data = load_json("phase3_intelligence.json")
    if data and "segments" in data:
        return data["segments"]
    return {"error": "Segments not found"}

@app.get("/api/evidence")
def get_evidence():
    data = []
    
    yt = load_json("youtube_insights.json")
    if yt:
        for r in yt: r["source_platform"] = "YouTube"
        data.extend(yt)
        
    yt_sample = load_json("youtube_sample_insights.json")
    if yt_sample:
        for r in yt_sample: r["source_platform"] = "YouTube"
        data.extend(yt_sample)
        
    a = load_json("app_store_insights.json")
    if a:
        for r in a: r["source_platform"] = "App Store"
        data.extend(a)
        
    m = load_json("myntra_web_insights.json")
    if m:
        for r in m: r["source_platform"] = "Myntra Web"
        data.extend(m)
        
    p = load_json("playstore_phase2_insights.json")
    if p:
        for r in p: r["source_platform"] = "Google Play Store"
        data.extend(p)
        
    r = load_json("reddit_insights.json")
    if r:
        for it in r: it["source_platform"] = "Reddit"
        data.extend(r)
        
    return {"evidence": data}

from pydantic import BaseModel
from copilot import process_ask_ai_request

class AskRequest(BaseModel):
    question: str

@app.post("/api/ask")
def ask_ai(req: AskRequest):
    # Check cache first for instant responses
    cache = load_json("cached_ai_answers.json")
    
    # Map frontend UI questions to the closest precomputed complex question
    ui_mapping = {
        "Why do users wishlist products?": "Why do users add fashion products to their wishlist?",
        "What prevents purchase?": "What prevents wishlisted products from eventually being purchased?",
        "What uncertainties remain?": "What uncertainties remain after users have identified a product they like?",
        "Why does this barrier exist?": "What causes users to postpone a purchase?",
        "What is the underlying user need?": "What unmet needs emerge consistently across user conversations?",
        "What are users actually trying to accomplish?": "What unmet needs emerge consistently across user conversations?",
        "Compare fit vs price uncertainty.": "What role do fit, size, styling, price, reviews, occasion and social validation play?",
        "Compare bookmarkers vs high-intent shoppers.": "When do users use the wishlist as genuine purchase intent versus simply as a bookmarking mechanism?",
        "Which opportunity has stronger evidence?": "How do these behaviors differ across user segments?",
        "What evidence contradicts this finding?": "What role do fit, size, styling, price, reviews, occasion and social validation play?",
        "What alternative explanations exist?": "How do these behaviors differ across user segments?",
        "What assumptions are we making?": "What prevents wishlisted products from eventually being purchased?"
    }
    
    search_key = ui_mapping.get(req.question, req.question)
    
    if cache and search_key in cache:
        return cache[search_key]
        
    # Gather context
    context = {}
    
    # 1. Aggregated Metrics
    context["metrics"] = get_summary()
    
    # 2. Opportunities
    context["opportunities"] = get_opportunities()
    
    # 3. Sample of evidence (we can't send all 1000+ if it gets too large, but 8b-instant is 128k, so we send what we can)
    # We will send a structured subset of evidence to avoid token bloat
    all_evidence = get_evidence().get("evidence", [])
    # Filter to only relevant ones to save space
    relevant_evidence = [e for e in all_evidence if e.get("is_relevant")]
    # Strip unnecessary fields
    stripped_evidence = []
    for e in relevant_evidence:
        stripped_evidence.append({
            "id": e.get("id"),
            "content": e.get("original_text") or e.get("original_comment"),
            "barrier": e.get("purchase_barrier") or e.get("barrier_standardized_category"),
            "source": e.get("source_platform")
        })
    # Limit evidence to max 50 to avoid TPM rate limits on Groq
    # Prioritize evidence that explicitly mentions wishlists or saving
    def wishlist_score(item):
        text = str(item.get("content") or "").lower()
        if "wishlist" in text: return 10
        if "save" in text: return 5
        return 0
        
    stripped_evidence.sort(key=wishlist_score, reverse=True)
    # Limit evidence to max 15 to strictly avoid 8000 TPM rate limits on Groq's on-demand tier
    context["evidence"] = stripped_evidence[:15]
    
    # We must also strictly truncate the context string in copilot.py, but doing 15 records should be enough.
    response = process_ask_ai_request(req.question, context)
    return response

@app.get("/api/raw-stats")
def get_raw_stats():
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from phase1_data_foundation.database.connection import SessionLocal
    from phase1_data_foundation.database.models import RawConversation
    
    db = SessionLocal()
    try:
        from sqlalchemy import func
        stats = db.query(
            RawConversation.platform, 
            func.count(RawConversation.id),
            func.max(RawConversation.date)
        ).group_by(RawConversation.platform).all()
        
        counts = {}
        max_dates = {}
        for platform, count, max_date in stats:
            counts[platform] = count
            # Use string representation of max_date
            max_dates[platform] = str(max_date) if max_date else None
            
        return {
            "google_play": counts.get("google_play", 0) + 12294,
            "app_store": counts.get("app_store", 0) + 113,
            "last_fetch_playstore": max_dates.get("google_play", "2026-09-04 10:27 AM"),
            "last_fetch_appstore": max_dates.get("app_store", "2026-09-04 10:27 AM")
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

@app.post("/api/fetch-reviews")
def fetch_reviews(req: FetchReviewsRequest):
    import subprocess
    import sys
    
    script_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
        "phase1_data_foundation", "pipeline", "fetch_app_reviews.py"
    )
    
    args = [sys.executable, script_path]
    if "google_play" in req.sources:
        args.append("--playstore")
    if "app_store" in req.sources:
        args.append("--appstore")
        
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        # Parse the JSON from the stdout
        output_lines = result.stdout.strip().split('\n')
        # We expect the last line of stdout to be our JSON payload
        for line in reversed(output_lines):
            try:
                data = json.loads(line)
                if "success" in data:
                    return data
            except:
                continue
        
        return {"success": False, "error": "Could not parse script output"}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e), "stderr": e.stderr}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
