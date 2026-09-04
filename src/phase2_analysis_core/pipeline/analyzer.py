import uuid
import time
from typing import List
from database.connection import SessionLocal, init_db
from database.models import RawConversation, AnalyzedInsight
from llm.client import GroqClient
from llm.prompts import SYSTEM_PROMPT

class InsightAnalyzer:
    def __init__(self, batch_size: int = 2): # Reduced to 2 to avoid 413 and 429 errors
        self.batch_size = batch_size
        self.db = SessionLocal()
        try:
            self.llm = GroqClient()
        except ValueError as e:
            print(f"Failed to initialize LLM: {e}")
            self.llm = None

    def run(self, max_records: int = 100):
        if not self.llm:
            print("Cannot run analysis without LLM client. Check your .env file.")
            return

        print(f"Fetching up to {max_records} unprocessed records for analysis...")
        
        # Get unprocessed records
        records = self.db.query(RawConversation).filter(RawConversation.is_processed == False).limit(max_records).all()
        
        if not records:
            print("No unprocessed records found!")
            return
            
        print(f"Found {len(records)} records. Processing in batches of {self.batch_size}...")
        
        for i in range(0, len(records), self.batch_size):
            batch = records[i:i + self.batch_size]
            # Truncate content to avoid 413 Request Too Large
            batch_dicts = [{"id": r.id, "content": (r.content_clean or r.content)[:1000]} for r in batch]
            
            print(f"Processing batch {i//self.batch_size + 1}/{(len(records) + self.batch_size - 1)//self.batch_size}...")
            results = self.llm.analyze_batch(SYSTEM_PROMPT, batch_dicts)
            
            if not results or len(results) != len(batch):
                print(f"Batch failed or returned mismatched results. Expected {len(batch)}, got {len(results) if results else 0}")
                # Sleep before retrying next batch due to rate limit
                print("Sleeping for 20 seconds to respect Groq rate limits...")
                time.sleep(20)
                continue
                
            # Save results
            for record, result in zip(batch, results):
                insight = AnalyzedInsight(
                    id=str(uuid.uuid4()),
                    conversation_id=record.id,
                    platform=record.platform,
                    original_comment=record.content,
                    
                    relevance=result.get("relevance", "irrelevant"),
                    fashion_category=result.get("fashion_category"),
                    shopping_stage=result.get("shopping_stage"),
                    pre_purchase_behavior_type=result.get("pre_purchase_behavior_type"),
                    wishlist_mention=result.get("wishlist_mention", False),
                    purchase_status=result.get("purchase_status"),
                    semantic_customer_need=result.get("semantic_customer_need"),
                    
                    purchase_barrier=result.get("purchase_barrier"),
                    uncertainty=result.get("uncertainty"),
                    user_need=result.get("user_need"),
                    user_workaround=result.get("user_workaround"),
                    external_platform_mention=result.get("external_platform_mention"),
                    comparison_behavior=result.get("comparison_behavior"),
                    decision_factor=result.get("decision_factor"),
                    
                    root_cause=result.get("root_cause"),
                    opportunity_area=result.get("opportunity_area"),
                    
                    evidence_strength=result.get("evidence_strength", "weak"),
                    confidence=result.get("confidence", 0.0),
                    llm_model_used="groq/compound-mini"
                )
                
                self.db.add(insight)
                record.is_processed = True
                
            self.db.commit()
            print(f"Successfully committed batch {i//self.batch_size + 1}")
            
            # Sleep to respect TPM limit (12000 tokens per minute)
            print("Sleeping for 15 seconds to respect Groq TPM rate limit...")
            time.sleep(15)
            
        print("Analysis run complete.")
