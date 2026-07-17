# Risk Assessment
## RetailVision AI

---

## 1. Computer Vision Risks

### 1.1. Occlusion
- **Risk:** Customers blocking each other, or shelves blocking the view of a customer's hands, leading to broken tracks or missed behavior classifications.
- **Mitigation Strategy:** Utilize ByteTrack, which is robust against short-term occlusions. For severe occlusions, rely on temporal heuristics (e.g., if a customer disappears behind a shelf and reappears, infer their behavior based on dwell time).

### 1.2. Multiple Customers (Crowding)
- **Risk:** High density of shoppers causing bounding boxes to overlap heavily, confusing the tracking engine.
- **Mitigation Strategy:** Tune the Non-Maximum Suppression (NMS) threshold. Define "maximum capacity" thresholds for ROI zones where analysis reliability drops and flag these segments in the analytics.

### 1.3. Poor Lighting & Glare
- **Risk:** Low contrast or glare from store windows rendering products or hands invisible.
- **Mitigation Strategy:** Implement a pre-processing step using OpenCV to normalize lighting (e.g., Histogram Equalization) before passing frames to YOLO. Recommend hardware (camera) adjustments to clients if software fixes are insufficient.

### 1.4. Motion Blur
- **Risk:** Fast-moving customers causing blurry frames, leading to failed person detections.
- **Mitigation Strategy:** Ensure videos are captured at a minimum of 15 FPS, preferably 30 FPS. If blur is detected, rely on adjacent, clearer frames for tracking interpolation.

### 1.5. Shelf Blocking
- **Risk:** High shelves physically preventing the camera from seeing the aisle floor, cutting off the lower half of bounding boxes.
- **Mitigation Strategy:** Train/fine-tune the detection model to recognize partial bodies (head and shoulders) robustly rather than requiring full-body visibility.

### 1.6. Camera Movement
- **Risk:** If a fixed camera is bumped or vibrates, predefined ROI zone polygons will no longer align with the physical shelves.
- **Mitigation Strategy:** Implement a background subtraction or feature-matching check at the start of video processing to detect camera shift. If a shift is detected beyond a threshold, halt processing and alert the user to redefine zones.

---

## 2. Classification Risks

### 2.1. False Positives
- **Risk:** The system incorrectly classifies a "Touching" event as a "Picking and Putting" event (e.g., customer rests hand on shelf).
- **Mitigation Strategy:** Implement strict temporal thresholds (e.g., hand must intersect the product zone for >1.5 seconds) to filter out transient touches.

### 2.2. False Negatives
- **Risk:** The system entirely misses a picking event due to a fast motion or partial occlusion.
- **Mitigation Strategy:** Lower the confidence threshold for behavior classification triggers, prioritizing recall over precision in specific high-value zones.
