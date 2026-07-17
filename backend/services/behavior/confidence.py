import numpy as np

class ConfidenceEngine:
    def __init__(self, fps=15):
        self.fps = fps
        
    def calculate(self, event):
        """
        Calculates a dynamic confidence score [0.0, 1.0] for a behavior event.
        Based on:
        - YOLO base confidence (mean over event frames)
        - Duration of the event (too short = lower confidence)
        - Jitter/Variance stability
        """
        frames = event['frames']
        if not frames:
            return 0.0
            
        base_confs = [f['confidence'] for f in frames]
        mean_base = np.mean(base_confs)
        
        duration_frames = len(frames)
        # Assuming typical behaviors last between 1 and 5 seconds
        duration_score = min(1.0, duration_frames / (self.fps * 3))
        
        # Jitter stability
        areas = [f['area'] for f in frames]
        area_variance = np.var(areas)
        stability_score = 1.0
        if area_variance > 100000:
            stability_score = 0.8
            
        final_conf = (mean_base * 0.5) + (duration_score * 0.3) + (stability_score * 0.2)
        return round(float(min(1.0, max(0.0, final_conf))), 4)
