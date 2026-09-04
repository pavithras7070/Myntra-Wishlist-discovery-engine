import time
import json
from typing import List, Dict, Any
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

class RedditKeylessCollector(BaseCollector):
    def __init__(self, search_queries: List[str], limit: int = 100):
        self.search_queries = search_queries
        self.limit = limit
        
        self.include_keywords = [
            'wishlist', 'save', 'cart', 'wait', 'size', 'fit', 
            'quality', 'material', 'fake', 'review', 'youtube', 
            'instagram', 'compare'
        ]
        
        self.exclude_keywords = [
            'delivery', 'refund', 'customer service', 'customer care', 
            'payment failed', 'delayed', 'courier'
        ]
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def _is_relevant(self, text: str) -> bool:
        text_lower = text.lower()
        if 'myntra' not in text_lower:
            return False
        for ex in self.exclude_keywords:
            if ex in text_lower:
                return False
        for inc in self.include_keywords:
            if inc in text_lower:
                return True
        return False

    def collect(self) -> List[Dict[str, Any]]:
        print(f"Starting Selenium Reddit collection across queries: {self.search_queries}")
        records = []
        
        for query in self.search_queries:
            # We hit the JSON search endpoint via the browser instead of requests to bypass 403
            url = f"https://www.reddit.com/r/IndianFashionAddicts/search.json?q={query}&restrict_sr=1&limit=50"
            print(f"Loading {url}")
            self.driver.get(url)
            time.sleep(3) # Wait for anti-bot
            
            try:
                # The browser will render the raw JSON text wrapped in a <pre> tag
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                pre_tag = soup.find('pre')
                if pre_tag:
                    data = json.loads(pre_tag.text)
                else:
                    # sometimes it just renders as text
                    data = json.loads(soup.text)
                
                posts = data.get('data', {}).get('children', [])
                
                for post in posts:
                    post_data = post.get('data', {})
                    title = post_data.get('title', '')
                    selftext = post_data.get('selftext', '')
                    full_text = f"{title}\n{selftext}"
                    
                    if self._is_relevant(full_text):
                        records.append({
                            'platform': 'reddit',
                            'source_url': f"https://reddit.com{post_data.get('permalink', '')}",
                            'author': post_data.get('author', 'unknown'),
                            'content': full_text,
                            'date': datetime.utcfromtimestamp(post_data.get('created_utc', 0)),
                            'rating': None,
                            'metadata': {
                                'score': post_data.get('score', 0),
                                'num_comments': post_data.get('num_comments', 0),
                                'query': query
                            }
                        })
            except Exception as e:
                print(f"Failed to parse JSON from browser for {query}: {e}")
                
        self.driver.quit()
        print(f"Found {len(records)} highly relevant Reddit posts.")
        return records[:self.limit]
