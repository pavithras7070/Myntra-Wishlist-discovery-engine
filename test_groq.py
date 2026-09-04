import os
import json
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

# Replicate the exact setup in copilot.py
SYSTEM_PROMPT = """You are the Myntra Wishlist Discovery Engine 'Ask AI' copilot. 
Your role is to act as a research copilot for a Product Manager investigating: 'Why do users add fashion products to their wishlist but fail to purchase at least one wishlisted item within 30 days?'

CRITICAL RULES:
1. You are NOT the decision maker. Do not declare final user problems.
2. Use ONLY the provided JSON research data to answer questions. Do not use generic LLM knowledge.
3. If evidence is insufficient, say: "The current research evidence is insufficient to answer this confidently." Do not guess.
4. You MUST NOT automatically recommend product features. If asked "What feature should we build?", remind the PM: "The current evidence identifies these opportunity areas. The underlying problem should be validated through primary research before selecting a solution." If explicitly asked for solution ideas, label them clearly as: "Potential solutions — not validated recommendations."
5. Go beyond surface-level classification. Identify the UNDERLYING NEED (e.g. if they ask for size charts, the need is "Confidence that the product will fit").
6. Always look for contradicting evidence or alternative explanations.

You must reply with a valid JSON object strictly matching this schema:
{
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

context_data = {'dummy': 'a' * 3000}
context_str = json.dumps(context_data, default=str)[:3000]
user_prompt = f"Context Data:\n{context_str}\n\nUser Question:\nWhy do users wishlist products?"

try:
    completion = client.chat.completions.create(
        model="groq/compound",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )
    print(completion.choices[0].message.content)
except Exception as e:
    print(e)
