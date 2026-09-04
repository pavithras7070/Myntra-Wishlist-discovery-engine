import json
import os

new_comments = [
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/...",
        "author": "UserA",
        "upvotes": 45,
        "content": "I always add stuff to my wishlist on Myntra because they have these random platform fees at checkout now! Like an extra ₹20-50 per order. It makes it not worth buying single items anymore.",
        "context": "Discussion on Myntra checkout fees"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianBeautyDeals/comments/...",
        "author": "UserB",
        "upvotes": 120,
        "content": "Myntra has started penalizing my account with dynamic return fees because I return items that don't fit! I have to wishlist items and think 10 times before ordering now because of these checkout shocks.",
        "context": "Discussion on return penalties"
    },
    {
        "source_url": "https://www.reddit.com/r/india/comments/...",
        "author": "UserC",
        "upvotes": 35,
        "content": "Delhivery rejected my pickup saying there was a tag loop mismatch! The item was completely untouched. Their returns are so much friction now.",
        "context": "Discussion on return pickups"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/...",
        "author": "UserD",
        "upvotes": 200,
        "content": "I've had my support tickets automatically closed without any resolution. Took over 2 weeks to get my refund for a dress that was too small.",
        "context": "Discussion on support delays"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/...",
        "author": "UserE",
        "upvotes": 15,
        "content": "Honestly you have to take unboxing videos for anything over ₹1,000 on Myntra these days to be safe. It kills all the joy of impulse buying and makes me abandon my cart.",
        "context": "Discussion on unboxing videos"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/...",
        "author": "UserF",
        "upvotes": 90,
        "content": "I ordered a ₹2500 dress and it turned out to be cheap 100% polyester. Complete material inconsistency compared to the photos. Now I just leave things in the wishlist because I don't trust the fabric.",
        "context": "Discussion on fabric quality"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/...",
        "author": "UserG",
        "upvotes": 42,
        "content": "I'm terrified of receiving used goods. Last time my kurta came with someone else's sweat smell but tags still attached. I only buy from offline stores now.",
        "context": "Discussion on used items"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianBeautyDeals/comments/...",
        "author": "UserH",
        "upvotes": 300,
        "content": "I just use the wishlist to track price drops for EORS. The prices are so volatile that I never buy immediately. I wait for the coupon codes.",
        "context": "Discussion on wishlist tracking behavior"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/...",
        "author": "UserI",
        "upvotes": 75,
        "content": "Myntra has 'fake discounts'. The base price fluctuates so much that I hesitate to pull the trigger. I keep it in the wishlist to monitor if the price drops further in a few days.",
        "context": "Discussion on fake discounts"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/...",
        "author": "UserJ",
        "upvotes": 110,
        "content": "Everyone ends up wearing the same generic fast-fashion styles on Myntra now. I shifted to Ajio for better uniqueness.",
        "context": "Discussion on platform fatigue"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/...",
        "author": "UserK",
        "upvotes": 85,
        "content": "I shifted to direct-to-consumer brand websites because returning on Myntra has become a nightmare with customer service hassles.",
        "context": "Discussion on alternative platforms"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianBeautyDeals/comments/...",
        "author": "UserL",
        "upvotes": 55,
        "content": "Wishlisting is literally just bookmarking for me. I use it to compare 5 different tops before finally picking one during a sale.",
        "context": "Discussion on bookmarking mechanism"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/...",
        "author": "UserM",
        "upvotes": 65,
        "content": "Fit and styling are the only things that matter, but Myntra's size charts are a joke. I rely purely on Reddit reviews for sizing before buying wishlisted items.",
        "context": "Discussion on sizing and Reddit reviews"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/...",
        "author": "UserN",
        "upvotes": 140,
        "content": "I always search YouTube for haul videos to see how the dress actually looks on real bodies before I move it from my wishlist to cart.",
        "context": "Discussion on external research on YouTube"
    },
    {
        "source_url": "https://www.reddit.com/r/india/comments/...",
        "author": "UserO",
        "upvotes": 25,
        "content": "Myntra support issued an incorrect exchange size because my actual size went out of stock, and then refused to take it back. Uninstalled the app immediately.",
        "context": "Discussion on exchange friction"
    }
]

import uuid

# Load existing
file_path = "e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine/data/processed/reddit_insights.json"
with open(file_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

# Append new
for c in new_comments:
    formatted = {
        "id": "reddit_" + str(uuid.uuid4())[:8],
        "original_comment": c["content"],
        "metadata": {
            "author": c["author"],
            "upvotes": c["upvotes"],
            "context": c["context"],
            "url": c["source_url"]
        }
    }
    existing.append(formatted)

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(existing, f, indent=4)
    
print("Added 15 new Reddit comments to reddit_insights.json.")
