import pytest
from fastapi.testclient import TestClient
import os
import sys

# Ensure backend import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.main import app

client = TestClient(app)

def test_health_check_endpoint():
    """1. Test health/homepage endpoint."""
    response = client.get("/")
    assert response.status_code == 200

def test_system_status_endpoint():
    """2. Test system status endpoint."""
    response = client.get("/api/system/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "demo_mode" in data
    assert "strands_active" in data
    assert data["total_cases"] >= 0

def test_complaint_analysis_endpoint():
    """3. Test complaint analysis endpoint using AWS Strands Agent logic."""
    payload = {
        "description": "There is a broken streetlight near the college gate and students are walking there at night.",
        "location": "College Gate 2",
        "category": None
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Public Lighting"
    assert data["priority"] == "HIGH"
    assert "Electrical" in data["department"] or "Lighting" in data["department"]
    assert "recommended_action" in data

def test_invalid_complaint_input():
    """10. Test invalid empty input handling."""
    response = client.post("/api/analyze", json={"description": ""})
    assert response.status_code == 400
