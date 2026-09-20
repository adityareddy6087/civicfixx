import sqlite3
import json
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from backend.config import DATABASE_PATH

_db_initialized = False

def get_db_connection():
    global _db_initialized
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    if not _db_initialized:
        _db_initialized = True
        init_db_schema(conn)
    return conn

def init_db_schema(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS civic_cases (
            case_id TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            confidence REAL NOT NULL,
            location TEXT NOT NULL,
            department TEXT NOT NULL,
            recommended_action TEXT NOT NULL,
            safety_risk TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            related_cases TEXT,
            ai_summary TEXT,
            image_url TEXT
        )
    """)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM civic_cases")
    count = cursor.fetchone()[0]
    if count == 0:
        seed_data(cursor)
        conn.commit()

def init_db():
    conn = get_db_connection()
    conn.close()

def seed_data(cursor):
    now = datetime.now(timezone.utc).isoformat()
    seeds = [
        {
            "case_id": "CFX-1001",
            "description": "Broken streetlight near the college gate causing poor visibility for students walking at night.",
            "category": "Public Lighting",
            "priority": "HIGH",
            "confidence": 0.94,
            "location": "Main College Road, Gate 2",
            "department": "Public Lighting / Electrical Maintenance",
            "recommended_action": "Deploy field unit to replace damaged bulb and inspect line wiring immediately.",
            "safety_risk": "High — night safety risk for students & pedestrians",
            "status": "In Progress",
            "created_at": now,
            "updated_at": now,
            "related_cases": json.dumps(["CFX-0982"]),
            "ai_summary": "P1 safety report for non-functional illumination near high-footfall educational facility.",
            "image_url": "https://images.unsplash.com/photo-1517649763962-0c623266010b?w=600&auto=format&fit=crop"
        },
        {
            "case_id": "CFX-1002",
            "description": "Deep dangerous pothole near the central bus stop damaging tires and causing traffic slowdown.",
            "category": "Roads & Highways",
            "priority": "HIGH",
            "confidence": 0.96,
            "location": "Central Bus Terminus, Lane 4",
            "department": "Municipal Roads & Infrastructure Dept",
            "recommended_action": "Schedule emergency asphalt patch repair and place hazard warning cones.",
            "safety_risk": "High — severe risk of vehicle accidents and motorcycle crashes",
            "status": "Assigned",
            "created_at": now,
            "updated_at": now,
            "related_cases": json.dumps(["CFX-0975", "CFX-0991"]),
            "ai_summary": "Severe asphalt depression posing immediate hazard to public transit and commuters.",
            "image_url": "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop"
        },
        {
            "case_id": "CFX-1003",
            "description": "Overflowing garbage bin near the local vegetable market causing severe odor and health hazard.",
            "category": "Sanitation & Waste",
            "priority": "MEDIUM",
            "confidence": 0.92,
            "location": "Sector 5 Commercial Market",
            "department": "Solid Waste Management Department",
            "recommended_action": "Dispatch compactor truck for clearance and disinfect container area.",
            "safety_risk": "Medium — sanitation and public health concern",
            "status": "Reported",
            "created_at": now,
            "updated_at": now,
            "related_cases": json.dumps([]),
            "ai_summary": "Uncollected municipal waste accumulating near commercial food stalls.",
            "image_url": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=600&auto=format&fit=crop"
        },
        {
            "case_id": "CFX-1004",
            "description": "Clean water pipe leaking on main road wasting hundreds of liters of water per hour.",
            "category": "Water & Drainage",
            "priority": "HIGH",
            "confidence": 0.95,
            "location": "Subhash Avenue, near Water Tank",
            "department": "Water Supply & Sewerage Board",
            "recommended_action": "Isolate pipeline segment and repair ruptured joint.",
            "safety_risk": "Medium — water wastage and potential road erosion",
            "status": "In Progress",
            "created_at": now,
            "updated_at": now,
            "related_cases": json.dumps([]),
            "ai_summary": "Pressurized potable water main leak creating roadway flooding.",
            "image_url": "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=600&auto=format&fit=crop"
        },
        {
            "case_id": "CFX-1005",
            "description": "Broken concrete footpath slab near primary school causing children to trip.",
            "category": "Pedestrian Safety",
            "priority": "MEDIUM",
            "confidence": 0.90,
            "location": "Greenwood School Lane",
            "department": "Civic Works & Pedestrian Safety",
            "recommended_action": "Replace fractured concrete pavers and level walk surface.",
            "safety_risk": "Medium — tripping hazard for school children and elderly",
            "status": "Resolved",
            "created_at": now,
            "updated_at": now,
            "related_cases": json.dumps([]),
            "ai_summary": "Pedestrian pathway slab fracture successfully repaired.",
            "image_url": None
        }
    ]
    for s in seeds:
        cursor.execute("""
            INSERT INTO civic_cases (
                case_id, description, category, priority, confidence, location,
                department, recommended_action, safety_risk, status, created_at,
                updated_at, related_cases, ai_summary, image_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s["case_id"], s["description"], s["category"], s["priority"], s["confidence"],
            s["location"], s["department"], s["recommended_action"], s["safety_risk"],
            s["status"], s["created_at"], s["updated_at"], s["related_cases"],
            s["ai_summary"], s["image_url"]
        ))

def create_case(case_data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    
    # Generate sequential or UUID case ID
    case_id = case_data.get("case_id")
    if not case_id:
        cursor.execute("SELECT COUNT(*) FROM civic_cases")
        cnt = cursor.fetchone()[0] + 1006
        case_id = f"CFX-{cnt}"

    related = json.dumps(case_data.get("related_cases", []))

    cursor.execute("""
        INSERT INTO civic_cases (
            case_id, description, category, priority, confidence, location,
            department, recommended_action, safety_risk, status, created_at,
            updated_at, related_cases, ai_summary, image_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id,
        case_data["description"],
        case_data["category"],
        case_data["priority"],
        case_data.get("confidence", 0.95),
        case_data.get("location", "General Area"),
        case_data["department"],
        case_data["recommended_action"],
        case_data.get("safety_risk", "Low"),
        case_data.get("status", "Reported"),
        now,
        now,
        related,
        case_data.get("ai_summary", f"Case created for {case_data['category']} issue."),
        case_data.get("image_url")
    ))
    conn.commit()
    conn.close()
    return get_case(case_id)

def get_case(case_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM civic_cases WHERE case_id = ?", (case_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["related_cases"] = json.loads(d["related_cases"]) if d["related_cases"] else []
        return d
    return None

def get_all_cases(category: Optional[str] = None, status: Optional[str] = None, priority: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM civic_cases WHERE 1=1"
    params = []

    if category:
        query += " AND category LIKE ?"
        params.append(f"%{category}%")
    if status:
        query += " AND status = ?"
        params.append(status)
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    if search:
        query += " AND (description LIKE ? OR location LIKE ? OR case_id LIKE ?)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")
        params.append(f"%{search}%")

    query += " ORDER BY created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        d = dict(r)
        d["related_cases"] = json.loads(d["related_cases"]) if d["related_cases"] else []
        results.append(d)
    return results

def update_case_status(case_id: str, new_status: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
        UPDATE civic_cases
        SET status = ?, updated_at = ?
        WHERE case_id = ?
    """, (new_status, now, case_id))
    conn.commit()
    conn.close()
    return get_case(case_id)

def find_related_cases(description: str, category: Optional[str] = None, location: Optional[str] = None) -> List[Dict[str, Any]]:
    cases = get_all_cases(category=category)
    if not cases:
        cases = get_all_cases()
    
    desc_words = set(description.lower().split())
    matches = []

    for c in cases:
        c_words = set(c["description"].lower().split())
        common = desc_words.intersection(c_words)
        if common:
            similarity = len(common) / max(len(desc_words), 1)
            if similarity > 0.15 or (c["category"].lower() in description.lower()):
                matches.append({
                    "case_id": c["case_id"],
                    "description": c["description"],
                    "category": c["category"],
                    "similarity_score": round(similarity, 2),
                    "status": c["status"],
                    "location": c["location"]
                })

    matches.sort(key=lambda x: x["similarity_score"], reverse=True)
    return matches[:3]
