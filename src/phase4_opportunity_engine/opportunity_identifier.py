from typing import Dict, Any, List

class OpportunityIdentifier:
    def __init__(self, intelligence_data: Dict[str, Any]):
        self.segments = intelligence_data.get("segments", [])
        self.metrics = intelligence_data.get("metrics", {})
        self.workarounds = self.metrics.get("workaround_frequencies", {})

    def identify(self) -> List[Dict[str, Any]]:
        opportunities = []
        
        for i, segment in enumerate(self.segments):
            segment_name = segment.get("segment_name", "Unknown Segment")
            
            # Synthesize name deterministically based on the persona
            words = segment_name.split()
            opp_name = " ".join(words[:-1]) + " Solution" if len(words) > 1 else segment_name + " Solution"
            
            base_barrier = segment.get("dominant_barriers", ["Unknown"])[0]
            
            # Find related workarounds from the metrics
            related_workarounds = []
            for w_name, w_count in self.workarounds.items():
                if w_count > 0:
                    related_workarounds.append(w_name)
                    
            opportunities.append({
                "opportunity_id": f"opp_{i+1:03d}_{base_barrier[:8].lower()}",
                "opportunity_name": opp_name,
                "user_need": f"Users need to overcome {base_barrier} to confidently purchase.",
                "affected_segments": [segment.get("segment_id")],
                "evidence_count": segment.get("size", 0),
                "existing_workarounds": related_workarounds[:3],
                "base_barrier": base_barrier # temporary field for scorer
            })
            
        return opportunities
