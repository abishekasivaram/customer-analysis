import glob
import json
import os
import csv
from backend.core.logger import bus_logger

class CustomerJourneyAnalyzer:
    def __init__(self):
        self.output_dir = "outputs/business"
        
    def analyze(self):
        bus_logger.info("Starting Customer Journey analysis.")
        timeline_files = glob.glob("outputs/behavior/timeline/*_timeline.json")
        zone_files = glob.glob("outputs/analytics/*_zone_analytics.json")
        
        journeys = {}
        
        # Load behavior timelines
        for tf in timeline_files:
            base_name = os.path.basename(tf).replace("_timeline.json", "")
            with open(tf, 'r') as f:
                events = json.load(f)
            
            for ev in events:
                cid = f"{base_name}_{ev['track_id']}"
                if cid not in journeys:
                    journeys[cid] = {
                        "customer_id": cid,
                        "entry_time": float('inf'),
                        "exit_time": 0.0,
                        "zones_visited": [], # mock since zone JSON doesn't track per user easily here
                        "behavior_timeline": [],
                        "time_in_each_zone": {},
                        "longest_interaction": "",
                        "exit_behavior": "UNKNOWN"
                    }
                journeys[cid]["entry_time"] = min(journeys[cid]["entry_time"], ev['start_time'])
                journeys[cid]["exit_time"] = max(journeys[cid]["exit_time"], ev['end_time'])
                journeys[cid]["behavior_timeline"].append(ev['behavior'])
                
        # Calculate derived journey stats
        for cid, j in journeys.items():
            j["journey_duration"] = j["exit_time"] - j["entry_time"]
            j["exit_behavior"] = j["behavior_timeline"][-1] if j["behavior_timeline"] else "UNKNOWN"
            # Deduplicate behavior for longest interaction logic mock
            j["number_of_stops"] = len(j["behavior_timeline"])
            j["longest_interaction"] = j["exit_behavior"] # simplify
        
        results = list(journeys.values())
        
        with open(os.path.join(self.output_dir, "customer_journey_report.json"), 'w') as f:
            json.dump(results, f, indent=4)
            
        if results:
            with open(os.path.join(self.output_dir, "customer_journey_report.csv"), 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
                
        bus_logger.info(f"Analyzed {len(results)} customer journeys.")
        return results
