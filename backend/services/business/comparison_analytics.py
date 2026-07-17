import json
import os
import csv
from backend.core.logger import bus_logger

class ComparisonAnalytics:
    def __init__(self):
        self.output_dir = "outputs/business"
        
    def analyze(self, zone_perfs, retail_summary):
        bus_logger.info("Starting Comparison Analytics.")
        
        # Sort zones by visitors
        sorted_zones = sorted(zone_perfs, key=lambda x: x['visitors'], reverse=True)
        
        comps = {
            "zone_comparison": {z['zone']: z['visitors'] for z in sorted_zones},
            "behaviour_comparison": retail_summary.get('total_behaviors', 0), # Simplified
            "interaction_comparison": {z['zone']: z.get('interaction_count', 0) for z in sorted_zones},
            "dwell_comparison": {z['zone']: z.get('average_dwell_time', 0) for z in sorted_zones}
        }
        
        with open(os.path.join(self.output_dir, "comparison_report.json"), 'w') as f:
            json.dump(comps, f, indent=4)
            
        with open(os.path.join(self.output_dir, "comparison_report.csv"), 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=comps.keys())
            writer.writeheader()
            # Serialize the dicts
            row = {
                "zone_comparison": json.dumps(comps["zone_comparison"]),
                "behaviour_comparison": comps["behaviour_comparison"],
                "interaction_comparison": json.dumps(comps["interaction_comparison"]),
                "dwell_comparison": json.dumps(comps["dwell_comparison"])
            }
            writer.writerow(row)
            
        bus_logger.info("Comparison Analytics completed.")
        return comps
