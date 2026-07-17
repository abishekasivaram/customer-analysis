import numpy as np

class BehaviorClassifier:
    def __init__(self, fps=15):
        self.fps = fps
        self.vel_threshold = 5.0 # Pixels per frame to be considered "stopped"
        
    def classify_track(self, kinematics):
        """
        Takes a list of kinematic frame dictionaries for a single customer.
        Returns a list of behavior events.
        """
        events = []
        if not kinematics:
            return events
            
        current_event = None
        
        # We will use a sliding window approach for heuristics.
        # But for simplicity in this baseline, we can define states based on velocity and aspect ratio.
        for i, k in enumerate(kinematics):
            behavior = "UNKNOWN"
            
            # Simple Heuristics:
            # 1. If velocity is high, they are walking/moving. (UNKNOWN / MOVING)
            # 2. If velocity is low, they are stopped.
            # 3. If stopped and aspect ratio drops significantly -> TURNING_TO_SHELF
            # 4. If stopped and area expands -> reaching out -> TOUCHING or PICKING
            
            # Look at a short history
            history_len = min(i, self.fps)
            if history_len > 0:
                recent_vels = [x['velocity'] for x in kinematics[i-history_len:i+1]]
                avg_vel = np.mean(recent_vels)
                
                recent_ars = [x['aspect_ratio'] for x in kinematics[i-history_len:i+1]]
                ar_variance = np.var(recent_ars)
                
                recent_areas = [x['area'] for x in kinematics[i-history_len:i+1]]
                area_variance = np.var(recent_areas)
                
                if avg_vel < self.vel_threshold:
                    # Stopped near shelf
                    if ar_variance > 0.05:
                        behavior = "TURNING_TO_SHELF"
                    elif area_variance > 50000:
                        # Massive arm reach
                        if np.mean(recent_areas) > np.mean([x['area'] for x in kinematics[max(0, i-self.fps*3):i+1]]):
                            behavior = "PICKING_AND_PUTTING" # Assuming area expansion
                        else:
                            behavior = "PICKING_AND_RETURNING" # Fluctuation
                    else:
                        behavior = "TOUCHING"
                else:
                    behavior = "UNKNOWN"
            
            # Event state machine
            if current_event is None:
                current_event = {
                    'behavior': behavior,
                    'start_frame': k['frame'],
                    'end_frame': k['frame'],
                    'frames': [k]
                }
            elif current_event['behavior'] == behavior:
                current_event['end_frame'] = k['frame']
                current_event['frames'].append(k)
            else:
                # Minimum duration filter to prevent micro-jitter events (e.g. 0.5s = 7 frames)
                if len(current_event['frames']) > (self.fps * 0.5) and current_event['behavior'] != "UNKNOWN":
                    events.append(current_event)
                
                current_event = {
                    'behavior': behavior,
                    'start_frame': k['frame'],
                    'end_frame': k['frame'],
                    'frames': [k]
                }
                
        # Append last event
        if current_event and len(current_event['frames']) > (self.fps * 0.5) and current_event['behavior'] != "UNKNOWN":
            events.append(current_event)
            
        return events
