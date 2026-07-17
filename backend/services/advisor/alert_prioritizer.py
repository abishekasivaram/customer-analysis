class AlertPrioritizer:
    def __init__(self, rule_engine):
        self.rules = rule_engine

    def prioritize(self, alerts):
        prioritized = []
        for alert in alerts:
            # Alerts from phase 3 have severity: High, Medium, Low
            sev = alert.get("severity", "Medium")
            # Upgrade severity based on zone or rules if needed
            if "Checkout" in alert.get("zone", "") and sev == "High":
                alert["severity"] = "Critical"
                
            prioritized.append(alert)
            
        priority_map = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
        return sorted(prioritized, key=lambda x: priority_map.get(x.get("severity"), 0), reverse=True)
