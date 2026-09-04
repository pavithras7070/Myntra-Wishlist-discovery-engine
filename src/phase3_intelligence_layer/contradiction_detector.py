from typing import List, Dict, Any
from models import ContradictionReport

class ContradictionDetector:
    def __init__(self, insights: List[Dict[str, Any]]):
        self.insights = [i for i in insights if i.get("is_relevant")]

    def detect(self, top_barriers: List[str]) -> List[ContradictionReport]:
        reports = []
        
        for barrier in top_barriers:
            if not barrier or barrier == "Unknown":
                continue
                
            supporting = []
            contradicting = []
            
            for item in self.insights:
                if item.get("purchase_barrier") == barrier:
                    # Supporting evidence: User postponed or abandoned
                    if item.get("shopping_stage") in ["Consideration", "Unknown", "Discovery", "Product Evaluation"]:
                        supporting.append(item)
                    # Contradicting evidence: User purchased anyway despite the barrier
                    elif item.get("shopping_stage") == "Purchase":
                        contradicting.append(item)
                        
            supp_count = len(supporting)
            contra_count = len(contradicting)
            total = supp_count + contra_count
            
            if total > 0:
                ratio = contra_count / total
                # Reduce confidence if contradiction ratio is high
                confidence = 1.0 - (ratio * 1.5)
                confidence = max(0.1, min(1.0, confidence))
                
                reports.append(ContradictionReport(
                    insight=f"Barrier: {barrier}",
                    supporting_count=supp_count,
                    contradicting_count=contra_count,
                    contradiction_ratio=round(ratio, 2),
                    contradicting_examples=[c.get("original_text", "") for c in contradicting[:3]],
                    confidence_adjusted=round(confidence, 2)
                ))
                
        return reports
