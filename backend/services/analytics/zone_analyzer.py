import json
import csv
import yaml
from pathlib import Path
import cv2
import numpy as np

class ZoneAnalyzer:
    def __init__(self, fps=15, config_path="configs/analytics.yaml"):
        self.fps = fps
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        self.zones = self.config.get('zones', [])
        
    def _is_in_zone(self, cx, cy, poly_coords):
        # Ray casting or cv2.pointPolygonTest
        pts = np.array(poly_coords, np.int32)
        pts = pts.reshape((-1, 1, 2))
        return cv2.pointPolygonTest(pts, (cx, cy), False) >= 0

    def analyze(self, detections_json, behaviors_json, base_name):
        with open(detections_json, 'r') as f:
            detections = json.load(f)
        with open(behaviors_json, 'r') as f:
            behaviors = json.load(f)
            
        # Structure to hold metrics per zone
        zone_metrics = {z['id']: {
            'name': z['name'],
            'customer_count': 0,
            'total_dwell_frames': 0,
            'visits': 0,
            'peak_occupancy': 0,
            'behaviors_observed': {},
            'visitors': set(),
            'frame_occupancy': {}
        } for z in self.zones}
        
        # Populate
        for d in detections:
            x1, y1, x2, y2 = d['bbox']
            cx, cy = (x1+x2)/2, (y1+y2)/2
            f_num = d['frame']
            cid = d.get('customer_id')
            
            for z in self.zones:
                if self._is_in_zone(cx, cy, z['coords']):
                    zid = z['id']
                    
                    if cid is not None:
                        zone_metrics[zid]['visitors'].add(cid)
                        zone_metrics[zid]['total_dwell_frames'] += 1
                        
                    # Occupancy per frame
                    zone_metrics[zid]['frame_occupancy'][f_num] = zone_metrics[zid]['frame_occupancy'].get(f_num, 0) + 1
                    
        # Extract behaviors in zones
        for b in behaviors:
            tid = b['track_id']
            # Simplification: assume if a track was in a zone, its behavior happened there
            # Real implementation would intersect the behavior frame window with the track's zone presence
            for z in self.zones:
                if tid in zone_metrics[z['id']]['visitors']:
                    beh = b['behavior']
                    if beh not in zone_metrics[z['id']]['behaviors_observed']:
                        zone_metrics[z['id']]['behaviors_observed'][beh] = 0
                    zone_metrics[z['id']]['behaviors_observed'][beh] += 1
                    
        # Finalize stats
        results = []
        for zid, stats in zone_metrics.items():
            visitors = len(stats['visitors'])
            dwell = round((stats['total_dwell_frames'] / self.fps) / max(1, visitors), 2)
            peak = max(stats['frame_occupancy'].values()) if stats['frame_occupancy'] else 0
            
            res = {
                'zone_id': zid,
                'zone_name': stats['name'],
                'customer_count': visitors,
                'average_dwell_time_seconds': dwell,
                'average_visits': visitors,
                'peak_occupancy': peak,
                'behaviors_observed': str(stats['behaviors_observed']),
                'average_confidence': 0.0, # Placeholder, depends on confidence module integration
                'average_time_spent': dwell
            }
            results.append(res)
            
        out_dir = Path("outputs/analytics")
        with open(out_dir / f"{base_name}_zone_analytics.json", 'w') as f:
            json.dump(results, f, indent=4)
            
        if results:
            keys = results[0].keys()
            with open(out_dir / f"{base_name}_zone_analytics.csv", 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(results)
                
        return results
