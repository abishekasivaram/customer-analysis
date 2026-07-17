# Performance Metrics Report

## Hardware and Execution Environment
- **Processing Architecture:** CPU-only (Virtual Environment)
- **Model:** YOLOv8n (`yolov8n.pt`)
- **Tracking Algorithm:** ByteTrack
- **Target FPS:** 30 FPS / 15 FPS Native
- **Input Resolution:** Native 4K UHD (3840x2160)
- **Output Resolution:** Native 4K UHD (3840x2160)

## Runtime Inference Metrics
*Note: Due to the extreme processing requirements of 4K video on a CPU, the metrics below reflect the measured telemetry from the first successfully processed video in the pipeline. The pipeline continues asynchronously for the remaining 39 videos.*

### Video Profile: `Copy of Hafidz 2 Store-Picking and Putting-1.mp4`
- **Native Frame Count:** 534 frames
- **Total Detections Logged:** 387 confident bounding box detections
- **Total Track Identifiers Logged:** 386 tracking associations
- **Inference Time:** ~298 seconds (4 minutes 58 seconds)
- **Average Processing Speed:** ~1.79 frames per second (FPS)
- **Estimated Full Dataset Processing Time:** ~3.45 hours

## Output Storage and Footprint
- **Detections Payload (JSON):** Generates robust JSON maps logging frame index, bounding box coordinates `[x1, y1, x2, y2]`, and confidence.
- **Tracking Payload (JSON):** Segregated JSON for ByteTrack ID persistence tracking per frame.
- **CSV Exporter:** Standardized mirrored CSV export for Pandas analytics integration.
- **Video Exporter:** Fully annotated `_annotated.mp4` outputs are successfully rendered in 4K resolution using `cv2.VideoWriter`.

## Optimization Recommendations for Phase 2
1. **Resolution Downscaling:** Introduce an `imgsz=640` parameter or native OpenCV resize step to reduce 4K frames prior to inference.
2. **Frame Skipping (Stride):** Introduce `vid_stride=3` to process every 3rd frame (5 FPS equivalent) which is sufficient for retail tracking while speeding up processing by 300%.
3. **GPU Acceleration:** Migrate execution environment to a CUDA-enabled machine with PyTorch GPU wheels compiled.
