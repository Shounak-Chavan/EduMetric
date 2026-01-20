const API_BASE = "http://localhost:8000";

// ---- Session helpers (inline for now) ----
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

const token = localStorage.getItem("accessToken");

const createBox = document.getElementById("createAssignmentBox");
const uploadBox = document.getElementById("uploadPdfBox");

// Role-based UI
if (user.role !== "teacher") {
  createBox.style.display = "none";
  uploadBox.style.display = "none";
}

// ---- Fetch assignments ----
async function loadAssignments() {
  const res = await fetch(`${API_BASE}/assignments`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const data = await res.json();

  const list = document.getElementById("assignmentsList");
  list.innerHTML = "";

  data.forEach(a => {
    const li = document.createElement("li");

    li.innerHTML = `
      <b>${a.title || "PDF Assignment"}</b><br>
      ${a.description || ""}<br>
      <small>ID: ${a.id}</small><br>
    `;

    // Student: show submit button
    if (user.role === "student") {
      const btn = document.createElement("button");
      btn.innerText = "Submit";
      btn.onclick = () => {
        localStorage.setItem("selectedAssignmentId", a.id);
        window.location.href = "submissions.html";
      };
      li.appendChild(btn);
    }

    list.appendChild(li);
  });
}

// ---- Teacher: Create TEXT assignment ----
document.getElementById("createAssignmentBtn").onclick = async () => {
  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;

  if (!title || !description) {
    alert("Title and description required");
    return;
  }

  const res = await fetch(`${API_BASE}/assignments`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ title, description })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "Failed to create assignment");
    return;
  }

  alert("Assignment created!");
  document.getElementById("title").value = "";
  document.getElementById("description").value = "";
  loadAssignments();
};

// ---- Teacher: Upload PDF assignment ----
document.getElementById("uploadPdfBtn").onclick = async () => {
  const fileInput = document.getElementById("pdfFile");

  if (!fileInput.files.length) {
    alert("Select a PDF file first");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const res = await fetch(`${API_BASE}/assignments/upload-pdf`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`
    },
    body: formData
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "PDF upload failed");
    return;
  }

  alert("PDF assignment uploaded!");
  fileInput.value = "";
  loadAssignments();
};

// Initial load
loadAssignments();
