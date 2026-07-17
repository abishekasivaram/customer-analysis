import glob
import json
import os
import csv
from backend.core.logger import bus_logger

class ZonePerformanceEngine:
    def __init__(self):
        self.output_dir = "outputs/business"
        
    def analyze(self):
        bus_logger.info("Starting Zone Performance analysis.")
        zone_files = glob.glob("outputs/analytics/*_zone_analytics.json")
        
        zones_summary = {}
        
        for zf in zone_files:
            with open(zf, 'r') as f:
                zones = json.load(f)
                
            for metrics in zones:
                zone_name = metrics.get('zone_id', 'Unknown Zone')
                if zone_name not in zones_summary:
                    zones_summary[zone_name] = {
                        "zone": zone_name,
                        "visitors": 0,
                        "average_dwell_time": 0.0,
                        "peak_occupancy": 0,
                        "interaction_count": 0,
                        "conversion_rate": 0.0
                    }
                z = zones_summary[zone_name]
                z["visitors"] += metrics.get("customer_count", 0)
                z["peak_occupancy"] = max(z["peak_occupancy"], metrics.get("peak_occupancy", 0))
                # Running average approximation
                z["average_dwell_time"] = (z["average_dwell_time"] + metrics.get("average_dwell_time_seconds", 0)) / 2 if z["average_dwell_time"] > 0 else metrics.get("average_dwell_time_seconds", 0)
                
                # Behaviors might be a string representation of a dict
                b_str = metrics.get("behaviors_observed", "{}")
                try:
                    import ast
                    b_dict = ast.literal_eval(b_str) if isinstance(b_str, str) else b_str
                    if isinstance(b_dict, dict):
                        z["interaction_count"] += sum(b_dict.values())
                except:
                    pass
                
        # Calculate conversion rate heuristics (e.g. interaction / visitors)
        for z in zones_summary.values():
            if z["visitors"] > 0:
                z["conversion_rate"] = min(1.0, z["interaction_count"] / z["visitors"])
                
        results = list(zones_summary.values())
        
        with open(os.path.join(self.output_dir, "zone_performance.json"), 'w') as f:
            json.dump(results, f, indent=4)
            
        if results:
            with open(os.path.join(self.output_dir, "zone_performance.csv"), 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
                
        bus_logger.info(f"Analyzed {len(results)} zones.")
        return results
