# Dataset Analysis Report

## Dataset Summary
- **Total Videos Discovered:** 40
- **Valid Videos (Readable & Decodable):** 40
- **Invalid/Corrupt Videos:** 0
- **Total Dataset Frame Count:** 22,263 frames
- **Total Dataset Duration:** 1,471.13 seconds (~24.5 minutes)

## Technical Specifications
Based on the `metadata.csv` extracted programmatically by the Phase 1 metadata service:
- **Resolution:** 100% of videos are native 4K UHD (`3840x2160`).
- **Aspect Ratio:** All videos maintain a standard `1.78` (16:9) aspect ratio.
- **Framerate:** Varies slightly around ~15 FPS (ranging from 14.98 to 15.15 FPS).
- **Video Codec:** `hevc` (High Efficiency Video Coding / H.265).
- **Average Duration:** ~36.78 seconds per video.
- **Average Frames per Video:** ~556 frames.

## Dataset Highlights
The dataset provides high-fidelity top-down and angled perspectives of retail store customers. The 4K resolution allows the AI to track small objects (like hands or products) with high accuracy. 
The 15 FPS framerate acts as a natural `vid_stride` equivalent, preventing the pipeline from over-saturating on duplicate frames during high-activity segments while maintaining tracking fidelity in ByteTrack.

## Analysis Conclusion
The provided HackZen dataset is fully operational and decodable by the Phase 1 pipeline using `OpenCV-Python`. No data fabrication or normalization was required, as every asset passed validation identically.
