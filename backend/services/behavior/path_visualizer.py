import cv2
import yaml
import numpy as np
from pathlib import Path

class PathVisualizer:
    def __init__(self, config_path="configs/analytics.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        self.trail_length = self.config.get('visualizer', {}).get('trail_length', 30)
        self.history = {} # track_id -> list of (cx, cy)
        
        # Consistent color map per track_id for visual clarity
        np.random.seed(42) # Not strictly necessary, but good for consistent UI
        
    def _get_color(self, track_id):
        # Generate pseudo-random distinct colors per ID
        r = (track_id * 50) % 255
        g = (track_id * 80) % 255
        b = (track_id * 110) % 255
        return (int(b), int(g), int(r))
        
    def update_and_draw(self, frame, track_id, cx, cy):
        """
        Updates the coordinate history for the track_id and draws the trailing path on the frame.
        """
        if track_id not in self.history:
            self.history[track_id] = []
            
        self.history[track_id].append((int(cx), int(cy)))
        
        # Keep only trailing elements
        if len(self.history[track_id]) > self.trail_length:
            self.history[track_id].pop(0)
            
        color = self._get_color(track_id)
        
        # Draw lines with fading thickness/alpha
        pts = self.history[track_id]
        for i in range(1, len(pts)):
            thickness = max(1, int(5 * (i / len(pts))))
            cv2.line(frame, pts[i-1], pts[i], color, thickness)
            
        return frame
        
    def clean_stale_tracks(self, active_track_ids):
        """Removes trails for tracks that are no longer active to prevent ghosting."""
        stale_ids = [tid for tid in self.history if tid not in active_track_ids]
        for tid in stale_ids:
            del self.history[tid]
