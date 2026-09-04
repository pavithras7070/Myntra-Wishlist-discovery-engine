from typing import Dict, Any, List

class PrioritizationScorer:
    def __init__(self, intelligence_data: Dict[str, Any]):
        self.metrics = intelligence_data.get("metrics", {})
        self.contradictions = intelligence_data.get("contradictions", [])
        
        self.weights = {
            "frequency": 0.15,
            "severity": 0.15,
            "purchase_relevance": 0.20,
            "intent_relevance": 0.15,
            "workaround_effort": 0.10,
            "product_leverage": 0.10,
            "evidence_strength": 0.15
        }

    def score(self, opps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        total_conv = self.metrics.get("relevant_conversations", 1)
        
        for opp in opps:
            barrier = opp.get("base_barrier", "")
            evidence_count = opp.get("evidence_count", 0)
            
            # Frequency (relative to total relevant dataset)
            freq_score = min(10.0, (evidence_count / total_conv) * 10.0 * 2) # * 2 modifier to stretch the scale
            
            # Severity (heuristically bounded for AI generated)
            sev_score = 7.5
            
            # Purchase relevance (assume high for extracted barriers)
            pr_score = 8.0
            
            # Intent relevance (assume high)
            ir_score = 8.0
            
            # Workaround Effort (bump if there are known workarounds)
            we_score = 7.0 if opp.get("existing_workarounds") else 4.0
            
            # Implementation Effort (Product Leverage): Lower score means harder to implement.
            # We assign realistic proxy scores based on the domain complexity of the theme.
            theme = opp.get("opportunity_name", "").lower()
            if "sizing" in theme or "fit" in theme:
                pl_score = 2.0  # Very hard (Requires ML/AR size recommendations)
            elif "styling" in theme or "comparison" in theme:
                pl_score = 3.0  # Hard (Requires outfit builder / visual mix-match UI)
            elif "quality" in theme or "durability" in theme:
                pl_score = 4.5  # Medium-Hard (Requires video integration or better zoom UX)
            elif "price" in theme or "value" in theme:
                pl_score = 6.0  # Medium (Price drop alerts / UI tweaks)
            elif "represent" in theme or "accuracy" in theme:
                pl_score = 7.5  # Medium-Easy (Content guidelines / better QA)
            elif "trust" in theme or "platform" in theme:
                pl_score = 9.0  # Easy (Policy UI copy changes, transparency badges)
            else:
                pl_score = 5.0
            
            # Evidence strength - check contradiction report
            es_score = 8.5
            for c in self.contradictions:
                if c.get("insight") == f"Barrier: {barrier}":
                    confidence = c.get("confidence_adjusted", 1.0)
                    es_score = es_score * confidence
                    
            overall = (
                (freq_score * self.weights["frequency"]) +
                (sev_score * self.weights["severity"]) +
                (pr_score * self.weights["purchase_relevance"]) +
                (ir_score * self.weights["intent_relevance"]) +
                (we_score * self.weights["workaround_effort"]) +
                (pl_score * self.weights["product_leverage"]) +
                (es_score * self.weights["evidence_strength"])
            )
            
            opp.update({
                "frequency_score": round(freq_score, 1),
                "severity_score": round(sev_score, 1),
                "purchase_relevance_score": round(pr_score, 1),
                "intent_relevance_score": round(ir_score, 1),
                "workaround_effort_score": round(we_score, 1),
                "product_leverage_score": round(pl_score, 1),
                "evidence_strength_score": round(es_score, 1),
                "overall_opportunity_score": round(overall, 2),
                "confidence": round(es_score / 10.0, 2)
            })
            
            # clean up temporary field
            if "base_barrier" in opp:
                del opp["base_barrier"]
                
        return sorted(opps, key=lambda x: x["overall_opportunity_score"], reverse=True)
