import os
from typing import List, Dict, Any
from datetime import datetime
from .base_collector import BaseCollector
try:
    import praw
except ImportError:
    praw = None

class RedditCollector(BaseCollector):
    def __init__(self, subreddit_name: str, limit: int = 100):
        self.subreddit_name = subreddit_name
        self.limit = limit
        
        client_id = os.getenv('REDDIT_CLIENT_ID')
        client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        user_agent = os.getenv('REDDIT_USER_AGENT', 'myntra_scraper:v1.0')
        
        self.reddit = None
        if praw and client_id and client_secret:
            try:
                self.reddit = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent
                )
            except Exception as e:
                print(f"Failed to initialize Reddit client: {e}")

    def collect(self) -> List[Dict[str, Any]]:
        """Collect recent posts from the subreddit."""
        if not self.reddit:
            print("Reddit API credentials not found or praw not installed. Skipping Reddit collection.")
            return []

        records = []
        try:
            subreddit = self.reddit.subreddit(self.subreddit_name)
            for submission in subreddit.new(limit=self.limit):
                records.append({
                    'platform': 'reddit',
                    'source_url': f"https://reddit.com{submission.permalink}",
                    'author': submission.author.name if submission.author else 'deleted',
                    'content': f"{submission.title}\n{submission.selftext}",
                    'date': datetime.utcfromtimestamp(submission.created_utc),
                    'rating': None,
                    'metadata': {
                        'subreddit': self.subreddit_name,
                        'score': submission.score,
                        'num_comments': submission.num_comments
                    }
                })
        except Exception as e:
            print(f"Error collecting from Reddit: {e}")
            
        return records
