# Detailed Edge Cases: AI-Powered Myntra Wishlist Discovery Engine

This document outlines the detailed edge cases, potential failure modes, and corner scenarios for the AI-Powered Discovery Engine, derived from the problem statement and phase-wise architecture.

Addressing these edge cases is critical to ensuring the validity of the insights and preventing the system from generating misleading hypotheses.

---

## Phase 1: Data Foundation (Data Collection & Normalization)

### 1. Linguistic and Syntactic Challenges
*   **Hinglish & Code-Switching:** Users frequently blend Hindi and English (e.g., "Size ekdum perfect hai but material is thoda rough"). Standard NLP models might misclassify or fail to extract the barrier (material) and the positive attribute (size).
*   **Sarcasm and Irony:** "Great fit! If you are a toddler." Simple sentiment analysis or naive LLM prompts might classify this as a positive review regarding fit, completely missing the size barrier.
*   **Typographical Errors and Slang:** "wshtlst" (wishlist), "rtrn" (return), "osm" (awesome). The normalizer must handle heavy internet slang without losing semantic meaning.

### 2. Data Quality and Noise
*   **Compound/Mixed Reviews:** "I loved the red dress, but the blue one I added to my wishlist was out of stock, and the delivery was late." The system must attribute the correct sentiment and barrier to the correct product/action, avoiding cross-contamination.
*   **Spam, Bots, and Competitor Bashing:** Coordinated fake reviews or generic spam (e.g., "Use code XYZ for 50% off") that could skew quantitative frequency metrics if not aggressively filtered.
*   **Contextless Short Reviews:** "Nice," "Bad," or "Too small." While "too small" is actionable, "bad" provides no root cause. The system must prevent these from diluting the "Unknown" category in the taxonomy.
*   **PII Leakage:** Users occasionally post phone numbers, order IDs, or addresses in reviews. The normalizer must reliably redact this before it enters the Data Lake.

---

## Phase 2: AI Analysis Core (Taxonomy & Extraction)

### 3. Misinterpretation of Intent and Behavior
*   **Colloquial vs. Literal "Wishlist":** A user saying "Gucci is on my wishlist for when I get rich" (aspirational) vs. "I added this Zara top to my wishlist yesterday" (active consideration). The engine must distinguish between high-intent app actions and general aspirations.
*   **Implicit vs. Explicit Barriers:** "I'll wait for the Big Fashion Festival." The user hasn't explicitly stated "the price is currently too high," but the implicit barrier is price/discount expectation. The Root Cause Analyzer (Stage 4) must capture this without hallucinating.
*   **Attribution of External Research:** "Saw this on a Myntra haul on YT, but buying from AJIO because it's cheaper." The system must correctly attribute the discovery to YouTube, the comparison to AJIO, and the barrier to price, rather than concluding the user is looking for Myntra reviews on AJIO.

### 4. LLM Hallucinations and Extraction Failures
*   **Taxonomy Hallucination:** The LLM inventing a new category of "Uncertainty" (e.g., "Astrological incompatibility") that sounds plausible in context but is garbage data. Function calling/JSON mode strictness is required.
*   **Conflating Observation with Inference:** A user says, "I didn't buy it." The LLM infers, "User didn't buy because of price." This violates the core rule of separating *Observed Evidence* from *AI Interpretation*. The pipeline must enforce strict boundaries.

---

## Phase 3: Intelligence Layer (Segments & Contradictions)

### 5. Segmentation Edge Cases
*   **Sparse or Micro-Segments:** The clustering algorithm might find a highly specific segment (e.g., "Users who only buy purple shoes on Tuesdays"). The system must enforce a minimum support threshold (e.g., >2% of dataset) to avoid surfacing irrelevant noise.
*   **Overlapping/Dynamic User Profiles:** A user might be highly price-sensitive for basic t-shirts but brand-loyal and price-insensitive for sneakers. Segments must be contextualized by fashion category, not just globally applied to the user hash.

### 6. Contradiction Detection Failures
*   **False Contradictions:** "The medium was too small" vs. "The large was too big." These aren't contradictions; they represent a root cause of "inconsistent sizing gaps." The detector must be nuanced enough to recognize this rather than flagging it as conflicting evidence.
*   **Missing Nuance in Consensus:** 90% of users say quality is bad, 10% say it's good. The 10% might be referring to a specific batch or vendor. The engine should highlight the context of the minority opinion rather than just presenting a raw 90/10 split.

---

## Phase 4: Opportunity Engine (Scoring & Prioritization)

### 7. Scoring and Ranking Skews
*   **The "Measurability" Bias (Echo Chamber):** Problems that are easy for the LLM to detect (e.g., explicit price complaints) naturally score higher in *Frequency* than subtle UX issues (e.g., comparison overload). The scoring formula must account for the *Severity* and *Purchase Relevance* to prevent obvious, low-leverage insights from dominating the Opportunity Matrix.
*   **Misjudging Product Leverage:** The engine might identify "Brands use cheap material" as a top opportunity. However, Myntra (the platform) has low leverage to change a third-party brand's manufacturing process. The system must correctly score *Product Leverage* to favor platform-level solutions (e.g., better material filtering or fabric zoom features) over manufacturing issues.
*   **Hypothesis Creep:** AI-generated hypotheses (Level 2) slowly being treated as Validated Findings (Level 3) by users of the dashboard over time. The UI must aggressively visually distinguish the hypothesis level.

---

## Phase 5: Dashboard & Evidence Explorer

### 8. UI and Performance Edge Cases
*   **Evidence Traceability Breakage:** If the Data Lake is purged or updated and UUIDs change, the Evidence Explorer links from the Opportunity Matrix to the raw source text will break. Referential integrity is paramount.
*   **Data Overload in Visualization:** Rendering a network graph (Barrier Co-occurrence) or Sankey diagram (External Research Map) with 10,000 nodes will freeze the browser. The API must aggregate and paginate data effectively.
*   **Context Loss in Snippets:** Showing only the extracted sentence in the Evidence Explorer might strip away crucial context. The UI must provide a "View Full Original Conversation" button for every snippet to maintain trust and explainability.
