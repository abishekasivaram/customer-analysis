import numpy as np

class EventDetector:
    def __init__(self, fps=15):
        self.fps = fps
        self.window_size = fps * 2 # 2 seconds window
        
    def group_by_track(self, detections):
        """Groups flat detections into a dictionary by customer_id."""
        tracks = {}
        for d in detections:
            cid = d.get('customer_id')
            if cid is None:
                continue
            if cid not in tracks:
                tracks[cid] = []
            tracks[cid].append(d)
            
        # Sort by frame
        for cid in tracks:
            tracks[cid] = sorted(tracks[cid], key=lambda x: x['frame'])
            
        return tracks

    def extract_kinematics(self, track_frames):
        """Calculates centroid velocity, aspect ratio, and area for a track."""
        kinematics = []
        for i, f in enumerate(track_frames):
            x1, y1, x2, y2 = f['bbox']
            width = x2 - x1
            height = y2 - y1
            area = width * height
            aspect_ratio = width / height if height > 0 else 0
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            
            vx, vy = 0, 0
            if i > 0:
                prev_x1, prev_y1, prev_x2, prev_y2 = track_frames[i-1]['bbox']
                prev_cx = (prev_x1 + prev_x2) / 2
                prev_cy = (prev_y1 + prev_y2) / 2
                vx = cx - prev_cx
                vy = cy - prev_cy
                
            velocity = np.sqrt(vx**2 + vy**2)
            
            kinematics.append({
                'frame': f['frame'],
                'bbox': f['bbox'],
                'confidence': f['confidence'],
                'width': width,
                'height': height,
                'area': area,
                'aspect_ratio': aspect_ratio,
                'velocity': velocity,
                'cx': cx,
                'cy': cy
            })
        return kinematics
