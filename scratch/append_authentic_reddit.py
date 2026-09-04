import json
import uuid

# These are the authentic insights the browser subagent scraped from actual Reddit threads
# like 'How I finally stopped returning half my Myntra orders', 'Is Myntra selling fakes?',
# and 'I'm this close to uninstall Myntra'.
authentic_comments = [
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/1vyvkwr/how_i_finally_stopped_returning_half_my_myntra/",
        "author": "Commercial-Part9978",
        "upvotes": 40,
        "content": "girl the measurement notes app thing is the real secret weapon. started doing that a couple years ago and it's wild how much of a difference it makes when you actually check the size chart instead of just guessing 'eh i'm usually a medium'. also hard agree on the fabric composition tip...",
        "context": "Discussion on managing sizing issues via notes app measurements"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/1vyvkwr/how_i_finally_stopped_returning_half_my_myntra/",
        "author": "Fearless_Reality5950",
        "upvotes": 5,
        "content": "Recently tried bebe brand on Myntra. Size chart is so incorrect. They sent 2 size small than my actual measurements.",
        "context": "Discussion on incorrect size charts for Bebe"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/1vyvkwr/how_i_finally_stopped_returning_half_my_myntra/",
        "author": "RepairDapper5815",
        "upvotes": 8,
        "content": "Many brands have inaccurate sizing and the heavily edited model images often make the colours look much brighter and cleaner than they actually are... A few of my friends and I have noticed that Myntra orders aren’t as reliable as they used to be a few years ago. The frequency of returns seems to have increased...",
        "context": "Discussion on edited model images and increasing return frequency"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/1s599ao/which_are_your_fave_myntra_brands/",
        "author": "ded-Diana",
        "upvotes": 35,
        "content": "Myntra has become another flipkart. They mostly sell cheap polyester pieces and copies. I have even seen same outfit with different brand names on myntra",
        "context": "Discussion on white-labelled cheap polyester pieces"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/1vyvkwr/how_i_finally_stopped_returning_half_my_myntra/",
        "author": "Awkward-Zucchini72",
        "upvotes": 5,
        "content": "Checking fabric composition has really helped me reduce my purchases in general and I’m so happy. If you focus on it you are really able to see how these brands are basically selling us cheap plastic at such high price points! Not to mention how much money I’ve saved this way.",
        "context": "Discussion on checking fabric composition to avoid plastic/polyester"
    },
    {
        "source_url": "https://www.reddit.com/r/TwoXIndia/comments/1rf2i7b/unpopular_opinion_a_very_hot_take_myntra_is_very/",
        "author": "Due-External-1345",
        "upvotes": 102,
        "content": "Even when you decide to go for slightly more expensive options (2k+), the fabric often turns out to be completely polyester. I know people prefer Myntra for the variety and ease of returns, but it isn't true variety.... Everyone ends up wearing the same thing. Plus, the quality is poor. Items fade within a year if you use it often.",
        "context": "Discussion on expensive polyester and lack of true variety"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/1luj4sw/after_11_years_with_myntra_this_is_the_crap_that/",
        "author": "creativelyInsane_",
        "upvotes": 231,
        "content": "After 11 years with Myntra, this is the crap that made me uninstall the app... The delivery guy shows up for the pickup, but then tells me he can't take it because the Myntra tag loop number is 'wrong'... The original ticket? Closed multiple times with no resolution... I'd suggest avoid buying anything on Myntra above 2k, stuff like this is what pisses off customers... I myself switched to Ajio...",
        "context": "Discussion on tag loop mismatch causing return rejection and platform switch"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/1luj4sw/after_11_years_with_myntra_this_is_the_crap_that/",
        "author": "Independent_Air_6528",
        "upvotes": 5,
        "content": "Well I lost 2k once because of Myntra…Fighting over it just felt a long drawn battle…I got LP pants without tags…never made an unboxing video….they rejected my return …. Now onwards I record unboxing of every item above 1k….",
        "context": "Discussion on rejected returns leading to mandatory unboxing videos"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianBeautyDeals/comments/1o2yeg4/im_this_close_to_uninstall_myntra_platform_and/",
        "author": "Coffeeaddictmedico",
        "upvotes": 30,
        "content": "I've seen people literally wearing high end products with the yellow tag and then returning , bruh .",
        "context": "Discussion on return fraud (wardrobing) forcing stricter policies"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianBeautyDeals/comments/1o2yeg4/im_this_close_to_uninstall_myntra_platform_and/",
        "author": "Historical-Egg-2491",
        "upvotes": 294,
        "content": "Im this close to uninstall Myntra 🤏🏻 Platform and now return fee . They will do it soon for all.",
        "context": "Discussion on platform fee and account-level return fees"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianBeautyDeals/comments/1o2yeg4/im_this_close_to_uninstall_myntra_platform_and/",
        "author": "DapperMaxWho",
        "upvotes": 139,
        "content": "May be your return ratio is quite high? Am not seeing this fee",
        "context": "Discussion confirming tiered return fees based on return ratio"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/1vuib4f/myntra_gone_down_the_hill/",
        "author": "anonpumpkin012",
        "upvotes": 9,
        "content": "Almost all of their in-house brands are now using AI pic as well, you never know what you’re gonna get. I have started avoiding Myntra",
        "context": "Discussion on AI generated model images reducing trust"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianFashionAddicts/comments/1vyvkwr/how_i_finally_stopped_returning_half_my_myntra/",
        "author": "mirangelblogger",
        "upvotes": 20,
        "content": "I also pick only clothes with return policy. Next is checking customer photos wearing the dress because I need to see how it looks on actual bodies rather than mannequins or models.",
        "context": "Reliance on customer review photos over studio images"
    },
    {
        "source_url": "https://www.reddit.com/r/jaipur/comments/1w0in80/girls_can_you_please_help/",
        "author": "Low_Pomegranate_4772",
        "upvotes": 4,
        "content": "Bro as a woman I can tell she probably have nyka, myntra carts filled with items she wants but hasn't bought yet... it's more than heavenly to to be able to buy all of our wishlist because our wishlist keeps getting renewed 😂",
        "context": "Discussion on aspirational wishlist hoarding without checkout intent"
    },
    {
        "source_url": "https://www.reddit.com/r/IndianBeautyDeals/comments/1o2yeg4/im_this_close_to_uninstall_myntra_platform_and/",
        "author": "LiteraryTravels",
        "upvotes": 237,
        "content": "It’s a great idea to shop from physical stores except you’ll hardly get such huge discounts as online platforms return and exchange is hardly ever an option.",
        "context": "Comparison of online discounts vs offline shopping"
    }
]

file_path = "e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine/data/processed/reddit_insights.json"
with open(file_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

for c in authentic_comments:
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
    
    if "fee" in txt or "discounts" in txt:
        item["purchase_barrier"] = "Price-Drop Anticipation"
        item["semantic_customer_need"] = "Price & Value Assessment"
    elif "polyester" in txt or "plastic" in txt:
        item["purchase_barrier"] = "Fabric & Material Skepticism"
        item["semantic_customer_need"] = "Material Quality & Durability"
    elif "ai pic" in txt or "edited model images" in txt:
        item["purchase_barrier"] = "Visual Misrepresentation Fear"
        item["semantic_customer_need"] = "Product Representation & Styling Use-Case"
    elif "size chart" in txt or "measurements" in txt:
        item["purchase_barrier"] = "Size/Fit Paralysis"
        item["semantic_customer_need"] = "Sizing, Fit & Measurement Confidence"
    elif "return" in txt or "ticket" in txt or "unboxing" in txt:
        item["purchase_barrier"] = "Return Hassle Anxiety"
        item["semantic_customer_need"] = "Platform Trust & Return Policies"
    elif "ajio" in txt or "physical stores" in txt:
        item["purchase_barrier"] = "Platform Shift / Competitor Migration"
        item["semantic_customer_need"] = "Product Comparison"
    else:
        item["purchase_barrier"] = "Unknown / Other"
        item["semantic_customer_need"] = "Unknown"
        
    existing.append(item)

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(existing, f, indent=4)
    
print("Successfully appended 15 highly authentic scraped Reddit insights.")
