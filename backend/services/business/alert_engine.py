import json
import os
import yaml
from backend.core.logger import bus_logger

class AlertEngine:
    def __init__(self, config_path="configs/business.yaml"):
        self.output_dir = "outputs/business"
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.thresholds = self.config.get('thresholds', {})
        
    def analyze(self, zone_perfs):
        bus_logger.info("Starting Business Alert analysis.")
        alerts = []
        
        congestion_threshold = self.thresholds.get('congestion', 15)
        low_activity = self.thresholds.get('zone_activity_low', 2)
        
        for z in zone_perfs:
            zone = z['zone']
            visitors = z['visitors']
            
            if visitors >= congestion_threshold:
                alerts.append({
                    "severity": "HIGH",
                    "timestamp": "Now",
                    "zone": zone,
                    "description": f"High congestion detected in {zone} ({visitors} visitors).",
                    "recommendation": "Increase staff allocation."
                })
            
            if visitors <= low_activity:
                alerts.append({
                    "severity": "LOW",
                    "timestamp": "Now",
                    "zone": zone,
                    "description": f"Low activity in {zone}.",
                    "recommendation": "Consider marketing displays or promotions."
                })
                
            if z.get('interaction_count', 0) > 20:
                alerts.append({
                    "severity": "MEDIUM",
                    "timestamp": "Now",
                    "zone": zone,
                    "description": f"High interaction in {zone}.",
                    "recommendation": "Monitor inventory levels."
                })
                
        with open(os.path.join(self.output_dir, "business_alerts.json"), 'w') as f:
            json.dump(alerts, f, indent=4)
            
        bus_logger.info(f"Generated {len(alerts)} business alerts.")
        return alerts
