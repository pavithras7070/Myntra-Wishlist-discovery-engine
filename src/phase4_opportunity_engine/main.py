import json
import os
from .opportunity_identifier import OpportunityIdentifier
from .prioritization_scorer import PrioritizationScorer
from .hypothesis_manager import HypothesisManager
from .models import OpportunityMatrix, Opportunity

def run_phase4():
    print("Loading intelligence data from Phase 3...")
    processed_dir = 'e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine/data/processed'
    in_path = os.path.join(processed_dir, 'phase3_intelligence.json')
    
    try:
        with open(in_path, 'r', encoding='utf-8') as f:
            intelligence_data = json.load(f)
    except Exception as e:
        print(f"Failed to load {in_path}: {e}")
        return
        
    print("Running Opportunity Identifier...")
    identifier = OpportunityIdentifier(intelligence_data)
    base_opps = identifier.identify()
    
    print("Running Prioritization Scorer...")
    scorer = PrioritizationScorer(intelligence_data)
    scored_opps = scorer.score(base_opps)
    
    print("Running Hypothesis Manager...")
    manager = HypothesisManager()
    final_opps_raw = manager.map_journey_and_level(scored_opps)
    
    # Validate with Pydantic
    final_opps = [Opportunity(**o) for o in final_opps_raw]
    matrix = OpportunityMatrix(opportunities=final_opps)
    
    out_path = os.path.join(processed_dir, 'phase4_opportunity_matrix.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(matrix.model_dump_json(indent=4))
        
    print(f"Phase 4 complete! Opportunity Matrix saved to {out_path}")
    print(f"Total Opportunities Discovered & Scored: {len(final_opps)}")

if __name__ == "__main__":
    run_phase4()
