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
    filepath: str = ""
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

import sys
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

async def _run_pipeline(session_id: str, filepath: str = None):
    job = _jobs[session_id]
    job.status = "Running"
    job.started_time = time.time()
    
    try:
        if filepath:
            filename = os.path.basename(filepath)
            video_info = {"filepath": filepath, "filename": filename}
            
            job.current_stage = "Validation"
            job.progress = 5.0
            
            job.current_stage = "Preprocessing (FFmpeg)"
            import subprocess
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            
            processed_path = os.path.join(os.path.dirname(filepath), filename.replace('orig_', ''))
            ffmpeg_cmd = [
                ffmpeg_exe, "-y", "-i", filepath,
                "-vf", "scale=640:-1:flags=fast_bilinear",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28",
                processed_path
            ]
            await asyncio.to_thread(subprocess.run, ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Update filepath to the processed file for YOLO
            video_info["filepath"] = processed_path
            job.filepath = processed_path
            
            job.current_stage = "YOLO Detection"
            job.progress = 10.0
            from backend.services.engine import initialize_model, process_video
            model = await asyncio.to_thread(initialize_model)
            
            def update_progress(pct: float):
                # Map 0.0-1.0 to 10.0-40.0
                job.progress = 10.0 + (pct * 30.0)
                
            await asyncio.to_thread(process_video, video_info, model, update_progress)
            job.progress = 40.0
            
            job.current_stage = "Behavior Recognition"
            import backend.run_phase2 as phase2
            await asyncio.to_thread(phase2.run_phase2)
            job.progress = 70.0
            
            job.current_stage = "Business Analytics"
            import backend.run_phase3 as phase3
            await asyncio.to_thread(phase3.run)
            job.progress = 85.0
            
            job.current_stage = "Recommendation Engine"
            import backend.run_phase4 as phase4
            await asyncio.to_thread(phase4.run)
            job.progress = 95.0
            
            job.current_stage = "Report Generation"
            await asyncio.sleep(0.5)
            
        job.current_stage = "Completed"
        job.progress = 100.0
        job.status = "Completed"
        job.completed_time = time.time()
        job.duration = job.completed_time - job.started_time
    except Exception as e:
        import traceback
        traceback.print_exc()
        job.status = "Cancelled"
        job.current_stage = f"Failed: {str(e)}"

async def start_job(session_id: str, filepath: str = None):
    if session_id in _jobs and filepath:
        _jobs[session_id].filepath = filepath
    asyncio.create_task(_run_pipeline(session_id, filepath))

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
