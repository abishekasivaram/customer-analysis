# Environment & Dependency Report

## System Information
- **Operating System:** Windows 11
- **CPU Model:** Intel64 Family 6 Model 154 Stepping 4, GenuineIntel
- **Number of CPU Cores:** 6 Physical, 8 Logical
- **RAM Installed:** 7.69 GB
- **GPU Model:** None (Virtualized Environment)
- **CUDA Version:** None
- **Python Version:** 3.14.6

## AI Stack
- **PyTorch Version:** 2.13.0+cpu
- **Ultralytics Version:** 8.4.98
- **OpenCV Version:** 5.0.0
- **NumPy Version:** 2.5.1
- **Pandas Version:** 3.0.3
- **FastAPI Version:** 0.139.2

## Runtime Configuration
- **Device Used:** CPU
- **Detection Model:** YOLOv8n (`yolov8n.pt`)
- **Tracker Configuration:** ByteTrack (`bytetrack.yaml` natively bundled with Ultralytics via `lap`)
- **Confidence Threshold:** 0.50
- **Image Resolution Used:** Native 4K UHD (3840x2160) input, resized natively by YOLOv8 engine internally to 640x640 for inference.
- **Batch Size:** 1 (Frame-by-Frame streaming)
- **Processing Mode:** Asynchronous Offline Batch Processing
