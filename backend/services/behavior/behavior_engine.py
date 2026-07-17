import json
import csv
import os
from pathlib import Path
from backend.services.behavior.event_detector import EventDetector
from backend.services.behavior.behavior_classifier import BehaviorClassifier
from backend.services.behavior.confidence import ConfidenceEngine

def process_video_behavior(video_name, fps=15):
    """
    Reads Phase 1 detection JSON and generates Phase 2 behavior events.
    Returns a list of structured event dictionaries.
    """
    base_name = os.path.splitext(os.path.basename(video_name))[0]
    json_path = Path("outputs/detection/json") / f"{base_name}.json"
    
    if not json_path.exists():
        # Fallback to tracks file if standard json not found
        json_path = Path("outputs/detection/json") / f"{base_name}_tracks.json"
        if not json_path.exists():
            return []
            
    with open(json_path, 'r') as f:
        detections = json.load(f)
        
    detector = EventDetector(fps=fps)
    classifier = BehaviorClassifier(fps=fps)
    conf_engine = ConfidenceEngine(fps=fps)
    
    tracks = detector.group_by_track(detections)
    
    all_events = []
    
    for cid, track_frames in tracks.items():
        kinematics = detector.extract_kinematics(track_frames)
        raw_events = classifier.classify_track(kinematics)
        
        for event in raw_events:
            final_conf = conf_engine.calculate(event)
            start_frame = event['start_frame']
            end_frame = event['end_frame']
            start_time = round(start_frame / fps, 2)
            end_time = round(end_frame / fps, 2)
            
            structured_event = {
                "track_id": cid,
                "behavior": event['behavior'],
                "start_frame": start_frame,
                "end_frame": end_frame,
                "start_time": start_time,
                "end_time": end_time,
                "confidence": final_conf
            }
            all_events.append(structured_event)
            
    # Export to JSON
    out_json = Path("outputs/behavior/json") / f"{base_name}_behavior.json"
    with open(out_json, 'w') as f:
        json.dump(all_events, f, indent=4)
        
    # Export to CSV
    out_csv = Path("outputs/behavior/csv") / f"{base_name}_behavior.csv"
    if all_events:
        keys = all_events[0].keys()
        with open(out_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_events)
            
    return all_events
