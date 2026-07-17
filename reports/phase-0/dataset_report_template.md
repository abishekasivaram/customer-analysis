# Enhanced Dataset Report Template
## RetailVision AI

*(Note: This is a template. It must be populated once the actual dataset videos are provided in the `/datasets` folder.)*

---

## 1. Dataset Overview

- **Total number of videos:** [e.g., 10]
- **Total dataset duration:** [e.g., 05:30:15]
- **Primary Use Case:** Retail Behavior Analysis

---

## 2. Video Metadata

| Video Name | Resolution | FPS | Frame Count | Duration | Codec |
|---|---|---|---|---|---|
| `[filename.mp4]` | `[1920x1080]` | `[30]` | `[18000]` | `[00:10:00]` | `[H.264]` |
| ... | ... | ... | ... | ... | ... |

*(A complete CSV version of this table will be generated as `video_metadata.csv`)*

---

## 3. Camera & Environment Analysis

For each video, log the environmental factors that will impact AI inference:

### Video: `[filename.mp4]`
- **Camera Position:** [e.g., High-angle corner mount / Eye-level shelf mount]
- **Lighting Quality:** [e.g., Bright fluorescent / Dim / High Glare]
- **Shelf Visibility:** [e.g., Full aisle visible / Only bottom 3 shelves visible]
- **Customer Walking Area:** [e.g., Unobstructed / Narrow aisle]
- **Remarks:** [e.g., Camera vibrates occasionally when heavy carts pass.]

---

## 4. Behavior Visibility Assessment

Assess the dataset for the presence and clarity of target behaviors.

| Behaviour Type | Count Found | Visibility Level | Confidence Rating (1-10) | Notes |
|---|---|---|---|---|
| **Touching** | `[Count]` | `[Clear / Partial / Ambiguous]` | `[1-10]` | `[e.g., Hands often obscured by body]` |
| **Turning To Shelf** | `[Count]` | `[Clear / Partial / Ambiguous]` | `[1-10]` | `[e.g., Highly visible]` |
| **Picking And Returning** | `[Count]` | `[Clear / Partial / Ambiguous]` | `[1-10]` | `[e.g., Requires close tracking of hand]` |
| **Picking And Putting** | `[Count]` | `[Clear / Partial / Ambiguous]` | `[1-10]` | `[e.g., Cart often blocks view of putting]` |

---

## 5. Dataset Quality Conclusion & Risks
*Provide a summary of the dataset's quality. Identify any severe occlusion levels, lighting issues, or lack of specific behaviors that might require dataset augmentation or model fine-tuning.*
