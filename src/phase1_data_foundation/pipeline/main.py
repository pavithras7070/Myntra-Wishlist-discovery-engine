import os
import sys
# Add parent directory to path so we can import internal modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import init_db, SessionLocal
from database.models import RawConversation
from normalizer.data_normalizer import DataNormalizer
from collectors.playstore_collector import PlayStoreCollector
from collectors.reddit_collector import RedditCollector
from collectors.youtube_collector import YouTubeCollector
from collectors.appstore_collector import AppStoreCollector
from collectors.youtube_collector_keyless import YouTubeKeylessCollector
from collectors.product_review_collector import ProductReviewCrawler
from collectors.forum_collector import ForumCollector
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

load_dotenv()

def run_pipeline():
    print("Initializing Database...")
    init_db()
    
    collectors = [
        # App Stores (Now protected by keyword pre-filter!)
        PlayStoreCollector(app_id='com.myntra.android', count=3000),
        AppStoreCollector(app_name='myntra', app_id=907394059, count=500),
        
        # Product Reviews via Category Crawler
        ProductReviewCrawler(category_url='https://www.myntra.com/womens-western-wear', max_products=250),
        
        # YouTube Videos (needs specific video_id, skipping for massive batch)
        # YouTubeKeylessCollector(video_id='dummy_id', limit=500)
    ]
    
    all_raw_records = []
    
    for collector in collectors:
        print(f"Running collector: {collector.__class__.__name__}...")
        records = collector.collect()
        print(f"Found {len(records)} records from {collector.__class__.__name__}")
        all_raw_records.extend(records)
        
    print(f"Total raw records collected: {len(all_raw_records)}")
    
    db = SessionLocal()
    saved_count = 0
    duplicate_count = 0
    skipped_irrelevant_count = 0
    
    for record in all_raw_records:
        normalized = DataNormalizer.normalize_record(record)
        
        # Apply Keyword Pre-Filter
        if not DataNormalizer.is_relevant_for_discovery(normalized['content_clean'] or normalized['content']):
            skipped_irrelevant_count += 1
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
            # Duplicate content_hash
            db.rollback()
            duplicate_count += 1
            
    db.close()
    
    print(f"Pipeline completed successfully.")
    print(f"New records saved: {saved_count}")
    print(f"Irrelevant records skipped (pre-filter): {skipped_irrelevant_count}")
    print(f"Duplicates skipped: {duplicate_count}")

if __name__ == "__main__":
    run_pipeline()
