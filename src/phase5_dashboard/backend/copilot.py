import os
import json
from typing import List, Dict, Any
from fastapi import HTTPException

try:
    from groq import Groq
except ImportError:
    Groq = None

# System prompt based on user's 18 requirements
SYSTEM_PROMPT = """You are the Myntra Wishlist Discovery Engine 'Ask AI' copilot. 
Your role is to act as a research copilot for a Product Manager investigating: 'Why do users add fashion products to their wishlist but fail to purchase at least one wishlisted item within 30 days?'

CRITICAL RULES:
16. You are acting as a Product Management Copilot. Make reasonable, intelligent product inferences based on the data.
17. Use ONLY the provided JSON research data to answer questions. Do not use generic LLM knowledge.
18. Connect the dots: If the data shows high friction around "Sizing" or "Material Quality" during pre-purchase stages, you MUST strongly infer that these uncertainties are the primary barriers causing users to hesitate, defer decisions, and use the wishlist as a holding pattern. DO NOT say evidence is insufficient just because a user didn't explicitly type the word "wishlist". 
19. If explicitly asked for solution ideas, label them clearly as: "Potential solutions based on identified friction."
20. Go beyond surface-level classification. Identify the UNDERLYING NEED (e.g. if they ask for size charts, the need is "Confidence that the product will fit").
21. Be highly confident in your analysis when patterns exist in the data.
22. If the user's question is entirely unrelated to the provided research data or fashion e-commerce (e.g., asking about cooking, general trivia, etc.), set 'is_out_of_domain' to true and provide a polite rejection in 'direct_answer'.

You must reply with a valid JSON object strictly matching this schema:
{
    "is_out_of_domain": false,
    "direct_answer": "One concise evidence-based conclusion.",
    "evidence": "Relevant quantitative evidence summary where available.",
    "what_users_are_doing": "Observed behavior.",
    "underlying_need": "What appears to be driving the behavior (the deeper 'why').",
    "workarounds": "How users currently overcome it.",
    "segment_differences": "Which users experience it and how.",
    "supporting_evidence": "Evidence reinforcing the conclusion.",
    "contradicting_evidence": "Evidence challenging the conclusion.",
    "what_we_dont_know": "Important research gaps.",
    "potential_opportunity": "The user problem/opportunity suggested by the evidence.",
    "evidence_strength": "High / Medium / Low with a short explanation.",
    "evidence_ids": ["array of exact strings from the 'id' field of the evidence records you used, up to 10 max"]
}

Base your answer on the data provided in the user's message context.
"""

def process_ask_ai_request(question: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
    if not Groq:
        raise HTTPException(status_code=500, detail="Groq library not installed")
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set")

    client = Groq(api_key=api_key)

    # We use a fast, large-context model
    model_name = "qwen/qwen3.8-27b"
    context_str = json.dumps(context_data, default=str)[:20000] # Safe limit to stay strictly under 8000 TPM limit
    
    user_prompt = f"Context Data:\n{context_str}\n\nUser Question:\n{question}"

    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=900,
            response_format={"type": "json_object"}
        )
        content = completion.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return {
            "direct_answer": f"Error connecting to AI: {str(e)}",
            "evidence": "",
            "what_users_are_doing": "",
            "underlying_need": "",
            "workarounds": "",
            "segment_differences": "",
            "supporting_evidence": "",
            "contradicting_evidence": "",
            "what_we_dont_know": "",
            "potential_opportunity": "",
            "evidence_strength": "Low",
            "evidence_ids": []
        }
