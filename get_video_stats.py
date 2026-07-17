import os
import cv2
import json

directory = 'datasets'
stats = []
for filename in os.listdir(directory):
    if filename.endswith('.mp4'):
        filepath = os.path.join(directory, filename)
        cap = cv2.VideoCapture(filepath)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0
        file_size = os.path.getsize(filepath)
        
        # Getting Codec (FourCC)
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
        
        stats.append({
            'filename': filename,
            'resolution': f"{width}x{height}",
            'fps': round(fps, 2),
            'frame_count': frame_count,
            'duration': round(duration, 2),
            'file_size_mb': round(file_size / (1024 * 1024), 2),
            'codec': codec
        })

print(json.dumps(stats, indent=2))
