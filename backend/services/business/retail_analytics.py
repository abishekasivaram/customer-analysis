import glob
import json
import os
import csv
from backend.core.logger import bus_logger

class RetailAnalyticsEngine:
    def __init__(self):
        self.output_dir = "outputs/business"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def analyze(self):
        bus_logger.info("Starting Retail Analytics generation.")
        behavior_files = glob.glob("outputs/behavior/json/*_behavior.json")
        timeline_files = glob.glob("outputs/behavior/timeline/*_timeline.json")
        zone_files = glob.glob("outputs/analytics/*_zone_analytics.json")
        
        total_customers = set()
        total_events = 0
        behavior_counts = {}
        total_duration = 0.0
        
        for bf in behavior_files:
            base_name = os.path.basename(bf).replace("_behavior.json", "")
            with open(bf, 'r') as f:
                events = json.load(f)
                total_events += len(events)
                for ev in events:
                    total_customers.add(f"{base_name}_{ev['track_id']}")
                    b = ev['behavior']
                    behavior_counts[b] = behavior_counts.get(b, 0) + 1
                    total_duration += (ev['end_time'] - ev['start_time'])
                    
        total_unique = len(total_customers)
        avg_dwell = total_duration / total_unique if total_unique > 0 else 0
        
        summary = {
            "total_customers": total_unique,
            "unique_customers": total_unique, # heuristic
            "returning_customers": 0, # requires facial rec, stub for now
            "average_visit_duration": avg_dwell,
            "average_dwell_time": avg_dwell,
            "peak_shopping_time": "12:00 PM", # mock based on missing wall clock time
            "average_store_occupancy": total_unique / len(behavior_files) if behavior_files else 0,
            "customer_flow_rate": total_unique / (len(behavior_files) * 60) if behavior_files else 0, # per minute
            "total_events": total_events,
            "total_behaviors": total_events
        }
        
        # Write JSON
        with open(os.path.join(self.output_dir, "retail_summary.json"), 'w') as f:
            json.dump(summary, f, indent=4)
            
        # Write CSV
        with open(os.path.join(self.output_dir, "retail_summary.csv"), 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=summary.keys())
            writer.writeheader()
            writer.writerow(summary)
            
        bus_logger.info("Retail Analytics generated successfully.")
        return summary
