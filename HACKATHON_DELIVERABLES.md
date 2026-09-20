# CivicFix — Hackathon Deliverables & Pitch Package

---

## 1. Hackathon Submission Text (Copy & Paste Ready)

- **Project Name**: CivicFix
- **Tagline**: From civic complaints to real action.
- **Problem Statement**:
  Citizens across cities report infrastructure issues daily—potholes, dark streetlights, water leaks, overflowing waste—yet traditional municipal portals act as passive complaint bins. Reports remain unclassified, unprioritized, and untracked, leading to delayed repairs and public safety risks.
- **Solution**:
  CivicFix is an agentic civic issue resolution platform powered by **AWS Strands Agents SDK**. Rather than acting as a simple conversational chatbot, CivicFix deploys multi-step AI agents that process citizen complaints, execute dedicated tools to classify category and priority, detect duplicate reports, route cases to responsible municipal divisions, and generate field technician dispatch plans.
- **How It Works**:
  1. Citizen submits issue text, location, or image via the modern web app.
  2. AWS Strands Agent orchestrates a 6-step reasoning pipeline.
  3. Custom `@tool` suite evaluates severity, department mapping, and duplicate detection.
  4. Structured Civic Case (`CFX-XXXX`) is logged in SQLite database.
  5. Municipal Operations Dashboard tracks resolution status from `Reported` to `Resolved`.
- **AWS Technology Used**: AWS Strands Agents SDK (`strands-agents`).
- **Why AWS Strands Agents SDK**:
  Strands provides model-driven agent orchestration, native tool calling via `@tool` decorators, multi-step workflow execution, and cloud-native extensibility.
- **Innovation**:
  AI-assisted duplicate issue matching links multiple reports of the same physical problem to a single root civic case, reducing municipal backlog.
- **Tech Stack**: Python 3.11, AWS Strands Agents SDK, FastAPI, SQLite, Pydantic, Vanilla HTML5/CSS3/JS, Pytest.
- **GitHub Repository**: https://github.com/adityareddy6087/civicfixx
- **Live Demo URL**: https://e33d9568a03503c5-103-47-124-98.serveousercontent.com

---

## 2. 60-Second Founder Pitch Script

> **[0:00–0:10] Problem**:
> "Every day, thousands of citizens report broken streetlights, dangerous potholes, and water leaks. But traditional portals are black holes—complaints sit in unorganized databases for weeks."
>
> **[0:10–0:25] Solution**:
> "Meet **CivicFix**: from civic complaints to real action. Powered by **AWS Strands Agents SDK**, CivicFix turns raw citizen reports into structured, actionable municipal cases in seconds."
>
> **[0:25–0:40] How Strands Operates**:
> "When a citizen reports a dark streetlight near a college gate, our Strands Agent executes a multi-step tool workflow: classifying the category, scoring safety risk as HIGH priority, routing to the Electrical Maintenance division, checking for duplicate reports, and generating an instant technician repair plan."
>
> **[0:40–0:55] Impact & Differentiation**:
> "CivicFix isn't a chatbot—it's an AI teammate for municipal operations that deduplicates reports and tracks cases from report to resolution."
>
> **[0:55–1:00] Call to Action**:
> "CivicFix: From civic complaints to real action. Thank you!"

---

## 3. 2–3 Minute Demo Video Script (With Exact Timestamps)

- **0:00–0:15 | The Civic Problem**
  *(Visual: Show traditional municipal form vs cluttered inbox)*
  *"In cities everywhere, reporting a pothole or broken streetlight feels like sending a message into a void. Municipalities are overwhelmed with unstructured reports and struggle to triage urgent safety hazards."*

- **0:15–0:30 | Introducing CivicFix**
  *(Visual: CivicFix homepage with hero banner and tagline)*
  *"This is CivicFix—an agentic civic issue resolution platform powered by AWS Strands Agents SDK. CivicFix doesn't just collect complaints; it takes action."*

- **0:30–1:20 | Live AI Agent Workflow**
  *(Visual: Click 1-Click Demo button 'Broken streetlight near college gate' and submit)*
  *"Watch what happens when a citizen reports a broken streetlight near a college gate at night. As soon as we submit, the AWS Strands Agent triggers its tool orchestration layer."*
  *(Visual: Highlight step-by-step thinking visualizer 1 through 6)*
  *"Step 1 parses context. Step 2 calls `classify_issue()` to identify Public Lighting. Step 3 calls `assess_priority()` flagging HIGH priority due to student night safety. Step 4 maps `identify_department()` to Electrical Maintenance. Step 5 checks `detect_related_cases()`, and Step 6 registers Case `CFX-1006`."*

- **1:20–1:45 | Case Creation & Operations Dashboard**
  *(Visual: Scroll to Operations Dashboard, view case cards, open modal, click status update)*
  *"The case immediately appears on the Operations Dashboard. Officers can view high priority alerts, inspect the AI-generated resolution plan, and update status live from Assigned to In Progress to Resolved."*

- **1:45–2:10 | AWS Strands Architecture**
  *(Visual: Show Architecture diagram)*
  *"Under the hood, AWS Strands Agents SDK acts as our core orchestration engine, calling modular Python `@tool` functions and maintaining extensible agent memory."*

- **2:10–2:30 | Impact & Future Scope**
  *(Visual: Show live URL and statistics)*
  *"CivicFix reduces response times from days to minutes. Thank you!"*

---

## 4. 15+ Judge Q&A Preparation Sheet

1. **Q: Why use an AI Agent instead of a traditional chatbot?**
   *A: A traditional chatbot only generates conversational text back to the user. CivicFix uses an AI Agent to execute tools, make structured decisions, route cases to specific databases, and initiate real-world operational workflows.*

2. **Q: Why did you choose AWS Strands Agents SDK?**
   *A: AWS Strands Agents SDK provides model-driven orchestration with `@tool` decorators, dynamic tool chaining, and clean separation between agent reasoning and backend execution.*

3. **Q: What makes CivicFix innovative compared to existing portals?**
   *A: Three key innovations: automated safety-risk priority scoring, AI-assisted duplicate issue matching across citizen reports, and automated field technician repair plan generation.*

4. **Q: How does priority assessment work?**
   *A: The `assess_priority()` tool evaluates keywords, location sensitivity (e.g. schools, college gates, hospitals), and category hazard weights to classify issues into HIGH, MEDIUM, or LOW.*

5. **Q: How does duplicate issue detection work?**
   *A: The `detect_related_cases()` tool searches the database for overlapping categories, locations, and semantic text similarity, linking related citizen reports to a single master case.*

6. **Q: How do you prevent or reduce hallucination risk?**
   *A: Agent tool execution is strictly bounded using Pydantic models, deterministic fallback rules, and validated enum taxonomies for categories and departments.*

7. **Q: How does DEMO_MODE work?**
   *A: When `DEMO_MODE=true`, the system executes deterministic fallback tool pipelines so judges and evaluators can test the entire workflow without requiring AWS IAM keys or paid API keys.*

8. **Q: Why SQLite for the database?**
   *A: SQLite provides lightweight, zero-configuration file-based persistence ideal for serverless containers and fast local/cloud verification.*

9. **Q: How would municipal authorities integrate with CivicFix?**
   *A: Municipalities can connect their existing ERP/work order systems directly to our FastAPI REST endpoints (`/api/cases`).*

10. **Q: How will the system scale to high city traffic?**
    *A: FastAPI is asynchronously non-blocking. Database layers can easily transition from SQLite to Amazon Aurora / PostgreSQL for multi-region scale.*

11. **Q: How do you protect citizen data privacy?**
    *A: Anonymous reporting option is supported, and no personal identifying information (PII) is stored in complaint descriptions.*

12. **Q: How is the responsible department selected?**
    *A: The `identify_department()` tool maps classified categories against municipal organizational charts.*

13. **Q: How do you validate AI decisions?**
    *A: Every AI decision includes an explicit confidence metric and reasoning summary for human-in-the-loop review by municipal staff.*

14. **Q: What is the future scope of CivicFix?**
    *A: Mobile app with GIS GPS mapping, image computer vision for automated pothole depth measurement, and SMS citizen status notifications.*

15. **Q: What was technically difficult during development?**
    *A: Building a real-time visual progress step indicator that mirrors the internal multi-step tool execution of the AWS Strands Agent.*

16. **Q: What did your team actually build today?**
    *A: Full-stack application: FastAPI backend, AWS Strands Agent tool suite, SQLite database engine, responsive operations frontend dashboard, automated test suite, Docker container setup, and live cloud deployment.*
