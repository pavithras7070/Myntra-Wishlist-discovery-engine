import json
import os
from collections import defaultdict

data = json.load(open("e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine/data/processed/phase3_intelligence.json", encoding="utf-8"))

metrics = data.get("metrics", {})
needs_counts = metrics.get("semantic_customer_needs", {})

semantic_metrics = {}

for need, data_dict in needs_counts.items():
    if not need or need == "Unknown":
        continue
        
    count = data_dict.get("count", 0)
    avg_severity = data_dict.get("avg_severity", 1.0)
    avg_relevance = data_dict.get("avg_relevance", 1.0)
    workarounds = data_dict.get("workarounds", {})
    
    # Calculate an Evidence Strength Indicator based on count and severity
    if count >= 15 or (count > 10 and avg_severity >= 1.8):
        strength = "Strong"
    elif count >= 5 or (count > 2 and avg_severity >= 1.5):
        strength = "Moderate"
    else:
        strength = "Low"
        
    # Get top 2 workarounds
    top_workarounds = sorted(workarounds.items(), key=lambda x: x[1], reverse=True)[:2]
    workaround_str = ", ".join([w[0] for w in top_workarounds]) if top_workarounds else "None recorded"
        
    sources_dict = data_dict.get("sources", {})
    actual_sources_count = len(sources_dict.keys()) if sources_dict else 1
    
    semantic_metrics[need] = {
        "Total Count": count,
        "Sources Count": actual_sources_count,
        "Evidence Strength Indicator": strength,
        "Severity Score": round(avg_severity, 2),
        "Relevance Score": round(avg_relevance, 2),
        "Common Workarounds": workaround_str,
        "Raw Counts By Source": data_dict.get("sources", {"All Sources": count}),
        "Addressing": f"Semantic Need: {need}"
    }

with open("e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine/data/processed/phase3_aggregated_metrics.json", "w", encoding="utf-8") as f:
    json.dump(semantic_metrics, f, indent=4)

print(f"Dynamically generated semantic metrics for {len(semantic_metrics)} distinct underlying needs.")
