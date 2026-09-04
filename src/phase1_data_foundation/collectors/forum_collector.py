from typing import List, Dict, Any
from .base_collector import BaseCollector
from datetime import datetime

try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

class ForumCollector(BaseCollector):
    def __init__(self, query: str, limit: int = 20):
        self.query = query
        self.limit = limit

    def collect(self) -> List[Dict[str, Any]]:
        if not DDGS:
            print("duckduckgo-search is not installed. Skipping Forum Collector.")
            return []
            
        print(f"Searching web forums for query: '{self.query}'")
        records = []
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(self.query, max_results=self.limit))
                
                for res in results:
                    records.append({
                        'platform': 'web_forum_search',
                        'source_url': res.get('href', ''),
                        'author': 'unknown_search_result',
                        'content': res.get('body', ''), # Using search snippet as content
                        'date': datetime.utcnow(),
                        'rating': None,
                        'metadata': {
                            'search_query': self.query,
                            'title': res.get('title', '')
                        }
                    })
        except Exception as e:
            print(f"Error during forum search: {e}")
            
        return records
