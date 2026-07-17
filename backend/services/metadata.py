import cv2
import os
import json
import csv
from backend.core.config import OUTPUTS_DIR
from backend.core.logger import proc_logger

def extract_metadata(videos):
    metadata_list = []
    for video in videos:
        filepath = video['filepath']
        cap = cv2.VideoCapture(filepath)
        
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
        file_size = os.path.getsize(filepath)
        
        meta = {
            "Video Name": video['filename'],
            "Category": video['category'],
            "Resolution": f"{width}x{height}",
            "FPS": round(fps, 2),
            "Duration": round(frame_count / fps, 2) if fps else 0,
            "Frame Count": frame_count,
            "Codec": codec,
            "Bitrate": "Unknown",
            "Aspect Ratio": f"{width/height:.2f}" if height else "Unknown",
            "File Size": file_size
        }
        metadata_list.append(meta)
        cap.release()
        
    json_path = OUTPUTS_DIR / "detection" / "reports" / "metadata.json"
    csv_path = OUTPUTS_DIR / "detection" / "reports" / "metadata.csv"
    
    with open(json_path, 'w') as f:
        json.dump(metadata_list, f, indent=4)
        
    if metadata_list:
        keys = metadata_list[0].keys()
        with open(csv_path, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(metadata_list)
            
    proc_logger.info(f"Metadata extracted for {len(videos)} videos.")
