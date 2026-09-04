import json
import glob

def fix_wishlist_relevance():
    files = glob.glob('e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine/data/processed/*_insights.json')
    
    for f_path in files:
        with open(f_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        modified = False
        for item in data:
            current_wr = item.get("wishlist_relevance")
            
            # Heuristic for wishlist relevance
            if item.get("wishlist_mention") is True or "wishlist" in str(item.get("original_text", "")).lower() or "cart" in str(item.get("original_text", "")).lower():
                new_wr = "Direct Wishlist Evidence"
            elif item.get("shopping_stage") in ["Pre-Purchase", "Discovery", "Consideration", "Product Evaluation", "Evaluation"]:
                new_wr = "Indirect Wishlist-Relevant Evidence"
            else:
                new_wr = "General Shopping Evidence"
                
            if current_wr != new_wr:
                item["wishlist_relevance"] = new_wr
                modified = True
                
        if modified:
            with open(f_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"Updated {f_path}")

if __name__ == "__main__":
    fix_wishlist_relevance()
