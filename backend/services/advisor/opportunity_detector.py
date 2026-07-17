import uuid

class OpportunityDetector:
    def __init__(self, rule_engine):
        self.rules = rule_engine

    def detect(self, dashboard_data, trends):
        opportunities = []
        zones = dashboard_data.get("zones", [])
        
        for zone in zones:
            z_name = zone.get("zone", "Unknown Zone")
            int_count = zone.get("interaction_count", 0)
            visitors = zone.get("visitors", 0)
            
            int_rate = (int_count / visitors * 100) if visitors > 0 else 0
            
            if int_rate > self.rules.get_threshold("interaction", "high"):
                opportunities.append({
                    "opportunity_id": f"OPP-{uuid.uuid4().hex[:8]}",
                    "type": "High Engagement Shelf",
                    "zone": z_name,
                    "description": f"Zone exhibits exceptionally high engagement ({int_rate:.1f}%). Ideal for premium product placement.",
                    "potential_impact": "High ROI on upselling."
                })
                
        return opportunities
