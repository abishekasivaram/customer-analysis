import cv2
import os
from backend.core.logger import proc_logger, err_logger

def validate_video(video_info):
    filepath = video_info['filepath']
    
    if os.path.getsize(filepath) == 0:
        err_logger.error(f"Validation failed: Empty file {filepath}")
        return False, "Empty file"
        
    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        err_logger.error(f"Validation failed: Corrupted or unsupported file {filepath}")
        return False, "Corrupted or unsupported"
        
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if frame_count <= 0 or fps <= 0:
        err_logger.error(f"Validation failed: Invalid frame count or fps in {filepath}")
        cap.release()
        return False, "Invalid metadata"
        
    cap.release()
    proc_logger.info(f"Validation successful: {video_info['filename']}")
    return True, "Valid"
