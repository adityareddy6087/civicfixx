"""
AWS Strands Agents SDK Tools for CivicFix.
Each tool is decorated with @tool for Strands Agent orchestration.
"""

from typing import Dict, Any, List, Optional
import json

try:
    from strands import tool
except ImportError:
    # Graceful fallback decorator if strands is initializing
    def tool(func):
        return func

from backend.database import (
    find_related_cases, create_case, update_case_status as db_update_status,
    get_case as db_get_case, get_all_cases
)

CATEGORIES = [
    "Public Lighting",
    "Roads & Highways",
    "Sanitation & Waste",
    "Water & Drainage",
    "Pedestrian Safety",
    "Parks & Recreation",
    "Public Infrastructure",
    "Traffic & Mobility",
    "Other Civic Issue"
]

DEPARTMENTS = {
    "Public Lighting": "Public Lighting & Electrical Maintenance Division",
    "Roads & Highways": "Municipal Roads, Pothole Repair & Infrastructure Dept",
    "Sanitation & Waste": "Solid Waste Management & Public Health Department",
    "Water & Drainage": "Water Supply, Pipeline & Sewerage Operations Board",
    "Pedestrian Safety": "Pedestrian Infrastructure & Footpath Safety Cell",
    "Parks & Recreation": "City Horticulture & Public Parks Authority",
    "Public Infrastructure": "Public Works & Structural Maintenance Division",
    "Traffic & Mobility": "Traffic Management & Street Signage Bureau",
    "Other Civic Issue": "General Civic Grievance & Rapid Response Cell"
}

@tool
def classify_issue(description: str) -> Dict[str, Any]:
    """
    Classify a citizen's complaint into a standard civic issue category.
    """
    desc = description.lower()
    if any(w in desc for w in ["light", "dark", "street light", "lamp", "bulb", "electricity", "pole"]):
        cat = "Public Lighting"
    elif any(w in desc for w in ["pothole", "road", "asphalt", "tar", "hole", "street", "crack"]):
        cat = "Roads & Highways"
    elif any(w in desc for w in ["garbage", "trash", "waste", "smell", "dump", "bin", "clean", "odor"]):
        cat = "Sanitation & Waste"
    elif any(w in desc for w in ["water", "leak", "pipe", "drain", "sewage", "flood", "overflow"]):
        cat = "Water & Drainage"
    elif any(w in desc for w in ["footpath", "sidewalk", "paver", "walkway", "pedestrian", "slab", "trip"]):
        cat = "Pedestrian Safety"
    elif any(w in desc for w in ["park", "bench", "tree", "playground", "garden"]):
        cat = "Parks & Recreation"
    elif any(w in desc for w in ["signal", "traffic", "sign", "zebra"]):
        cat = "Traffic & Mobility"
    else:
        cat = "Public Infrastructure"

    return {
        "category": cat,
        "confidence": 0.95
    }

@tool
def assess_priority(description: str, category: str, location: str = "") -> Dict[str, Any]:
    """
    Assess priority (HIGH, MEDIUM, LOW), confidence level, safety risk, and reasoning.
    """
    desc = description.lower()
    high_keywords = ["danger", "urgent", "broken streetlight", "night", "accident", "school", "hospital", "college", "main road", "leak", "deep pothole", "child", "hazard", "overflow", "severe"]
    medium_keywords = ["garbage", "footpath", "odor", "smell", "inconvenience", "slowdown"]

    matched_high = [w for w in high_keywords if w in desc]
    matched_medium = [w for w in medium_keywords if w in desc]

    if matched_high or category in ["Public Lighting", "Roads & Highways", "Water & Drainage"]:
        priority = "HIGH"
        safety_risk = "High — potential hazard to citizens, pedestrians, or public safety"
        reason = f"High severity identified due to critical infrastructure impact ({category}) and risk indicators: {', '.join(matched_high) if matched_high else 'active infrastructure fault'}."
    elif matched_medium or category in ["Sanitation & Waste", "Pedestrian Safety"]:
        priority = "MEDIUM"
        safety_risk = "Medium — public health or convenience impact requiring prompt attention"
        reason = f"Moderate severity issue affecting daily public use and municipal cleanliness in {location}."
    else:
        priority = "LOW"
        safety_risk = "Low — routine maintenance or non-urgent request"
        reason = "Non-emergency civic maintenance report."

    return {
        "priority": priority,
        "confidence": 0.94,
        "safety_risk": safety_risk,
        "reason": reason
    }

@tool
def identify_department(category: str) -> str:
    """
    Identify the responsible municipal department for a given category.
    """
    return DEPARTMENTS.get(category, "General Civic Grievance & Rapid Response Cell")

@tool
def detect_related_cases(description: str, location: str = "") -> List[str]:
    """
    Check database for duplicate or related civic cases based on description and location.
    """
    matches = find_related_cases(description=description, location=location)
    return [m["case_id"] for m in matches]

@tool
def create_civic_case(issue_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new structured civic case in the database.
    """
    return create_case(issue_data)

@tool
def update_case_status(case_id: str, new_status: str) -> Optional[Dict[str, Any]]:
    """
    Update the operational status of an existing civic case.
    """
    return db_update_status(case_id, new_status)

@tool
def get_case_status(case_id: str) -> Optional[Dict[str, Any]]:
    """
    Get current status and details of a specific civic case.
    """
    return db_get_case(case_id)

@tool
def generate_case_summary(case_id: str) -> str:
    """
    Generate an executive AI summary for a civic case.
    """
    case = db_get_case(case_id)
    if not case:
        return f"Case {case_id} not found."
    return f"Case {case['case_id']} ({case['category']} - {case['priority']} Priority): {case['description']}. Assigned to {case['department']}. Current Status: {case['status']}."

@tool
def generate_resolution_plan(category: str, priority: str) -> str:
    """
    Generate recommended action and field technician dispatch plan.
    """
    if category == "Public Lighting":
        return "Dispatch electrical line crew with bucket truck to inspect wiring and replace luminaire fixture."
    elif category == "Roads & Highways":
        return "Deploy rapid road repair squad to lay asphalt cold-mix patch and place traffic safety cones."
    elif category == "Sanitation & Waste":
        return "Dispatch waste compactor truck to clear container overflow and sanitize surrounding area."
    elif category == "Water & Drainage":
        return "Shut off local supply valve, locate pipe rupture, and execute emergency line seal."
    elif category == "Pedestrian Safety":
        return "Dispatch public works team to relay broken concrete footpath slabs and restore pedestrian safety."
    else:
        return "Assign municipal officer for field inspection and resource scheduling within 24 hours."
