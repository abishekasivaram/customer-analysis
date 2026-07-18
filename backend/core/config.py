import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
OUTPUTS_DIR = BASE_DIR / "outputs"
MODELS_DIR = BASE_DIR / "models" / "person_detection"

# Ensure output dirs exist
os.makedirs(OUTPUTS_DIR / "detection" / "videos", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "detection" / "json", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "detection" / "csv", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "detection" / "reports", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "logs", exist_ok=True)

# Phase 2 & 3 Directories
os.makedirs(OUTPUTS_DIR / "behavior" / "json", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "behavior" / "csv", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "behavior" / "timeline", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "behavior" / "videos", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "analytics", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "analytics" / "heatmaps", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "analytics" / "charts", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "business", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "business" / "graphs", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "advisor", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "advisor" / "reports", exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

CONFIDENCE_THRESHOLD = 0.25
MODEL_NAME = "yolov8m.pt"
MODEL_PATH = MODELS_DIR / MODEL_NAME
