# Detection JSON Schema Documentation

## File Structure Overview
The JSON artifacts are exported as a flat JSON array of objects. Each object represents a single positive detection (or tracked entity) within a specific frame. The structure makes it trivial to deserialize into Pandas DataFrames or JSON document stores (like MongoDB).

## JSON Payload Schema

### Required Fields
- `frame` (integer): The 1-indexed frame number within the source video where the detection occurred.
- `customer_id` (integer | null): The unique tracking integer assigned by ByteTrack. If tracking fails or is untracked, this defaults to `null`.
- `bbox` (array of floats): The bounding box array formatted as `[x1, y1, x2, y2]`.
- `confidence` (float): The probabilistic confidence score of the YOLO detection.
- `class` (string): The string label of the detected object (always `"person"` for Phase 1).

### Optional Fields
- None. (All fields are explicitly rendered for every detection to ensure schema consistency, though `customer_id` may be `null`).

### Data Types & Example Values
```json
[
  {
    "frame": 1,
    "customer_id": 1,
    "bbox": [1520.4, 820.1, 1680.5, 1200.7],
    "confidence": 0.8845,
    "class": "person"
  }
]
```

## Explanations
- **Bounding Box Coordinate System:** Bounding boxes are stored as exact pixel coordinates mapped to the native video resolution (3840x2160). The format `[x1, y1, x2, y2]` corresponds to `[Top-Left X, Top-Left Y, Bottom-Right X, Bottom-Right Y]`. Origin `(0,0)` is the top-left corner of the video frame.
- **Confidence Meaning:** A float between `0.0` and `1.0` reflecting the neural network's certainty that the bounded pixels contain a "person". Thresholded at `>= 0.50`.
- **Track ID Meaning:** A persistent integer assigned by the ByteTrack algorithm. If a person is assigned `customer_id: 1` in frame 1, the tracker will attempt to assign `customer_id: 1` to that same person in frame 2 based on LAP spatial intersection over union (IOU).
- **Timestamp Format:** The current Phase 1 outputs do not explicitly store timestamps in the array to minimize payload size. Timestamps can be derived dynamically by dividing the `frame` field by the video's FPS (stored in `metadata.csv`).
