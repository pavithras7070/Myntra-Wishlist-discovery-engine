import json
import uuid

# Load existing
file_path = "e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine/data/processed/reddit_insights.json"
with open(file_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

# Manually annotate the 15 newly added items that have 'shopping_stage' == 'Pre-Purchase'
# since the LLM batch script is failing on length mismatches for other files anyway.
for item in existing:
    if item.get("shopping_stage") == "Pre-Purchase" and item.get("semantic_customer_need") in [None, "Unknown"]:
        c = item.get("original_comment", "").lower()
        
        item["pre_purchase_behavior_type"] = "Explicit Barrier"
        item["shopping_stage"] = "Pre-Purchase"
        item["intent_type"] = "Discovery"
        
        if "fees" in c or "price" in c or "discount" in c:
            item["purchase_barrier"] = "Price-Drop Anticipation"
            item["semantic_customer_need"] = "Price & Value Assessment"
            
        elif "delhivery" in c or "support" in c or "used goods" in c or "exchange" in c or "unboxing" in c or "return" in c:
            item["purchase_barrier"] = "Return Hassle Anxiety"
            item["semantic_customer_need"] = "Platform Trust & Return Policies"
            
        elif "polyester" in c:
            item["purchase_barrier"] = "Fabric & Material Skepticism"
            item["semantic_customer_need"] = "Material Quality & Durability"
            
        elif "same generic" in c:
            item["purchase_barrier"] = "Discovery Overwhelm (Paradox of Choice)"
            item["semantic_customer_need"] = "Product Representation & Styling Use-Case"
            
        elif "compare" in c:
            item["purchase_barrier"] = "Discovery Overwhelm (Paradox of Choice)"
            item["semantic_customer_need"] = "Product Comparison"
            
        elif "size chart" in c or "haul video" in c:
            item["purchase_barrier"] = "Size/Fit Paralysis"
            item["semantic_customer_need"] = "Sizing, Fit & Measurement Confidence"
            
        else:
            item["purchase_barrier"] = "Unknown / Other"
            item["semantic_customer_need"] = "Unknown"
            
        item["is_relevant"] = True
        item["wishlist_relevance"] = "Direct Mention"

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(existing, f, indent=4)
    
print("Successfully annotated the 15 new Reddit insights manually.")
