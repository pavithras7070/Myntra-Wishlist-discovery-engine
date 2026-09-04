from sqlalchemy import Column, String, Integer, DateTime, Boolean, JSON, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class RawConversation(Base):
    __tablename__ = 'raw_conversations'
    id = Column(String, primary_key=True)
    platform = Column(String)
    source_url = Column(String)
    author_hash = Column(String)
    content = Column(String)
    content_clean = Column(String)
    language = Column(String)
    date = Column(DateTime)
    rating = Column(Integer, nullable=True)
    metadata_col = Column('metadata_json', JSON)
    content_hash = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_processed = Column(Boolean, default=False)
    
    # Relationship to analyzed insights
    insights = relationship("AnalyzedInsight", back_populates="conversation")

class AnalyzedInsight(Base):
    __tablename__ = 'analyzed_insights'
    
    id = Column(String, primary_key=True)
    conversation_id = Column(String, ForeignKey('raw_conversations.id'))
    
    # Denormalized for easy querying
    platform = Column(String)
    original_comment = Column(String)
    
    # Stage 1: Relevance
    relevance = Column(String) # high, medium, low, irrelevant
    
    # Stage 2: Behavior
    fashion_category = Column(String, nullable=True)
    shopping_stage = Column(String, nullable=True)
    pre_purchase_behavior_type = Column(String, nullable=True)
    wishlist_mention = Column(Boolean, default=False)
    purchase_status = Column(String, nullable=True)
    semantic_customer_need = Column(String, nullable=True)
    
    # Stage 3: Barrier & Problem
    purchase_barrier = Column(JSON, nullable=True) # List of strings
    uncertainty = Column(JSON, nullable=True)
    user_need = Column(JSON, nullable=True)
    user_workaround = Column(JSON, nullable=True)
    external_platform_mention = Column(JSON, nullable=True)
    comparison_behavior = Column(String, nullable=True)
    decision_factor = Column(JSON, nullable=True)
    
    # Stage 4: Root Cause
    root_cause = Column(JSON, nullable=True)
    opportunity_area = Column(JSON, nullable=True)
    
    # Meta
    evidence_strength = Column(String) # strong, moderate, weak
    confidence = Column(Float)
    llm_model_used = Column(String)
    processing_timestamp = Column(DateTime, default=datetime.utcnow)
    
    conversation = relationship("RawConversation", back_populates="insights")
