import uuid
import datetime
from backend.services.advisor.rule_engine import RuleEngine
from backend.services.advisor.confidence_engine import ConfidenceEngine

class EngagementAdvisor:
    def __init__(self, rule_engine: RuleEngine, confidence_engine: ConfidenceEngine):
        self.rules = rule_engine
        self.conf_engine = confidence_engine

    def analyze(self, dashboard_data, trends):
        recommendations = []
        zones = dashboard_data.get("zones", [])
        
        dwell_high = self.rules.get_threshold("dwell_time", "high")
        interaction_low = self.rules.get_threshold("interaction", "low")
        
        for zone in zones:
            avg_dwell = zone.get("average_dwell_time", 0)
            interactions = zone.get("interaction_count", 0)
            visitors = zone.get("visitors", 0)
            z_name = zone.get("zone", "Unknown Zone")
            
            interaction_rate = (interactions / visitors * 100) if visitors > 0 else 0
            trend_val = trends.get("zone_trend", {}).get(z_name, {}).get("trend", "stable")
            
            if avg_dwell >= dwell_high and interaction_rate <= interaction_low:
                rec = self._build_rec(
                    z_name, "Medium", "HighDwellLowInteraction",
                    f"Pricing/Promotion Opportunity in {z_name}",
                    f"Customers linger ({avg_dwell}s) but rarely interact.",
                    avg_dwell, interaction_rate, trend_val,
                    "Recommend improving pricing or prominent promotions."
                )
                recommendations.append(rec)
                
        return recommendations
        
    def _build_rec(self, zone_name, priority, rule_name, title, desc, dwell, int_rate, trend, action):
        conf = self.conf_engine.compute_confidence(2, trend)
        return {
            "recommendation_id": f"REC-EA-{uuid.uuid4().hex[:8]}",
            "category": "Customer Engagement",
            "priority": priority,
            "confidence": conf,
            "title": title,
            "description": desc,
            "reasoning": [f"Dwell time: {dwell}s", f"Interaction rate: {int_rate:.1f}%"],
            "supporting_metrics": {"dwell_time": dwell, "interaction_rate": int_rate},
            "expected_business_impact": "Improved customer engagement.",
            "estimated_improvement": "Higher likelihood to pick product.",
            "generated_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "triggered_rule": rule_name,
            "affected_metrics": ["dwell_time", "interaction_rate"],
            "business_objective": "Customer Engagement",
            "recommended_action": action,
            "expected_improvement": "Reduced hesitation time",
            "estimated_business_impact": "High",
            "estimated_roi": "Medium",
            "implementation_difficulty": "Medium",
            "risk_level": "Low",
            "validation_status": "PENDING",
            "impact_score": 70
        }
