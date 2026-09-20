import pytest
from fastapi.testclient import TestClient
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.main import app

client = TestClient(app)

def test_case_creation_retrieval_and_update():
    """6, 7, 8. Test case creation, listing, retrieval, and status updates."""
    # Step 1: Create Case
    new_case_payload = {
        "description": "Clean water pipeline leaking heavily near water tower",
        "category": "Water & Drainage",
        "priority": "HIGH",
        "confidence": 0.95,
        "location": "Subhash Avenue",
        "department": "Water Supply & Sewerage Board",
        "recommended_action": "Isolate supply valve and replace damaged pipe fitting",
        "safety_risk": "Medium water loss",
        "image_url": "https://example.com/leak.jpg"
    }
    
    create_res = client.post("/api/cases", json=new_case_payload)
    assert create_res.status_code == 201
    created_data = create_res.json()
    case_id = created_data["case_id"]
    assert case_id.startswith("CFX-")

    # Step 2: List Cases
    list_res = client.get("/api/cases")
    assert list_res.status_code == 200
    cases_list = list_res.json()
    assert any(c["case_id"] == case_id for c in cases_list)

    # Step 3: Retrieve Specific Case
    get_res = client.get(f"/api/cases/{case_id}")
    assert get_res.status_code == 200
    assert get_res.json()["case_id"] == case_id

    # Step 4: Update Case Status
    update_res = client.patch(f"/api/cases/{case_id}", json={"status": "In Progress"})
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "In Progress"

def test_related_cases_detection():
    """9. Test related / duplicate cases matching endpoint."""
    res = client.post("/api/cases/related", json={
        "description": "Broken streetlight near college gate",
        "category": "Public Lighting",
        "location": "College Gate"
    })
    assert res.status_code == 200
    data = res.json()
    assert "related_cases" in data
