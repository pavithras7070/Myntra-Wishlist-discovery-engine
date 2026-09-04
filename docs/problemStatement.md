# Problem Statement: AI-Powered Discovery Engine for Myntra

## 1. Project Context

You are building an AI-Powered Discovery Engine for the Growth team at Myntra.

Myntra is an online fashion shopping platform where millions of users browse fashion products, save products they like, and add products to their wishlists.

A wishlist is an important behavioral signal because the user has explicitly expressed interest in a product but has not purchased it yet.

Over time, users may accumulate many wishlisted products, but only a subset of those products eventually result in a purchase.

Myntra's strategic business goal is:

> Increase the percentage of users who purchase at least one item from their wishlist within 30 days of adding it.

Improving wishlist-to-purchase conversion could increase:

- Purchase frequency
- Monetization from existing users
- Conversion of existing high-intent demand
- Customer lifetime value

However, the underlying user problem is UNKNOWN.

The purpose of this project is to discover the user problem through evidence.

DO NOT assume the answer is fit, size, price, styling, reviews, quality, comparison, or any other predefined problem.

The eventual product solution cannot rely on monetary incentives such as discounts, coupons, cashback, rewards, or price reductions.

---

# 2. Primary Objective

Build an AI-powered research and discovery engine that analyzes public user conversations and feedback at scale to identify:

- Why users wishlist fashion products
- What different types of wishlist intent exist
- Why wishlisted products are not purchased
- What causes users to postpone purchases
- What uncertainties remain after users identify a product they like
- How users compare shortlisted products
- What information users seek before purchasing
- What information users seek outside Myntra or other fashion platforms
- What workarounds users currently use
- How these behaviors differ across user segments
- What unmet needs occur repeatedly
- Which opportunity areas could plausibly influence wishlist-to-purchase conversion

The system must go beyond simple review summarization and sentiment analysis.

It should identify behavioral patterns, root causes, user needs, workarounds, and opportunity areas.

---

# 3. Core Research Questions

The discovery engine must investigate the following questions.

## Wishlist Intent

1. Why do users add fashion products to a wishlist?
2. What different types of intent does a wishlist action represent?
3. When does wishlist activity represent strong purchase intent?
4. When is wishlist activity primarily bookmarking or inspiration?
5. Do users wishlist products for future occasions, comparison, price monitoring, or later consideration?
6. What behavioral signals distinguish high-intent wishlist users from low-intent wishlist users?

## Wishlist-to-Purchase Drop-off

1. Why do users fail to purchase products they have previously saved?
2. What causes users to postpone a purchase?
3. At which stage between wishlist and purchase does friction occur?
4. What causes users to abandon a wishlisted product?
5. What causes users to switch to another product?
6. What causes users to eventually purchase a wishlisted product?

## Purchase Uncertainty

Investigate what users are uncertain about before purchasing.

Potential areas include, but are not limited to:

- Fit
- Size
- Quality
- Material
- Appearance
- Styling
- Price/value
- Reviews
- Occasion suitability
- Brand trust
- Product authenticity
- Availability
- Delivery
- Returns/exchanges
- Social validation
- Comparison with alternatives

Do not assume any one of these is the dominant issue.

Identify which issues actually appear in the evidence.

## Comparison Behavior

1. How do users compare shortlisted fashion products?
2. Which product attributes do they compare?
3. Do they compare several products on the same platform?
4. Do they compare Myntra with AJIO, Amazon, brand websites, or other platforms?
5. What information helps them choose one product over another?
6. What creates comparison overload or decision difficulty?

## External Research

Identify what users do outside Myntra before purchasing.

Investigate behavior involving:

- Google
- Reddit
- YouTube
- Instagram
- Influencers
- Friends/family
- Other shopping platforms
- Brand websites
- Fashion communities
- Product review sites

For each external behavior, identify:

- What information the user is looking for
- Why they are looking for it
- Why they use an external source
- Whether this indicates an unmet need inside the shopping experience

## User Segmentation

Identify meaningful behavioral user segments based on evidence.

Possible dimensions include:

- Shopping frequency
- Fashion involvement
- Purchase intent
- Product category
- Occasion
- Price sensitivity
- Discovery behavior
- Comparison behavior
- Online shopping experience
- Reliance on external research
- Confidence in purchase decisions

Do not create arbitrary segments without supporting evidence.

## Unmet Needs

Identify recurring unmet needs that could influence the transition from product interest to purchase.

---

# 4. Data Sources

The system should be designed to work with publicly available information from multiple sources.

Prioritize:

## App Reviews

- Google Play Store reviews
- Apple App Store reviews

## Community Discussions

- Reddit
- Fashion communities
- Shopping forums
- Public discussion boards

## Social and Video

- YouTube comments
- Public social media conversations where accessible

## Product-Level Feedback

- Product reviews
- Product Q&A
- Public customer discussions

## Competitive and Category Context

Where useful, include conversations about:

- Myntra
- AJIO
- Other online fashion marketplaces
- Brand-owned fashion websites
- General online fashion shopping

Every record should preserve source metadata wherever possible.

---

# 5. Discovery Taxonomy

For each relevant conversation, extract structured information wherever possible.

Use the following fields:

- Source
- Platform
- Date
- Original User Comment
- Relevance
- Fashion Category
- Shopping Stage
- Wishlist/Save Mention
- Intent Type
- Purchase Status
- Purchase Barrier
- Uncertainty
- User Need
- User Workaround
- External Platform Mention
- Comparison Behavior
- Decision Factor
- User Segment
- Root Cause
- Opportunity Area
- Evidence Strength
- Confidence

If a field cannot be determined from the source, mark it as unknown/null.

Never invent information.

---

# 6. Shopping Journey Framework

Analyze user conversations in the context of the following shopping journey:

Discovery
    ↓
Product Evaluation
    ↓
Wishlist / Save
    ↓
Consideration
    ↓
Comparison / Research
    ↓
Purchase Confidence
    ↓
Cart
    ↓
Purchase
    ↓
Post-Purchase

Pay particular attention to the transition:

Wishlist / Save
    ↓
Purchase

Identify where friction, uncertainty, hesitation, or unmet needs occur.

---

# 7. AI Analysis Pipeline

Build the analysis pipeline in multiple stages.

## Stage 1: Data Collection

Collect and normalize data from the available sources.

Store source, date, platform, and original content.

## Stage 2: Relevance Detection

Identify content related to:

- Online fashion shopping
- Wishlist/save behavior
- Product consideration
- Purchase hesitation
- Purchase decisions
- Product comparison
- Fashion-shopping uncertainty
- Pre-purchase research

Filter irrelevant content.

## Stage 3: Behavioral Extraction

Identify what the user is actually doing.

Examples:

- Browsing
- Saving
- Wishlisting
- Revisiting
- Delaying
- Comparing
- Searching reviews
- Searching externally
- Asking friends
- Waiting for a future occasion
- Switching products
- Abandoning
- Purchasing

## Stage 4: Problem and Barrier Extraction

Identify what prevents the desired behavior.

Do not stop at surface-level statements.

Example:

User statement:
"I read many reviews because I am not sure about the size."

Extract:

- Surface behavior: Reading reviews
- Uncertainty: Size/fit confidence
- Potential barrier: Low confidence in expected fit
- Workaround: Review research

## Stage 5: Root Cause Analysis

Separate:

Symptom
→ Behavior
→ Barrier
→ Underlying uncertainty
→ Root cause

Do not treat symptoms as root causes.

## Stage 6: User Segmentation

Cluster users based on behavioral patterns, needs, barriers, and intent.

Segments must be explainable and evidence-based.

## Stage 7: Opportunity Identification

Convert recurring problems and unmet needs into potential opportunity areas.

Each opportunity should include:

- Opportunity name
- User need
- Affected segment
- Evidence
- Frequency
- Severity
- Purchase relevance
- Existing workaround
- Potential product leverage
- Confidence

---

# 8. Quantitative Analysis

Quantify patterns wherever the dataset allows.

Measure:

- Total conversations analyzed
- Relevant conversations
- Frequency of each intent type
- Frequency of each purchase barrier
- Frequency of each uncertainty
- Frequency of external research
- Frequency of comparison behavior
- Segment prevalence
- Barrier co-occurrence
- Trend over time where sufficient data exists

For every percentage or count, clearly identify:

- Numerator
- Denominator
- Sample size
- Time period, where relevant

Do not fabricate metrics.

If the dataset is insufficient to support a quantitative conclusion, explicitly state that.

---

# 9. Opportunity Prioritization

Do not simply list problems.

Compare and prioritize opportunity areas using:

### Frequency
How often does the problem occur?

### Severity
How strongly does it affect users?

### Purchase Relevance
How directly could solving it influence wishlist-to-purchase behavior?

### Intent Relevance
Does the problem occur among high-intent users?

### Workaround Effort
How much effort do users spend solving the problem today?

### Product Leverage
Can Myntra realistically address the problem through product or experience changes?

### Evidence Strength
How strong and consistent is the evidence?

Create an opportunity score/ranking based on these dimensions.

Clearly show the evidence supporting the ranking.

---

# 10. Required Outputs

The discovery engine should produce the following outputs.

## Output 1: Executive Summary

Summarize:

- Major user behaviors
- Major wishlist intent types
- Major purchase barriers
- Important uncertainties
- Important workarounds
- Important user segments
- Highest-potential opportunities

## Output 2: Wishlist Intent Taxonomy

Classify the different reasons users save/wishlist products.

## Output 3: Purchase Barrier Landscape

Show the major reasons users postpone, abandon, or redirect purchases.

## Output 4: Uncertainty Map

Show what information users still need before purchasing.

## Output 5: Workaround Map

Show how users currently solve those uncertainties or problems.

## Output 6: External Research Map

Show what users search for outside Myntra and why.

## Output 7: Segment Analysis

Show how purchase barriers and unmet needs differ across segments.

## Output 8: Opportunity Matrix

Rank the strongest opportunity areas using the prioritization framework.

## Output 9: Evidence Explorer

Every major insight must be traceable back to supporting user conversations.

The user should be able to move from:

Opportunity
→ Theme
→ Segment
→ Evidence
→ Original source

---

# 11. Evidence and Explainability

Every major insight must contain:

- Insight
- Supporting evidence
- Number of supporting conversations
- Sources
- Representative anonymized examples
- Confidence level
- Whether the insight is directly observed or inferred

Example:

Instead of:

"Users do not purchase because of sizing."

Produce:

"Size/fit uncertainty appeared in X of Y relevant conversations. Users frequently described reading reviews or seeking external information to reduce uncertainty."

The system must clearly separate:

### Observed evidence

What users explicitly said or did.

### AI interpretation

What the model infers from the evidence.

### Hypothesis

What should be validated through primary research.

Do not present hypotheses as proven facts.

---

# 12. Contradictory Evidence

The system must actively look for conflicting evidence.

If some users indicate that price is the main barrier while others indicate that price is irrelevant, surface both patterns.

Do not force all users into one narrative.

For each major insight, consider:

- Supporting evidence
- Contradictory evidence
- Exceptions
- Confidence

---

# 13. Research Hypothesis Management

Maintain three levels of knowledge:

## Level 1: Existing / Industry Hypotheses

Possible problems suggested by broader industry understanding.

## Level 2: AI-Generated Hypotheses

Potential patterns identified from the analyzed user data.

## Level 3: Validated Findings

Patterns confirmed or challenged through primary research.

The discovery engine must NOT claim that an AI-generated hypothesis is a validated user problem.

---

# 14. Product-Solution Constraint

The discovery engine must remain solution-neutral.

Do not recommend a product feature simply because a particular problem appears frequently.

First determine:

1. Is the problem real?
2. How frequently does it occur?
3. Who experiences it?
4. How severe is it?
5. Does it plausibly affect wishlist-to-purchase conversion?
6. What workarounds already exist?
7. Can Myntra realistically address it?

Only after this discovery process should the problem be taken forward to primary research and eventual MVP development.

The eventual solution must NOT use monetary incentives.

---

# 15. Quality Requirements

The system should:

- Be evidence-driven
- Preserve source traceability
- Avoid hallucinated facts
- Avoid fabricated statistics
- Avoid duplicate insights
- Distinguish correlation from causation
- Distinguish observed behavior from interpretation
- Handle conflicting evidence
- Make confidence explicit
- Support filtering by source, segment, category, barrier, intent, and shopping stage
- Allow opportunity areas to be compared side by side

---

# 16. Final Goal

The final output of this AI Discovery Engine should answer:

> "What are the most important evidence-backed user problems preventing online fashion shoppers from converting product interest into purchase, which user segments experience them, how frequently and severely they occur, what workarounds users currently use, what information they seek, and which opportunities are most promising to validate through primary research?"

The system should take the project from:

Unknown Problem
    ↓
Large-Scale User Evidence
    ↓
Behavior Patterns
    ↓
Root Causes
    ↓
User Segments
    ↓
Opportunity Areas
    ↓
Prioritized Hypotheses
    ↓
Primary Research

Do not build the final product solution at this stage.

The immediate goal is to build a reliable AI-powered discovery system that helps a Product Manager discover and prioritize the underlying user problem.

# Research Relevance to the Wishlist → Purchase Journey

When collecting and analyzing reviews and conversations, prioritize evidence about the user's fashion purchase decision journey, even when the user does not explicitly mention "Wishlist."

Look for evidence across:
Wishlist/Save → Revisit → Re-evaluation → Purchase Confidence → Add to Cart → Purchase/Abandonment.

Do not restrict retrieval to the keyword "wishlist."

# Business Metric Relevance

Every identified opportunity must be evaluated against the target business metric:

> 30-Day Wishlist-to-Purchase Conversion =
> % of users who purchase at least one wishlisted item within 30 days of adding it.

For every opportunity, determine:

1. Which user behavior in the wishlist-to-purchase journey it affects
2. How the problem could prevent a wishlist item from being purchased
3. Which stage of the funnel it influences
4. Whether the available evidence suggests a plausible relationship with purchase conversion
5. What leading behavioral metric could indicate improvement
6. The strength of evidence connecting the problem to the business metric

Map each identified opportunity to the relevant stage(s) of the wishlist-to-purchase journey, using the following framework as a starting point:

Wishlist Added
→ Wishlist Revisit
→ Product Re-evaluation
→ Purchase Confidence
→ Add to Cart
→ Purchase

If research reveals a meaningful user behavior or stage that does not fit this framework, flag it as an emerging stage rather than forcing it into an existing category.

Do not claim causality unless supported by evidence.

Rank opportunities not only by frequency or severity, but by their potential relevance to the stated business metric.