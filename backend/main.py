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
