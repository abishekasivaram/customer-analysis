# Configuration Standards
## RetailVision AI

---

## 1. Overview
This document outlines the standards for configuring environments, managing secrets, and standardizing system pathways across Development, Staging, and Production deployments.

---

## 2. Configuration Strategy
- **12-Factor App Methodology:** All configurations that vary between environments must be stored in the environment variables, never hardcoded in the application.
- **.env Files:** Used exclusively for local development. These must be added to `.gitignore`.
- **Secrets Management:** In production, secrets must be injected via secure vaults (e.g., AWS Secrets Manager, HashiCorp Vault) or Kubernetes Secrets.

---

## 3. Environment Variables
Standard prefixes must be used:
- `APP_`: General application settings (e.g., `APP_ENV=production`, `APP_PORT=8000`).
- `DB_`: Database connection settings (e.g., `DB_URI=mongodb://...`, `DB_NAME=retailvision`).
- `REDIS_`: Task queue and cache settings.
- `JWT_`: Authentication secrets (e.g., `JWT_SECRET_KEY`, `JWT_EXPIRE_MINUTES`).
- `AI_`: Model specific settings (e.g., `AI_CONFIDENCE_THRESHOLD=0.5`).

---

## 4. Logging Standards
- **Format:** JSON formatted logs in Production for easy ingestion by ELK/Datadog. Standard text format in Development for readability.
- **Levels:**
  - `DEBUG`: Detailed information, typically of interest only when diagnosing problems.
  - `INFO`: Confirmation that things are working as expected.
  - `WARNING`: An indication that something unexpected happened, but the software is still working.
  - `ERROR`: A serious problem, the software has not been able to perform some function.
- **Destination:** stdout/stderr. Do not write logs directly to the filesystem within containers.

---

## 5. Storage Paths
- **Temporary Storage:** `/tmp/retailvision/uploads/` for chunked uploads or transient video processing. Must be cleaned up automatically.
- **Persistent Media Storage:** AWS S3 or MinIO. Bucket nomenclature: `rv-media-prod`, `rv-media-staging`.
- **Model Paths:** Pre-trained weights should be stored in a centralized directory mapped via volumes: `/models/weights/yolov8_retail.pt`.

---

## 6. Limits and Thresholds
- **Upload Limits:** Maximum video upload size capped at 2GB (configurable via `APP_MAX_UPLOAD_SIZE`).
- **Processing Timeouts:** AI processing tasks have a hard timeout of 4 hours to prevent stuck workers.

---

## 7. Caching Strategy
- **Layer:** Redis.
- **Data:** Dashboard KPIs and aggregated analytics are cached with a TTL of 15 minutes.
- **Invalidation:** Cache is automatically invalidated when a new video finishes processing for the corresponding project.
