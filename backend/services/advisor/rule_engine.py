import yaml
import os
from backend.core.logger import rule_logger

class RuleEngine:
    def __init__(self, config_path="configs/advisor_rules.yaml"):
        self.config_path = config_path
        self.rules = self.load_config()

    def load_config(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                rule_logger.info(f"Loaded rules from {self.config_path}")
                return config
        except Exception as e:
            rule_logger.error(f"Failed to load rules config: {e}")
            return {
                "engagement": {"low": 30, "medium": 60, "high": 80},
                "interaction": {"low": 10, "medium": 25, "high": 50},
                "dwell_time": {"low": 2, "medium": 5, "high": 10},
                "congestion": {"warning": 60, "critical": 85},
                "health_score": {"warning": 70, "critical": 50},
                "priorities": {"critical_roi_threshold": 80, "high_roi_threshold": 60, "medium_roi_threshold": 40}
            }

    def get_threshold(self, category, level):
        return self.rules.get(category, {}).get(level, 0)
