import json
import csv
import os
from backend.core.config import OUTPUTS_DIR

def export_detections(video_name, detections):
    base_name = os.path.splitext(video_name)[0]
    json_path = OUTPUTS_DIR / "detection" / "json" / f"{base_name}.json"
    csv_path = OUTPUTS_DIR / "detection" / "csv" / f"{base_name}.csv"
    
    with open(json_path, 'w') as f:
        json.dump(detections, f, indent=4)
        
    if detections:
        keys = detections[0].keys()
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(detections)
            
def export_tracks(video_name, tracks):
    base_name = os.path.splitext(video_name)[0]
    json_path = OUTPUTS_DIR / "detection" / "json" / f"{base_name}_tracks.json"
    csv_path = OUTPUTS_DIR / "detection" / "csv" / f"{base_name}_tracks.csv"
    
    with open(json_path, 'w') as f:
        json.dump(tracks, f, indent=4)
        
    if tracks:
        keys = tracks[0].keys()
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(tracks)
