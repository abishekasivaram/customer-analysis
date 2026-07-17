import uuid
import datetime
from backend.services.advisor.rule_engine import RuleEngine
from backend.services.advisor.confidence_engine import ConfidenceEngine

class LayoutOptimizer:
    def __init__(self, rule_engine: RuleEngine, confidence_engine: ConfidenceEngine):
        self.rules = rule_engine
        self.conf_engine = confidence_engine

    def analyze(self, dashboard_data, trends):
        recommendations = []
        zones = dashboard_data.get("zones", [])
        
        congestion_critical = self.rules.get_threshold("congestion", "critical")
        congestion_warning = self.rules.get_threshold("congestion", "warning")
        
        for zone in zones:
            peak_occ = zone.get("peak_occupancy", 0)
            avg_dwell = zone.get("average_dwell_time", 0)
            z_name = zone.get("zone", "Unknown Zone")
            
            # Simple heuristic: Peak Occupancy relative to hardcoded max of 5 (for HackZen dataset context)
            congestion_ratio = (peak_occ / 5.0) * 100 if peak_occ > 0 else 0
            
            trend_str = "stable"
            
            if congestion_ratio >= congestion_critical:
                rec = self._build_rec(
                    z_name, "High", "CriticalCongestion",
                    f"Critical congestion in {z_name}",
                    f"Peak occupancy reached {peak_occ}. Aisle widening or product relocation is recommended.",
                    congestion_ratio, avg_dwell, trend_str
                )
                recommendations.append(rec)
            elif congestion_ratio >= congestion_warning:
                rec = self._build_rec(
                    z_name, "Medium", "WarningCongestion",
                    f"High traffic in {z_name}",
                    f"Traffic is building in {z_name}. Monitor for layout bottlenecks.",
                    congestion_ratio, avg_dwell, trend_str
                )
                recommendations.append(rec)
                
        return recommendations
        
    def _build_rec(self, zone_name, priority, rule_name, title, desc, congestion_ratio, dwell, trend):
        conf = self.conf_engine.compute_confidence(2, trend)
        return {
            "recommendation_id": f"REC-LO-{uuid.uuid4().hex[:8]}",
            "category": "Store Layout",
            "priority": priority,
            "confidence": conf,
            "title": title,
            "description": desc,
            "reasoning": [f"Congestion ratio at {congestion_ratio:.1f}%", f"Average dwell time: {dwell}s"],
            "supporting_metrics": {"congestion_ratio": congestion_ratio, "dwell_time": dwell},
            "expected_business_impact": "Improved customer flow and reduced bottlenecking.",
            "estimated_improvement": "15-20% flow rate increase",
            "generated_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "triggered_rule": rule_name,
            "affected_metrics": ["customer_flow", "store_congestion_index"],
            "business_objective": "Congestion Reduction",
            "recommended_action": f"Widen aisle or distribute popular products in {zone_name}",
            "expected_improvement": "Reduced dwell time in bottlenecks",
            "estimated_business_impact": "High",
            "estimated_roi": "Medium",
            "implementation_difficulty": "High",
            "risk_level": "Low",
            "validation_status": "PENDING",
            "impact_score": 85 if priority == "High" else 65
        }
