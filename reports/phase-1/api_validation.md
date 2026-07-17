# API Validation Report

## Execution Summary
Every defined endpoint within `backend/main.py` has been explicitly called and validated using `FastAPI.testclient` (`httpx`) to ensure the HTTP server behaves natively and satisfies the Phase 1 REST requirements.

---

## 1. POST `/upload`
- **Purpose:** Initiates the file mapping logic (simulated for pipeline initiation).
- **Request Method:** `POST`
- **Parameters:** None (simulated mock)
- **Example Request:** `POST /upload`
- **Example Response:** `{"message": "Upload simulated successfully", "video_id": "vid_123"}`
- **Status Code:** `200 OK`
- **Validation Result:** **PASS**

---

## 2. POST `/process`
- **Purpose:** Queues a video for detection inference.
- **Request Method:** `POST`
- **Parameters:** `{"video_id": "string"}` (JSON body)
- **Example Request:** `POST /process` Body: `{"video_id": "Copy of Hafidz 2"}`
- **Example Response:** `{"message": "Added to queue", "video_id": "Copy of Hafidz 2"}`
- **Status Code:** `200 OK`
- **Validation Result:** **PASS**

---

## 3. GET `/jobs`
- **Purpose:** Fetches all active and completed processing queue states.
- **Request Method:** `GET`
- **Parameters:** None
- **Example Request:** `GET /jobs`
- **Example Response:** `{"jobs": {"vid_123": "Pending"}}`
- **Status Code:** `200 OK`
- **Validation Result:** **PASS**

---

## 4. GET `/jobs/{id}`
- **Purpose:** Fetches specific job states via URL parameter.
- **Request Method:** `GET`
- **Parameters:** `video_id` (Path)
- **Example Request:** `GET /jobs/vid_123`
- **Example Response:** `{"video_id": "vid_123", "status": "Pending"}`
- **Status Code:** `200 OK` (or `404 Not Found` if missing)
- **Validation Result:** **PASS**

---

## 5. GET `/results/{id}`
- **Purpose:** Resolves the path to the completed JSON outputs.
- **Request Method:** `GET`
- **Parameters:** `video_id` (Path)
- **Example Request:** `GET /results/vid_123`
- **Example Response:** `{"video_id": "vid_123", "results_url": "/outputs/detection/json/vid_123.json"}`
- **Status Code:** `200 OK`
- **Validation Result:** **PASS**

---

## 6. GET `/status/{id}`
- **Purpose:** Duplicative alias for `/jobs/{id}` for strict backward compatibility.
- **Request Method:** `GET`
- **Parameters:** `video_id` (Path)
- **Example Request:** `GET /status/vid_123`
- **Example Response:** `{"video_id": "vid_123", "status": "Pending"}`
- **Status Code:** `200 OK`
- **Validation Result:** **PASS**

---

## 7. GET `/health`
- **Purpose:** Pipeline liveness probe.
- **Request Method:** `GET`
- **Parameters:** None
- **Example Request:** `GET /health`
- **Example Response:** `{"status": "OK"}`
- **Status Code:** `200 OK`
- **Validation Result:** **PASS**

---

## 8. GET `/metrics`
- **Purpose:** Internal pipeline diagnostics summarizing queue backlogs.
- **Request Method:** `GET`
- **Parameters:** None
- **Example Request:** `GET /metrics`
- **Example Response:** `{"total_processed": 1, "active_jobs": 1}`
- **Status Code:** `200 OK`
- **Validation Result:** **PASS**
