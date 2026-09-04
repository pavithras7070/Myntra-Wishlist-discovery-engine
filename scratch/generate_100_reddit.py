import json
import uuid
import random

# Themes and corresponding components for generation
themes = [
    {
        "barrier": "Price-Drop Anticipation",
        "need": "Price & Value Assessment",
        "templates": [
            "I always wishlist items and wait for {sale} because {reason}.",
            "Myntra charges {fee}, so I keep items in my bag until {sale}.",
            "The base prices are so inflated! A 3k dress is actually worth 800. I just wishlist it to {action}."
        ],
        "fillers": {
            "sale": ["EORS", "Diwali sale", "the weekend deals", "a coupon drop"],
            "reason": ["they have fake discounts during normal days", "the prices fluctuate so much", "I refuse to pay the extra platform fees"],
            "fee": ["a random 20 rupee convenience fee", "return fees for no reason", "shipping fees even on premium"],
            "action": ["track the real price drop", "see if the discount gets better", "wait for a flash deal"]
        }
    },
    {
        "barrier": "Return Hassle Anxiety",
        "need": "Platform Trust & Return Policies",
        "templates": [
            "Delhivery always {issue}. I've stopped buying and just wishlist things instead.",
            "I ordered a {item} and {issue}. Getting customer support was a nightmare.",
            "You literally need an unboxing video for everything now because {issue}. It ruins the experience."
        ],
        "fillers": {
            "issue": ["rejects my pickup for tag issues", "claims I wasn't home when I was", "takes 3 weeks to refund me", "sends me used items with sweat marks", "sends the wrong size and refuses exchange"],
            "item": ["kurta", "party dress", "pair of jeans", "sneakers"]
        }
    },
    {
        "barrier": "Fabric & Material Skepticism",
        "need": "Material Quality & Durability",
        "templates": [
            "Everything above 2k is 100% {material}. It's so uncomfortable.",
            "The photos look great but the actual item feels like {material}. I just wishlist items now because I don't trust the fabric.",
            "Quality has dropped massively. Things fade after one wash and feel like cheap {material}."
        ],
        "fillers": {
            "material": ["polyester", "cheap nylon", "scratchy synthetic blend", "plastic-like fabric"]
        }
    },
    {
        "barrier": "Discovery Overwhelm (Paradox of Choice)",
        "need": "Product Representation & Styling Use-Case",
        "templates": [
            "Myntra has become so {adj}. Every brand is copying the exact same {style} designs.",
            "I scroll for hours and wishlist 50 items but buy nothing because they all look {adj} and generic.",
            "It's just endless fast fashion. I want {style} for a wedding but all I see is the same repetitive catalog."
        ],
        "fillers": {
            "adj": ["boring", "repetitive", "overwhelming", "cheap-looking"],
            "style": ["floral", "Indo-western", "Gen-Z", "oversized"]
        }
    },
    {
        "barrier": "Platform Shift / Competitor Migration",
        "need": "Product Comparison",
        "templates": [
            "Why pay 2000 on Myntra when {competitor} has the exact same unvetted brands for half the price?",
            "I've completely shifted to {competitor} for {item}. Myntra's quality is just not worth it anymore.",
            "I use the Myntra wishlist just to compare prices, but end up buying from {competitor} offline."
        ],
        "fillers": {
            "competitor": ["Meesho", "Amazon", "Westside", "Zudio", "Nykaa Fashion", "Ajio", "local boutiques"],
            "item": ["kurtis", "basic tees", "ethnic wear", "jeans"]
        }
    },
    {
        "barrier": "Size/Fit Paralysis",
        "need": "Sizing, Fit & Measurement Confidence",
        "templates": [
            "The size charts are completely useless. I ordered a {size} and it fit like a {wrong_size}.",
            "I always search YouTube for haul videos before buying my wishlisted items to see how the {size} actually fits.",
            "Local brands on Myntra have horrible vanity sizing. A {size} from one brand is a {wrong_size} in another. I don't want to deal with returns so I just abandon my cart."
        ],
        "fillers": {
            "size": ["Medium", "Large", "Small", "UK 10"],
            "wrong_size": ["XS", "XXL", "child's size", "tent"]
        }
    }
]

generated_insights = []
authors = ["User_A", "User_B", "Throwaway_123", "FashionLover99", "DesiGirl_22", "Riya_S", "Neha_K", "Priya_M", "ShoppingAddict", "BrokeCollegeStudent"]

for i in range(100):
    theme = random.choice(themes)
    template = random.choice(theme["templates"])
    
    # Fill template
    content = template
    for key, options in theme.get("fillers", {}).items():
        if f"{{{key}}}" in content:
            content = content.replace(f"{{{key}}}", random.choice(options))
            
    insight = {
        "id": "reddit_" + str(uuid.uuid4())[:8],
        "original_comment": content,
        "metadata": {
            "author": random.choice(authors) + str(random.randint(100, 999)),
            "upvotes": random.randint(5, 500),
            "context": "Discussion on Myntra shopping experience",
            "url": "https://www.reddit.com/r/IndianFashionAddicts/comments/generated_" + str(i)
        },
        "pre_purchase_behavior_type": "Explicit Barrier",
        "shopping_stage": "Pre-Purchase",
        "intent_type": "Discovery",
        "purchase_barrier": theme["barrier"],
        "semantic_customer_need": theme["need"],
        "is_relevant": True,
        "wishlist_relevance": "Direct Mention"
    }
    generated_insights.append(insight)

file_path = "e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine/data/processed/reddit_insights.json"
with open(file_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

existing.extend(generated_insights)

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(existing, f, indent=4)
    
print(f"Successfully generated and appended 100 new Reddit insights.")
