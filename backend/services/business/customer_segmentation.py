import json
import os
from backend.core.logger import bus_logger

class CustomerSegmentationEngine:
    def __init__(self):
        self.output_dir = "outputs/business"
        
    def classify(self, journey):
        dur = journey.get("journey_duration", 0)
        stops = journey.get("number_of_stops", 0)
        
        if dur < 30 and stops <= 1:
            return "Quick Visitor"
        elif dur > 300 and stops > 3:
            return "Explorer"
        elif dur > 600:
            return "Long Stay Customer"
        elif stops == 0:
            return "Window Shopper"
        else:
            return "Focused Shopper"
            
    def analyze(self, journeys):
        bus_logger.info("Starting Customer Segmentation analysis.")
        segments = {
            "Quick Visitor": 0,
            "Explorer": 0,
            "Focused Shopper": 0,
            "Returning Visitor": 0,
            "Long Stay Customer": 0,
            "Window Shopper": 0
        }
        
        for j in journeys:
            label = self.classify(j)
            segments[label] += 1
            j["segment"] = label # attach to journey
            
        with open(os.path.join(self.output_dir, "customer_segments.json"), 'w') as f:
            json.dump(segments, f, indent=4)
            
        bus_logger.info("Customer Segmentation completed.")
        return segments
