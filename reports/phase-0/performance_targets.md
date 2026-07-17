# Performance Targets
## RetailVision AI

These performance targets serve as the acceptance criteria for future development phases. The system must meet or exceed these metrics in production environments.

---

## 1. AI Accuracy Targets

| Metric | Target | Definition / Measurement |
|---|---|---|
| **Person Detection Accuracy (mAP@0.5)** | > 90% | Mean Average Precision of the YOLO model on standard retail evaluation datasets. |
| **Tracking Accuracy (MOTA)** | > 85% | Multiple Object Tracking Accuracy, accounting for false positives, false negatives, and identity switches. |
| **Behaviour Classification Accuracy** | > 80% | F1-Score for correctly identifying specific interactions (e.g., Picking and Putting) against a manually annotated ground-truth test set. |

---

## 2. Processing Speed Targets

| Metric | Target | Definition / Measurement |
|---|---|---|
| **AI Inference Target FPS** | > 15 FPS | The entire pipeline (Detection + Tracking + Behavior Classification) must process at least 15 frames per second on a standard T4 GPU per video stream. |
| **Upload Processing Time** | < 2x Video Length | A 10-minute video should be fully processed and analytics available within 20 minutes of upload completion. |

---

## 3. Web Platform Performance

| Metric | Target | Definition / Measurement |
|---|---|---|
| **Dashboard Load Time** | < 1.5 seconds | Time to Interactive (TTI) for the main analytics dashboard on a standard broadband connection. |
| **API Response Time (p95)** | < 300 ms | 95th percentile response time for all non-file-upload REST API endpoints. |
| **Report Generation Time** | < 5 seconds | Time taken to compile and return a downloadable PDF/CSV report from the database. |

---

## 4. System Reliability

| Metric | Target | Definition / Measurement |
|---|---|---|
| **System Availability** | 99.9% | Uptime of the web application and API layer, excluding scheduled maintenance. |
| **Fault Tolerance** | Zero Data Loss | If an AI worker node crashes mid-processing, the task queue must successfully reassign the video to a new node. |
