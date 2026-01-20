const API_BASE = "http://localhost:8000";

// ---- Session helpers ----
function requireAuth() {
  const token = localStorage.getItem("accessToken");
  if (!token) window.location.href = "login.html";
}

function getCurrentUser() {
  const user = localStorage.getItem("currentUser");
  return user ? JSON.parse(user) : null;
}

// ---- Page setup ----
requireAuth();

const user = getCurrentUser();
if (!user || user.role !== "student") {
  alert("Students only");
  window.location.href = "dashboard.html";
}

const token = localStorage.getItem("accessToken");
const assignmentSelect = document.getElementById("assignmentSelect");
const pdfInput = document.getElementById("pdfFile");

// ---- Load assignments ----
async function loadAssignments() {
  const res = await fetch(`${API_BASE}/assignments`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const data = await res.json();

  assignmentSelect.innerHTML = "";

  data.forEach(a => {
    const opt = document.createElement("option");
    opt.value = a.id;
    opt.innerText = a.title || `PDF Assignment (ID ${a.id})`;
    assignmentSelect.appendChild(opt);
  });

  // If coming from assignments page
  const selectedId = localStorage.getItem("selectedAssignmentId");
  if (selectedId) {
    assignmentSelect.value = selectedId;
    localStorage.removeItem("selectedAssignmentId");
  }
}

// ---- Submit PDF ----
document.getElementById("submitPdfBtn").onclick = async () => {
  const assignment_id = assignmentSelect.value;

  if (!pdfInput.files.length) {
    alert("Please select a PDF file");
    return;
  }

  const formData = new FormData();
  formData.append("file", pdfInput.files[0]);

  const res = await fetch(
    `${API_BASE}/assignments/${assignment_id}/submit-pdf`,
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`
      },
      body: formData
    }
  );

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "PDF submission failed");
    return;
  }

  alert("PDF submitted successfully!");
  window.location.href = "dashboard.html";
};

// Initial load
loadAssignments();
