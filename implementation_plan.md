# Implement Live Video Processing Pipeline

This plan outlines the architectural changes required to connect the frontend upload UI to the backend AI pipeline, allowing users to upload a video, watch it process in real-time, and have the dashboard seamlessly reflect the new insights.

## Proposed Changes

### 1. Frontend: Connect File Upload (`frontend/src/components/workspace/ProcessingSessionManager.tsx`)
- [MODIFY] `ProcessingSessionManager.tsx`: Update the `handleUpload` function to construct a `FormData` object containing the selected video file and send it to the `/upload` API endpoint as `multipart/form-data`.

### 2. Backend: File Reception (`backend/main.py`)
- [MODIFY] `main.py`: Refactor the `/upload` endpoint to accept `UploadFile`. It will save the uploaded video to the `datasets/` directory (e.g., `datasets/uploads/{filename}`) and pass the file path to the `job_manager`.

### 3. Backend: Real Pipeline Execution (`backend/services/job_manager.py`)
- [MODIFY] `job_manager.py`: Completely replace the mocked `_simulate_pipeline` sleep loop with the actual AI pipeline logic. 
  - **Stage 1 (Detection & Tracking):** Execute YOLOv8 and ByteTrack on the single uploaded video using `engine.process_video`.
  - **Stage 2 (Behavior Analysis):** Execute `run_phase2()` to analyze spatial behavior and generate heatmaps.
  - **Stage 3 (Business Analytics):** Execute `run_phase3()` to compile the new data into the master KPI summaries.
  - **Stage 4 (Recommendations):** Execute `run_phase4()` to generate new AI recommendations based on the updated dataset.
  - The job manager will update the `current_stage` and `progress` fields appropriately so the frontend progress bar reflects true backend progress.

## Verification Plan
1. Upload a short sample video (e.g., one of the existing 4K videos or a new one) via the dashboard UI.
2. Watch the progress bar advance as YOLO detection runs.
3. Once completed, navigate to the Executive Dashboard and verify that total metrics (e.g., Total Visitors, Overall Health) have been updated to include the new video's data.
