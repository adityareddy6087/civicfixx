/**
 * CivicFix Frontend JavaScript Engine
 * Interacts with FastAPI backend and AWS Strands Agent Orchestrator.
 */

const DEMO_PRESETS = [
  {
    desc: "There is a broken streetlight near the college gate and students are walking there at night.",
    location: "Main College Gate, Sector 4",
    category: "Public Lighting"
  },
  {
    desc: "Deep dangerous pothole near the central bus stop damaging car tires and causing traffic slowdown.",
    location: "Central Bus Stand Road",
    category: "Roads & Highways"
  },
  {
    desc: "Overflowing garbage bin near the local vegetable market causing severe odor and public health concern.",
    location: "Sector 5 Commercial Market",
    category: "Sanitation & Waste"
  },
  {
    desc: "Clean water pipe leaking on main road wasting hundreds of liters of drinking water per hour.",
    location: "Subhash Avenue, near Water Tank",
    category: "Water & Drainage"
  },
  {
    desc: "Broken concrete footpath slab near primary school causing children and elderly pedestrians to trip.",
    location: "Greenwood School Lane",
    category: "Pedestrian Safety"
  }
];

let allCases = [];

document.addEventListener("DOMContentLoaded", () => {
  checkSystemStatus();
  fetchCases();
});

// Load quick demo preset into form
function loadDemoPreset(index) {
  const preset = DEMO_PRESETS[index];
  if (!preset) return;
  
  document.getElementById("complaint-desc").value = preset.desc;
  document.getElementById("complaint-location").value = preset.location;
  document.getElementById("complaint-category").value = preset.category;
  
  // Smooth scroll to form
  document.getElementById("report-section").scrollIntoView({ behavior: "smooth" });
}

// Fetch system health & status
async function checkSystemStatus() {
  try {
    const res = await fetch("/api/system/status");
    if (res.ok) {
      const data = await res.json();
      const statusText = document.getElementById("agent-status-text");
      if (data.strands_active) {
        statusText.textContent = data.demo_mode ? "AWS Strands (Demo Mode)" : "AWS Strands SDK Active";
      }
    }
  } catch (err) {
    console.warn("Could not check system status:", err);
  }
}

// Handle complaint submission
async function handleComplaintSubmit(event) {
  event.preventDefault();
  
  const desc = document.getElementById("complaint-desc").value.trim();
  const location = document.getElementById("complaint-location").value.trim() || "General Area";
  const category = document.getElementById("complaint-category").value || null;
  const image_url = document.getElementById("complaint-image").value.trim() || null;

  if (!desc) return;

  setLoadingState(true);
  resetWorkflowSteps();

  try {
    // Simulate step-by-step visual animation for hackathon presentation
    await animateStep(1); // Understanding issue
    await animateStep(2); // Classifying category
    await animateStep(3); // Assessing priority
    await animateStep(4); // Identifying department
    await animateStep(5); // Checking related cases

    // Send API Request to FastAPI -> AWS Strands Agent
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        description: desc,
        location: location,
        category: category,
        image_url: image_url
      })
    });

    if (!response.ok) {
      throw new Error(`API returned error status ${response.status}`);
    }

    const result = await response.json();
    await animateStep(6); // Case creation ready

    renderAnalysisResult(result, desc, location, image_url);
  } catch (error) {
    alert("Error running AWS Strands Agent analysis: " + error.message);
  } finally {
    setLoadingState(false);
  }
}

function setLoadingState(isLoading) {
  const btn = document.getElementById("submit-btn");
  const spinner = document.getElementById("btn-spinner");
  const text = document.getElementById("btn-text");

  btn.disabled = isLoading;
  if (isLoading) {
    spinner.classList.remove("hidden");
    text.textContent = "Agent Executing Tools...";
  } else {
    spinner.classList.add("hidden");
    text.textContent = "🚀 Run AWS Strands Agent Analysis";
  }
}

function resetWorkflowSteps() {
  document.getElementById("workflow-status-badge").textContent = "Executing...";
  document.getElementById("workflow-status-badge").className = "badge badge-info";
  for (let i = 1; i <= 6; i++) {
    const el = document.getElementById(`step-${i}`);
    el.className = "step-item";
  }
  document.getElementById("result-container").classList.add("hidden");
}

async function animateStep(stepNum) {
  const el = document.getElementById(`step-${stepNum}`);
  if (!el) return;
  
  el.className = "step-item active";
  await new Promise(resolve => setTimeout(resolve, 350));
  el.className = "step-item completed";
}

function renderAnalysisResult(result, rawDesc, location, imageUrl) {
  const container = document.getElementById("result-container");
  document.getElementById("workflow-status-badge").textContent = "Analysis Complete";
  document.getElementById("workflow-status-badge").className = "badge badge-success";

  const priorityBadgeClass = result.priority === "HIGH" ? "badge-high" : (result.priority === "MEDIUM" ? "badge-medium" : "badge-low");
  const relatedCasesCount = result.related_cases.length;
  const relatedText = relatedCasesCount > 0 ? `${relatedCasesCount} Potential Duplicate(s) Found (${result.related_cases.join(", ")})` : "No direct duplicates found";

  container.innerHTML = `
    <div class="card result-card">
      <div class="result-header">
        <div>
          <span class="result-label">AI Analyzed Civic Issue</span>
          <h3 class="result-title">${escapeHtml(result.issue)}</h3>
        </div>
        <span class="badge ${priorityBadgeClass}">${result.priority} PRIORITY</span>
      </div>

      <div class="result-grid">
        <div class="result-field">
          <div class="result-label">Category</div>
          <div class="result-val">${escapeHtml(result.category)}</div>
        </div>
        <div class="result-field">
          <div class="result-label">Confidence</div>
          <div class="result-val">${(result.confidence * 100).toFixed(0)}% AI Certainty</div>
        </div>
        <div class="result-field">
          <div class="result-label">Responsible Department</div>
          <div class="result-val">${escapeHtml(result.department)}</div>
        </div>
        <div class="result-field">
          <div class="result-label">Safety Risk Level</div>
          <div class="result-val">${escapeHtml(result.safety_risk)}</div>
        </div>
      </div>

      <div class="result-field" style="margin-bottom: 14px;">
        <div class="result-label">AI Priority Reasoning</div>
        <div class="result-val" style="font-weight: 500; font-size: 0.88rem;">${escapeHtml(result.reason)}</div>
      </div>

      <div class="result-field" style="margin-bottom: 14px;">
        <div class="result-label">Recommended Field Action</div>
        <div class="result-val" style="font-weight: 600; color: #60a5fa;">${escapeHtml(result.recommended_action)}</div>
      </div>

      <div class="result-field" style="margin-bottom: 20px;">
        <div class="result-label">Duplicate / Related Issues</div>
        <div class="result-val" style="font-size: 0.85rem; color: #fbbf24;">🔍 ${escapeHtml(relatedText)}</div>
      </div>

      <button class="btn btn-primary btn-block" onclick="saveAsOfficialCase(${JSON.stringify({
        description: rawDesc,
        category: result.category,
        priority: result.priority,
        confidence: result.confidence,
        location: location,
        department: result.department,
        recommended_action: result.recommended_action,
        safety_risk: result.safety_risk,
        image_url: imageUrl
      }).replace(/"/g, '&quot;')})">
        📌 Confirm & Register Civic Case
      </button>
    </div>
  `;

  container.classList.remove("hidden");
  container.scrollIntoView({ behavior: "smooth" });
}

// Create case via API
async function saveAsOfficialCase(casePayload) {
  try {
    const res = await fetch("/api/cases", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(casePayload)
    });

    if (res.ok) {
      const created = await res.json();
      alert(`🎉 Civic Case ${created.case_id} registered successfully!`);
      document.getElementById("complaint-form").reset();
      document.getElementById("result-container").classList.add("hidden");
      fetchCases();
      document.getElementById("dashboard-section").scrollIntoView({ behavior: "smooth" });
    } else {
      alert("Failed to save case.");
    }
  } catch (err) {
    alert("Error creating case: " + err.message);
  }
}

// Fetch cases & render dashboard
async function fetchCases() {
  try {
    const res = await fetch("/api/cases");
    if (res.ok) {
      allCases = await res.json();
      renderStats(allCases);
      renderCases(allCases);
    }
  } catch (err) {
    console.error("Failed to load cases:", err);
  }
}

function renderStats(cases) {
  document.getElementById("stat-total").textContent = cases.length;
  document.getElementById("stat-high").textContent = cases.filter(c => c.priority === "HIGH").length;
  document.getElementById("stat-progress").textContent = cases.filter(c => c.status === "In Progress" || c.status === "Assigned").length;
  document.getElementById("stat-resolved").textContent = cases.filter(c => c.status === "Resolved").length;
}

function filterCases() {
  const search = document.getElementById("search-input").value.toLowerCase();
  const cat = document.getElementById("filter-category").value;
  const prio = document.getElementById("filter-priority").value;
  const stat = document.getElementById("filter-status").value;

  const filtered = allCases.filter(c => {
    const matchSearch = !search || c.case_id.toLowerCase().includes(search) || c.description.toLowerCase().includes(search) || c.location.toLowerCase().includes(search);
    const matchCat = !cat || c.category === cat;
    const matchPrio = !prio || c.priority === prio;
    const matchStat = !stat || c.status === stat;
    return matchSearch && matchCat && matchPrio && matchStat;
  });

  renderCases(filtered);
}

function renderCases(cases) {
  const grid = document.getElementById("cases-grid");
  if (!cases || cases.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: var(--text-muted);">
        No civic cases match the selected filters.
      </div>
    `;
    return;
  }

  grid.innerHTML = cases.map(c => {
    const badgeClass = c.priority === "HIGH" ? "badge-high" : (c.priority === "MEDIUM" ? "badge-medium" : "badge-low");
    const statusBadgeClass = c.status === "Resolved" ? "badge-success" : (c.status === "In Progress" ? "badge-medium" : "badge-info");
    
    return `
      <div class="case-card" onclick="openCaseModal('${c.case_id}')">
        <div>
          <div class="case-card-header">
            <span class="case-id-tag">${c.case_id}</span>
            <div>
              <span class="badge ${badgeClass}" style="margin-right: 4px;">${c.priority}</span>
              <span class="badge ${statusBadgeClass}">${c.status}</span>
            </div>
          </div>
          <div class="case-card-desc">${escapeHtml(c.description)}</div>
        </div>

        <div>
          <div style="font-size: 0.8rem; color: var(--text-dim); margin-bottom: 4px;">
            📍 ${escapeHtml(c.location)}
          </div>
          <div class="case-card-footer">
            <span>🏛️ ${escapeHtml(c.category)}</span>
            <span>${new Date(c.created_at).toLocaleDateString()}</span>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

// Case Modal & Timeline Logic
function openCaseModal(caseId) {
  const c = allCases.find(item => item.case_id === caseId);
  if (!c) return;

  document.getElementById("modal-case-id").textContent = c.case_id;
  const prioBadge = document.getElementById("modal-priority-badge");
  prioBadge.textContent = c.priority + " PRIORITY";
  prioBadge.className = `badge ${c.priority === 'HIGH' ? 'badge-high' : (c.priority === 'MEDIUM' ? 'badge-medium' : 'badge-low')}`;

  const statuses = ["Reported", "AI Analyzed", "Assigned", "In Progress", "Resolved"];
  const currentIdx = statuses.indexOf(c.status);

  const timelineHtml = `
    <div class="timeline">
      ${statuses.map((s, idx) => {
        let stepClass = "";
        if (idx === currentIdx) stepClass = "active";
        else if (idx < currentIdx) stepClass = "passed";
        return `
          <div class="timeline-step ${stepClass}">
            <div class="timeline-dot">${idx < currentIdx ? '✓' : (idx + 1)}</div>
            <div class="timeline-label">${s}</div>
          </div>
        `;
      }).join("")}
    </div>
  `;

  document.getElementById("modal-body").innerHTML = `
    <div style="margin-bottom: 16px;">
      <h4 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 6px;">${escapeHtml(c.description)}</h4>
      <p style="font-size: 0.85rem; color: var(--text-muted);">Location: 📍 ${escapeHtml(c.location)}</p>
    </div>

    ${timelineHtml}

    <div class="result-grid" style="margin-top: 20px;">
      <div class="result-field">
        <div class="result-label">Category</div>
        <div class="result-val">${escapeHtml(c.category)}</div>
      </div>
      <div class="result-field">
        <div class="result-label">Assigned Department</div>
        <div class="result-val">${escapeHtml(c.department)}</div>
      </div>
    </div>

    <div class="result-field" style="margin-bottom: 14px;">
      <div class="result-label">Recommended Action Plan</div>
      <div class="result-val" style="color: #60a5fa;">${escapeHtml(c.recommended_action)}</div>
    </div>

    <div class="result-field" style="margin-bottom: 20px;">
      <div class="result-label">Safety & Risk Assessment</div>
      <div class="result-val">${escapeHtml(c.safety_risk)}</div>
    </div>

    <div style="border-top: 1px solid var(--border-color); padding-top: 16px; margin-top: 16px;">
      <label style="font-weight: 700; color: #fff; margin-bottom: 8px;">Update Operational Status:</label>
      <div style="display: flex; gap: 10px; flex-wrap: wrap;">
        ${statuses.map(s => `
          <button class="btn btn-sm ${s === c.status ? 'btn-primary' : 'btn-secondary'}" onclick="updateStatus('${c.case_id}', '${s}')">
            ${s}
          </button>
        `).join("")}
      </div>
    </div>
  `;

  document.getElementById("case-modal").classList.remove("hidden");
}

async function updateStatus(caseId, newStatus) {
  try {
    const res = await fetch(`/api/cases/${caseId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus })
    });

    if (res.ok) {
      closeCaseModal();
      await fetchCases();
    } else {
      alert("Status update failed");
    }
  } catch (err) {
    alert("Error updating status: " + err.message);
  }
}

function closeCaseModal() {
  document.getElementById("case-modal").classList.add("hidden");
}

function closeModalOnOverlay(e) {
  if (e.target.id === "case-modal") {
    closeCaseModal();
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
