# Project Inventory

## Folder Tree
- `backend/`
  - `core/`
  - `services/`
    - `advisor/`
    - `analytics/`
    - `behavior/`
    - `business/`
- `configs/`
- `datasets/`
- `reports/`
- `tests/`
*(Missing: `frontend/`, `outputs/`, `models/`, `scripts/`)*

## Implemented Modules
Based on source code analysis:
- **Phase 1 (Detection & Tracking)**: `engine.py`, `run_pipeline.py`
- **Phase 2 (Behavior Recognition)**: `backend/services/behavior/`, `run_phase2.py`, `evaluate_phase2.py`, `generate_phase2_reports.py`
- **Phase 3 (Business Analytics)**: `backend/services/analytics/`, `backend/services/business/`, `run_phase3.py`
- **Phase 4 (AI Advisor)**: `backend/services/advisor/`, `run_phase4.py`

## Missing Modules
- `frontend/` (No UI implemented)
- `outputs/` (Generated outputs are not available in this clone)
- `scripts/` (No utility scripts folder)

## Dependencies
- **Python Packages**: Listed in `backend/requirements.txt` (FastAPI, uvicorn, ultralytics, opencv-python, pandas, pydantic)
- **Frontend Packages**: None (No frontend)

## Configuration Files
- `configs/advisor_rules.yaml`
- `configs/analytics.yaml`
- `configs/business.yaml`

## Scripts
- `backend/run_pipeline.py`
- `backend/run_phase2.py`
- `backend/evaluate_phase2.py`
- `backend/generate_phase2_reports.py`
- `backend/run_phase3.py`
- `backend/run_phase4.py`
- `backend/render_two_videos.py`
- `get_video_stats.py`

## Tests
- `tests/advisor/`
- `tests/behavior/`
- `tests/business/`
- `tests/test_api.py`

## Generated Outputs (if present)
- Generated artifacts are not available in this clone.

---

## API Routers (FastAPI Endpoints)
*Defined in `backend/main.py`*

**Phase 1**
- `/process` (POST): Queues video processing (Consumes: `ProcessRequest`, Produces: JSON)
- `/status/{video_id}` (GET): Gets processing status
- `/results/{video_id}` (GET): Gets path to detection JSON
- `/health` (GET): Health check
- `/upload` (POST): Simulates upload
- `/jobs` (GET): Lists all jobs
- `/jobs/{video_id}` (GET): Gets specific job status
- `/metrics` (GET): Gets processing metrics

**Phase 2**
- `/analyze` (POST): Queues Phase 2 analysis
- `/behaviors` (GET): Gets behaviors
- `/behavior/{track_id}` (GET): Gets behavior for track ID
- `/timeline` (GET): Gets timeline
- `/summary` (GET): Gets behavior summary
- `/behavior-video/{video_id}` (GET): Gets annotated behavior video URL
- `/heatmaps` (GET): Gets list of heatmaps
- `/heatmap/{heatmap_type}` (GET): Gets specific heatmap URL
- `/zones` (GET): Gets zones list
- `/zone/{zone_id}` (GET): Gets specific zone info
- `/analytics/summary` (GET): Gets Phase 2 analytics summary

**Phase 3**
- `/retail/summary` (GET): Gets business summary
- `/retail/kpis` (GET): Gets KPIs
- `/retail/flow` (GET): Gets customer flow
- `/retail/zones` (GET): Gets zone performance
- `/retail/customers` (GET): Gets customer segments
- `/retail/journeys` (GET): Gets customer journeys
- `/retail/interactions` (GET): Gets interactions
- `/retail/insights` (GET): Gets business insights
- `/retail/metrics` (GET): Gets business metrics
- `/retail/trends` (GET): Gets trends
- `/retail/alerts` (GET): Gets alerts
- `/retail/dashboard` (GET): Gets dashboard
- `/retail/export/json` (GET): Export JSON
- `/retail/export/csv` (GET): Export CSV
- `/dashboard/data` (GET): Dashboard data

**Phase 4**
- `/advisor/recommendations` (GET): Gets recommendations
- `/advisor/summary` (GET): Gets advisor dashboard
- `/advisor/store-health` (GET): Gets store health score
- `/advisor/alerts` (GET): Gets prioritized alerts
- `/advisor/opportunities` (GET): Gets business opportunities
- `/advisor/executive-report` (GET): Gets executive summary
- `/advisor/business-score` (GET): Gets business score

---

## Services

- **Detection & Tracking**: Defined in `backend/services/engine.py`. Purpose: Run YOLOv8 and ByteTrack on raw video. Used by: Phase 1 Pipeline. Outputs: detections & tracks (JSON/CSV).
- **Behavior Recognition**: Defined in `backend/services/behavior/`. Purpose: Classify picking, touching, viewing behaviors. Used by: Phase 2. Outputs: Behavior logs and events.
- **Analytics & Business**: Defined in `backend/services/analytics/` & `backend/services/business/`. Purpose: Calculate dwell time, heatmaps, KPIs, flow. Used by: Phase 3. Outputs: Dashboards, business JSON files.
- **Advisor**: Defined in `backend/services/advisor/`. Purpose: Generate recommendations and store health scores. Used by: Phase 4. Outputs: Advisor metrics.

---

## Dependency Graph
Phase 1 (Detection & Tracking) 
  ↓
Phase 2 (Behavior Recognition)
  ↓
Phase 3 (Business Analytics)
  ↓
Phase 4 (AI Advisor)
  ↓
*(Frontend UI Not Implemented)*
