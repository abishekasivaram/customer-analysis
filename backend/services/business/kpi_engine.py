import json
import os
from backend.core.logger import bus_logger

class KPIEngine:
    def __init__(self):
        self.output_dir = "outputs/business"
        
    def analyze(self, retail_summary, dwells, segments, zone_perfs):
        bus_logger.info("Starting KPI Engine analysis.")
        
        # Calculate conversion: Quick proxy = buyers / total. 
        # For Hackzen we might say "Picking" is buying.
        picking_events = sum([z.get('interaction_count', 0) for z in zone_perfs])
        total_customers = retail_summary.get('total_customers', 1)
        conversion = min(1.0, picking_events / total_customers) if total_customers else 0
        
        kpi_data = {
            "average_visit_time": retail_summary.get('average_visit_duration', 0),
            "customer_conversion": conversion,
            "average_interaction_count": picking_events / total_customers if total_customers else 0,
            "store_utilization": 0.65, # Mock heuristic representing overall traffic vs space
            "zone_utilization": {z['zone']: min(1.0, z['visitors']/100) for z in zone_perfs},
            "peak_hour": "14:00", # Mock
            "heatmap_density": "High",
            "behavior_distribution": segments,
            "most_popular_zone": max(zone_perfs, key=lambda x: x['visitors'])['zone'] if zone_perfs else None,
            "least_popular_zone": min(zone_perfs, key=lambda x: x['visitors'])['zone'] if zone_perfs else None
        }
        
        with open(os.path.join(self.output_dir, "kpi_dashboard.json"), 'w') as f:
            json.dump(kpi_data, f, indent=4)
            
        bus_logger.info("KPI Engine analysis completed.")
        return kpi_data
