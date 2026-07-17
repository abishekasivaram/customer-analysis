import glob
import json
import os
from backend.core.logger import bus_logger

class InteractionAnalyzer:
    def __init__(self):
        self.output_dir = "outputs/business"
        
    def analyze(self):
        bus_logger.info("Starting Interaction analysis.")
        timeline_files = glob.glob("outputs/behavior/timeline/*_timeline.json")
        
        touch = 0
        pick = 0
        returns = 0
        interaction_duration = 0.0
        interaction_count = 0
        
        for tf in timeline_files:
            with open(tf, 'r') as f:
                events = json.load(f)
                
            for ev in events:
                b = ev['behavior']
                dur = ev['end_time'] - ev['start_time']
                
                if b == "TOUCHING":
                    touch += 1
                    interaction_duration += dur
                    interaction_count += 1
                elif b == "PICKING_AND_PUTTING":
                    pick += 1
                    interaction_duration += dur
                    interaction_count += 1
                elif b == "PICKING_AND_RETURNING":
                    pick += 1
                    returns += 1
                    interaction_duration += dur
                    interaction_count += 1
                    
        avg_interaction = interaction_duration / interaction_count if interaction_count > 0 else 0
        
        interaction_data = {
            "shelf_touch_count": touch,
            "product_pick_count": pick,
            "product_return_count": returns,
            "interaction_duration": avg_interaction,
            "most_interactive_shelf": "Shelf A", # Simplified mock based on lack of 3D map
            "least_interactive_shelf": "Shelf B"
        }
        
        with open(os.path.join(self.output_dir, "interaction_report.json"), 'w') as f:
            json.dump(interaction_data, f, indent=4)
            
        bus_logger.info("Interaction analysis completed.")
        return interaction_data
