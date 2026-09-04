from typing import List, Dict, Any

class HypothesisManager:
    def __init__(self):
        self.stage_mapping = {
            "size_fit": "Product Re-evaluation",
            "return_policy": "Purchase Confidence",
            "quality": "Product Re-evaluation",
            "price": "Add to Cart",
            "link": "Discovery",
            "photo": "Product Re-evaluation",
            "trust": "Purchase Confidence",
            "fabric": "Product Re-evaluation",
            "styling": "Wishlist Revisit"
        }

    def map_journey_and_level(self, opps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for opp in opps:
            opp_name_lower = opp.get("opportunity_name", "").lower()
            
            # Map journey stage heuristically based on keywords
            assigned_stages = []
            for keyword, stage in self.stage_mapping.items():
                if keyword in opp_name_lower:
                    if stage not in assigned_stages:
                        assigned_stages.append(stage)
                        
            if not assigned_stages:
                assigned_stages = ["General Consideration"]
                
            opp["journey_stage"] = assigned_stages
            
            # Architecture Rule: AI generated insights MUST be Level 2 maximum.
            opp["hypothesis_level"] = "Level 2: AI-Generated Hypothesis"
            
            # Generate a leading behavioral metric to track this hypothesis
            opp["leading_behavioral_metric"] = f"Track user conversion drop-off connected to {assigned_stages[0]}"
            
        return opps
