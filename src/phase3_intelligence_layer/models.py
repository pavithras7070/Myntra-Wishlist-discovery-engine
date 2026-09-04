from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SegmentProfile(BaseModel):
    segment_id: str
    segment_name: str
    description: str
    size: int
    percentage: float
    dominant_barriers: List[str]
    dominant_behaviors: List[str]
    representative_quotes: List[str]
    # Additional Fields added during Phase 2 Taxonomy Alignment
    barrier_standardized_category: Optional[str] = None
    barrier_raw_evidence: Optional[str] = None
    decision_relevance: Optional[str] = None
    wishlist_relevance: Optional[str] = None
    evidence_strength: str

class ContradictionReport(BaseModel):
    insight: str
    supporting_count: int
    contradicting_count: int
    contradiction_ratio: float
    contradicting_examples: List[str]
    confidence_adjusted: float

class QuantitativeMetrics(BaseModel):
    total_conversations: int
    relevant_conversations: int
    relevance_percentage: float
    shopping_stages: Dict[str, int]
    intent_frequencies: Dict[str, int]
    barrier_frequencies: Dict[str, int]
    uncertainty_frequencies: Dict[str, int]
    workaround_frequencies: Dict[str, int]
    wishlist_mentions: int
    decision_relevance_distribution: Dict[str, int]
    wishlist_relevance_distribution: Dict[str, int]
    barrier_co_occurrences: Dict[str, Dict[str, int]]
    pre_purchase_behavior_types: Dict[str, int]
    semantic_customer_needs: Dict[str, Any]

class IntelligenceReport(BaseModel):
    metrics: QuantitativeMetrics
    segments: List[SegmentProfile]
    contradictions: List[ContradictionReport]
