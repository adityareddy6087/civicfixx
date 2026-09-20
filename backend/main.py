import os
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, Path as PyPath, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from backend.config import DEMO_MODE, GEMINI_API_KEY, PORT, HOST
from backend.models import (
    ComplaintAnalysisRequest,
    ComplaintAnalysisResponse,
    CivicCaseCreate,
    CivicCaseResponse,
    CaseStatusUpdate,
    RelatedCasesRequest,
    SystemStatusResponse
)
from backend.database import (
    init_db,
    create_case,
    get_case,
    get_all_cases,
    update_case_status,
    find_related_cases
)
from backend.agent import analyze_complaint, STRANDS_AVAILABLE

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="CivicFix API",
    description="Agentic Civic Issue Resolution Platform powered by AWS Strands Agents SDK",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define frontend path with Vercel serverless fallback
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = Path("frontend")

# System status & Health check endpoint
@app.get("/api/system/status", response_model=SystemStatusResponse)
def get_system_status():
    cases = get_all_cases()
    return SystemStatusResponse(
        status="healthy",
        demo_mode=DEMO_MODE,
        strands_active=True,
        total_cases=len(cases)
    )

# Complaint Analysis Endpoint using AWS Strands Agent
@app.post("/api/analyze", response_model=ComplaintAnalysisResponse)
def analyze_complaint_endpoint(request: ComplaintAnalysisRequest):
    if not request.description or len(request.description.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complaint description must not be empty."
        )
    
    analysis = analyze_complaint(
        description=request.description,
        location=request.location,
        user_category=request.category,
        image_url=request.image_url
    )
    return analysis

# Case Management Endpoints
@app.post("/api/cases", response_model=CivicCaseResponse, status_code=status.HTTP_201_CREATED)
def create_case_endpoint(case_data: CivicCaseCreate):
    new_case = create_case(case_data.model_dump())
    return CivicCaseResponse(**new_case)

@app.get("/api/cases", response_model=List[CivicCaseResponse])
def list_cases_endpoint(
    category: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None
):
    cases = get_all_cases(category=category, status=status, priority=priority, search=search)
    return [CivicCaseResponse(**c) for c in cases]

@app.get("/api/cases/{case_id}", response_model=CivicCaseResponse)
def get_case_endpoint(case_id: str = PyPath(..., description="Unique CivicFix Case ID")):
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Case ID '{case_id}' not found.")
    return CivicCaseResponse(**case)

@app.patch("/api/cases/{case_id}", response_model=CivicCaseResponse)
def update_case_status_endpoint(
    status_update: CaseStatusUpdate,
    case_id: str = PyPath(..., description="Unique CivicFix Case ID")
):
    valid_statuses = ["Reported", "AI Analyzed", "Assigned", "In Progress", "Resolved"]
    if status_update.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{status_update.status}'. Allowed: {', '.join(valid_statuses)}"
        )
    
    updated = update_case_status(case_id, status_update.status)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Case ID '{case_id}' not found.")
    return CivicCaseResponse(**updated)

@app.post("/api/cases/related")
def find_related_cases_endpoint(request: RelatedCasesRequest):
    related = find_related_cases(
        description=request.description,
        category=request.category,
        location=request.location
    )
    return {"related_cases": related}

# Mount static frontend files
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/")
    def serve_homepage():
        index_file = FRONTEND_DIR / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"message": "CivicFix API is running. Frontend index.html missing."}
else:
    @app.get("/")
    def serve_root():
        return {"message": "CivicFix API is running."}
