# Development Roadmap
## RetailVision AI

---

## Phase 0: Enterprise Foundation (Current)
**Focus:** Architecture, Standards, and Documentation.
- **Expected Deliverables:** Software Architecture, Database Design, API Specs, Coding Standards, Design System, Risk Assessment.
- **Acceptance Criteria:** All documents completed and approved. Project structure initialized.
- **Verification Strategy:** Manual review of all markdown documents and folder verification.

---

## Phase 1: Core Infrastructure & Ingestion
**Focus:** Backend setup, Database connection, and Video Upload handling.
- **Dependencies:** Completion of Phase 0.
- **Expected Deliverables:** 
  - FastAPI server running.
  - MongoDB connection established.
  - POST `/videos/upload` endpoint implemented.
  - Cloud storage (S3/MinIO) integration for video saving.
- **Acceptance Criteria:** A user can upload a video via API, and the metadata is saved in MongoDB.
- **Verification Strategy:** Postman/cURL API tests. Database inspection.

---

## Phase 2: AI Pipeline Integration (Detection & Tracking)
**Focus:** Implementing the core vision models.
- **Dependencies:** Phase 1 (Video ingestion).
- **Expected Deliverables:**
  - Background worker setup (Celery/Redis).
  - YOLOv8 integration for person detection.
  - ByteTrack integration for temporal tracking.
  - Data saving pipeline (Tracks to MongoDB).
- **Acceptance Criteria:** Processing a video successfully generates track histories in the database.
- **Verification Strategy:** Visualizing bounding boxes and track IDs on a sample output video to manually verify accuracy.

---

## Phase 3: Spatial & Behavior Analytics
**Focus:** Zone mapping and heuristic behavior classification.
- **Dependencies:** Phase 2 (Tracking data).
- **Expected Deliverables:**
  - Logic to define polygonal Zones (Shelves, Aisles).
  - Intersection logic (Track vs. Zone).
  - Rule-based state machine for identifying Behaviors (Touching, Picking).
  - Analytics Aggregation jobs (Hourly rollups).
- **Acceptance Criteria:** The system successfully identifies and logs specific behavior events based on tracks entering/interacting with zones.
- **Verification Strategy:** Compare system output against a manually annotated test video. Must meet performance targets.

---

## Phase 4: Web Dashboard & UI
**Focus:** Frontend visualization of the data.
- **Dependencies:** Phase 3 (Aggregated Analytics).
- **Expected Deliverables:**
  - React SPA setup.
  - Authentication UI.
  - Video management dashboard.
  - Analytics charts (Dwell times, conversion rates).
- **Acceptance Criteria:** Users can log in, view processed videos, and interact with data visualizations.
- **Verification Strategy:** End-to-end UI testing (e.g., Cypress or Playwright).

---

## Phase 5 (Future Milestone): AI Business Advisor & ReID
**Focus:** Advanced features and multi-camera support.
- **Expected Deliverables:** LLM integration for text-based insights. Re-Identification models for tracking across cameras.
