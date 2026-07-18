import os
import sys
import asyncio

# Setup path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.job_manager import create_job, start_job, _run_pipeline
from backend.core.logger import proc_logger

async def main():
    video_path = r"d:\customer-analysis\datasets\live\Copy of Hafidz 2 Store-Touching-10.mp4"
    if not os.path.exists(video_path):
        print("Video not found:", video_path)
        return
        
    filename = os.path.basename(video_path)
    job = create_job(filename)
    job.filepath = video_path
    
    print(f"Starting pipeline for {filename}, Session ID: {job.session_id}")
    await _run_pipeline(job.session_id, video_path)
    print("Pipeline finished!")

if __name__ == "__main__":
    asyncio.run(main())
