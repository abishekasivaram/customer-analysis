import glob
import json
import os
import csv
from backend.core.logger import bus_logger

class DwellTimeAnalyzer:
    def __init__(self):
        self.output_dir = "outputs/business"
        
    def analyze(self):
        bus_logger.info("Starting Dwell Time analysis.")
        timeline_files = glob.glob("outputs/behavior/timeline/*_timeline.json")
        
        dwells = []
        behavior_dwells = {}
        
        for tf in timeline_files:
            with open(tf, 'r') as f:
                events = json.load(f)
                
            for ev in events:
                duration = ev['end_time'] - ev['start_time']
                dwells.append(duration)
                
                b = ev['behavior']
                if b not in behavior_dwells:
                    behavior_dwells[b] = []
                behavior_dwells[b].append(duration)
                
        # Aggregate stats
        avg_dwell = sum(dwells) / len(dwells) if dwells else 0
        max_dwell = max(dwells) if dwells else 0
        min_dwell = min(dwells) if dwells else 0
        
        beh_dwell_stats = {}
        for b, d_list in behavior_dwells.items():
            beh_dwell_stats[b] = sum(d_list) / len(d_list)
            
        dwell_data = {
            "average_dwell_time": avg_dwell,
            "maximum_dwell_time": max_dwell,
            "minimum_dwell_time": min_dwell,
            "zone_dwell_time": {}, # Derived from zone metrics in dashboard gen
            "behavior_dwell_time": beh_dwell_stats
        }
        
        with open(os.path.join(self.output_dir, "dwell_report.json"), 'w') as f:
            json.dump(dwell_data, f, indent=4)
            
        bus_logger.info("Dwell Time analysis completed.")
        return dwell_data
