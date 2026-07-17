import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
OUTPUTS_DIR = BASE_DIR / "outputs"
MODELS_DIR = BASE_DIR / "models" / "person_detection"

# Ensure output dirs exist
os.makedirs(OUTPUTS_DIR / "detection" / "videos", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "detection" / "json", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "detection" / "csv", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "detection" / "reports", exist_ok=True)
os.makedirs(OUTPUTS_DIR / "logs", exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

CONFIDENCE_THRESHOLD = 0.5
MODEL_NAME = "yolov8n.pt"
MODEL_PATH = MODELS_DIR / MODEL_NAME
