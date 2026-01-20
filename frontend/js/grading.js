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
if (!user || user.role !== "teacher") {
  alert("Teachers only");
  window.location.href = "dashboard.html";
}

const token = localStorage.getItem("accessToken");

const assignmentInput = document.getElementById("assignmentId");
const submissionInput = document.getElementById("submissionId");
const resultBox = document.getElementById("resultBox");
const viewDetailBtn = document.getElementById("viewDetailBtn");

// Hide result + view button initially
resultBox.innerText = "";
viewDetailBtn.style.display = "none";

// ---- Grade submission ----
document.getElementById("gradeBtn").onclick = async () => {
  const assignment_id = assignmentInput.value.trim();
  const submission_id = submissionInput.value.trim();

  if (!assignment_id || !submission_id) {
    alert("Assignment ID and Submission ID required");
    return;
  }

  if (isNaN(assignment_id) || isNaN(submission_id)) {
    alert("IDs must be numbers");
    return;
  }

  try {
    const res = await fetch(
      `${API_BASE}/grading/assignments/${assignment_id}/submissions/${submission_id}`,
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      }
    );

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || "Grading failed");
      return;
    }

    // Pretty display result
    resultBox.innerText = JSON.stringify(data, null, 2);

    // Store submission_id for detail page
    localStorage.setItem("lastGradedSubmissionId", submission_id);

    viewDetailBtn.style.display = "inline-block";

  } catch (err) {
    console.error("Grading error:", err);
    alert("Server error. Please try again.");
  }
};

// ---- View submission detail ----
viewDetailBtn.onclick = () => {
  const id = localStorage.getItem("lastGradedSubmissionId");
  if (!id) {
    alert("No submission ID found");
    return;
  }

  window.location.href = `submissions.html?id=${id}`;
};
