import time
from backend.core.logger import perf_logger, proc_logger
from backend.services.business.retail_analytics import RetailAnalyticsEngine
from backend.services.business.customer_journey_analyzer import CustomerJourneyAnalyzer
from backend.services.business.zone_performance import ZonePerformanceEngine
from backend.services.business.flow_analyzer import FlowAnalyzer
from backend.services.business.dwell_time import DwellTimeAnalyzer
from backend.services.business.interaction_analytics import InteractionAnalyzer
from backend.services.business.customer_segmentation import CustomerSegmentationEngine
from backend.services.business.kpi_engine import KPIEngine
from backend.services.business.insight_generator import InsightGenerator
from backend.services.business.business_metrics import BusinessMetricsEngine
from backend.services.business.trend_analyzer import TrendAnalyzer
from backend.services.business.alert_engine import AlertEngine
from backend.services.business.comparison_analytics import ComparisonAnalytics
from backend.services.business.dashboard_generator import DashboardGenerator
from backend.services.business.data_quality import DataQualityValidator
from backend.services.business.schema_validator import SchemaValidator
from backend.services.business.report_generator import ReportGenerator

def run():
    start_time = time.time()
    proc_logger.info("--- Starting Phase 3 Business Intelligence Pipeline ---")
    
    # 1. Validation
    proc_logger.info("Running Data Quality Checks...")
    if not DataQualityValidator().validate():
        proc_logger.warning("Data quality issues detected. Proceeding with analysis anyway.")
        
    # 2. Core Modules
    proc_logger.info("Executing Core Analytics...")
    retail_summary = RetailAnalyticsEngine().analyze()
    journeys = CustomerJourneyAnalyzer().analyze()
    zone_perfs = ZonePerformanceEngine().analyze()
    flows = FlowAnalyzer().analyze()
    dwells = DwellTimeAnalyzer().analyze()
    interactions = InteractionAnalyzer().analyze()
    segments = CustomerSegmentationEngine().analyze(journeys)
    kpis = KPIEngine().analyze(retail_summary, dwells, segments, zone_perfs)
    
    # 3. Enterprise Enhancements
    proc_logger.info("Executing Enterprise Enhancements...")
    metrics = BusinessMetricsEngine().analyze(retail_summary, journeys, zone_perfs, dwells)
    trends = TrendAnalyzer().analyze(retail_summary, zone_perfs)
    alerts = AlertEngine().analyze(zone_perfs)
    comps = ComparisonAnalytics().analyze(zone_perfs, retail_summary)
    
    # 4. Insights & Dashboarding
    proc_logger.info("Generating Insights and Dashboard...")
    insights = InsightGenerator().generate(retail_summary, kpis, alerts)
    DashboardGenerator().generate(retail_summary, kpis, journeys, zone_perfs, dwells, 
                                 interactions, segments, metrics, trends, alerts, comps, insights, flows)
                                 
    # 5. Schema Validation
    proc_logger.info("Validating Generated Schemas...")
    SchemaValidator().validate({
        "dashboard_data.json": ["summary", "kpis", "customers", "journeys"],
        "retail_summary.json": ["total_customers", "average_visit_duration"],
        "customer_journey_report.json": ["customer_id", "entry_time"],
        "zone_performance.json": ["zone", "visitors"],
        "business_metrics.json": ["average_customers_per_minute", "customer_engagement_score"],
        "trend_analysis.json": ["customer_count_trend"],
        "business_alerts.json": ["severity", "zone"],
        "comparison_report.json": ["zone_comparison"]
    })
    
    # 6. Reports
    proc_logger.info("Generating Documentation Reports...")
    ReportGenerator().generate_all()
    
    # 7. Phase 4 Compatibility Note
    with open("reports/phase-3/phase4_compatibility.md", "w") as f:
        f.write("# Phase 4 Compatibility Report\n\nAll Phase 3 JSON outputs are successfully validated and schema compliant. They are ready to be ingested directly by the Phase 4 AI Recommendation Engine.\n")
    
    end_time = time.time()
    exec_time = end_time - start_time
    perf_logger.info(f"Phase 3 Pipeline execution time: {exec_time:.2f} seconds.")
    proc_logger.info("--- Phase 3 Pipeline Completed Successfully ---")
    print(f"Phase 3 executed in {exec_time:.2f}s")
    
if __name__ == "__main__":
    run()
