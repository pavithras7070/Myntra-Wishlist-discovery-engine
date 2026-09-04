from collections import Counter
from typing import List, Dict, Any
from models import QuantitativeMetrics

class QuantitativeAggregator:
    def __init__(self, insights: List[Dict[str, Any]]):
        self.insights = insights
        self.relevant_insights = [i for i in insights if i.get("is_relevant")]

    def aggregate(self) -> QuantitativeMetrics:
        total = len(self.insights)
        relevant = len(self.relevant_insights)
        perc = (relevant / total * 100) if total > 0 else 0.0

        stages = Counter(i.get("shopping_stage", "Unknown") for i in self.relevant_insights)
        intents = Counter(i.get("intent_type", "Unknown") for i in self.relevant_insights if i.get("intent_type") and i.get("intent_type") != "Unknown")
        barriers = Counter(i.get("purchase_barrier", ["Unknown"])[0] if isinstance(i.get("purchase_barrier"), list) and i.get("purchase_barrier") else "Unknown" for i in self.relevant_insights)
        uncertainties = Counter(i.get("uncertainty", "Unknown") for i in self.relevant_insights if i.get("uncertainty") and i.get("uncertainty") != "Unknown")
        workarounds = Counter(i.get("user_workaround", "Unknown") for i in self.relevant_insights if i.get("user_workaround") and i.get("user_workaround") not in ["Unknown", "null"])
        
        pre_purchase_behavior_list = []
        for i in self.relevant_insights:
            b_type = i.get("pre_purchase_behavior_type")
            if not b_type or str(b_type).lower() in ["n/a", "nan", "unknown"]:
                # Try to classify based on existing fields
                if i.get("purchase_barrier") and i.get("purchase_barrier") not in ["Unknown", "N/A", "None"]:
                    b_type = "Explicit Barrier"
                elif i.get("uncertainty") and i.get("uncertainty") not in ["Unknown", "N/A", "None"]:
                    b_type = "Implicit Uncertainty"
                else:
                    b_type = "Pure Shopping Intent"
            pre_purchase_behavior_list.append(b_type)

        pre_purchase_behavior = Counter(pre_purchase_behavior_list)
        
        # Semantic Theme Normalization Map
        def normalize_theme(need_str):
            n = need_str.lower()
            if any(k in n for k in ["size", "sizing", "fit", "measure", "tall"]):
                return "Sizing, Fit & Measurement Confidence"
            if any(k in n for k in ["material", "tactile", "quality", "print", "durability", "fabric", "shape", "retention"]):
                return "Material Quality & Durability"
            if any(k in n for k in ["price", "value", "affordable", "money", "sasta"]):
                return "Price & Value Assessment"
            if any(k in n for k in ["return", "refund", "credit", "trust", "reliability"]):
                return "Platform Trust & Return Policies"
            if any(k in n for k in ["represent", "accuracy", "visual", "appearance"]):
                return "Product Representation & Accuracy"
            if any(k in n for k in ["styling", "style", "discovery", "compare", "comparison", "personal", "suitability", "brand", "aesthetics"]):
                return "Styling Use-Case & Comparison"
            return need_str
            return need_str
            
        semantic_needs = {}
        for item in self.relevant_insights:
            raw_need = item.get("semantic_customer_need")
            if not raw_need or raw_need == "Unknown":
                continue
                
            need = normalize_theme(raw_need)
                
            if need not in semantic_needs:
                semantic_needs[need] = {
                    "count": 0,
                    "workarounds": Counter(),
                    "severity_scores": [],
                    "relevance_scores": [],
                    "sources": Counter()
                }
                
            semantic_needs[need]["count"] += 1
            raw_source = str(item.get("platform", item.get("source_platform", "Unknown"))).lower()
            source_map = {
                "myntra_web": "Myntra Web",
                "myntra_product_reviews": "Myntra Web",
                "ecommerce_reviews": "Myntra Web",
                "app_store": "App Store",
                "myntra-fashion-shopping-app": "App Store",
                "youtube_comments": "YouTube",
                "youtube": "YouTube",
                "google_play": "Google Play Store",
                "play_store": "Google Play Store",
                "com.myntra.android": "Google Play Store",
                "reddit": "Reddit",
                "": "Reddit",
                "unknown": "Reddit"
            }
            source = source_map.get(raw_source, "Unknown")
            semantic_needs[need]["sources"][source] += 1
            
            workaround = item.get("user_workaround")
            if workaround and workaround not in ["Unknown", "null"]:
                if isinstance(workaround, list):
                    for w in workaround:
                        semantic_needs[need]["workarounds"][w] += 1
                else:
                    semantic_needs[need]["workarounds"][workaround] += 1
                    
            strength = item.get("evidence_strength")
            if strength == "strong":
                semantic_needs[need]["severity_scores"].append(3)
            elif strength == "moderate":
                semantic_needs[need]["severity_scores"].append(2)
            else:
                semantic_needs[need]["severity_scores"].append(1)
                
            relevance = item.get("relevance")
            if relevance == "high":
                semantic_needs[need]["relevance_scores"].append(3)
            elif relevance == "medium":
                semantic_needs[need]["relevance_scores"].append(2)
            else:
                semantic_needs[need]["relevance_scores"].append(1)

        # Finalize averages
        for need, data in semantic_needs.items():
            if data["severity_scores"]:
                data["avg_severity"] = sum(data["severity_scores"]) / len(data["severity_scores"])
            else:
                data["avg_severity"] = 1.0
            
            if data["relevance_scores"]:
                data["avg_relevance"] = sum(data["relevance_scores"]) / len(data["relevance_scores"])
            else:
                data["avg_relevance"] = 1.0
                
            data["workarounds"] = dict(data["workarounds"])
            data["sources"] = dict(data.get("sources", {}))
            del data["severity_scores"]
            del data["relevance_scores"]
        decision_relevance = Counter(i.get("decision_relevance", "Unknown") for i in self.relevant_insights)
        wishlist_relevance = Counter(i.get("wishlist_relevance", "Unknown") for i in self.relevant_insights)
        wishlist_mentions = sum(1 for i in self.relevant_insights if i.get("wishlist_mention") is True)

        # Barrier Co-occurrence Matrix
        co_occurrences: Dict[str, Dict[str, int]] = {}
        for item in self.relevant_insights:
            b = item.get("semantic_customer_need")
            u = item.get("uncertainty")
            if b and b != "Unknown" and u and u != "Unknown":
                if isinstance(u, list):
                    u = u[0] if len(u) > 0 else "Unknown"
                if isinstance(b, list):
                    b = b[0] if len(b) > 0 else "Unknown"
                if b not in co_occurrences:
                    co_occurrences[b] = {}
                co_occurrences[b][u] = co_occurrences[b].get(u, 0) + 1

        return QuantitativeMetrics(
            total_conversations=total,
            relevant_conversations=relevant,
            relevance_percentage=perc,
            shopping_stages=dict(stages),
            intent_frequencies=dict(intents),
            barrier_frequencies=dict(barriers),
            uncertainty_frequencies=dict(uncertainties),
            workaround_frequencies=dict(workarounds),
            wishlist_mentions=wishlist_mentions,
            decision_relevance_distribution=dict(decision_relevance),
            wishlist_relevance_distribution=dict(wishlist_relevance),
            barrier_co_occurrences=co_occurrences,
            pre_purchase_behavior_types=dict(pre_purchase_behavior),
            semantic_customer_needs=dict(semantic_needs)
        )
