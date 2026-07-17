# Phase 1 — Person Detection Engine

## Objective

Build a production-grade customer detection system capable of detecting every visible customer in the retail surveillance videos.

This phase focuses only on customer detection.

Do NOT implement:

- Tracking
- Behavior Classification
- Analytics
- Dashboard Logic

Detection only.

---

# Business Goal

The entire RetailVision AI platform depends on reliable customer detection.

Every downstream module uses these detections:

Person Detection
→ Tracking
→ Behavior Recognition
→ Analytics
→ Business Intelligence

If detections are inaccurate, all later analytics become unreliable.

---

# Technical Requirements

## Detection Model

Evaluate and select the best model.

Recommended:

- YOLOv11
- YOLOv12
- YOLOv8

Document justification.

---

# Input

Retail CCTV Videos

Supported:

mp4
avi
mov

---

# Output

For every frame:

```json
{
  "frame": 101,
  "customer_id": null,
  "bbox": [x1,y1,x2,y2],
  "confidence": 0.96,
  "class": "person"
}
```

---

# Detection Requirements

Detect:

✓ Standing customers

✓ Walking customers

✓ Customers near shelves

✓ Customers holding baskets

✓ Partially visible customers

---

# Bounding Box Quality

Bounding boxes should:

- Cover full body when visible
- Remain stable
- Minimize jitter
- Minimize missed detections

---

# Performance Metrics

Capture:

Precision

Recall

FPS

Average Confidence

False Positives

False Negatives

---

# Video Processing Pipeline

Video
↓
Frame Extraction
↓
Person Detection
↓
Bounding Box Rendering
↓
JSON Export
↓
Annotated Video Export

---

# Outputs Required

## Annotated Videos

Store:

outputs/detection/videos/

---

## Detection JSON

Store:

outputs/detection/json/

---

## Detection CSV

Store:

outputs/detection/csv/

Example:

frame,bbox_x1,bbox_y1,bbox_x2,bbox_y2,confidence

---

## Detection Statistics

Store:

outputs/detection/reports/

---

# Report Requirements

Generate:

detection_summary.md

Including:

Total Frames

Total Detections

Average Confidence

Lowest Confidence

Highest Confidence

FPS

Model Used

Hardware Used

---

# Edge Cases

Evaluate:

Customer near shelf

Customer partially hidden

Customer entering frame

Customer leaving frame

Customer near camera edge

---

# Folder Structure

backend/

models/person_detection/

outputs/detection/

reports/phase-1/

tests/person_detection/

---

# Constraints

No mock data

Use actual competition videos

Generate actual outputs

Store actual metrics

No hardcoded values

---

# Success Criteria

PASS only if:

✓ Every video processed

✓ Annotated videos generated

✓ Detection JSON generated

✓ Detection statistics generated

✓ Detection report generated

✓ False detections documented