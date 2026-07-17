from backend.core.logger import adv_logger

class ConfidenceEngine:
    def __init__(self):
        pass

    def compute_confidence(self, supporting_metrics_count, historical_agreement, rule_base_confidence=80.0):
        # Base confidence from the rule itself
        confidence = rule_base_confidence
        
        # Increase confidence by 5% for each supporting metric (up to 15%)
        metric_bonus = min(supporting_metrics_count * 5.0, 15.0)
        confidence += metric_bonus
        
        # Adjust based on historical trend agreement
        if historical_agreement == "strong":
            confidence += 5.0
        elif historical_agreement == "weak":
            confidence -= 10.0
        elif historical_agreement == "contradictory":
            confidence -= 25.0
            
        # Bound between 0 and 100
        return max(0.0, min(100.0, confidence))
