import json
import glob
import os
from quantitative_aggregator import QuantitativeAggregator
from segmentation_engine import SegmentationEngine
from contradiction_detector import ContradictionDetector
from models import IntelligenceReport

def run_phase3():
    print("Loading insights from Phase 2...")
    processed_dir = 'e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine/data/processed'
    
    insight_files = glob.glob(os.path.join(processed_dir, '*_insights.json'))
    
    all_insights = []
    for f in insight_files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                data = json.load(file)
                all_insights.extend(data)
        except Exception as e:
            print(f"Failed to load {f}: {e}")
            
    print(f"Loaded {len(all_insights)} total insights across all sources.")
    
    # --- Inject standardized barrier themes based on actual raw barriers ---
    def standardize_barrier(raw: str) -> str:
        if not raw:
            return "Unknown / Other"
        r = raw.lower()
        if any(k in r for k in ["size", "fit", "measure", "waist", "length", "too big", "too small", "inseam"]):
            return "Size/Fit Paralysis"
        elif any(k in r for k in ["quality", "material", "fabric", "durability", "cheap", "print", "comfort"]):
            return "Fabric & Material Skepticism"
        elif any(k in r for k in ["photo", "picture", "color", "look", "match actual", "misrepresentation"]):
            return "Visual Misrepresentation Fear"
        elif any(k in r for k in ["price", "cost", "expensive", "sale", "discount", "tax", "overpriced"]):
            return "Price-Drop Anticipation"
        elif any(k in r for k in ["return", "exchange", "refund", "policy", "deny"]):
            return "Return Hassle Anxiety"
        elif any(k in r for k in ["occasion", "match", "wardrobe", "event"]):
            return "Occasion Matching & Wardrobe Coordination"
        elif any(k in r for k in ["too many", "options", "decide", "discovery", "similar"]):
            return "Discovery Overwhelm (Paradox of Choice)"
        elif any(k in r for k in ["app", "bug", "tech", "wishlist", "bag", "deliverable", "account", "missing brand tag", "tag", "packaging", "platform"]):
            return "Checkout / App Friction"
        return "Unknown / Other"
        
    for item in all_insights:
        raw_b = item.get("purchase_barrier")
        if isinstance(raw_b, list) and len(raw_b) > 0:
            item["barrier_standardized_category"] = standardize_barrier(raw_b[0])
        elif isinstance(raw_b, str):
            item["barrier_standardized_category"] = standardize_barrier(raw_b)
        else:
            item["barrier_standardized_category"] = "Unknown / Other"
    # ----------------------------------------------------------------------

    
    # 1. Quantitative Aggregator
    print("Running Quantitative Aggregator...")
    aggregator = QuantitativeAggregator(all_insights)
    metrics = aggregator.aggregate()
    
    # 2. Segmentation Engine
    print("Running Segmentation Engine...")
    segmenter = SegmentationEngine(all_insights)
    segments = segmenter.cluster_segments()
    
    # 3. Contradiction Detector
    print("Running Contradiction Detector...")
    detector = ContradictionDetector(all_insights)
    top_barriers = [b for b, count in sorted(metrics.barrier_frequencies.items(), key=lambda x: x[1], reverse=True)[:5]]
    contradictions = detector.detect(top_barriers)
    
    # Combine into final report
    report = IntelligenceReport(
        metrics=metrics,
        segments=segments,
        contradictions=contradictions
    )
    
    out_path = os.path.join(processed_dir, 'phase3_intelligence.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(report.model_dump_json(indent=4))
        
    print(f"Phase 3 complete! Intelligence report saved to {out_path}")

if __name__ == "__main__":
    run_phase3()
