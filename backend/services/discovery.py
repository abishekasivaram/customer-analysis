import os
from backend.core.config import DATASETS_DIR
from backend.core.logger import proc_logger

SUPPORTED_FORMATS = ('.mp4', '.avi', '.mov', '.mkv')

def discover_videos():
    videos = []
    proc_logger.info(f"Scanning directory: {DATASETS_DIR}")
    if not os.path.exists(DATASETS_DIR):
        return videos
        
    for root, _, files in os.walk(DATASETS_DIR):
        for file in files:
            if file.lower().endswith(SUPPORTED_FORMATS):
                category = os.path.basename(root)
                if category == "datasets":
                    category = "uncategorized"
                filepath = os.path.join(root, file)
                videos.append({
                    "filename": file,
                    "filepath": filepath,
                    "category": category
                })
    proc_logger.info(f"Discovered {len(videos)} videos.")
    return videos
