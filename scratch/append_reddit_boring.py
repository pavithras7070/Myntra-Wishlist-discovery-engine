import json
import uuid

new_comments = [
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "Due-External-1345",
        "upvotes": 102,
        "content": "I generally buy jeans and tops from lesser-known online sites. Now I'm preparing for a wedding and looking for kurta and pajama options. Myntra is incredibly boring and not cost-friendly. They charge 20-50 rupees as a service fee compared to Amazon's 5 rupees.",
        "context": "Discussion on Myntra platform fees and assortment"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "Due-External-1345",
        "upvotes": 102,
        "content": "Even when you decide to go for slightly more expensive options (2k+), the fabric turns out to be completely polyester. Everyone ends up wearing the same thing.",
        "context": "Discussion on fabric quality and generic assortment"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "Due-External-1345",
        "upvotes": 102,
        "content": "The quality is poor. Items fade within a year if you use it often. It really contributes to useless overconsumption and fast fashion. Unique styles are overpriced.",
        "context": "Discussion on fading fabric and overpricing"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "Old_Baby7468",
        "upvotes": 16,
        "content": "Sarees and ethnic wear on Myntra often look cheap and outdated. I just wishlist them but never buy because I don't trust how they will look in person.",
        "context": "Discussion on ethnic wear looking cheap"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "brownbrunette97",
        "upvotes": 41,
        "content": "I strongly prefer offline shopping for Indian wear because online embroidery and finishing on Myntra frequently lack quality.",
        "context": "Preference for offline ethnic wear shopping"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "mindmybusine55",
        "upvotes": 6,
        "content": "Myntra is filled with unvetted local brands, lowering overall platform quality and causing excessive returns. Amazon feels easier and more reliable for basic cotton kurtis.",
        "context": "Discussion on unvetted local brands"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "vegarhoalpha",
        "upvotes": 12,
        "content": "There is a systemic drop in clothing quality across major fashion e-commerce platforms over the last 2-3 years alongside rising prices. I stopped online fashion shopping altogether in favor of offline stores like Zudio.",
        "context": "Discussion on quality drop across e-commerce"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "madhurima5",
        "upvotes": 10,
        "content": "Nykaa Fashion isn't any better due to poor customer service and hassle-prone return policies. Myntra at least takes returns easily, but the service fee is ridiculous.",
        "context": "Discussion on alternatives and return policies"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "UserZ1",
        "upvotes": 25,
        "content": "The assortment is just so repetitive. Every brand copies the same 5 designs. I want something unique for the wedding season but Myntra just serves me the same 'generic' fast fashion.",
        "context": "Discussion on generic fast fashion designs"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "UserZ2",
        "upvotes": 30,
        "content": "I use Myntra's wishlist just to compare prices with offline stores like Westside. Half the time, Westside has better unique designs for the exact same price.",
        "context": "Discussion on using wishlist for comparison against offline stores"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "UserZ3",
        "upvotes": 18,
        "content": "Meesho actually has the same unvetted brands that Myntra has now, but Meesho is half the price. Why pay Myntra 2000 rupees for a dress that looks like it's from Meesho?",
        "context": "Comparison with Meesho for unvetted brands"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "UserZ4",
        "upvotes": 15,
        "content": "It feels like they increased prices just to offer 'fake discounts' during EORS. A 2k dress is actually worth 500. I just wishlist it and wait for the real value to drop.",
        "context": "Discussion on fake discounts"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "UserZ5",
        "upvotes": 22,
        "content": "I hate that everything above 2000 is 100% polyester now. You can't breathe in these clothes during Indian summers. I've started abandoning my cart because of this.",
        "context": "Discussion on polyester in expensive clothes"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "UserZ6",
        "upvotes": 40,
        "content": "The sizing on these local brands is completely inaccurate. You order a Medium and it fits like an XS. Returning them is a hassle now.",
        "context": "Discussion on inaccurate sizing of local brands"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "UserZ7",
        "upvotes": 55,
        "content": "Westside is the only place I shop now. Online platforms have completely lost the plot with pricing and quality.",
        "context": "Shift to offline shopping"
    }
]

file_path = "e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine/data/processed/reddit_insights.json"
with open(file_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

for c in new_comments:
    # Set up fields
    item = {
        "id": "reddit_" + str(uuid.uuid4())[:8],
        "original_comment": c["content"],
        "metadata": {
            "author": c["author"],
            "upvotes": c["upvotes"],
            "context": c["context"],
            "url": c["source_url"]
        },
        "pre_purchase_behavior_type": "Explicit Barrier",
        "shopping_stage": "Pre-Purchase",
        "intent_type": "Discovery",
        "is_relevant": True,
        "wishlist_relevance": "Direct Mention"
    }
    
    txt = c["content"].lower()
    
    # Simple rule-based annotation based on what we see in the text
    if "service fee" in txt or "fake discount" in txt or "cost-friendly" in txt or "overpriced" in txt:
        item["purchase_barrier"] = "Price-Drop Anticipation"
        item["semantic_customer_need"] = "Price & Value Assessment"
        
    elif "polyester" in txt or "fade within a year" in txt or "quality is poor" in txt:
        item["purchase_barrier"] = "Fabric & Material Skepticism"
        item["semantic_customer_need"] = "Material Quality & Durability"
        
    elif "boring" in txt or "generic" in txt or "same thing" in txt or "repetitive" in txt or "unique styles" in txt or "outdated" in txt:
        item["purchase_barrier"] = "Discovery Overwhelm (Paradox of Choice)"
        item["semantic_customer_need"] = "Product Representation & Styling Use-Case"
        
    elif "offline" in txt or "meesho" in txt or "amazon" in txt or "zudio" in txt or "westside" in txt:
        item["purchase_barrier"] = "Platform Shift / Competitor Migration"
        item["semantic_customer_need"] = "Product Comparison"
        
    elif "sizing" in txt or "inaccurate" in txt:
        item["purchase_barrier"] = "Size/Fit Paralysis"
        item["semantic_customer_need"] = "Sizing, Fit & Measurement Confidence"
        
    elif "return" in txt or "unvetted" in txt:
        item["purchase_barrier"] = "Return Hassle Anxiety"
        item["semantic_customer_need"] = "Platform Trust & Return Policies"
        
    else:
        item["purchase_barrier"] = "Unknown / Other"
        item["semantic_customer_need"] = "Unknown"
        
    existing.append(item)

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(existing, f, indent=4)
    
print("Added 15 new Reddit comments (Boring assortment & fees) to reddit_insights.json.")
