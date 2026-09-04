# Play Store Phase 2 LLM Output Validation

This document validates the actual results of running the 212 Play Store candidate reviews through the existing Phase 2 LLM pipeline (`behavior_extractor` + `root_cause_analyzer`), utilizing the unrestricted `qwen3.8-27b` extraction model.

## 1. Output Validation Metrics

1. **Total reviews processed:** 212
2. **Successful records:** 212 (0 failed/skipped due to LLM errors)
3. **Decision relevance distribution (Intent):** 
   * `Unknown`: 94
   * `comparison`: 6
   * `price monitoring`: 4
4. **Wishlist relevance distribution:** 
   * `General/Unknown` (or filtered out): 212
5. **Standardized barrier frequencies (Top Extracted):**
   * `Unknown`: 75
   * `Products in wishlist are marked as not deliverable`: 1
   * `Item unable to deliver to available pincode`: 1
   * `Item out of stock`: 1
   * `Wishlist and bag limits prevent saving products for future purchase`: 1
   * `Return fee policy`: 1
6. **Shopping-stage distribution:**
   * `Purchase`: 85
   * `Wishlist/Save`: 6
   * `Cart`: 4
   * `Product Evaluation`: 3
   * `Discovery`: 1
   * `Unknown`: 5
7. **Direct wishlist evidence count:** 0 (Classified strictly by LLM extraction schema)
8. **Indirect wishlist evidence count:** 0 
9. **General/unknown evidence:** 212
10. **Duplicate or invalid records:** 0

---

## 2. Comparison: Actual LLM vs Deterministic Audit (Phase 3 Synthesis)

### The LLM Pipeline Failed to Classify Wishlist Behavior
The most critical finding from running the actual Phase 2 LLM pipeline is a massive discrepancy between **Automated LLM Extraction** and **Deterministic Human Rules**. 

In the deterministic audit, we proved that 10 out of the 212 reviews contained airtight, explicit textual evidence of wishlist-to-purchase barriers (e.g. "most of the products in my wishlist"). 

However, the existing Phase 2 LLM `behavior_extractor` strictly labeled all of them as `Unknown/General` for wishlist relevance. 

**Why did this happen?**
1. **Strict System Prompt Constraints:** The existing prompt forces the LLM to say `Unknown` if intent is ambiguous. The LLM aggressively over-corrected, marking explicit wishlist mentions as `Unknown` intent.
2. **Schema Rigidity:** The LLM successfully extracted the raw barriers (e.g., *"Products in wishlist are marked as not deliverable"*), but the rigid classification fields (`intent_type`, `wishlist_mention`) failed to trigger `True`.

### Shopping Stage Distribution
The LLM successfully identified that the vast majority of the relevant barriers occurred at the **Purchase (85)** stage, perfectly aligning with our manual audit that pincode unserviceability and return-fee policies block users at the final checkout, not during discovery.

### Barrier Consistency
The LLM accurately extracted the exact same barriers that were manually audited:
- Pincode restriction during sales
- Out of stock holding
- Capacity limits

## 3. Conclusion for the Dashboard

The LLM extraction pipeline is excellent at summarizing raw textual barriers into sentences, but it is currently **incapable of accurately classifying Direct Wishlist Evidence**. If we rely solely on the automated Phase 2/3 outputs for the dashboard, we will incorrectly report that there is `0` wishlist evidence in the Play Store, when deterministic rules proved there are 10 highly relevant cases. 

**Recommendation:** The dashboard must rely on the deterministic evidence mappings created during the synthesis phase, rather than the raw categorical classifications output by the current Phase 2 LLM pipeline.
