import json
import os
import time
from backend.core.logger import adv_logger, adv_perf_logger
from backend.services.advisor.rule_engine import RuleEngine
from backend.services.advisor.confidence_engine import ConfidenceEngine
from backend.services.advisor.recommendation_generator import RecommendationGenerator
from backend.services.advisor.business_summary import BusinessSummaryEngine
from backend.services.advisor.alert_prioritizer import AlertPrioritizer
from backend.services.advisor.opportunity_detector import OpportunityDetector
from backend.services.advisor.executive_report import ExecutiveReportGenerator

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def run():
    start_time = time.time()
    adv_logger.info("--- Starting Phase 4 Business Advisor Engine ---")
    
    OUTPUTS = "outputs/business/"
    
    dashboard_data = load_json(os.path.join(OUTPUTS, "dashboard_data.json"))
    metrics = load_json(os.path.join(OUTPUTS, "business_metrics.json"))
    trends = load_json(os.path.join(OUTPUTS, "trend_analysis.json"))
    flow_data = load_json(os.path.join(OUTPUTS, "customer_flow.json"))
    alerts = load_json(os.path.join(OUTPUTS, "business_alerts.json"))
    
    rule_engine = RuleEngine()
    conf_engine = ConfidenceEngine()
    
    # 1. Generate Recommendations
    rec_gen = RecommendationGenerator(rule_engine, conf_engine)
    recs = rec_gen.generate(dashboard_data, trends, flow_data)
    
    # 2. Store Health
    bs_engine = BusinessSummaryEngine(rule_engine)
    health = bs_engine.generate_store_health(metrics, trends, dashboard_data)
    
    # 3. Alert Prioritization
    ap = AlertPrioritizer(rule_engine)
    prioritized_alerts = ap.prioritize(alerts)
    
    # 4. Opportunity Detection
    od = OpportunityDetector(rule_engine)
    opportunities = od.detect(dashboard_data, trends)
    
    # 5. Executive Report & JSON dumping
    os.makedirs("outputs/advisor", exist_ok=True)
    with open("outputs/advisor/recommendations.json", "w", encoding="utf-8") as f:
        json.dump(recs, f, indent=4)
        
    with open("outputs/advisor/store_health.json", "w", encoding="utf-8") as f:
        json.dump(health, f, indent=4)
        
    with open("outputs/advisor/prioritized_alerts.json", "w", encoding="utf-8") as f:
        json.dump(prioritized_alerts, f, indent=4)
        
    with open("outputs/advisor/opportunities.json", "w", encoding="utf-8") as f:
        json.dump(opportunities, f, indent=4)
        
    # Recommendation Ranking (Enhancement 6)
    with open("outputs/advisor/recommendation_ranking.json", "w", encoding="utf-8") as f:
        ranking = [{"id": r["recommendation_id"], "title": r["title"], "impact_score": r["impact_score"]} for r in recs]
        json.dump(ranking, f, indent=4)
        
    # Advisor Dashboard
    adv_dash = {
        "store_health": health,
        "top_recommendations": recs[:5],
        "critical_alerts": [a for a in prioritized_alerts if a.get("severity") == "Critical"],
        "opportunities": opportunities,
        "trend_summary": trends
    }
    with open("outputs/advisor/advisor_dashboard.json", "w", encoding="utf-8") as f:
        json.dump(adv_dash, f, indent=4)
        
    er = ExecutiveReportGenerator()
    er.generate(health, recs, prioritized_alerts, opportunities)
    
    from backend.services.advisor.report_generator import AdvisorReportGenerator
    arg = AdvisorReportGenerator()
    arg.generate_all()
    
    end_time = time.time()
    exec_time = end_time - start_time
    adv_perf_logger.info(f"Phase 4 executed in {exec_time:.3f}s")
    print(f"Phase 4 executed successfully in {exec_time:.3f}s")

if __name__ == "__main__":
    run()
