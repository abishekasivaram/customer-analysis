from backend.core.logger import val_logger

class RecommendationValidator:
    def __init__(self):
        self.required_fields = [
            "recommendation_id", "category", "priority", "confidence", "title",
            "description", "reasoning", "supporting_metrics", "expected_business_impact",
            "estimated_improvement", "generated_timestamp",
            "triggered_rule", "affected_metrics", "business_objective", "recommended_action",
            "expected_improvement", "estimated_business_impact", "estimated_roi",
            "implementation_difficulty", "risk_level", "validation_status"
        ]

    def validate(self, rec: dict) -> bool:
        for field in self.required_fields:
            if field not in rec:
                val_logger.error(f"Validation failed: Missing field '{field}' in recommendation {rec.get('title', 'Unknown')}")
                return False
                
        # Validate priorities
        valid_priorities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        rec["priority"] = str(rec.get("priority", "")).upper()
        if rec["priority"] not in valid_priorities:
            val_logger.error(f"Validation failed: Invalid priority '{rec.get('priority')}'")
            return False
            
        rec["validation_status"] = "PASS"
        return True
