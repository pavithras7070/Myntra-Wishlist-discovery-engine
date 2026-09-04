import os
import json
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Setup Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

class Insight(BaseModel):
    source_id: str
    platform: str
    date: str
    original_text: str
    is_relevant: bool
    shopping_stage: str
    wishlist_mention: bool
    intent_type: str
    purchase_status: str
    purchase_barrier: List[str]
    uncertainty: str
    user_need: str
    user_workaround: str
    evidence_level: str
    observed_evidence: str

def process_reddit():
    import glob
    print("Loading raw Reddit data...")
    raw_dir = "e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine/data/raw/reddit/2026-09-02"
    files = glob.glob(f"{raw_dir}/reddit_raw*.json")
    
    data = []
    for f_path in files:
        with open(f_path, 'r', encoding='utf-8') as f:
            data.extend(json.load(f))
            
    print(f"Loaded {len(data)} raw comments across {len(files)} files. Processing heuristically...")
    insights = []
    
    for i, item in enumerate(data):
        text = item['original_text'].lower()
        
        # Categorize into TOP 3 themes based on keywords
        if any(k in text for k in ["size", "measure", "fit", "large", "medium", "small"]):
            barrier = "Sizing, Fit & Measurement Confidence"
            need = "Accurate Size Selection"
        elif any(k in text for k in ["cotton", "plastic", "fabric", "material", "feel", "quality"]):
            barrier = "Material Quality & Durability"
            need = "Fabric Quality Verification"
        elif any(k in text for k in ["return", "refund", "fee", "scam"]):
            barrier = "Platform Trust & Return Policies"
            need = "Hassle-Free Returns"
        else:
            barrier = "Product Representation & Styling Use-Case"
            need = "Visualizing the Product"
            
        workaround = "Unknown"
        if "notes app" in text or "measur" in text:
            workaround = "Using measuring tapes and notes apps"
        elif "photos" in text or "reviews" in text:
            workaround = "Relying on customer photos over models"
            
        insight_dict = {
            "source_id": f"reddit_{i}",
            "platform": "reddit",
            "date": item["date"],
            "original_text": item["original_text"],
            "is_relevant": True,
            "shopping_stage": "Pre-Purchase",
            "wishlist_mention": False,
            "intent_type": "Evaluation",
            "purchase_status": "Abandoned",
            "purchase_barrier": [barrier],
            "semantic_customer_need": barrier,
            "uncertainty": need,
            "user_need": need,
            "user_workaround": workaround,
            "evidence_level": "Explicit",
            "evidence_strength": "strong",
            "relevance": "high",
            "observed_evidence": "Extracted from Reddit comments",
            "pre_purchase_behavior_type": "Explicit Barrier"
        }
        insights.append(insight_dict)
            
    out_path = "e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine/data/processed/reddit_insights.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(insights, f, indent=4)
        
    print(f"Successfully processed {len(insights)} Reddit comments and saved to {out_path}.")

if __name__ == "__main__":
    process_reddit()
