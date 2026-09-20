from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ComplaintAnalysisRequest(BaseModel):
    description: str = Field(..., description="Description of the civic issue reported by the citizen")
    location: str = Field("General Area", description="Physical location or address of the issue")
    category: Optional[str] = Field(None, description="Optional user-provided category")
    image_url: Optional[str] = Field(None, description="Optional photo or evidence URL")

class RelatedCaseInfo(BaseModel):
    case_id: str
    description: str
    similarity_score: float
    status: str

class ComplaintAnalysisResponse(BaseModel):
    issue: str
    category: str
    priority: str  # LOW, MEDIUM, HIGH
    confidence: float
    reason: str
    department: str
    recommended_action: str
    safety_risk: str
    related_cases: List[str] = []
    case_id: Optional[str] = None

class CivicCaseCreate(BaseModel):
    description: str
    category: str
    priority: str
    confidence: float = 0.95
    location: str = "General Area"
    department: str
    recommended_action: str
    safety_risk: str = "Low"
    image_url: Optional[str] = None
    ai_summary: Optional[str] = None

class CivicCaseResponse(BaseModel):
    case_id: str
    description: str
    category: str
    priority: str
    confidence: float
    location: str
    department: str
    recommended_action: str
    safety_risk: str
    status: str  # Reported, AI Analyzed, Assigned, In Progress, Resolved
    created_at: str
    updated_at: str
    related_cases: List[str] = []
    ai_summary: Optional[str] = None
    image_url: Optional[str] = None

class CaseStatusUpdate(BaseModel):
    status: str = Field(..., description="New status: Reported | AI Analyzed | Assigned | In Progress | Resolved")

class RelatedCasesRequest(BaseModel):
    description: str
    category: Optional[str] = None
    location: Optional[str] = None

class SystemStatusResponse(BaseModel):
    status: str
    demo_mode: bool
    strands_active: bool
    total_cases: int
    version: str = "1.0.0"
