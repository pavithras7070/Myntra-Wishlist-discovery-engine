import os
import json
from typing import List, Dict, Any
from groq import Groq

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set correctly in .env")
            
        self.client = Groq(api_key=self.api_key)
        self.model = 'qwen/qwen3.8-27b'

    def analyze_batch(self, system_prompt: str, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not records:
            return []
            
        user_content = json.dumps([
            {
                "id": r['id'],
                "content": r['content']
            } for r in records
        ])
        
        prompt = f"{system_prompt}\n\nAnalyze these records and return a JSON object with a 'results' array:\n{user_content}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a JSON assistant. Output valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            result_text = response.choices[0].message.content
            parsed = json.loads(result_text)
            
            if "results" in parsed:
                return parsed["results"]
            else:
                print("Warning: 'results' key not found in Groq response")
                return []
                
        except Exception as e:
            print(f"Error during Groq API call: {e}")
            return []
