from typing import List, Dict, Any
from .base_collector import BaseCollector
from datetime import datetime
try:
    from youtube_comment_downloader import *
except Exception as e:
    print(f"DEBUG Youtube Import Error: {e}")
    YoutubeCommentDownloader = None

class YouTubeKeylessCollector(BaseCollector):
    def __init__(self, video_id: str, limit: int = 100):
        self.video_id = video_id
        self.limit = limit

    def collect(self) -> List[Dict[str, Any]]:
        if not YoutubeCommentDownloader:
            print("youtube-comment-downloader is not installed. Skipping YouTube collection.")
            return []
            
        print(f"Fetching keyless comments for YouTube video {self.video_id}...")
        records = []
        try:
            downloader = YoutubeCommentDownloader()
            comments = downloader.get_comments(self.video_id, sort_by=SORT_BY_RECENT)
            
            count = 0
            for comment in comments:
                if count >= self.limit:
                    break
                
                records.append({
                    'platform': 'youtube_keyless',
                    'source_url': f"https://www.youtube.com/watch?v={self.video_id}&lc={comment.get('cid', '')}",
                    'author': comment.get('author', 'unknown'),
                    'content': comment.get('text', ''),
                    'date': datetime.utcnow(), 
                    'rating': None,
                    'metadata': {
                        'video_id': self.video_id,
                        'votes': comment.get('votes', 0),
                        'time_parsed': comment.get('time', '')
                    }
                })
                count += 1
            return records
        except Exception as e:
            print(f"Error fetching from YouTube keyless: {e}")
            return []
