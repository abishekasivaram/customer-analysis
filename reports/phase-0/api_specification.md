# REST API Specification
## RetailVision AI

---

## 1. Overview
The backend exposes a RESTful API built with FastAPI. All endpoints (except login/health) require JWT authentication via the `Authorization: Bearer <token>` header.

---

## 2. Endpoints

### 2.1. Authentication

**`POST /auth/login`**
- **Purpose:** Authenticate user and issue JWT.
- **Method:** POST
- **Authentication:** None
- **Input (JSON):** `{"email": "user@example.com", "password": "password123"}`
- **Output (JSON):** `{"access_token": "eyJ...", "token_type": "bearer", "expires_in": 3600}`
- **Possible Errors:** `401 Unauthorized` (Invalid credentials), `422 Unprocessable Entity` (Validation error).

### 2.2. Video Management

**`POST /videos/upload`**
- **Purpose:** Upload a new video file to the system.
- **Method:** POST (multipart/form-data)
- **Authentication:** Required (JWT)
- **Input:** `file` (Binary), `project_id` (String)
- **Output (JSON):** `{"video_id": "vid_123", "status": "Uploaded", "message": "File saved successfully."}`
- **Possible Errors:** `400 Bad Request` (Invalid file format), `413 Payload Too Large`.

**`POST /videos/{video_id}/process`**
- **Purpose:** Trigger the AI pipeline on an uploaded video.
- **Method:** POST
- **Authentication:** Required (JWT)
- **Input (JSON):** `{"zones": [{...}], "parameters": {...}}`
- **Output (JSON):** `{"task_id": "tsk_456", "status": "Processing Started"}`
- **Possible Errors:** `404 Not Found` (Video does not exist), `409 Conflict` (Already processing).

**`GET /videos`**
- **Purpose:** Retrieve a list of videos for a project.
- **Method:** GET
- **Authentication:** Required (JWT)
- **Input (Query):** `?project_id=proj_123&page=1&limit=20`
- **Output (JSON):** `{"data": [{"video_id": "vid_123", "status": "Completed", ...}], "total": 1}`
- **Possible Errors:** `401 Unauthorized`.

### 2.3. Analytics & Reporting

**`GET /analytics`**
- **Purpose:** Retrieve aggregated metrics for dashboard charting.
- **Method:** GET
- **Authentication:** Required (JWT)
- **Input (Query):** `?project_id=proj_123&start_date=2023-01-01&end_date=2023-01-31&metric=dwell_time`
- **Output (JSON):** `{"timeline": [...], "totals": {...}}`
- **Possible Errors:** `400 Bad Request` (Invalid date range).

**`GET /dashboard`**
- **Purpose:** Retrieve high-level summary KPIs for the main dashboard view.
- **Method:** GET
- **Authentication:** Required (JWT)
- **Input (Query):** `?project_id=proj_123`
- **Output (JSON):** `{"total_customers": 120, "top_zone": "Shelf A", "picking_conversion_rate": 0.45}`
- **Possible Errors:** `401 Unauthorized`.

**`GET /reports`**
- **Purpose:** List available generated reports.
- **Method:** GET
- **Authentication:** Required (JWT)
- **Input (Query):** `?project_id=proj_123`
- **Output (JSON):** `{"reports": [{"id": "rep_1", "url": "https://...", "date": "..."}]}`
- **Possible Errors:** `401 Unauthorized`.

### 2.4. System Health

**`GET /health`**
- **Purpose:** Liveness probe for orchestration platforms (Kubernetes/Docker).
- **Method:** GET
- **Authentication:** None
- **Input:** None
- **Output (JSON):** `{"status": "OK", "database": "Connected", "queue": "Alive"}`
- **Possible Errors:** `503 Service Unavailable` (If DB/Queue is down).
