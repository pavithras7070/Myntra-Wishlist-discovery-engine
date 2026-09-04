import os
from typing import List, Dict, Any
from datetime import datetime
from .base_collector import BaseCollector

try:
    from googleapiclient.discovery import build
except ImportError:
    build = None

class YouTubeCollector(BaseCollector):
    def __init__(self, video_id: str, max_results: int = 100):
        self.video_id = video_id
        self.max_results = max_results
        
        api_key = os.getenv('YOUTUBE_API_KEY')
        self.youtube = None
        
        if build and api_key:
            try:
                self.youtube = build('youtube', 'v3', developerKey=api_key)
            except Exception as e:
                print(f"Failed to initialize YouTube client: {e}")

    def collect(self) -> List[Dict[str, Any]]:
        if not self.youtube:
            print("YouTube API credentials not found. Skipping YouTube collection.")
            return []

        records = []
        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=self.video_id,
                maxResults=min(self.max_results, 100) # API max is 100 per page
            )
            response = request.execute()

            for item in response.get('items', []):
                snippet = item['snippet']['topLevelComment']['snippet']
                records.append({
                    'platform': 'youtube',
                    'source_url': f"https://www.youtube.com/watch?v={self.video_id}&lc={item['id']}",
                    'author': snippet.get('authorDisplayName', 'unknown'),
                    'content': snippet.get('textDisplay', ''),
                    'date': snippet.get('publishedAt'),
                    'rating': None,
                    'metadata': {
                        'video_id': self.video_id,
                        'like_count': snippet.get('likeCount', 0)
                    }
                })
        except Exception as e:
            print(f"Error collecting from YouTube: {e}")
            
        return records
