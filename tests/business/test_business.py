import pytest
import os
import json
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.business.customer_segmentation import CustomerSegmentationEngine

client = TestClient(app)

def test_api_retail_summary():
    response = client.get("/retail/summary")
    assert response.status_code == 200
    assert "total_customers" in response.json() or "status" in response.json()

def test_api_dashboard_data():
    response = client.get("/dashboard/data")
    assert response.status_code == 200
    assert "summary" in response.json() or "status" in response.json()

def test_customer_segmentation_logic():
    engine = CustomerSegmentationEngine()
    
    j1 = {"journey_duration": 15, "number_of_stops": 0}
    assert engine.classify(j1) == "Quick Visitor"
    
    j2 = {"journey_duration": 400, "number_of_stops": 4}
    assert engine.classify(j2) == "Explorer"
    
    j3 = {"journey_duration": 650, "number_of_stops": 2}
    assert engine.classify(j3) == "Long Stay Customer"
    
    j4 = {"journey_duration": 100, "number_of_stops": 0}
    assert engine.classify(j4) == "Window Shopper"
    
    j5 = {"journey_duration": 150, "number_of_stops": 2}
    assert engine.classify(j5) == "Focused Shopper"
