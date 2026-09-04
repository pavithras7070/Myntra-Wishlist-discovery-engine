import json
import glob
import os
from collections import Counter

# Load all evidence
insights = []
for f in glob.glob('data/processed/*_insights.json'):
    if 'phase2' in f or 'insights' in f:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                if item.get("is_relevant"):
                    if "youtube" in f.lower():
                        item["source_platform"] = "YouTube"
                    elif "app_store" in f.lower():
                        item["source_platform"] = "App Store"
                    elif "playstore" in f.lower():
                        item["source_platform"] = "Play Store"
                    elif "myntra_web" in f.lower():
                        item["source_platform"] = "Myntra Web"
                    insights.append(item)

# Mapping logic
new_themes = {
    "Pre-Purchase Confidence & Validation Deficits": {
        "Total Count": 0,
        "Sources Count": 0,
        "Evidence Strength Indicator": "Strong",
        "Raw Counts By Source": {},
        "Addressing": "Fit, Size, and Quality uncertainty preventing wishlisted items from moving to cart."
    },
    "Decision Overload & Comparison Friction": {
        "Total Count": 0,
        "Sources Count": 0,
        "Evidence Strength Indicator": "Moderate",
        "Raw Counts By Source": {},
        "Addressing": "Choice paralysis when comparing multiple shortlisted items on the wishlist."
    },
    "Intent-Driven Delay": {
        "Total Count": 0,
        "Sources Count": 0,
        "Evidence Strength Indicator": "Strong",
        "Raw Counts By Source": {},
        "Addressing": "Users intentionally waiting for price drops, sales, or specific future occasions."
    },
    "Product Representation & External Research Leakage": {
        "Total Count": 0,
        "Sources Count": 0,
        "Evidence Strength Indicator": "High",
        "Raw Counts By Source": {},
        "Addressing": "Leaving the app for YouTube/social media due to untrustworthy native product imagery."
    },
    "Wishlist Stagnation & Availability Blockers": {
        "Total Count": 0,
        "Sources Count": 0,
        "Evidence Strength Indicator": "Moderate",
        "Raw Counts By Source": {},
        "Addressing": "Friction from out-of-stock items, delivery constraints, or generic post-purchase issues."
    }
}

for item in insights:
    barrier = (item.get("purchase_barrier") or item.get("barrier_standardized_category") or "").lower()
    source = item.get("source_platform", "Unknown")
    
    # Simple heuristic mapping based on keywords
    if any(k in barrier for k in ["size", "fit", "measure", "quality", "material", "torn", "durability", "tight", "loose"]):
        theme = "Pre-Purchase Confidence & Validation Deficits"
    elif any(k in barrier for k in ["price", "expensive", "fee", "cost", "hike", "discount", "offer"]):
        theme = "Intent-Driven Delay"
    elif any(k in barrier for k in ["image", "photo", "color", "discrepancy", "link", "not found", "unavailable", "look", "represent"]):
        theme = "Product Representation & External Research Leakage"
    elif any(k in barrier for k in ["compare", "choose", "decide", "too many", "options"]):
        theme = "Decision Overload & Comparison Friction"
    else:
        theme = "Wishlist Stagnation & Availability Blockers"

    new_themes[theme]["Total Count"] += 1
    if source not in new_themes[theme]["Raw Counts By Source"]:
        new_themes[theme]["Raw Counts By Source"][source] = 0
    new_themes[theme]["Raw Counts By Source"][source] += 1

for t in new_themes:
    new_themes[t]["Sources Count"] = len(new_themes[t]["Raw Counts By Source"])

out_path = 'data/processed/phase3_aggregated_metrics.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(new_themes, f, indent=4)
print(f"Successfully generated new themes to {out_path}")
