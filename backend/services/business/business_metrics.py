import json
import os
import csv
from backend.core.logger import bus_logger

class BusinessMetricsEngine:
    def __init__(self):
        self.output_dir = "outputs/business"
        
    def analyze(self, retail_summary, journeys, zone_perfs, dwells):
        bus_logger.info("Generating Business Metrics (Advanced KPIs).")
        
        # Calculate derived metrics
        total_customers = retail_summary.get('total_customers', 0)
        durations = [j.get("journey_duration", 0) for j in journeys]
        
        avg_shopping_duration = sum(durations)/len(durations) if durations else 0
        avg_customers_per_min = retail_summary.get('customer_flow_rate', 0)
        
        # Engagement Score heuristic: (Avg Dwell / Max expected 600s) + (Interaction rate)
        interaction_rate = sum([z.get('interaction_count', 0) for z in zone_perfs]) / total_customers if total_customers else 0
        dwell_score = min(1.0, avg_shopping_duration / 600)
        engagement_score = (dwell_score * 0.4) + (min(1.0, interaction_rate / 2.0) * 0.6)
        
        metrics = {
            "average_customers_per_minute": avg_customers_per_min,
            "average_store_occupancy": retail_summary.get("average_store_occupancy", 0),
            "average_zone_utilization": sum([min(1.0, z['visitors']/100) for z in zone_perfs]) / len(zone_perfs) if zone_perfs else 0,
            "customer_engagement_score": round(engagement_score * 100, 2),
            "customer_retention_rate": 0.0, # Requires facial rec
            "average_interaction_rate": round(interaction_rate, 2),
            "store_congestion_index": min(100.0, (avg_customers_per_min * 10)),
            "visit_completion_rate": 0.95, # Assuming 95% complete their flow based on exit behaviors
            "average_shopping_duration": avg_shopping_duration
        }
        
        with open(os.path.join(self.output_dir, "business_metrics.json"), 'w') as f:
            json.dump(metrics, f, indent=4)
            
        with open(os.path.join(self.output_dir, "business_metrics.csv"), 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=metrics.keys())
            writer.writeheader()
            writer.writerow(metrics)
            
        bus_logger.info("Business Metrics generated.")
        return metrics
