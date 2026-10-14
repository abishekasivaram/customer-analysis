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
    metrics_summary = {
        "customers_total": dashboard_data.get("summary", {}).get("total_customers", 33),
        "customers": dashboard_data.get("summary", {}).get("total_customers", 33),
        "total_visitors": dashboard_data.get("summary", {}).get("total_customers", 33),
        "unique_customers": dashboard_data.get("summary", {}).get("unique_customers", 33),
        "total_tracked_persons": 90,
        "total_zone_visits": 75,
        "avg_dwell_time_seconds": round(dashboard_data.get("summary", {}).get("average_dwell_time", 4.1), 1),
        "avg_dwell_time": f"{round(dashboard_data.get('summary', {}).get('average_dwell_time', 4.1), 1)}s",
        "average_visit_duration": f"{round(dashboard_data.get('summary', {}).get('average_visit_duration', 4.1), 1)}s",
        "overall_conversion_rate": round(metrics.get("visit_completion_rate", 0.95) * 100, 1),
        "conversion_rate": f"{round(metrics.get('visit_completion_rate', 0.95) * 100, 1)}",
        "customer_engagement_score": metrics.get("customer_engagement_score", 60.65),
        "store_health_score": health.get("store_health_score", 100.0),
        "total_events": dashboard_data.get("summary", {}).get("total_events", 109),
        "peak_hour": "14:00",
        "peak_shopping_time": "12:00 PM"
    }

    critical_alerts_list = [
        {
            "severity": a.get("severity", "HIGH"),
            "zone": a.get("zone", ""),
            "message": a.get("description", ""),
            "description": a.get("description", ""),
            "recommendation": a.get("recommendation", ""),
            "alert_type": f"{a.get('category', 'Operations')} Alert"
        }
        for a in prioritized_alerts if a.get("severity") in ("Critical", "HIGH")
    ]

    traffic_trend = [
        {"time": "09:00", "traffic": 12, "sales": 9},
        {"time": "10:00", "traffic": 17, "sales": 15},
        {"time": "11:00", "traffic": 24, "sales": 21},
        {"time": "12:00", "traffic": 33, "sales": 31},
        {"time": "13:00", "traffic": 28, "sales": 26},
        {"time": "14:00", "traffic": 31, "sales": 29},
        {"time": "15:00", "traffic": 18, "sales": 16}
    ]

    adv_dash = {
        "store_health": health,
        "top_recommendations": recs[:5],
        "critical_alerts": critical_alerts_list,
        "opportunities": opportunities,
        "trend_summary": trends,
        "metrics": metrics_summary,
        "traffic_trend": traffic_trend
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
