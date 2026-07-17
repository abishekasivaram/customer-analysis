# Database Design
## RetailVision AI

---

## 1. Overview
The database uses MongoDB, chosen for its flexibility with hierarchical metadata (like zones in a video) and time-series capability for tracking and analytics data.

---

## 2. Collections

### Users
**Purpose:** Manage authentication, roles, and tenant separation.
**Primary Fields:** `_id`, `email`, `password_hash`, `role` (Admin, Manager), `organization_id`, `created_at`.
**Relationships:** One-to-Many with Projects.
**Indexes:** Unique index on `email`.
**Expected Growth:** Low.

### Projects
**Purpose:** Group videos and analytics by specific store locations or campaigns.
**Primary Fields:** `_id`, `name`, `organization_id`, `description`, `created_at`.
**Relationships:** One-to-Many with Videos.
**Indexes:** Index on `organization_id`.
**Expected Growth:** Low to Medium.

### Videos
**Purpose:** Store metadata for uploaded videos and their processing state.
**Primary Fields:** `_id`, `project_id`, `filename`, `s3_key`, `status` (Pending, Processing, Completed, Failed), `duration`, `fps`, `resolution`, `created_at`.
**Relationships:** Many-to-One with Projects.
**Indexes:** Index on `project_id`, `status`.
**Expected Growth:** Medium (Hundreds to thousands of records).

### Settings (Configurations & Zones)
**Purpose:** Store video-specific configurations, most importantly defined ROI zones (shelves, aisles).
**Primary Fields:** `_id`, `video_id`, `zones` (Array of polygons with `zone_name`, `coordinates`), `parameters` (confidence thresholds).
**Relationships:** One-to-One with Videos.
**Indexes:** Index on `video_id`.
**Expected Growth:** Same as Videos collection.

### Frames (Optional / Temporary)
**Purpose:** Store highly granular frame-level metadata if required for debugging or complex temporal modeling. Usually avoided in production to save space.
**Expected Growth:** Extremely High. (Consider omitting or using a Time-Series collection with TTL).

### Detections
**Purpose:** Store raw bounding boxes from the Detection Engine.
**Primary Fields:** `_id`, `video_id`, `frame_number`, `boxes` (Array of `[x, y, w, h, conf, class]`).
**Relationships:** Many-to-One with Videos.
**Indexes:** Compound Index on `video_id` + `frame_number`.
**Expected Growth:** High. (Will utilize TTL indexes to clear raw data after aggregation).

### Tracks
**Purpose:** Store continuous tracking identities across time.
**Primary Fields:** `_id`, `video_id`, `track_id`, `start_frame`, `end_frame`, `trajectory` (Array of coordinates).
**Relationships:** Many-to-One with Videos.
**Indexes:** Index on `video_id` + `track_id`.
**Expected Growth:** Medium to High.

### Behaviours
**Purpose:** Log specific, classified behavior events.
**Primary Fields:** `_id`, `video_id`, `track_id`, `behavior_type` (e.g., "Picking And Putting"), `zone_id`, `start_time`, `end_time`, `confidence`.
**Relationships:** Linked to Videos, Tracks, and defined Zones.
**Indexes:** Index on `video_id`, `behavior_type`.
**Expected Growth:** Medium.

### Analytics (Aggregated)
**Purpose:** Store pre-computed hourly/daily statistics for fast dashboard rendering.
**Primary Fields:** `_id`, `project_id`, `date`, `hour`, `metric_type` (e.g., "Zone Dwell Time"), `value`.
**Relationships:** Linked to Projects.
**Indexes:** Compound Index on `project_id` + `date` + `metric_type`.
**Expected Growth:** Medium (Highly predictable).

### Reports
**Purpose:** Store references to generated PDF/CSV reports.
**Primary Fields:** `_id`, `project_id`, `report_url`, `type`, `generated_at`.
**Relationships:** Linked to Projects.
**Indexes:** Index on `project_id`.
**Expected Growth:** Low.
