from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="RetailVision AI API", description="Phase 1 API for Video Processing")

queue_status: Dict[str, str] = {}

class ProcessRequest(BaseModel):
    video_id: str

@app.post("/process")
def process_video_endpoint(req: ProcessRequest, background_tasks: BackgroundTasks):
    queue_status[req.video_id] = "Pending"
    return {"message": "Added to queue", "video_id": req.video_id}

@app.get("/status/{video_id}")
def get_status(video_id: str):
    if video_id not in queue_status:
        raise HTTPException(status_code=404, detail="Not found")
    return {"video_id": video_id, "status": queue_status[video_id]}

@app.get("/results/{video_id}")
def get_results(video_id: str):
    return {"video_id": video_id, "results_url": f"/outputs/detection/json/{video_id}.json"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.post("/upload")
def upload_video():
    return {"message": "Upload simulated successfully", "video_id": "vid_123"}

@app.get("/jobs")
def get_all_jobs():
    return {"jobs": queue_status}

@app.get("/jobs/{video_id}")
def get_job(video_id: str):
    if video_id not in queue_status:
        raise HTTPException(status_code=404, detail="Not found")
    return {"video_id": video_id, "status": queue_status[video_id]}

@app.get("/metrics")
def get_metrics():
    return {"total_processed": len(queue_status), "active_jobs": len([j for j in queue_status.values() if j == "Pending"])}

# --- Phase 2 Endpoints ---

@app.post("/analyze")
def analyze_video(req: ProcessRequest):
    return {"message": "Phase 2 Analysis queued", "video_id": req.video_id}

@app.get("/behaviors")
def get_behaviors():
    return {"behaviors": []}

@app.get("/behavior/{track_id}")
def get_behavior_by_track(track_id: int):
    return {"track_id": track_id, "behavior": "UNKNOWN"}

@app.get("/timeline")
def get_timeline():
    return {"timeline": []}

@app.get("/summary")
def get_behavior_summary():
    return {"total_behaviors": 0}

@app.get("/behavior-video/{video_id}")
def get_behavior_video(video_id: str):
    return {"video_url": f"/outputs/behavior/videos/{video_id}_behavior.mp4"}

@app.get("/heatmaps")
def get_heatmaps():
    return {"heatmaps": ["global", "touching", "turning_to_shelf", "picking_and_returning", "picking_and_putting", "dwell_time", "visit_frequency"]}

@app.get("/heatmap/{heatmap_type}")
def get_heatmap(heatmap_type: str):
    return {"heatmap_url": f"/outputs/analytics/heatmaps/{heatmap_type}_heatmap.png"}

@app.get("/zones")
def get_zones():
    return {"zones": ["Zone A", "Zone B", "Zone C", "Zone D"]}

@app.get("/zone/{zone_id}")
def get_zone(zone_id: str):
    return {"zone_id": zone_id, "customer_count": 0}

@app.get("/analytics/summary")
def get_analytics_summary():
    return {"peak_occupancy": 0, "total_visits": 0}

# --- Phase 3 Endpoints ---
@app.get("/retail/summary")
def get_retail_summary(): return {"status": "Available in outputs/business/retail_summary.json"}
@app.get("/retail/kpis")
def get_retail_kpis(): return {"status": "Available in outputs/business/kpi_dashboard.json"}
@app.get("/retail/flow")
def get_retail_flow(): return {"status": "Available in outputs/business/customer_flow.json"}
@app.get("/retail/zones")
def get_retail_zones(): return {"status": "Available in outputs/business/zone_performance.json"}
@app.get("/retail/customers")
def get_retail_customers(): return {"status": "Available in outputs/business/customer_segments.json"}
@app.get("/retail/journeys")
def get_retail_journeys(): return {"status": "Available in outputs/business/customer_journey_report.json"}
@app.get("/retail/interactions")
def get_retail_interactions(): return {"status": "Available in outputs/business/interaction_report.json"}
@app.get("/retail/insights")
def get_retail_insights(): return {"status": "Available in outputs/business/business_insights.json"}
@app.get("/retail/metrics")
def get_retail_metrics(): return {"status": "Available in outputs/business/business_metrics.json"}
@app.get("/retail/trends")
def get_retail_trends(): return {"status": "Available in outputs/business/trend_analysis.json"}
@app.get("/retail/alerts")
def get_retail_alerts(): return {"status": "Available in outputs/business/business_alerts.json"}
@app.get("/retail/dashboard")
def get_retail_dashboard(): return {"status": "Available in outputs/business/dashboard_cards.json"}
@app.get("/retail/export/json")
def get_retail_export_json(): return {"download_url": "/outputs/business/dashboard_data.json"}
@app.get("/retail/export/csv")
def get_retail_export_csv(): return {"download_url": "/outputs/business/retail_summary.csv"}
@app.get("/dashboard/data")
def get_dashboard_data(): return {"status": "Available in outputs/business/dashboard_data.json"}

# --- Phase 4 Endpoints ---
@app.get("/advisor/recommendations")
def get_advisor_recommendations(): return {"status": "Available in outputs/advisor/recommendations.json"}

@app.get("/advisor/summary")
def get_advisor_summary(): return {"status": "Available in outputs/advisor/advisor_dashboard.json"}

@app.get("/advisor/store-health")
def get_advisor_store_health(): return {"status": "Available in outputs/advisor/store_health.json"}

@app.get("/advisor/alerts")
def get_advisor_alerts(): return {"status": "Available in outputs/advisor/prioritized_alerts.json"}

@app.get("/advisor/opportunities")
def get_advisor_opportunities(): return {"status": "Available in outputs/advisor/opportunities.json"}

@app.get("/advisor/executive-report")
def get_advisor_executive_report(): return {"status": "Available in outputs/advisor/executive_summary.json"}

@app.get("/advisor/business-score")
def get_advisor_business_score(): return {"status": "Available in outputs/advisor/business_score.json"}
