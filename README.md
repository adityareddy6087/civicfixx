# CivicFix

> **From civic complaints to real action.**

[![Live Demo](https://img.shields.io/badge/Live_Demo-HTTPS_Active-brightgreen?style=for-the-badge&logo=fastapi)](https://e33d9568a03503c5-103-47-124-98.serveousercontent.com/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/adityareddy6087/civicfixx)
[![AWS Strands Agents SDK](https://img.shields.io/badge/AWS_Strands-Agents_SDK-ff9900?style=for-the-badge&logo=amazonaws)](https://strandsagents.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)](https://python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

CivicFix is an agentic civic issue resolution platform. Most municipal complaint portals merely collect user feedback into unstructured queues. CivicFix uses autonomous AI agents to transform raw complaints into structured, categorized, prioritized, and department-routed civic cases with actionable field response plans.

---

## 🚀 AWS Strands Agents SDK Integration

> **AWS Strands Agents SDK is the core agent orchestration layer of CivicFix.**

CivicFix uses the **AWS Strands Agents SDK** (`strands-agents`) to manage agent reasoning, tool selection, multi-step execution pipelines, and structured decision-making:

- **Agent Orchestration**: Strands coordinates multi-step reasoning cycles to analyze citizen reports.
- **Tool Suite**: Dedicated `@tool` functions (`classify_issue`, `assess_priority`, `identify_department`, `detect_related_cases`, `create_civic_case`, `generate_resolution_plan`).
- **Multi-Step Workflows**: Chaining tool execution dynamically based on issue complexity.
- **Extensibility**: Clean abstraction layer supporting Bedrock, LiteLLM, Gemini, and local deterministic fallback modes (`DEMO_MODE=true`).

---

## 🏛️ System Architecture

```
Citizen Report
      │
      ▼
Web Operations Dashboard (HTML5 / Vanilla CSS / JS)
      │
      ▼
FastAPI REST API (/api/analyze & /api/cases)
      │
      ▼
AWS Strands Agent (Multi-Step Reasoning Engine)
      │
      ├──> @tool classify_issue()
      ├──> @tool assess_priority()
      ├──> @tool identify_department()
      ├──> @tool detect_related_cases()
      ├──> @tool generate_resolution_plan()
      └──> @tool create_civic_case()
      │
      ▼
Civic Case Engine (SQLite Database)
      │
      ▼
Operations Dashboard & Real-Time Case Tracker
```

---

## ✨ Key Agentic Features

1. **Issue Understanding**: Natural language parsing of citizen complaints.
2. **Issue Classification**: Automatic taxonomy mapping (Public Lighting, Roads, Sanitation, Water, Pedestrian Safety).
3. **Severity & Priority Assessment**: Risk-weighted priority assignment (HIGH, MEDIUM, LOW).
4. **Safety Risk Escalation**: Automatic flagging of night-time hazards near schools, hospitals, or high-traffic zones.
5. **Department Routing**: Intelligent mapping to responsible municipal authorities.
6. **Related / Duplicate Issue Detection**: AI-assisted matching linking multiple citizen reports to a single root issue.
7. **Action Recommendation**: Field crew dispatch & repair protocol generation.
8. **Civic Case Creation**: Immutable structured case generation with unique ID tracking (`CFX-XXXX`).
9. **Status Lifecycle Tracking**: Status timeline transition (`Reported` → `AI Analyzed` → `Assigned` → `In Progress` → `Resolved`).
10. **Executive AI Case Summaries**: Concise summaries generated for municipal officers.
11. **One-Click Demo Presets**: Pre-configured hackathon test scenarios.
12. **Operations Dashboard**: Stat metrics, filtering, and real-time status management.

---

## 🛠️ Tech Stack

- **Core Framework**: Python 3.11+
- **Agent Orchestration**: AWS Strands Agents SDK (`strands-agents`)
- **Backend API**: FastAPI, Uvicorn, Pydantic v2
- **Database**: SQLite
- **Frontend**: Responsive HTML5, Vanilla CSS3 (Dark Glassmorphism UI), JavaScript ES6+
- **Testing**: Pytest, HTTPX

---

## ⚡ Quickstart & Installation

### 1. Clone & Navigate
```bash
git clone https://github.com/shashankr335-wq/civicfixx.git
cd civicfixx
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Default configuration runs in `DEMO_MODE=true` (zero API keys or AWS credentials required).

To enable live LLM reasoning, add your Gemini API Key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
DEMO_MODE=false
```

### 4. Run Application
```bash
python run.py
```
Open your browser at `http://localhost:8000`.

---

## 🧪 Automated Testing

Run the full automated test suite using `pytest`:

```bash
python -m pytest tests/ -v
```

The test suite validates:
- System health & API status (`GET /`, `GET /api/system/status`)
- Complaint analysis workflow (`POST /api/analyze`)
- Strands tool accuracy & agent execution
- Case creation, listing, retrieval, and status updates (`/api/cases`)
- Related case / duplicate detection logic
- Error handling & edge cases

---

## 📦 Production Deployment

CivicFix is containerized and deployment-ready via `Dockerfile` and `Procfile`.

### Docker
```bash
docker build -t civicfix .
docker run -p 8000:8000 civicfix
```

### Cloud Platforms (Render / Railway / Vercel / Hugging Face)
CivicFix automatically reads the `$PORT` environment variable supplied by host platforms:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

---

## 🎯 Hackathon Pitch & Presentation Assets

### 60-Second Pitch
> "Every single day, thousands of citizens report broken streetlights, hazardous potholes, and overflowing garbage. But traditional complaint systems are black holes—they just record text into a database where complaints sit unread.
>
> We built **CivicFix**: an AI agentic civic issue resolution platform powered by **AWS Strands Agents SDK**.
>
> CivicFix doesn't stop at reading a complaint. The Strands Agent analyzes the report, calculates safety risks, assigns priority, routes the issue to the exact municipal department, detects duplicate reports, and generates a field repair plan—turning a raw complaint into an actionable civic case in under 2 seconds.
>
> From civic complaints to real action."

---

## 📄 License

MIT License © 2026 CivicFix Team
