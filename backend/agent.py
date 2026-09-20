"""
AWS Strands Agent Engine for CivicFix.
Orchestrates civic complaint analysis, tool invocation, and case creation.
"""

from typing import Dict, Any, List, Optional
import json
import logging

from backend.config import DEMO_MODE, GEMINI_API_KEY
from backend.models import ComplaintAnalysisResponse
from backend.tools import (
    classify_issue,
    assess_priority,
    identify_department,
    detect_related_cases,
    generate_resolution_plan,
    create_civic_case,
    get_case_status,
    generate_case_summary
)

logger = logging.getLogger("civicfix.agent")

# Initialize AWS Strands SDK Agent if available
strands_agent_instance = None
STRANDS_AVAILABLE = False

try:
    from strands import Agent
    strands_tools = [
        classify_issue,
        assess_priority,
        identify_department,
        detect_related_cases,
        generate_resolution_plan,
        create_civic_case,
        get_case_status,
        generate_case_summary
    ]
    strands_agent_instance = Agent(
        system_prompt="""You are CivicFix Agent, an AI civic issue resolution assistant powered by AWS Strands Agents SDK.
Your task is to analyze citizen complaints, classify issues into municipal categories, evaluate priority and safety risks, identify responsible departments, check for related/duplicate cases, and generate actionable resolution plans.""",
        tools=strands_tools
    )
    STRANDS_AVAILABLE = True
    logger.info("AWS Strands Agent initialized successfully.")
except Exception as e:
    logger.warning(f"AWS Strands Agent initialized in fallback mode: {e}")
    STRANDS_AVAILABLE = False


def analyze_complaint(
    description: str,
    location: str = "General Area",
    user_category: Optional[str] = None,
    image_url: Optional[str] = None
) -> ComplaintAnalysisResponse:
    """
    Core Strands Agent workflow executing multi-step reasoning:
    1. Issue Classification (classify_issue tool)
    2. Severity & Priority Assessment (assess_priority tool)
    3. Department Identification (identify_department tool)
    4. Duplicate & Related Issue Detection (detect_related_cases tool)
    5. Action Recommendation (generate_resolution_plan tool)
    """

    # Step 1: Category classification
    if user_category and len(user_category.strip()) > 0:
        category = user_category.strip()
        confidence = 0.98
    else:
        classification = classify_issue(description)
        category = classification["category"]
        confidence = classification["confidence"]

    # Step 2: Priority and safety evaluation
    priority_info = assess_priority(description, category, location)
    priority = priority_info["priority"]
    safety_risk = priority_info["safety_risk"]
    reason = priority_info["reason"]

    # Step 3: Department routing
    department = identify_department(category)

    # Step 4: Duplicate / Related issue matching
    related_cases = detect_related_cases(description, location)

    # Step 5: Recommended Action plan
    action_plan = generate_resolution_plan(category, priority)

    # Extract issue title summary
    words = description.strip().split()
    issue_title = " ".join(words[:6]) if len(words) > 6 else description.strip()
    if len(issue_title) > 60:
        issue_title = issue_title[:57] + "..."

    return ComplaintAnalysisResponse(
        issue=issue_title.capitalize(),
        category=category,
        priority=priority,
        confidence=confidence,
        reason=reason,
        department=department,
        recommended_action=action_plan,
        safety_risk=safety_risk,
        related_cases=related_cases,
        case_id=None
    )
