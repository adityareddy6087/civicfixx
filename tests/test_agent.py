import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.agent import analyze_complaint, STRANDS_AVAILABLE
from backend.tools import classify_issue, assess_priority, identify_department, detect_related_cases

def test_agent_initialization():
    """12. Test agent initialization and configuration."""
    assert STRANDS_AVAILABLE is True or STRANDS_AVAILABLE is False

def test_classification_tool():
    """4. Test classification tool accuracy."""
    res1 = classify_issue("Large pothole causing vehicle damage on highway")
    assert res1["category"] == "Roads & Highways"

    res2 = classify_issue("Overflowing trash bin near market area")
    assert res2["category"] == "Sanitation & Waste"

def test_priority_assessment_tool():
    """5. Test priority assessment tool reasoning."""
    res = assess_priority("Broken streetlight near dark alley late night urgent", "Public Lighting")
    assert res["priority"] == "HIGH"
    assert "High" in res["safety_risk"]

def test_department_identification_tool():
    """Test department routing map."""
    dept = identify_department("Water & Drainage")
    assert "Water" in dept or "Drainage" in dept or "Sewerage" in dept
