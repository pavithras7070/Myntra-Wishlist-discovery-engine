import sys
import os
from dotenv import load_dotenv

# Add src to python path so we can import modules properly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import init_db
from pipeline.analyzer import InsightAnalyzer

def main():
    # Load .env file from root
    root_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    load_dotenv(dotenv_path=root_env_path)
    
    print("Initializing Phase 2 Analysis Core...")
    init_db()
    
    analyzer = InsightAnalyzer()
    
    # Process 100 records
    analyzer.run(max_records=100)

if __name__ == "__main__":
    main()
