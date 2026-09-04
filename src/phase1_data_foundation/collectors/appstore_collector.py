import requests
from typing import List, Dict, Any
from .base_collector import BaseCollector
from datetime import datetime

class AppStoreCollector(BaseCollector):
    def __init__(self, app_name: str, app_id: int, country: str = 'in', count: int = 50):
        self.app_name = app_name
        self.app_id = app_id
        self.country = country
        self.count = min(count, 500) # RSS limit is 500

    def collect(self) -> List[Dict[str, Any]]:
        print(f"Fetching reviews for {self.app_name} on App Store via iTunes RSS...")
        records = []
        
        # iTunes RSS feed for customer reviews
        url = f"https://itunes.apple.com/{self.country}/rss/customerreviews/id={self.app_id}/sortBy=mostRecent/json"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Failed to fetch App Store RSS feed. Status: {response.status_code}")
                return []
                
            data = response.json()
            entries = data.get('feed', {}).get('entry', [])
            
            # If there's only 1 entry, it might not be a list in some JSON parses of this feed
            if isinstance(entries, dict):
                entries = [entries]
                
            # First entry is usually metadata about the app, not a review
            for entry in entries:
                if len(records) >= self.count:
                    break
                    
                if 'author' not in entry:
                    continue # Skip metadata entry
                    
                records.append({
                    'platform': 'apple_app_store',
                    'source_url': entry.get('link', {}).get('attributes', {}).get('href', f"https://apps.apple.com/app/id{self.app_id}"),
                    'author': entry.get('author', {}).get('name', {}).get('label', 'unknown'),
                    'content': entry.get('content', {}).get('label', ''),
                    'date': datetime.utcnow(), # RSS doesn't always provide a clean date, use fallback
                    'rating': int(entry.get('im:rating', {}).get('label', 0)),
                    'metadata': {
                        'app_name': self.app_name,
                        'title': entry.get('title', {}).get('label', '')
                    }
                })
            return records
        except Exception as e:
            print(f"Error fetching from iTunes RSS: {e}")
            return []
