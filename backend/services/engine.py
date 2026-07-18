import cv2
import os
from ultralytics import YOLO
from backend.core.config import MODEL_PATH, CONFIDENCE_THRESHOLD, OUTPUTS_DIR
from backend.core.logger import proc_logger, err_logger, perf_logger
from backend.services.exporter import export_detections, export_tracks

def initialize_model():
    if not os.path.exists(MODEL_PATH):
        proc_logger.info("Downloading YOLOv8n model...")
        model = YOLO('yolov8n.pt')
        model.save(str(MODEL_PATH))
    else:
        model = YOLO(str(MODEL_PATH))
    return model

def process_video(video_info, model):
    filepath = video_info['filepath']
    filename = video_info['filename']
    base_name = os.path.splitext(filename)[0]
    
    cap = cv2.VideoCapture(filepath)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0: fps = 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    out_path = OUTPUTS_DIR / "detection" / "videos" / f"{base_name}_annotated.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(out_path), fourcc, fps, (width, height))
    
    detections = []
    tracks_data = []
    frame_idx = 0
    
    # Track person class (0) with lower resolution for speed
    results = model.track(source=filepath, conf=CONFIDENCE_THRESHOLD, classes=[0], tracker="botsort.yaml", stream=True, verbose=False, imgsz=320)
    
    for r in results:
        frame_idx += 1
            
        im0 = r.plot()
        out.write(im0)
        
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                track_id = int(box.id[0]) if box.id is not None else None
                
                det = {
                    "frame": frame_idx,
                    "customer_id": track_id,
                    "bbox": [round(x1,2), round(y1,2), round(x2,2), round(y2,2)],
                    "confidence": round(conf, 4),
                    "class": "person"
                }
                detections.append(det)
                
                if track_id is not None:
                    trk = {
                        "track_id": track_id,
                        "frame": frame_idx,
                        "bbox": [round(x1,2), round(y1,2), round(x2,2), round(y2,2)],
                        "confidence": round(conf, 4)
                    }
                    tracks_data.append(trk)
                    
    cap.release()
    out.release()
    
    # Convert OpenCV output to Web-playable H264
    proc_logger.info(f"Converting annotated video to H.264 format for web playback...")
    import subprocess
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    temp_path = str(out_path).replace(".mp4", "_temp.mp4")
    os.rename(str(out_path), temp_path)
    
    ffmpeg_cmd = [
        ffmpeg_exe, "-y", "-i", temp_path,
        "-c:v", "libx264", "-preset", "fast", "-crf", "28",
        str(out_path)
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(temp_path)
    
    export_detections(filename, detections)
    export_tracks(filename, tracks_data)
    
    import json
    metadata_path = OUTPUTS_DIR / "detection" / "json" / f"{base_name}_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump({"fps": fps}, f)
    
    proc_logger.info(f"Finished processing {filename}. Extracted {len(detections)} detections.")
