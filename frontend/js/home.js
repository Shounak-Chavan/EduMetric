// If already logged in → go to dashboard
const token = localStorage.getItem("accessToken");
if (token) {
  window.location.href = "dashboard.html";
}

// Buttons
document.getElementById("loginBtn").onclick = () => {
  window.location.href = "login.html";
};

document.getElementById("registerBtn").onclick = () => {
  window.location.href = "register.html";
};
