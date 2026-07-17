import json
import csv
from pathlib import Path

def generate_timeline(events, base_name):
    """
    Sorts all behavioral events chronologically and generates a timeline export.
    """
    # Sort events by start_time
    sorted_events = sorted(events, key=lambda x: x['start_time'])
    
    # Export to JSON
    out_json = Path("outputs/behavior/timeline") / f"{base_name}_timeline.json"
    with open(out_json, 'w') as f:
        json.dump(sorted_events, f, indent=4)
        
    # Export to CSV
    out_csv = Path("outputs/behavior/timeline") / f"{base_name}_timeline.csv"
    if sorted_events:
        keys = sorted_events[0].keys()
        with open(out_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(sorted_events)
            
    return sorted_events
