import json
import os
from backend.core.logger import bus_logger

class InsightGenerator:
    def __init__(self):
        self.output_dir = "outputs/business"
        
    def generate(self, retail_summary, kpis, alerts):
        bus_logger.info("Starting Insight Generation.")
        insights = []
        
        # Priority mapping: 1 (Critical) to 5 (Info)
        
        # High level KPI insight
        conv = kpis.get("customer_conversion", 0)
        if conv < 0.2:
            insights.append({
                "priority": "HIGH",
                "severity": 2,
                "category": "Conversion",
                "description": f"Customer conversion rate is very low ({conv*100:.1f}%).",
                "recommendation": "Investigate shelf layout and product availability."
            })
        else:
            insights.append({
                "priority": "LOW",
                "severity": 5,
                "category": "Conversion",
                "description": f"Customer conversion rate is healthy ({conv*100:.1f}%).",
                "recommendation": "Maintain current merchandising strategy."
            })
            
        # Zone insights
        pop_zone = kpis.get("most_popular_zone")
        if pop_zone:
            insights.append({
                "priority": "MEDIUM",
                "severity": 4,
                "category": "Traffic",
                "description": f"{pop_zone} receives the highest customer traffic.",
                "recommendation": "Place high-margin products in this zone."
            })
            
        # Alert-driven insights
        for alert in alerts:
            insights.append({
                "priority": alert.get("severity", "HIGH"),
                "severity": 1 if alert.get("severity") == "HIGH" else 3,
                "category": "Operations",
                "description": alert.get("description", ""),
                "recommendation": alert.get("recommendation", "Review area immediately.")
            })
            
        # Sort by severity
        insights = sorted(insights, key=lambda x: x["severity"])
            
        with open(os.path.join(self.output_dir, "business_insights.json"), 'w') as f:
            json.dump(insights, f, indent=4)
            
        with open(os.path.join(self.output_dir, "business_insights.md"), 'w') as f:
            f.write("# Business Insights Report\\n\\n")
            for ins in insights:
                f.write(f"### {ins['priority']} - {ins['category']}\\n")
                f.write(f"**Insight:** {ins['description']}\\n")
                f.write(f"**Recommendation:** {ins['recommendation']}\\n\\n")
            
        bus_logger.info("Insight Generation completed.")
        return insights
