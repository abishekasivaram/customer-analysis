import os
import sys
import traceback
from pathlib import Path

# Add backend to path so imports work correctly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.services.discovery import discover_videos
from backend.services.validation import validate_video
from backend.services.metadata import extract_metadata
from backend.services.engine import initialize_model, process_video
from backend.core.logger import proc_logger, err_logger

def run():
    videos = discover_videos()
    valid_videos = []
    for v in videos:
        is_valid, _ = validate_video(v)
        if is_valid:
            valid_videos.append(v)
            
    if not valid_videos:
        proc_logger.warning("No valid videos to process.")
        return
        
    extract_metadata(valid_videos)
    
    try:
        model = initialize_model()
    except Exception as e:
        err_logger.error(f"Failed to load model: {e}")
        return
        
    completed = 0
    failed = 0
    
    for i, video in enumerate(valid_videos):
        proc_logger.info(f"Processing {i+1}/{len(valid_videos)}: {video['filename']}")
        try:
            process_video(video, model)
            completed += 1
        except Exception as e:
            err_logger.error(f"Failed to process {video['filename']}: {e}")
            err_logger.error(traceback.format_exc())
            failed += 1
            
    proc_logger.info(f"Pipeline finished. Completed: {completed}, Failed: {failed}")

if __name__ == "__main__":
    run()
