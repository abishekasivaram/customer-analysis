import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_process_video():
    response = client.post("/process", json={"video_id": "vid_123"})
    assert response.status_code == 200
    assert response.json() == {"message": "Added to queue", "video_id": "vid_123"}

def test_get_status():
    client.post("/process", json={"video_id": "vid_123"})
    response = client.get("/status/vid_123")
    assert response.status_code == 200
    assert response.json() == {"video_id": "vid_123", "status": "Pending"}

def test_get_results():
    response = client.get("/results/vid_123")
    assert response.status_code == 200
    assert "results_url" in response.json()
