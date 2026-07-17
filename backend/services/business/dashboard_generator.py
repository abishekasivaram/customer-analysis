import json
import os
from backend.core.logger import bus_logger

class DashboardGenerator:
    def __init__(self):
        self.output_dir = "outputs/business"
        
    def generate(self, retail_summary, kpis, journeys, zone_perfs, dwells, 
                 interactions, segments, metrics, trends, alerts, comps, insights, flows):
        bus_logger.info("Generating unified Dashboard JSON.")
        
        dashboard_data = {
            "summary": retail_summary,
            "kpis": metrics,  # Advanced KPIs
            "customers": segments,
            "journeys": journeys[:10], # Top 10 for dashboard preview to avoid massive JSON
            "zones": zone_perfs,
            "heatmaps": {"status": "Available in outputs/analytics/heatmaps"},
            "charts": {"status": "Available in outputs/analytics/charts and outputs/business/graphs"},
            "alerts": alerts,
            "trends": trends,
            "insights": insights,
            "comparisons": comps,
            "flow": flows
        }
        
        with open(os.path.join(self.output_dir, "dashboard_data.json"), 'w') as f:
            json.dump(dashboard_data, f, indent=4)
            
        # Also generate dashboard_cards.json explicitly requested
        cards = {
            "Total Customers": retail_summary.get('total_customers', 0),
            "Active Customers": sum([1 for j in journeys if j.get('exit_time') == 0]), # mockup active
            "Average Dwell Time": dwells.get('average_dwell_time', 0),
            "Peak Zone": kpis.get('most_popular_zone', 'N/A'),
            "Most Common Behaviour": max(segments, key=segments.get) if segments else 'N/A',
            "Customer Engagement Score": metrics.get('customer_engagement_score', 0),
            "Peak Occupancy": max([z['peak_occupancy'] for z in zone_perfs]) if zone_perfs else 0,
            "Store Utilization": f"{kpis.get('store_utilization', 0) * 100}%"
        }
        
        with open(os.path.join(self.output_dir, "dashboard_cards.json"), 'w') as f:
            json.dump(cards, f, indent=4)
            
        bus_logger.info("Dashboard JSON generated successfully.")
        return dashboard_data
