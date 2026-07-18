import os
import sys
from pathlib import Path

# Add project root to python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from backend.core.config import DATASETS_DIR, OUTPUTS_DIR, MODELS_DIR
import backend.run_pipeline as phase1
import backend.run_phase2 as phase2
import backend.run_phase3 as phase3
import backend.run_phase4 as phase4

def main():
    print("--- RetailVision AI Runtime Orchestrator ---")
    
    # 1. Validate Environment & Directories
    print("Validating directories...")
    if not DATASETS_DIR.exists():
        print(f"Error: {DATASETS_DIR} does not exist.")
        sys.exit(1)
        
    print("Directory structure is valid.")
    
    # 2. Execute Phase 1
    print("\n--- Running Phase 1 (Detection) ---")
    try:
        phase1.run()
    except Exception as e:
        print(f"Phase 1 Failed: {e}")
        sys.exit(1)
        
    # 3. Execute Phase 2
    print("\n--- Running Phase 2 (Behavior) ---")
    try:
        phase2.run_phase2()
    except Exception as e:
        print(f"Phase 2 Failed: {e}")
        sys.exit(1)
        
    # 4. Execute Phase 3
    print("\n--- Running Phase 3 (Analytics) ---")
    try:
        phase3.run()
    except Exception as e:
        print(f"Phase 3 Failed: {e}")
        sys.exit(1)
        
    # 5. Execute Phase 4
    print("\n--- Running Phase 4 (Advisor) ---")
    try:
        phase4.run()
    except Exception as e:
        print(f"Phase 4 Failed: {e}")
        sys.exit(1)
        
    print("\n--- All Phases Completed Successfully! ---")
    
if __name__ == "__main__":
    main()
