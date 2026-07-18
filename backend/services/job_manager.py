import asyncio
import time
import uuid
from typing import Dict, Any, List
from pydantic import BaseModel

class JobStatus(BaseModel):
    session_id: str
    video_name: str
    upload_time: float
    started_time: float = 0
    completed_time: float = 0
    duration: float = 0
    current_stage: str = "Validation"
    progress: float = 0.0
    status: str = "Queued"
    stages: List[str] = [
        "Validation",
        "Frame Extraction",
        "YOLO Detection",
        "ByteTrack Tracking",
        "Behavior Recognition",
        "Business Analytics",
        "Recommendation Engine",
        "Report Generation",
        "Completed"
    ]

# In-memory store for demo
_jobs: Dict[str, JobStatus] = {}

def create_job(video_name: str) -> JobStatus:
    session_id = str(uuid.uuid4())
    job = JobStatus(session_id=session_id, video_name=video_name, upload_time=time.time())
    _jobs[session_id] = job
    return job

def get_job(session_id: str) -> JobStatus:
    return _jobs.get(session_id)

def get_all_jobs() -> List[JobStatus]:
    return list(_jobs.values())

async def _simulate_pipeline(session_id: str):
    job = _jobs[session_id]
    job.status = "Running"
    job.started_time = time.time()
    
    # Realistically, this would call actual pipeline functions.
    # For HackZen, we simulate the progress of the pipeline to keep the demo reliable and fast.
    
    total_stages = len(job.stages) - 1 # Last is 'Completed'
    
    for i in range(total_stages):
        if job.status == "Cancelled":
            return
        
        job.current_stage = job.stages[i]
        
        # Simulate processing time for each stage
        # We make it fast enough for a demo, but slow enough to see the UI update
        duration = 2.0 if job.stages[i] != "Report Generation" else 1.0
        
        steps = 10
        for step in range(steps):
            if job.status == "Cancelled":
                return
            await asyncio.sleep(duration / steps)
            job.progress = ((i * steps) + step + 1) / (total_stages * steps) * 100.0
            
    job.current_stage = "Completed"
    job.progress = 100.0
    job.status = "Completed"
    job.completed_time = time.time()
    job.duration = job.completed_time - job.started_time

def start_job(session_id: str):
    # Kick off the async task
    asyncio.create_task(_simulate_pipeline(session_id))

def cancel_job(session_id: str):
    if session_id in _jobs:
        _jobs[session_id].status = "Cancelled"
        
def resume_job(session_id: str):
    if session_id in _jobs and _jobs[session_id].status == "Cancelled":
        _jobs[session_id].status = "Queued"
        start_job(session_id)

def delete_job(session_id: str):
    if session_id in _jobs:
        del _jobs[session_id]
