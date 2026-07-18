import os
import sys
import time
import subprocess
import httpx
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from backend.core.config import OUTPUTS_DIR

def run_tests():
    print("\n--- Running Pytest ---")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BASE_DIR)
    result = subprocess.run(["pytest", "tests/"], cwd=str(BASE_DIR), env=env, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("Tests failed.")
    return result.returncode == 0

def test_api():
    print("\n--- Testing API Endpoints ---")
    # Start server in background
    server_process = subprocess.Popen(["uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"], cwd=str(BASE_DIR))
    time.sleep(5) # Wait for startup
    
    endpoints = [
        "/health", "/metrics", "/behaviors", "/timeline", "/summary", 
        "/heatmaps", "/zones", "/analytics/summary", "/retail/summary",
        "/advisor/recommendations"
    ]
    
    success = True
    try:
        with httpx.Client(base_url="http://127.0.0.1:8000") as client:
            for endpoint in endpoints:
                resp = client.get(endpoint)
                if resp.status_code == 200:
                    print(f"[PASS] GET {endpoint} - {resp.elapsed.total_seconds():.3f}s")
                else:
                    print(f"[FAIL] GET {endpoint} returned {resp.status_code}")
                    success = False
    except Exception as e:
        print(f"API Test Failed: {e}")
        success = False
    finally:
        server_process.terminate()
        server_process.wait()
        
    return success

def main():
    print("--- RetailVision AI Verification ---")
    test_ok = run_tests()
    api_ok = test_api()
    
    if test_ok and api_ok:
        print("\nAll verifications passed!")
    else:
        print("\nVerification failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
