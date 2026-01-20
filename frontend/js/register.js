const API_BASE = "http://localhost:8000";

document.getElementById("registerBtn").onclick = async () => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const role = document.getElementById("role").value;

  if (!email || !password) {
    alert("Email and password required");
    return;
  }

  try {
    // Call /auth/register/{role}
    const res = await fetch(`${API_BASE}/auth/register/${role}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Registration failed");
    }

    alert("Registered successfully! Now login.");
    window.location.href = "login.html";

  } catch (err) {
    alert(err.message);
  }
};
