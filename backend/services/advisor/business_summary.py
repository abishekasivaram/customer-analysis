from backend.core.logger import adv_logger

class BusinessSummaryEngine:
    def __init__(self, rule_engine):
        self.rules = rule_engine

    def generate_store_health(self, metrics, trends, dashboard_data):
        # Health formula (0-100)
        # Base: 100
        health = 100.0
        
        # Penalize for critical congestion (up to 20 pts)
        congestion_index = metrics.get("store_congestion_index", 0)
        if congestion_index > 80:
            health -= 20
        elif congestion_index > 50:
            health -= 10
            
        # Reward for engagement score (up to 15 pts)
        engagement = metrics.get("customer_engagement_score", 0)
        if engagement > 80:
            pass # keep health high
        elif engagement < 40:
            health -= 15
            
        # Penalize for dead zones
        zones = dashboard_data.get("zones", [])
        dead_zones = sum(1 for z in zones if z.get("visitors", 0) == 0)
        health -= (dead_zones * 5)
        
        # Keep bounded
        health = max(0.0, min(100.0, health))
        
        status = "Healthy"
        if health < self.rules.get_threshold("health_score", "critical"):
            status = "Critical"
        elif health < self.rules.get_threshold("health_score", "warning"):
            status = "Warning"
            
        return {
            "store_health_score": round(health, 1),
            "status": status,
            "metrics_used": ["congestion_index", "engagement_score", "dead_zones"]
        }
