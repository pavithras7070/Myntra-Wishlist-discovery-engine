import os
import sys
import json
import logging

# Mute logging to avoid polluting json output
logging.basicConfig(level=logging.ERROR)

# Add parent directory to path so we can import internal modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import init_db, SessionLocal
from database.models import RawConversation
from normalizer.data_normalizer import DataNormalizer
from collectors.playstore_collector import PlayStoreCollector
from collectors.appstore_collector import AppStoreCollector
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

load_dotenv()

import argparse

def fetch_recent_app_reviews(do_playstore, do_appstore):
    init_db()
    
    collectors = []
    if do_playstore:
        collectors.append(PlayStoreCollector(app_id='com.myntra.android', count=50))
    if do_appstore:
        collectors.append(AppStoreCollector(app_name='myntra', app_id=907394059, count=50))
        
    all_raw_records = []
    for collector in collectors:
        records = collector.collect()
        all_raw_records.extend(records)
        
    db = SessionLocal()
    saved_count = 0
    duplicate_count = 0
    skipped_count = 0
    
    for record in all_raw_records:
        normalized = DataNormalizer.normalize_record(record)
        
        # Pre-filter out purely noisy/irrelevant comments
        if not DataNormalizer.is_relevant_for_discovery(normalized['content_clean'] or normalized['content']):
            skipped_count += 1
            continue
            
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
        
        db.add(db_record)
        try:
            db.commit()
            saved_count += 1
        except IntegrityError:
            db.rollback()
            duplicate_count += 1
            
    db.close()
    
    # Return JSON for stdout consumption by the FastAPI backend
    print(json.dumps({
        "success": True,
        "saved_count": saved_count,
        "duplicate_count": duplicate_count,
        "skipped_count": skipped_count
    }))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--playstore', action='store_true', help='Fetch Play Store reviews')
    parser.add_argument('--appstore', action='store_true', help='Fetch App Store reviews')
    args = parser.parse_args()
    
    fetch_recent_app_reviews(args.playstore, args.appstore)
