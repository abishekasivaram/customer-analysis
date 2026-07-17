import uuid
import datetime
from backend.services.advisor.rule_engine import RuleEngine
from backend.services.advisor.confidence_engine import ConfidenceEngine

class FlowOptimizer:
    def __init__(self, rule_engine: RuleEngine, confidence_engine: ConfidenceEngine):
        self.rules = rule_engine
        self.conf_engine = confidence_engine

    def analyze(self, flow_data, trends):
        recommendations = []
        
        # flow_data has dead_zones and congested_areas
        dead_zones = flow_data.get("dead_zones", [])
        
        for dz in dead_zones:
            rec = self._build_rec(
                dz, "Medium", "LowCustomerFlow",
                f"Dead Zone Detected: {dz}",
                f"The zone {dz} has abnormally low traffic.",
                dz, "stable",
                "Recommend improving store entrance visibility or placing high-demand items nearby."
            )
            recommendations.append(rec)
                
        return recommendations
        
    def _build_rec(self, zone_name, priority, rule_name, title, desc, dz, trend, action):
        conf = self.conf_engine.compute_confidence(1, trend)
        return {
            "recommendation_id": f"REC-FO-{uuid.uuid4().hex[:8]}",
            "category": "Store Flow",
            "priority": priority,
            "confidence": conf,
            "title": title,
            "description": desc,
            "reasoning": [f"Zone is identified as a dead zone in flow mapping."],
            "supporting_metrics": {"dead_zone": dz},
            "expected_business_impact": "Improved store-wide footfall.",
            "estimated_improvement": "Elimination of cold spots.",
            "generated_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "triggered_rule": rule_name,
            "affected_metrics": ["customer_flow"],
            "business_objective": "Traffic Optimization",
            "recommended_action": action,
            "expected_improvement": "More balanced store utilization",
            "estimated_business_impact": "High",
            "estimated_roi": "Medium",
            "implementation_difficulty": "Medium",
            "risk_level": "Low",
            "validation_status": "PENDING",
            "impact_score": 60
        }
