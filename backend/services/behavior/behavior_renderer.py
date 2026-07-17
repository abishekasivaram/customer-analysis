import cv2
import json
import yaml
from pathlib import Path
import os
from backend.services.behavior.path_visualizer import PathVisualizer

class BehaviorRenderer:
    def __init__(self, fps=15, config_path="configs/analytics.yaml"):
        self.fps = fps
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.behavior_colors = self.config.get('behavior_colors', {})
        self.path_viz = PathVisualizer(config_path=config_path)
        
    def _get_color(self, behavior):
        # Default white
        return tuple(self.behavior_colors.get(behavior, [255, 255, 255]))
        
    def render(self, video_path, detections_json, behaviors_json, output_path):
        """
        Renders a new video with track IDs, bounding boxes, behavior, confidence, timestamp, duration, and path.
        """
        cap = cv2.VideoCapture(str(video_path))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out_fps = cap.get(cv2.CAP_PROP_FPS) or self.fps
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, out_fps, (width, height))
        
        with open(detections_json, 'r') as f:
            detections = json.load(f)
            
        with open(behaviors_json, 'r') as f:
            behaviors = json.load(f)
            
        # Index detections by frame
        det_by_frame = {}
        for d in detections:
            f_num = d['frame']
            if f_num not in det_by_frame:
                det_by_frame[f_num] = []
            det_by_frame[f_num].append(d)
            
        # Index behaviors by track_id to quickly find current active behavior
        
        frame_idx = 1
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            current_timestamp = frame_idx / out_fps
            active_ids = []
            
            if frame_idx in det_by_frame:
                for d in det_by_frame[frame_idx]:
                    tid = d.get('customer_id')
                    if tid is None: continue
                    active_ids.append(tid)
                    
                    x1, y1, x2, y2 = map(int, d['bbox'])
                    cx, cy = (x1+x2)//2, (y1+y2)//2
                    
                    # Find active behavior
                    current_beh = "UNKNOWN"
                    current_conf = 0.0
                    duration = 0.0
                    
                    for b in behaviors:
                        if b['track_id'] == tid and b['start_frame'] <= frame_idx <= b['end_frame']:
                            current_beh = b['behavior']
                            current_conf = b['confidence']
                            duration = (frame_idx - b['start_frame']) / out_fps
                            break
                            
                    color = self._get_color(current_beh)
                    
                    # Draw path trail
                    frame = self.path_viz.update_and_draw(frame, tid, cx, cy)
                    
                    # Draw BBox
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)
                    
                    # Overlay Dashboard style
                    text_lines = [
                        f"Track ID: {tid}",
                        f"Behavior: {current_beh}",
                        f"Confidence: {int(current_conf*100)}%",
                        f"Duration: {duration:.1f}s",
                        f"Time: {current_timestamp:.1f}s"
                    ]
                    
                    # Draw text panel
                    panel_w, panel_h = 400, 200
                    cv2.rectangle(frame, (x1, y1-panel_h), (x1+panel_w, y1), (0,0,0), -1)
                    # Semi transparency is complex in basic cv2 without addWeighted overhead, so solid black backing
                    
                    for i, txt in enumerate(text_lines):
                        cv2.putText(frame, txt, (x1 + 10, y1 - panel_h + 35 + (i*35)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
                                    
            self.path_viz.clean_stale_tracks(active_ids)
            
            out.write(frame)
            frame_idx += 1
            
        cap.release()
        out.release()
