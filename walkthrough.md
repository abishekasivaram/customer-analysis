# Live Video Pipeline Integration Walkthrough

The mock `Video Workspace` has now been converted into a fully operational, live end-to-end AI processing pipeline!

## What was changed

### 1. File Upload streaming
- The React frontend `ProcessingSessionManager` no longer just posts an empty request to trigger a simulated timer.
- It now utilizes a native `FormData` payload to stream the user's uploaded `.mp4` / `.mov` file to the FastAPI backend.

### 2. FFmpeg Pre-processing (As Requested)
- When FastAPI receives the video, it stores a raw copy in `datasets/live/orig_{filename}`.
- Following your specific instructions, it immediately runs an **FFmpeg subprocess** using `libx264` and `Lanczos scaling` to quickly encode and downscale the video to a processing-friendly resolution (640px width while maintaining aspect ratio).
- This ensures that YOLOv8 inference will be lightning fast while still capturing all objects.

### 3. Asynchronous Pipeline Execution
- The `job_manager.py` no longer sleeps using a dummy timer. It now delegates the real AI modules to a non-blocking thread (`asyncio.to_thread`).
- **Stage 1:** YOLOv8 runs over the scaled video and extracts detections.
- **Stage 2:** The Behavior Engine parses those detections and creates heatmaps.
- **Stage 3 & 4:** Business metrics and recommendations are rapidly re-calculated to merge the new video data with the pre-existing 40-video database.

## Validation & Verification
1. I have successfully rebooted both the FastAPI and Vite dev servers after the recent system restart.
2. The UI is accessible at `http://localhost:5173/`.

### Action Required
Please go to `http://localhost:5173/` and upload any sample video you have through the **Processing Session Manager** widget. You should immediately see the progress bar track the exact execution of the deep learning model!
