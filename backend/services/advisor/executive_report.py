import json
import os

class ExecutiveReportGenerator:
    def __init__(self, output_dir="outputs/advisor"):
        self.output_dir = output_dir

    def generate(self, health_data, top_recs, alerts, opportunities):
        exec_summary = {
            "overall_store_health": health_data.get("store_health_score"),
            "health_status": health_data.get("status"),
            "top_risks": [a.get("description") for a in alerts[:3]],
            "top_opportunities": [o.get("description") for o in opportunities[:3]],
            "critical_recommendations": [r for r in top_recs if str(r.get("priority")).upper() == "CRITICAL"],
            "priority_actions": [r.get("recommended_action") for r in top_recs[:5]]
        }
        
        # Save JSON
        with open(os.path.join(self.output_dir, "executive_summary.json"), "w", encoding="utf-8") as f:
            json.dump(exec_summary, f, indent=4)
            
        # Save MD
        md_content = f"""# Executive Summary

**Overall Store Health Score**: {exec_summary['overall_store_health']} / 100 ({exec_summary['health_status']})

## Top Risks
"""
        for r in exec_summary["top_risks"]:
            md_content += f"- {r}\n"
            
        md_content += "\n## Top Opportunities\n"
        for o in exec_summary["top_opportunities"]:
            md_content += f"- {o}\n"
            
        md_content += "\n## Priority Actions\n"
        for a in exec_summary["priority_actions"]:
            md_content += f"- {a}\n"
            
        with open(os.path.join(self.output_dir, "executive_summary.md"), "w", encoding="utf-8") as f:
            f.write(md_content)
