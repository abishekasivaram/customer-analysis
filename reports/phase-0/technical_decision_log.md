# Technical Decision Log
## RetailVision AI

This document records the primary technology choices, the rationale behind them, and the alternatives that were considered and rejected.

---

## 1. Object Detection: YOLO (You Only Look Once)
- **Decision:** Use YOLOv8 (or latest stable variant) for person detection.
- **Rationale:** YOLO provides the best balance of inference speed and accuracy. It is highly optimized for real-time processing and has a massive community supporting easy fine-tuning.
- **Alternatives Considered:**
  - *Faster R-CNN:* Rejected. Higher accuracy but significantly slower inference times, making it unsuitable for processing long videos cost-effectively.
  - *SSD (Single Shot MultiBox Detector):* Rejected. YOLO generally outperforms SSD in both speed and small-object detection in recent iterations.

## 2. Object Tracking: ByteTrack
- **Decision:** Use ByteTrack for associating detections across frames.
- **Rationale:** ByteTrack associates almost every detection box instead of only the high score ones, which makes it exceptionally robust to occlusions and low-confidence detections (common in retail environments).
- **Alternatives Considered:**
  - *DeepSORT:* Rejected. DeepSORT relies heavily on an appearance feature extractor (ReID), which is computationally heavy and often unnecessary for simple single-camera aisle tracking where ByteTrack's pure motion-based (Kalman filter) approach is sufficient and faster.

## 3. Backend Framework: FastAPI
- **Decision:** Use FastAPI (Python) for the core REST API.
- **Rationale:** Native asynchronous support, automatic Swagger/OpenAPI documentation generation, and extremely high performance. Since the AI ecosystem is Python-based, using a Python backend simplifies integration and sharing of data structures (Pydantic models).
- **Alternatives Considered:**
  - *Django:* Rejected. Too monolithic and opinionated. The ORM overhead is unnecessary since we are using MongoDB.
  - *Node.js (Express):* Rejected. Would require maintaining a separate microservice architecture just to bridge the JS API with the Python AI workers.

## 4. Frontend Framework: React (with TypeScript)
- **Decision:** Use React for the web dashboard.
- **Rationale:** Industry standard for enterprise SPAs. Massive ecosystem of charting libraries (Recharts) and UI components suitable for complex data visualization.
- **Alternatives Considered:**
  - *Vue.js:* Rejected. While excellent, React has a larger pool of enterprise-grade charting and data-grid libraries required for heavy analytics.

## 5. Database: MongoDB
- **Decision:** Use MongoDB as the primary datastore.
- **Rationale:** Video metadata, hierarchical zone definitions (polygons), and highly variable analytics payloads map perfectly to JSON document structures. Time-series data can also be handled efficiently.
- **Alternatives Considered:**
  - *PostgreSQL:* Rejected. While PostGIS can handle polygons, the rigidity of a relational schema would slow down early-stage iteration where AI output formats (behavior event schemas) may change frequently.

## 6. Video Processing Utility: OpenCV
- **Decision:** Use OpenCV for frame extraction, preprocessing, and drawing bounding boxes.
- **Rationale:** Standard library for computer vision tasks in Python. Highly optimized C++ backend.
- **Alternatives Considered:**
  - *FFmpeg (Directly):* While FFmpeg is used for video transcoding, OpenCV is preferred for the frame-by-frame matrix operations required before feeding data into YOLO.

## 7. Deployment & Orchestration: Docker
- **Decision:** Containerize all services using Docker.
- **Rationale:** Ensures environment consistency across local development and production. Essential for isolating complex Python ML dependencies (CUDA, PyTorch) from the host OS.
- **Alternatives Considered:**
  - *Virtual Environments (venv/Conda) directly on VMs:* Rejected. Prone to dependency drift and "works on my machine" issues. Harder to scale horizontally.
