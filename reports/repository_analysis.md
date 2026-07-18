# Repository Analysis

## Project Structure
The repository is structured as a monolithic backend application designed to process video datasets through an AI pipeline and expose the results via a FastAPI server. The root contains top-level directories: `backend`, `configs`, `datasets`, `reports`, and `tests`. 

## Backend Architecture
- **Core Engine:** Located in `backend/core/` and `backend/services/engine.py` (handles YOLO/ByteTrack detection).
- **Services:** Segmented logically into `advisor`, `analytics`, `behavior`, and `business`.
- **API Layer:** A single `main.py` entrypoint defining all Fast API routes.
- **Orchestration:** Sequential scripts (`run_pipeline.py`, `run_phase2.py`, etc.) manage the flow of data between services.

## Frontend Architecture
None implemented. The project relies entirely on the FastAPI backend to serve JSON and CSV payloads.

## Implemented Phases
- **Phase 1 (Detection):** Implemented via `backend/services/engine.py` and `run_pipeline.py`.
- **Phase 2 (Behavior):** Implemented via `backend/services/behavior/` and `run_phase2.py`.
- **Phase 3 (Analytics):** Implemented via `backend/services/analytics/` and `run_phase3.py`.
- **Phase 4 (Advisor):** Implemented via `backend/services/advisor/` and `run_phase4.py`.

## Available Datasets
The `datasets/` directory contains 40 raw 4K `.mp4` CCTV video clips (HackZen dataset), categorized by behaviors such as "Picking and Putting", "Touching", and "Turning to Shelf".

## Available Model Weights
The root directory contains `yolov8n.pt`. The `config.py` also dynamically downloads it into `models/person_detection/` if missing.

## API Routes
- **Phase 1:** `/process`, `/status/{video_id}`, `/results/{video_id}`, `/health`, `/upload`, `/jobs`, `/metrics`
- **Phase 2:** `/analyze`, `/behaviors`, `/behavior/{track_id}`, `/timeline`, `/summary`, `/behavior-video/{video_id}`, `/heatmaps`, `/heatmap/{type}`, `/zones`, `/zone/{id}`, `/analytics/summary`
- **Phase 3:** `/retail/summary`, `/retail/kpis`, `/retail/flow`, `/retail/zones`, `/retail/customers`, `/retail/journeys`, `/retail/interactions`, `/retail/insights`, `/retail/metrics`, `/retail/trends`, `/retail/alerts`, `/retail/dashboard`, `/retail/export/*`, `/dashboard/data`
- **Phase 4:** `/advisor/recommendations`, `/advisor/summary`, `/advisor/store-health`, `/advisor/alerts`, `/advisor/opportunities`, `/advisor/executive-report`, `/advisor/business-score`

## Execution Scripts
- `run_pipeline.py`, `run_phase2.py`, `run_phase3.py`, `run_phase4.py`, `evaluate_phase2.py`, `generate_phase2_reports.py`, `render_two_videos.py`, `get_video_stats.py`.

## Tests
Comprehensive `pytest` coverage exists in `tests/` for advisor, behavior, business, and `test_api.py`.

## Configuration Files
- `configs/advisor_rules.yaml`
- `configs/analytics.yaml`
- `configs/business.yaml`
- `backend/core/config.py`
