import sys
import os
import json
from datetime import datetime

# Setup paths
sys.path.append(os.path.join(os.getcwd(), 'src', 'phase1_data_foundation'))
sys.path.append(os.path.join(os.getcwd(), 'src', 'phase2_analysis_core'))

from dotenv import load_dotenv
load_dotenv()

from collectors.reddit_collector_keyless import RedditKeylessCollector
from database.connection import SessionLocal, init_db
from database.models import RawConversation
from normalizer.data_normalizer import DataNormalizer

from llm.client import GroqClient
from llm.prompts import SYSTEM_PROMPT

# 1. Fetch Reddit Data
queries = ['myntra wishlist', 'myntra wait', 'myntra size', 'myntra cart', 'myntra quality']
collector = RedditKeylessCollector(search_queries=queries, limit=50)
records = collector.collect()

if not records:
    print("No records found. Exiting.")
    sys.exit(0)

# 2. Save to Phase 1 DB
print("Saving to database...")
init_db()
db = SessionLocal()
for record in records:
    normalized = DataNormalizer.normalize_record(record)
    db_record = RawConversation(
        platform=normalized['platform'],
        source_url=normalized['source_url'],
        author_hash=normalized['author_hash'],
        content=normalized['content'],
        content_clean=normalized['content_clean'],
        language=normalized['language'],
        date=normalized['date'],
        rating=normalized['rating'],
        metadata_json=normalized['metadata_json'],
        content_hash=normalized['content_hash']
    )
    try:
        db.add(db_record)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Skipping duplicate record: {e}")

# 3. Analyze with LLM
print("Analyzing with LLM...")
llm = GroqClient()
# Convert records to dict with 'id' for the LLM client
for i, r in enumerate(records):
    r['id'] = str(i)
    r['content_clean'] = r['content']
    
new_insights = llm.analyze_batch(SYSTEM_PROMPT, records)

for i, parsed in enumerate(new_insights):
    parsed['source_id'] = 'live_reddit'
    parsed['platform'] = records[i].get('platform', 'reddit')
    parsed['date'] = records[i].get('date', str(datetime.utcnow()))
    parsed['original_text'] = records[i].get('content', '')
    parsed['is_relevant'] = True

# 4. Save Insights
insights_file = 'data/processed/reddit_insights.json'
with open(insights_file, 'w', encoding='utf-8') as f:
    json.dump(new_insights, f, indent=4, default=str)

print(f'Successfully saved {len(new_insights)} insights to {insights_file}')
