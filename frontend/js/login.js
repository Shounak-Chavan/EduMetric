const API_BASE = "http://localhost:8000";

document.getElementById("loginBtn").onclick = async () => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (!email || !password) {
    alert("Email and password required");
    return;
  }

  try {
    // 1) Call /auth/login
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Login failed");
    }

    // 2) Store JWT
    localStorage.setItem("accessToken", data.access_token);

    // 3) Call /auth/me
    const meRes = await fetch(`${API_BASE}/auth/me`, {
      headers: {
        "Authorization": `Bearer ${data.access_token}`
      }
    });

    const me = await meRes.json();

    if (!meRes.ok) {
      throw new Error("Failed to fetch user profile");
    }

    // 4) Store user profile
    localStorage.setItem("currentUser", JSON.stringify(me));

    // 5) Redirect to dashboard
    window.location.href = "dashboard.html";

  } catch (err) {
    alert(err.message);
  }
};
