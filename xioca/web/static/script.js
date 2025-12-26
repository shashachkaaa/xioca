// 📦 Xioca UserBot
// 👤 Copyright (C) 2025 shashachkaaa
//
// ⚖️ Licensed under GNU AGPL v3.0
// 🌐 Source: https://github.com/shashachkaaa/xioca
// 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

const API_URL = window.location.href;

function showToast(title, message, type = 'success') {
  const container = document.getElementById('notification-wrapper');
  
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  const iconClass = type === 'error' ? 'fa-exclamation-circle' : 'fa-check-circle';
  
  toast.innerHTML = `
    <i class="fas ${iconClass}"></i>
    <div class="toast-content">
      <h3>${title}</h3>
      <p>${message}</p>
    </div>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease forwards';
    toast.addEventListener('animationend', () => {
      toast.remove();
    });
  }, 3500);
}

function goToStep(stepNumber) {
  const steps = document.querySelectorAll('.step-content');
  
  steps.forEach(step => {
    step.classList.remove('active');
  });

  const target = document.getElementById(`step-${stepNumber}`);
  if (target) {
    target.classList.add('active');
  }
}

async function post(endpoint, headers) {
  try {
    const response = await fetch(API_URL + endpoint, {
      method: 'POST',
      headers: headers,
    });
    return await response.text();
  } catch (error) {
    showToast("Network Error", error.message, "error");
    return null;
  }
}

async function post_body(endpoint, body) {
  try {
    const response = await fetch(API_URL + endpoint, {
      method: 'POST',
      body: body
    });
    return await response.text();
  } catch (error) {
    showToast("Network Error", error.message, "error");
    return null;
  }
}

document.getElementById("btn-step-1").onclick = async () => {
  const btn = document.getElementById("btn-step-1");
  const _id = document.getElementById("api_id").value;
  const _hash = document.getElementById("api_hash").value;

  if (!_id || !_hash) {
    showToast("Validation", "Please enter both API ID and Hash", "error");
    return;
  }

  const originalText = btn.innerHTML;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Checking...';
  
  const headers = new Headers();
  headers.append('id', _id);
  headers.append('hash', _hash);

  const data = await post('tokens', headers);
  btn.innerHTML = originalText;

  if (data === 'dialog' || !data || data === null) {
    showToast('Success', 'Credentials accepted', 'success');
    goToStep(2);
  } else {
    showToast("Error", "Invalid credentials or server error", "error");
    console.log(data);
  }
};

document.getElementById("btn-step-2").onclick = async () => {
  const btn = document.getElementById("btn-step-2");
  const phone = document.getElementById("phone_number").value;

  if (!phone) {
    showToast("Validation", "Enter phone number", "error");
    return;
  }

  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

  let body = JSON.stringify({ "phone": phone });
  const data = await post_body("phone_request", body);
  
  btn.innerHTML = 'Send Code <i class="fas fa-paper-plane"></i>';

  showToast("Sent", "Code sent to your Telegram app", "success");
  goToStep(3);
};

document.getElementById("btn-step-3").onclick = async () => {
  await submitCode(false);
};

document.getElementById("btn-step-4").onclick = async () => {
  await submitCode(true);
};

async function submitCode(is2faStep) {
  const btnId = is2faStep ? "btn-step-4" : "btn-step-3";
  const btn = document.getElementById(btnId);
  const code = document.getElementById("phone_code").value;

  if (!code) {
    showToast("Validation", "Enter the code", "error");
    return;
  }

  let bodyData = { "code": code };
  const originalText = btn.innerHTML;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying...';

  if (is2faStep) {
    const password = document.getElementById("password").value;
    if (!password) {
      showToast("Validation", "Enter 2FA password", "error");
      btn.innerHTML = originalText;
      return;
    }
    bodyData["twofa"] = password;
  }

  const response = await post_body("enter_code", JSON.stringify(bodyData));
  btn.innerHTML = originalText;

  if (response === "no_twofa" || response === "invalid_twofa") {
    if (!is2faStep) {
       showToast("2FA Required", "Please enter your 2FA password", "error");
       goToStep(4);
    } else {
       showToast("Error", "Invalid 2FA password", "error");
    }
  } else if (response === "invalid_phone_code") {
    showToast("Error", "Invalid code. Try again.", "error");
  } else {
    showToast("Welcome", "You are successfully logged in!", "success");
    document.querySelector('.step-content.active').classList.remove('active');
    document.getElementById('step-success').classList.add('active');
  }
}

const themeToggleBtn = document.getElementById("theme-toggle");
const icon = themeToggleBtn.querySelector('i');

function toggleTheme() {
  document.body.classList.toggle("dark-theme");
  
  if (document.body.classList.contains("dark-theme")) {
    icon.classList.remove('fa-moon');
    icon.classList.add('fa-sun');
  } else {
    icon.classList.remove('fa-sun');
    icon.classList.add('fa-moon');
  }
}

themeToggleBtn.addEventListener("click", toggleTheme);

if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  toggleTheme();
}