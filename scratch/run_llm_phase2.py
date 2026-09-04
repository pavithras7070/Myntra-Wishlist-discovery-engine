import sys
import os
import json
from datetime import datetime

sys.path.append(os.path.join(os.getcwd(), 'src', 'phase2_analysis_core'))
from llm.client import GroqClient
from llm.prompts import SYSTEM_PROMPT

from dotenv import load_dotenv
load_dotenv()

llm = GroqClient()

with open('scratch/live_scraped_reviews.json', 'r', encoding='utf-8') as f:
    raw_records = json.load(f)

for i, r in enumerate(raw_records):
    r['id'] = str(i)

new_insights = llm.analyze_batch(SYSTEM_PROMPT, raw_records)

for i, parsed in enumerate(new_insights):
    parsed['source_id'] = 'live_scrape'
    parsed['platform'] = raw_records[i].get('platform', 'ecommerce_reviews')
    parsed['date'] = raw_records[i].get('date', str(datetime.utcnow()))
    parsed['original_text'] = raw_records[i].get('content', '')
    parsed['is_relevant'] = True

insights_file = 'data/processed/myntra_web_insights.json'
with open(insights_file, 'r', encoding='utf-8') as f:
    existing_insights = json.load(f)

existing_insights.extend(new_insights)

with open(insights_file, 'w', encoding='utf-8') as f:
    json.dump(existing_insights, f, indent=4)

print(f'Successfully appended {len(new_insights)} insights to {insights_file}')
