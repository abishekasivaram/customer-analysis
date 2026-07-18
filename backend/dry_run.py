import os
import sys
import traceback
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from backend.services.discovery import discover_videos
from backend.services.validation import validate_video
from backend.services.metadata import extract_metadata
from backend.services.engine import initialize_model, process_video

import backend.run_phase2 as phase2
import backend.run_phase3 as phase3
import backend.run_phase4 as phase4

def main():
    print("--- RetailVision AI DRY RUN ---")
    
    videos = discover_videos()
    if not videos:
        print("No videos found in datasets/")
        return
        
    target_video = videos[0]
    print(f"Selected sample video for Dry Run: {target_video['filename']}")
    
    is_valid, _ = validate_video(target_video)
    if not is_valid:
        print("Video validation failed.")
        return
        
    extract_metadata([target_video])
    
    try:
        print("\n--- PHASE 1: Detection ---")
        base_name = os.path.splitext(target_video['filename'])[0]
        json_path = os.path.join(BASE_DIR, "outputs", "detection", "json", f"{base_name}.json")
        if os.path.exists(json_path):
            print("Phase 1 output already exists. Skipping detection to save time.")
        else:
            model = initialize_model()
            process_video(target_video, model)
        print("Phase 1 completed.")
    except Exception as e:
        print(f"Phase 1 Failed: {e}")
        traceback.print_exc()
        sys.exit(1)
        
    try:
        print("\n--- PHASE 2: Behavior ---")
        phase2.run_phase2()
        print("Phase 2 completed.")
    except Exception as e:
        print(f"Phase 2 Failed: {e}")
        traceback.print_exc()
        sys.exit(1)
        
    try:
        print("\n--- PHASE 3: Analytics ---")
        phase3.run()
        print("Phase 3 completed.")
    except Exception as e:
        print(f"Phase 3 Failed: {e}")
        traceback.print_exc()
        sys.exit(1)
        
    try:
        print("\n--- PHASE 4: Advisor ---")
        phase4.run()
        print("Phase 4 completed.")
    except Exception as e:
        print(f"Phase 4 Failed: {e}")
        traceback.print_exc()
        sys.exit(1)

    print("\n--- DRY RUN SUCCESSFUL ---")

if __name__ == "__main__":
    main()
