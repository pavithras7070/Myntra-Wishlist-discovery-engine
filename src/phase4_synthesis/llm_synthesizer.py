import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def generate_synthesis():
    base_dir = "e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine"
    metrics_path = os.path.join(base_dir, "data", "processed", "phase3_aggregated_metrics.json")
    output_path = os.path.join(base_dir, "data", "processed", "phase4_synthesis.json")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if not os.path.exists(metrics_path):
        print(f"Error: {metrics_path} not found.")
        return
        
    with open(metrics_path, "r", encoding="utf-8") as f:
        aggregated_metrics = json.load(f)
        
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return
        
    client = genai.Client(api_key=api_key)
    
    system_prompt = """You are an expert Head of Product at a major fashion e-commerce company (like Myntra).
You are analyzing aggregated data of customer purchase barriers (specifically why users wishlist items but do not purchase them).
Your goal is to synthesize the quantitative data into strategic 'Key Customer Problems' and 'Opportunity Hypotheses'.

The input data contains aggregated semantic needs with Frequency (Total Count), Severity Score, Relevance Score, and Common Workarounds.
Rank your opportunity areas based on frequency, severity, and relevance to wishlist-to-purchase conversion.

Return the result STRICTLY as a JSON object with this exact structure:
{
    "key_customer_problems": [
        {
            "problem_name": "Name of the problem",
            "description": "Deep dive into what the customer is experiencing and why they are hesitating",
            "primary_workaround_used": "What users currently do to solve this",
            "severity_ranking": "High/Medium/Low"
        }
    ],
    "opportunity_hypotheses": [
        {
            "hypothesis_title": "Actionable product feature or UX change",
            "rationale": "Why this will solve the problem",
            "target_metric": "e.g., Wishlist-to-Cart Conversion",
            "impact_score": "High/Medium/Low"
        }
    ]
}"""

    prompt = f"{system_prompt}\n\nHere is the aggregated Phase 3 data:\n{json.dumps(aggregated_metrics, indent=2)}"
    
    print("Running Phase 4 LLM Synthesis...")
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        
        parsed_response = json.loads(response.text)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(parsed_response, f, indent=4)
            
        print(f"Synthesis complete! Saved to {output_path}")
        
    except Exception as e:
        print(f"Error during synthesis generation: {e}")

if __name__ == "__main__":
    generate_synthesis()
