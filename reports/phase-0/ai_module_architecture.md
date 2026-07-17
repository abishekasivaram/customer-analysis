# AI Module Architecture
## RetailVision AI

---

## 1. Overview
The AI Processing Layer is composed of highly decoupled, modular engines. This separation of concerns allows individual models to be upgraded, scaled, or replaced without affecting the rest of the pipeline.

---

## 2. Detection Engine

**Responsibilities:**
- Process individual video frames to locate target objects (primarily persons/customers).
- Output spatial bounding boxes with confidence scores.

**Inputs:**
- Raw Video Frames (NumPy arrays).
- Configuration: Confidence thresholds, NMS thresholds.

**Outputs:**
- Array of detections per frame: `[x_min, y_min, x_max, y_max, confidence, class_id]`.

**Dependencies:**
- YOLOv8 (or equivalent state-of-the-art object detection model).
- GPU computation (CUDA/cuDNN) for real-time performance.

**Future Extensibility:**
- Easy substitution of the YOLO weights for a retail-specific fine-tuned model.
- Addition of secondary detection models (e.g., detecting shopping baskets or specific products).

---

## 3. Tracking Engine

**Responsibilities:**
- Associate spatial detections across consecutive temporal frames to establish identity continuity (Track IDs).
- Handle short-term occlusions (e.g., customer walking behind a shelf).

**Inputs:**
- Bounding box arrays from the Detection Engine.
- Sequential video frames (optional, depending on the tracking algorithm).

**Outputs:**
- Array of tracks per frame: `[track_id, x_min, y_min, x_max, y_max, state]`.

**Dependencies:**
- ByteTrack algorithm.
- Detection Engine (must run prior).

**Future Extensibility:**
- Integration of Re-Identification (ReID) models to track customers across multiple cameras or after long-term occlusion.

---

## 4. Behaviour Recognition Engine

**Responsibilities:**
- Analyze track trajectories, temporal data, and spatial relationships to Regions of Interest (ROIs) to classify behaviors.
- Identify: Touching, Turning To Shelf, Picking And Returning, Picking And Putting.

**Inputs:**
- Track histories from the Tracking Engine.
- Pre-defined ROI coordinates (Shelves, checkout lines).

**Outputs:**
- Behavior Events: `{track_id, behavior_type, start_time, end_time, confidence, zone_id}`.

**Dependencies:**
- Tracking Engine.
- Spatial Configuration (Zone definitions).

**Future Extensibility:**
- Transitioning from heuristic/rule-based state machines to deep temporal action localization models (e.g., SlowFast, 3D CNNs).
- Adding new behavior classes (e.g., browsing, waiting in line).

---

## 5. Analytics Engine

**Responsibilities:**
- Roll up raw behavioral events and track data into actionable, aggregated metrics.
- Generate hourly/daily summaries (e.g., dwell times, shelf engagement rates, conversion proxies).

**Inputs:**
- Raw Behavior Events and Track data from MongoDB.

**Outputs:**
- Aggregated Time-Series Data for Dashboard consumption.

**Dependencies:**
- Database Layer (MongoDB).
- Background Job Scheduler (e.g., Celery/Cron).

**Future Extensibility:**
- Implementation of predictive analytics (forecasting peak hours based on historical data).

---

## 6. Recommendation Engine

**Responsibilities:**
- Act as an "AI Business Advisor" by analyzing the aggregated data and generating plain-text, actionable business recommendations for store managers.

**Inputs:**
- Aggregated Analytics Data.
- Historical Trends.

**Outputs:**
- Actionable Text Prompts: (e.g., "Endcap A has high engagement but low picking rate. Consider adjusting pricing or product placement.")

**Dependencies:**
- Analytics Engine.

**Future Extensibility:**
- Integration with Large Language Models (LLMs) to provide conversational querying of store analytics.
