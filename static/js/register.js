const passwordInput = document.getElementById('PasswordInput');
const passwordToggle = document.getElementById('PasswordToggle');
let passVisible = false;

console.log(localStorage.getItem("kurba"));
console.log(sessionStorage.getItem("kurbicka"));

localStorage.setItem("kurba", "cauky");
sessionStorage.setItem("kurbicka", "mnauky");

function togglePasswordVisibility() {
    if (passVisible) {
        passwordInput.type = 'password';
        passwordToggle.src = "../static/images/show.webp";
        passVisible = false;
    } else {
        passwordInput.type = 'text';
        passwordToggle.src = "../static/images/hide.webp";
        passVisible = true;
    }
}

function showPopup(message) {
  document.getElementById("popup-message").textContent = message;
  document.getElementById("popup").style.display = "flex";
}

function hidePopup() {
  document.getElementById("popup").style.display = "none";
}

async function handleUrlFormSubmit(event) {
  event.preventDefault();

  const form = event.target;
  const username = form.name.value.trim();
  const password = form.pass.value;

  // ✅ Step 1: Basic validation
  if (!username || !password) {
    showPopup("Please fill in all fields.");
    return;
  }

  if (password.length < 8) {
    showPopup("Password must be at least 8 characters.");
    return;
  }

  if(username.length < 3 || username.length > 20) {
    showPopup("Username must be between 3 and 20 characters.");
    return;
  }else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
    showPopup("Username can only contain letters, numbers, and underscores.");
    return;
  }

  const payload = {
    name: username,
    pass: password
  };

  try {
    // ✅ Step 2: Send data to backend
    const res = await fetch("/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const error = await res.json();
      showPopup(error.message || "Registration failed.");
      return;
    }

  } catch (err) {
    console.error(err);
    showPopup("Network error. Try again.");
  }
}

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("urlForm").addEventListener("submit", handleUrlFormSubmit);
});