import uuid
import datetime
from backend.services.advisor.rule_engine import RuleEngine
from backend.services.advisor.confidence_engine import ConfidenceEngine

class InventoryAdvisor:
    def __init__(self, rule_engine: RuleEngine, confidence_engine: ConfidenceEngine):
        self.rules = rule_engine
        self.conf_engine = confidence_engine

    def analyze(self, dashboard_data, trends):
        recommendations = []
        zones = dashboard_data.get("zones", [])
        
        interaction_low = self.rules.get_threshold("interaction", "low")
        interaction_high = self.rules.get_threshold("interaction", "high")
        
        for zone in zones:
            visitors = zone.get("visitors", 0)
            interactions = zone.get("interaction_count", 0)
            z_name = zone.get("zone", "Unknown Zone")
            
            # Simple heuristic
            interaction_rate = (interactions / visitors * 100) if visitors > 0 else 0
            trend_val = trends.get("zone_trend", {}).get(z_name, {}).get("trend", "stable")
            
            if visitors > 2 and interaction_rate <= interaction_low:
                rec = self._build_rec(
                    z_name, "Medium", "HighTrafficLowInteraction",
                    f"Low Product Visibility in {z_name}",
                    f"Zone has high traffic but low interaction rate ({interaction_rate:.1f}%).",
                    visitors, interaction_rate, trend_val,
                    "Recommend changing product placement or enhancing visibility."
                )
                recommendations.append(rec)
                
            elif interactions > 0 and interaction_rate >= interaction_high:
                rec = self._build_rec(
                    z_name, "High", "HighInteractionLowConversion",
                    f"Strong Engagement in {z_name}",
                    f"Zone has high interaction rate ({interaction_rate:.1f}%).",
                    visitors, interaction_rate, trend_val,
                    "Recommend promotional campaigns or ensuring stock levels."
                )
                recommendations.append(rec)
                
        return recommendations
        
    def _build_rec(self, zone_name, priority, rule_name, title, desc, visitors, int_rate, trend, action):
        conf = self.conf_engine.compute_confidence(3, trend)
        return {
            "recommendation_id": f"REC-IA-{uuid.uuid4().hex[:8]}",
            "category": "Merchandising",
            "priority": priority,
            "confidence": conf,
            "title": title,
            "description": desc,
            "reasoning": [f"Visitors: {visitors}", f"Interaction rate: {int_rate:.1f}%"],
            "supporting_metrics": {"visitors": visitors, "interaction_rate": int_rate},
            "expected_business_impact": "Optimized sales conversions.",
            "estimated_improvement": "10-15% increase in conversion",
            "generated_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "triggered_rule": rule_name,
            "affected_metrics": ["interaction_rate", "conversion_rate"],
            "business_objective": "Product Visibility",
            "recommended_action": action,
            "expected_improvement": "Increased product pickups",
            "estimated_business_impact": "Medium",
            "estimated_roi": "High",
            "implementation_difficulty": "Low",
            "risk_level": "Low",
            "validation_status": "PENDING",
            "impact_score": 75 if priority == "High" else 55
        }
