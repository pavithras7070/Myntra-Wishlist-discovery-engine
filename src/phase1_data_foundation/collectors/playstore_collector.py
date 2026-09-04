from typing import List, Dict, Any
from .base_collector import BaseCollector
from google_play_scraper import reviews, Sort

class PlayStoreCollector(BaseCollector):
    def __init__(self, app_id: str, lang: str = 'en', country: str = 'in', count: int = 100):
        self.app_id = app_id
        self.lang = lang
        self.country = country
        self.count = count

    def collect(self) -> List[Dict[str, Any]]:
        """Collect recent reviews for the configured app."""
        result, _ = reviews(
            self.app_id,
            lang=self.lang,
            country=self.country,
            sort=Sort.NEWEST,
            count=self.count
        )

        records = []
        for review in result:
            records.append({
                'platform': 'google_play',
                'source_url': f"https://play.google.com/store/apps/details?id={self.app_id}&reviewId={review['reviewId']}",
                'author': review.get('userName', 'unknown'),
                'content': review.get('content', ''),
                'date': review.get('at'),
                'rating': review.get('score'),
                'metadata': {
                    'app_id': self.app_id,
                    'thumbs_up_count': review.get('thumbsUpCount', 0),
                    'review_created_version': review.get('reviewCreatedVersion')
                }
            })
        return records
