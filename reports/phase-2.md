# RetailVision AI – Phase 2 Implementation
# Customer Behavior Recognition Engine

## Objective

Phase 2 builds the AI Behavior Recognition Engine on top of the completed Phase 1 Detection & Tracking Pipeline.

DO NOT rewrite or modify Phase 1.

Reuse:

- Detection JSON
- Tracking IDs
- Frame timestamps
- Bounding Boxes
- Metadata

The objective is to classify customer behavior using the real HackZen dataset.

No mock data.

No simulated events.

Everything must be generated from the actual processed videos.

---

# Phase Scope

Implement ONLY:

- Behavior Recognition
- Event Detection
- Temporal Analysis
- Behavior Timeline
- Behavior Reports
- APIs
- Testing

Do NOT rebuild:

- YOLO Detection
- ByteTrack
- Video Processing
- Metadata Extraction

---

# Supported Behaviors

The engine must recognize:

1. Touching Shelf

Definition:

Customer reaches shelf and touches products without taking them.

Output:

TOUCHING

---

2. Turning Toward Shelf

Definition:

Customer changes body orientation toward shelf.

Output:

TURNING_TO_SHELF

---

3. Picking and Returning

Definition:

Customer picks an item and places it back.

Output:

PICKING_AND_RETURNING

---

4. Picking and Putting

Definition:

Customer picks an item and keeps it.

Output:

PICKING_AND_PUTTING

---

# Folder Structure

backend/

services/

behavior/

behavior_engine.py

event_detector.py

timeline_builder.py

behavior_classifier.py

confidence.py

reports/

phase-2/

outputs/

behavior/

json/

csv/

timeline/

reports/

tests/

behavior/

---

# Module 1
Behavior Engine

Create

behavior_engine.py

Responsibilities

Read detection JSON

Read tracking IDs

Synchronize timestamps

Analyze every tracked customer

Generate behavior events

---

# Module 2
Behavior Classifier

Create

behavior_classifier.py

Input

Track ID

Bounding Boxes

Motion History

Output

Behavior Label

Behavior Confidence

Supported Labels

TOUCHING

TURNING_TO_SHELF

PICKING_AND_RETURNING

PICKING_AND_PUTTING

UNKNOWN

---

# Module 3
Temporal Event Detection

Behavior must not be classified using a single frame.

Instead

Analyze

Previous Frames

Current Frame

Future Frames

Create event windows.

Example

Frame 140

↓

Frame 155

↓

Frame 170

↓

Picking Detected

---

# Module 4
Timeline Builder

Generate

behavior timeline

Example

00:04

Customer 2

Touching

00:09

Customer 2

Picking

00:12

Customer 2

Returning

00:20

Customer 2

Leaves

Store timeline as

timeline.json

timeline.csv

---

# Module 5
Confidence Engine

Calculate confidence

Based on

Motion Stability

Track Stability

Frame Count

Behavior Duration

Generate

Behavior Confidence

Example

Touching

0.94

Picking

0.87

Returning

0.91

---

# Module 6
Behavior Reports

Generate

behavior_summary.md

Include

Total Customers

Total Behaviors

Touch Count

Picking Count

Returning Count

Turning Count

Behavior Duration

Average Behavior Confidence

Behavior Distribution

Timeline Summary

---

# Module 7
Behavior JSON

Generate

behavior.json

Example

{
    "track_id":3,

    "behavior":"PICKING_AND_RETURNING",

    "start_frame":120,

    "end_frame":180,

    "start_time":8.1,

    "end_time":12.0,

    "confidence":0.91
}

---

# Module 8
CSV Export

Generate

behavior.csv

Columns

Track ID

Behavior

Start Frame

End Frame

Start Time

End Time

Confidence

---

# Module 9
REST APIs

Implement

POST

/analyze

GET

/behaviors

GET

/behavior/{track_id}

GET

/timeline

GET

/summary

GET

/health

Swagger documentation required.

---

# Module 10
Logging

Generate

behavior.log

timeline.log

api.log

error.log

performance.log

---

# Module 11
Testing

Create tests

Behavior Classification

Timeline Generation

Confidence Calculation

API Validation

JSON Export

CSV Export

Report Generation

---

# Module 12
Execution

Run on the REAL HackZen dataset.

Generate behavior outputs for all videos.

Do NOT use mock values.

---

# Reports

Generate

reports/phase-2/

dataset_analysis.md

behavior_report.md

timeline_report.md

confidence_report.md

api_validation.md

performance_report.md

error_report.md

test_report.md

phase2_summary.md

---

# Required Evidence

Include

Behavior JSON

Behavior CSV

Timeline

Terminal logs

API screenshots

Sample outputs

Behavior report

---

# Acceptance Criteria

Dataset Loaded

PASS

Detection Loaded

PASS

Tracking Loaded

PASS

Behavior Recognition

PASS

Timeline Generated

PASS

JSON Export

PASS

CSV Export

PASS

Reports Generated

PASS

API Validation

PASS

Tests Passed

PASS

---

# Rules

Do NOT modify Phase 1.

Do NOT regenerate detections.

Consume Phase 1 outputs only.

No mock data.

No fabricated behaviors.

Everything must be generated from the actual dataset.

---

# Final Deliverable

Generate

reports/phase-2/final_phase2_report.md

Include

Executive Summary

Behavior Statistics

Timeline Analysis

Performance

Confidence Analysis

API Summary

Testing Summary

Known Limitations

Phase 3 Readiness

Overall Score

Final Recommendation

APPROVED

or

REQUIRES CHANGES