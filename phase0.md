# Phase 0 — Dataset Validation & Architecture Setup

## Objective

Build a complete understanding of the provided retail behavior dataset before implementing any AI models.

This phase is focused on analysis, validation, architecture planning, and project structure setup.

No behavior classification models should be built in this phase.

---

# Deliverables

1. Dataset Inspection Report
2. Video Metadata Report
3. Dataset Quality Assessment
4. Project Architecture Design
5. Folder Structure Initialization
6. Technical Feasibility Report

---

# Tasks

## Dataset Discovery

Analyze all provided videos and generate:

- Total number of videos
- Video names
- Video categories
- Duration of each video
- Resolution of each video
- FPS of each video
- Codec information
- Total dataset duration

---

## Camera Analysis

Determine:

- Camera angle
- Camera position
- Fixed camera or moving camera
- Shelf visibility
- Product visibility
- Customer visibility
- Occlusion level

Generate observations for every video.

---

## Retail Environment Analysis

Identify:

- Number of visible shelves
- Shelf locations
- Customer walking area
- Basket/cart visibility
- Billing counter visibility
- Entrance visibility
- Exit visibility

---

## Behavior Visibility Assessment

For each behavior class:

- Touching
- Turning To Shelf
- Picking And Returning
- Picking And Putting

Determine:

- Whether behavior is visually identifiable
- Whether behavior is partially visible
- Whether behavior is ambiguous

Provide confidence rating:

1-10

---

## Technical Feasibility Study

Assess feasibility of:

### Person Detection

Recommended Model:
YOLO

### Person Tracking

Recommended Model:
ByteTrack

### Zone Detection

Recommended Approach:
ROI Based Zones

### Behavior Recognition

Recommended Approach:
Hybrid Rule-Based + Temporal Classification

---

## Architecture Design

Generate complete architecture diagram.

Required architecture:

Video Input
→ Person Detection
→ Person Tracking
→ Zone Intelligence
→ Behavior Classification
→ Retail Analytics Engine
→ Dashboard
→ AI Business Advisor

---

## Project Structure

Create production-grade folder structure.

Example:

project-root/

backend/
frontend/
models/
analytics/
datasets/
reports/
tests/
configs/
docs/

---

# Output Files Required

dataset_report.md

video_metadata.csv

camera_analysis.md

technical_feasibility.md

project_architecture.md

folder_structure.md

---

# Constraints

- No mock analysis
- Use actual provided videos
- Use actual measurements
- Generate evidence-based observations
- Store reports inside /reports/phase-0

---

# Success Criteria

Phase passes only if:

- All videos analyzed
- Metadata extracted
- Architecture finalized
- Dataset quality validated
- Technical risks identified