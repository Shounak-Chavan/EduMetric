// ---- SESSION HELPERS (inline for now) ----
function requireAuth() {
  const token = localStorage.getItem("accessToken");
  if (!token) {
    window.location.href = "login.html";
  }
}

function logout() {
  localStorage.clear();
  window.location.href = "login.html";
}

function getCurrentUser() {
  const user = localStorage.getItem("currentUser");
  return user ? JSON.parse(user) : null;
}

// ---- PAGE LOGIC ----
requireAuth();

const user = getCurrentUser();

if (!user) {
  logout();
}

// Welcome text
document.getElementById("welcomeText").innerText =
  `Welcome ${user.email} (${user.role})`;

// ---- Role-based button visibility ----
if (user.role !== "student") {
  document.getElementById("submitAssignmentBtn").style.display = "none";
  document.getElementById("submitPdfBtn").style.display = "none";
}

if (user.role !== "teacher") {
  document.getElementById("uploadAssignmentPdfBtn").style.display = "none";
  document.getElementById("gradeSubmissionsBtn").style.display = "none";
}

// ---- Navigation (REAL redirects now) ----
document.getElementById("viewAssignmentsBtn").onclick = () => {
  window.location.href = "assignments.html";
};

document.getElementById("submitAssignmentBtn").onclick = () => {
  window.location.href = "submissions.html";
};

document.getElementById("submitPdfBtn").onclick = () => {
  window.location.href = "submissions_pdf.html";
};

document.getElementById("uploadAssignmentPdfBtn").onclick = () => {
  window.location.href = "assignments.html";
};

document.getElementById("gradeSubmissionsBtn").onclick = () => {
  window.location.href = "grading.html";
};

document.getElementById("viewSubmissionDetailBtn").onclick = () => {
  window.location.href = "submission_detail.html";
};

document.getElementById("logoutBtn").onclick = logout;
