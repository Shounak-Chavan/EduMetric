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

// ---- Submit assignment ----
document.getElementById("submitBtn").onclick = async () => {
  const assignment_id = assignmentSelect.value;
  const aim = document.getElementById("aim").value;
  const objectives = document.getElementById("objectives").value;
  const code = document.getElementById("code").value;
  const conclusion = document.getElementById("conclusion").value;

  if (!aim || !objectives || !code || !conclusion) {
    alert("All sections required");
    return;
  }

  const res = await fetch(`${API_BASE}/submissions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({
      assignment_id,
      aim,
      objectives,
      code,
      conclusion
    })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "Submission failed");
    return;
  }

  alert("Submission successful!");
  window.location.href = "dashboard.html";
};

// Initial load
loadAssignments();
