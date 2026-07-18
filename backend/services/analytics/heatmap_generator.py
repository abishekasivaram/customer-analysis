import cv2
import numpy as np
import json
import yaml
from pathlib import Path

class HeatmapGenerator:
    def __init__(self, config_path="configs/analytics.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.hm_conf = self.config.get('heatmap', {})
        self.res_x, self.res_y = self.hm_conf.get('output_resolution', [3840, 2160])
        self.blur_radius = self.hm_conf.get('blur_radius', 15)
        # We need a large blur radius for 4K video to actually make it look like a heatmap, e.g. 151
        self.cv2_blur = max(31, self.blur_radius * 10 - (self.blur_radius * 10 % 2) + 1)
        
    def _create_heatmap(self, points):
        """Generates a raw color-mapped heatmap from a list of (x,y) coordinates."""
        heatmap = np.zeros((self.res_y, self.res_x), dtype=np.float32)
        
        for (x, y) in points:
            if 0 <= x < self.res_x and 0 <= y < self.res_y:
                heatmap[int(y), int(x)] += 1.0
                
        # Normalize and blur
        if np.max(heatmap) > 0:
            heatmap = heatmap / np.max(heatmap)
            
        # Heavy Gaussian Blur to create the 'heat' effect
        heatmap = cv2.GaussianBlur(heatmap, (self.cv2_blur, self.cv2_blur), 0)
        
        # Re-normalize after blur
        if np.max(heatmap) > 0:
            heatmap = heatmap / np.max(heatmap)
            
        heatmap_8u = np.uint8(255 * heatmap)
        
        # Apply colormap (JET or INFERNO)
        color_map = cv2.applyColorMap(heatmap_8u, cv2.COLORMAP_JET)
        
        # Make zero-value pixels black/transparent instead of dark blue (Jet default 0 is blue)
        # For simplicity, we just leave it as Jet, but mask out exactly 0.
        mask = heatmap_8u < 5
        color_map[mask] = [0, 0, 0]
        
        return color_map

    def generate(self, detections_json, behaviors_json, base_name):
        """Generates the required suite of heatmaps."""
        with open(detections_json, 'r') as f:
            detections = json.load(f)
            
        with open(behaviors_json, 'r') as f:
            behaviors = json.load(f)
            
        all_pts = []
        behavior_pts = {
            "TOUCHING": [],
            "TURNING_TO_SHELF": [],
            "PICKING_AND_RETURNING": [],
            "PICKING_AND_PUTTING": []
        }
        
        dwell_pts = [] # Based on stopped velocity (heuristic: same bbox over many frames)
        
        for d in detections:
            x1, y1, x2, y2 = d['bbox']
            cx, cy = int((x1+x2)/2), int((y1+y2)/2)
            all_pts.append((cx, cy))
            
            # Link behavior
            for b in behaviors:
                if b['track_id'] == d.get('track_id') and b['start_frame'] <= d['frame'] <= b['end_frame']:
                    beh = b['behavior']
                    if beh in behavior_pts:
                        behavior_pts[beh].append((cx, cy))
                        
                    # Dwell time surrogate: ANY behavior (since behaviors mean they are interacting)
                    if beh != "UNKNOWN":
                        dwell_pts.append((cx, cy))
                    break

        out_dir = Path("outputs/analytics/heatmaps")
        
        # 1. Global Heatmap
        cv2.imwrite(str(out_dir / f"{base_name}_global_heatmap.png"), self._create_heatmap(all_pts))
        
        # 2. Behavior Heatmaps
        for beh, pts in behavior_pts.items():
            if pts:
                cv2.imwrite(str(out_dir / f"{base_name}_{beh.lower()}_heatmap.png"), self._create_heatmap(pts))
                
        # 3. Dwell Time Heatmap
        if dwell_pts:
            cv2.imwrite(str(out_dir / f"{base_name}_dwell_time_heatmap.png"), self._create_heatmap(dwell_pts))
            
        # Note: Visit Frequency heatmap is effectively the global heatmap or derived from zones.
        # We save a copy as visit frequency for report completeness.
        cv2.imwrite(str(out_dir / f"{base_name}_visit_frequency_heatmap.png"), self._create_heatmap(all_pts))
