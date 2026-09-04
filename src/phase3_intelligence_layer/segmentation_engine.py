from typing import List, Dict, Any
from collections import defaultdict
from models import SegmentProfile

class SegmentationEngine:
    def __init__(self, insights: List[Dict[str, Any]]):
        self.insights = [i for i in insights if i.get("is_relevant")]

    def cluster_segments(self) -> List[SegmentProfile]:
        # Advanced Behavioral Persona Clustering
        clusters = defaultdict(list)
        
        def map_to_persona(item):
            need = str(item.get("semantic_customer_need", "")).lower()
            barrier = str(item.get("barrier_standardized_category", "")).lower()
            workaround = str(item.get("user_workaround", "")).lower()
            
            text_block = f"{need} {barrier} {workaround}"
            
            if any(k in text_block for k in ["size", "sizing", "fit", "measure", "tall"]):
                return "Sizing & Fit Validators", "Shoppers who lack trust in digital size charts and rely on physical workarounds or cross-checking before buying."
            if any(k in text_block for k in ["material", "tactile", "quality", "print", "durability", "fabric"]):
                return "Quality & Durability Researchers", "Shoppers who hesitate to buy because they need to verify fabric quality and durability via reviews."
            if any(k in text_block for k in ["price", "value", "affordable", "money", "sasta"]):
                return "Price & Value Evaluators", "High-intent shoppers who use the wishlist strictly as a staging area to monitor price fluctuations and sales."
            if any(k in text_block for k in ["return", "refund", "credit", "trust", "reliability"]):
                return "Platform Trust Skeptics", "Users who abandon purchases to the wishlist due to fear of difficult return policies or platform unreliability."
            if any(k in text_block for k in ["represent", "accuracy", "visual", "appearance"]):
                return "Representation & Accuracy Checkers", "Users who hold items in the wishlist because they need to verify product description and visual appearance accuracy."
            if any(k in text_block for k in ["styling", "style", "discovery", "compare", "comparison", "personal", "suitability", "brand", "aesthetics"]):
                return "Styling & Comparison Seekers", "Users who treat the wishlist as a mood board to visually mix-and-match items and compare outfits."
                
            return "Other Browsers", "General shoppers lacking a strong specific barrier."
            
        for item in self.insights:
            decision_relevance = item.get("decision_relevance")
            if not decision_relevance or decision_relevance == "E. Unknown":
                stage = str(item.get("shopping_stage", "")).lower()
                if stage in ["discovery", "consideration", "product evaluation", "pre-purchase", "browsing", "cart"]:
                    decision_relevance = "A. Pre-Purchase Decision Evidence"
                elif stage in ["purchase", "post-purchase"]:
                    decision_relevance = "D. Post-Purchase Operational Complaint"
                else:
                    decision_relevance = "E. Unknown"
                    
            if decision_relevance in ["C. General Shopping/Fashion Discussion", "E. Unknown", "D. Post-Purchase Operational Complaint"]:
                continue
                
            persona_name, persona_desc = map_to_persona(item)
            if persona_name != "Other Browsers":
                clusters[(persona_name, persona_desc)].append(item)
            
        segments = []
        total_relevant = len(self.insights)
        
        # Sort clusters by size descending
        sorted_clusters = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)
        
        for i, (persona_tuple, items) in enumerate(sorted_clusters):
            persona_name, persona_desc = persona_tuple
            if len(items) < 3:
                continue
                
            size = len(items)
            perc = (size / total_relevant) * 100 if total_relevant > 0 else 0
            
            behaviors = set()
            barriers = set()
            quotes = []
            
            for item in items:
                stage = item.get("shopping_stage")
                if stage and stage != "Unknown":
                    behaviors.add(stage)
                
                b = item.get("barrier_standardized_category")
                if b and b != "Unknown / Other":
                    barriers.add(b)
                
                quote = item.get("original_text") or item.get("original_comment")
                if quote and len(quotes) < 3:
                    quotes.append(quote)
            
            seg = SegmentProfile(
                segment_id=f"seg_{i+1}_{persona_name.split()[1].lower()}",
                segment_name=persona_name,
                description=persona_desc,
                size=size,
                percentage=perc,
                dominant_barriers=list(barriers)[:3],
                dominant_behaviors=list(behaviors)[:3],
                representative_quotes=quotes,
                barrier_standardized_category="Multiple (Persona Grouping)",
                evidence_strength="Strong" if size > 10 else "Moderate"
            )
            segments.append(seg)
            
        return segments
