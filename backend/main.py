import os
import sys
# Add project root to path so 'backend' imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

from services.job_manager import create_job, get_job, get_all_jobs, start_job, cancel_job, resume_job, delete_job
from services.ai_assistant import ask_retail_ai, search_enterprise

app = FastAPI(title="RetailVision AI API", description="Phase 6 API for Enterprise Platform")

import os
if not os.path.exists("outputs"):
    os.makedirs("outputs")

from fastapi.staticfiles import StaticFiles
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_ai_endpoint(req: AskRequest):
    return {"response": ask_retail_ai(req.query)}

@app.get("/search")
def search_endpoint(q: str = ""):
    return {"results": search_enterprise(q)}




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

from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Response, UploadFile, File
import shutil
import subprocess

@app.post("/upload")
def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # Save the original file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    live_dir = os.path.join(base_dir, "datasets", "live")
    os.makedirs(live_dir, exist_ok=True)
    
    orig_path = os.path.join(live_dir, f"orig_{file.filename}")
    with open(orig_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    # Process with FFmpeg to scale and encode (as requested by user)
    processed_path = os.path.join(live_dir, file.filename)
    # Using libx264, scaling to 640px width (maintains aspect ratio) for fast YOLO processing
    ffmpeg_cmd = [
        ffmpeg_exe, "-y", "-i", orig_path,
        "-vf", "scale=640:-1:flags=lanczos",
        "-c:v", "libx264", "-preset", "fast", "-crf", "28",
        processed_path
    ]
    
    # Run FFmpeg synchronously before queueing
    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Create the job with the processed filename
    job = create_job(file.filename)
    background_tasks.add_task(start_job, job.session_id, processed_path)
    return {"message": "Upload simulated successfully", "session_id": job.session_id}

@app.get("/jobs")
def get_all_jobs_endpoint():
    return {"jobs": get_all_jobs()}

@app.get("/jobs/{session_id}")
def get_job_endpoint(session_id: str):
    job = get_job(session_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.model_dump()

@app.post("/jobs/{session_id}/cancel")
def cancel_job_endpoint(session_id: str):
    cancel_job(session_id)
    return {"message": "Cancelled"}

@app.post("/jobs/{session_id}/resume")
def resume_job_endpoint(session_id: str):
    resume_job(session_id)
    return {"message": "Resumed"}

@app.delete("/jobs/{session_id}")
def delete_job_endpoint(session_id: str):
    delete_job(session_id)
    return {"message": "Deleted"}

def get_file_response(path: str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(path, media_type="video/mp4", headers={"Accept-Ranges": "bytes"})

@app.get("/videos/{video_id}/original")
def get_original_video(video_id: str):
    job = get_job(video_id)
    if not job or not job.filepath or not os.path.exists(job.filepath):
        raise HTTPException(status_code=404, detail="Video not found")
    return get_file_response(job.filepath)

@app.get("/videos/{video_id}/annotated")
def get_annotated_video(video_id: str):
    job = get_job(video_id)
    if not job or not job.filepath:
        raise HTTPException(status_code=404, detail="Annotated video not found")
    
    base_name = os.path.splitext(os.path.basename(job.filepath))[0]
    annotated_path = os.path.join("outputs", "detection", "videos", f"{base_name}_annotated.mp4")
    
    if os.path.exists(annotated_path):
        return get_file_response(annotated_path)
    
    # Fallback to original if annotated is not yet ready
    return get_file_response(job.filepath)

@app.get("/system/health")
def get_system_health():
    import psutil
    return {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "backend": "Operational",
        "api": "Operational",
        "database": "Operational",
        "ai_engine": "Operational",
        "queue_length": len(get_all_jobs())
    }



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

@app.get("/timeline/{session_id}")
def get_session_timeline(session_id: str):
    job = get_job(session_id)
    if not job or not job.filepath:
        return {"events": []}
    base_name = os.path.splitext(os.path.basename(job.filepath))[0]
    timeline_path = os.path.join("outputs", "behavior", "timeline", f"{base_name}_timeline.json")
    data = load_json(timeline_path)
    if isinstance(data, dict) and "error" in data:
        return {"events": []}
        
    events = []
    if isinstance(data, list):
        for item in data:
            start_time = item.get("start_time", 0)
            m = int(start_time // 60)
            s_float = start_time % 60
            events.append({
                "timestamp": f"{m:02d}:{s_float:04.1f}",
                "time_sec": start_time,
                "customer_id": item.get("track_id", 0),
                "event": item.get("behavior", "UNKNOWN").replace("_", " ").title(),
                "zone": "Aisle"
            })
    return {"events": events}

@app.get("/summary/{session_id}")
def get_session_summary(session_id: str):
    job = get_job(session_id)
    if not job or not job.filepath:
        return {}
    base_name = os.path.splitext(os.path.basename(job.filepath))[0]
    behavior_path = os.path.join("outputs", "behavior", "json", f"{base_name}_behavior.json")
    behavior_data = load_json(behavior_path)
    
    if "error" in behavior_data:
        return {}
        
    customers = set()
    interactions = 0
    pickups = 0
    intent = 0
    
    if isinstance(behavior_data, list):
        for event in behavior_data:
            cust_id = event.get("track_id")
            if cust_id is not None:
                customers.add(cust_id)
            interactions += 1
            b_type = event.get("behavior", "")
            if b_type == "PICKING_AND_PUTTING":
                pickups += 1
                intent += 1
            elif b_type == "PICKING_AND_RETURNING":
                pickups += 1
            elif b_type == "TOUCHING":
                interactions += 1
                
    # Fix for Tracker Fragmentation inflating "People Detected"
    tracks_path = os.path.join("outputs", "detection", "json", f"{base_name}_tracks.json")
    tracks_data = load_json(tracks_path)
    people_detected = len(customers)
    if isinstance(tracks_data, list) and len(tracks_data) > 0:
        from collections import defaultdict
        frame_counts = defaultdict(int)
        for t in tracks_data:
            frame_counts[t.get("frame", 0)] += 1
        if frame_counts:
            people_detected = max(frame_counts.values())
                
    return {
        "people": people_detected,
        "interactions": interactions + pickups,
        "pickups": pickups,
        "intent": intent,
        "storeHealth": 85 + min(15, intent * 2), # Simple dynamic proxy for now
        "businessScore": 82 + min(18, intent * 2)
    }

@app.get("/summary")
def get_behavior_summary():
    return {"total_behaviors": 0}

@app.get("/behavior-video/{video_id}")
def get_behavior_video(video_id: str):
    return {"video_url": f"/outputs/behavior/videos/{video_id}_behavior.mp4"}

@app.get("/heatmaps")
def get_heatmaps():
    return {"heatmaps": ["global", "touching", "turning_to_shelf", "picking_and_returning", "picking_and_putting", "dwell_time", "visit_frequency"]}

@app.get("/heatmap-image/{session_id}/{heatmap_type}")
def get_session_heatmap(session_id: str, heatmap_type: str):
    job = get_job(session_id)
    if not job or not job.filepath:
        raise HTTPException(status_code=404, detail="Not found")
    base_name = os.path.splitext(os.path.basename(job.filepath))[0]
    heatmap_path = os.path.join("outputs", "analytics", "heatmaps", f"{base_name}_{heatmap_type}_heatmap.png")
    if os.path.exists(heatmap_path):
        return FileResponse(heatmap_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Heatmap not found")

@app.get("/zones")
def get_zones():
    return {"zones": ["Zone A", "Zone B", "Zone C", "Zone D"]}

@app.get("/zone/{zone_id}")
def get_zone(zone_id: str):
    return {"zone_id": zone_id, "customer_count": 0}

@app.get("/analytics/summary")
def get_analytics_summary():
    return {"peak_occupancy": 0, "total_visits": 0}

import json
import os

def load_json(filepath: str):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {"error": f"File not found: {filepath}"}

# --- Phase 3 Endpoints ---
@app.get("/retail/summary")
def get_retail_summary(): return load_json("outputs/business/retail_summary.json")
@app.get("/retail/kpis")
def get_retail_kpis(): return load_json("outputs/business/kpi_dashboard.json")
@app.get("/retail/flow")
def get_retail_flow(): return load_json("outputs/business/customer_flow.json")
@app.get("/retail/zones")
def get_retail_zones(): return load_json("outputs/business/zone_performance.json")
@app.get("/retail/customers")
def get_retail_customers(): return load_json("outputs/business/customer_segments.json")
@app.get("/retail/journeys")
def get_retail_journeys(): return load_json("outputs/business/customer_journey_report.json")
@app.get("/retail/interactions")
def get_retail_interactions(): return load_json("outputs/business/interaction_report.json")
@app.get("/retail/insights")
def get_retail_insights(): return load_json("outputs/business/business_insights.json")
@app.get("/retail/metrics")
def get_retail_metrics(): return load_json("outputs/business/business_metrics.json")
@app.get("/retail/trends")
def get_retail_trends(): return load_json("outputs/business/trend_analysis.json")
@app.get("/retail/alerts")
def get_retail_alerts(): return load_json("outputs/business/business_alerts.json")
@app.get("/retail/dashboard")
def get_retail_dashboard(): return load_json("outputs/business/dashboard_cards.json")
@app.get("/retail/export/json")
def get_retail_export_json(): return {"download_url": "/outputs/business/dashboard_data.json"}
@app.get("/retail/export/csv")
def get_retail_export_csv(): return {"download_url": "/outputs/business/retail_summary.csv"}
@app.get("/dashboard/data")
def get_dashboard_data(): return load_json("outputs/business/dashboard_data.json")

# --- Phase 4 Endpoints ---
@app.get("/advisor/recommendations")
def get_advisor_recommendations(): return load_json("outputs/advisor/recommendations.json")

@app.get("/advisor/summary")
def get_advisor_summary(): return load_json("outputs/advisor/advisor_dashboard.json")

@app.get("/advisor/store-health")
def get_advisor_store_health(): return load_json("outputs/advisor/store_health.json")

@app.get("/advisor/alerts")
def get_advisor_alerts(): return load_json("outputs/advisor/prioritized_alerts.json")

@app.get("/advisor/opportunities")
def get_advisor_opportunities(): return load_json("outputs/advisor/opportunities.json")

@app.get("/advisor/executive-report")
def get_advisor_executive_report(): return load_json("outputs/advisor/executive_summary.json")

@app.get("/advisor/business-score")
def get_advisor_business_score(): return load_json("outputs/advisor/business_score.json")
