from pydantic import BaseModel
from typing import List

class Opportunity(BaseModel):
    opportunity_id: str
    opportunity_name: str
    user_need: str
    affected_segments: List[str]
    journey_stage: List[str]
    evidence_count: int
    frequency_score: float
    severity_score: float
    purchase_relevance_score: float
    intent_relevance_score: float
    workaround_effort_score: float
    product_leverage_score: float
    evidence_strength_score: float
    overall_opportunity_score: float
    existing_workarounds: List[str]
    leading_behavioral_metric: str
    confidence: float
    hypothesis_level: str

class OpportunityMatrix(BaseModel):
    opportunities: List[Opportunity]
