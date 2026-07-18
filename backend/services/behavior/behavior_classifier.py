import numpy as np

class BehaviorClassifier:
    def __init__(self, fps=15):
        self.fps = int(fps)
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
        
        # State machine variables
        state = "UNKNOWN"
        state_duration = 0
        baseline_area = 0

        for i, k in enumerate(kinematics):
            history_len = min(i, self.fps)
            if history_len > 0:
                recent_vels = [x['velocity'] for x in kinematics[i-history_len:i+1]]
                avg_vel = np.mean(recent_vels)
                
                recent_ars = [x['aspect_ratio'] for x in kinematics[i-history_len:i+1]]
                rel_ar_var = np.var(recent_ars) / (np.mean(recent_ars) + 1e-6)
                
                recent_areas = [x['area'] for x in kinematics[i-history_len:i+1]]
                mean_area = np.mean(recent_areas)
                rel_area_var = np.var(recent_areas) / (mean_area + 1e-6)
                
                # State Machine Transitions
                if avg_vel < self.vel_threshold:
                    if state == "UNKNOWN":
                        state = "VIEWING"
                        baseline_area = mean_area
                        state_duration = 0
                        
                    elif state == "VIEWING":
                        # If aspect ratio changes significantly, they are turning towards the shelf
                        if rel_ar_var > 0.02:
                            state = "TURNING_TO_SHELF"
                        # If area starts to fluctuate, they are reaching
                        elif rel_area_var > 0.05:
                            state = "TOUCHING"
                            
                    elif state == "TURNING_TO_SHELF":
                        if rel_area_var > 0.05:
                            state = "TOUCHING"
                            
                    elif state == "TOUCHING":
                        # Dramatic change in area relative to baseline indicates picking
                        if rel_area_var > 0.15:
                            if mean_area > baseline_area * 1.05:
                                state = "PICKING_AND_PUTTING"
                            else:
                                state = "PICKING_AND_RETURNING"
                                
                    elif state in ["PICKING_AND_PUTTING", "PICKING_AND_RETURNING"]:
                        # Once picked, if velocity increases, they leave the shelf
                        if avg_vel >= self.vel_threshold:
                            state = "UNKNOWN"
                            
                    state_duration += 1
                else:
                    # Moving too fast
                    state = "UNKNOWN"
                    state_duration = 0
            
            behavior = state
            
            # Event state machine (same as before to aggregate frames)
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
                if len(current_event['frames']) > (self.fps * 0.5) and current_event['behavior'] not in ["UNKNOWN", "VIEWING"]:
                    events.append(current_event)
                
                current_event = {
                    'behavior': behavior,
                    'start_frame': k['frame'],
                    'end_frame': k['frame'],
                    'frames': [k]
                }
                
        # Append last event
        if current_event and len(current_event['frames']) > (self.fps * 0.5) and current_event['behavior'] not in ["UNKNOWN", "VIEWING"]:
            events.append(current_event)
            
        return events
