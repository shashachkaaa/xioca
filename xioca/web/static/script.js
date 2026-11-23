// 📦 Xioca UserBot
// 👤 Copyright (C) 2025 shashachkaaa
//
// ⚖️ Licensed under GNU AGPL v3.0
// 🌐 Source: https://github.com/shashachkaaa/xioca
// 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

const API_URL = new URL('/', window.location.href).toString();

function showToast(title, message, type = 'success') {
  const container = document.getElementById('notification-wrapper');
  
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  const iconClass = type === 'error' ? 'fa-exclamation-circle' : 'fa-check-circle';
  
  toast.innerHTML = `
    <i class="fas ${iconClass}"></i>
    <div class="toast-content">
      <h3></h3>
      <p></p>
    </div>
  `;
  // Always treat error details as text, not HTML.
  toast.querySelector('h3').textContent = title;
  toast.querySelector('p').textContent = String(message).slice(0, 320);

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
    const body = await response.text();
    return response.ok ? body : (body || `HTTP ${response.status}`);
  } catch (error) {
    return `Network error: ${error.message}`;
  }
}

async function post_body(endpoint, body) {
  try {
    const response = await fetch(API_URL + endpoint, {
      method: 'POST',
      body: body
    });
    const text = await response.text();
    return response.ok ? text : (text || `HTTP ${response.status}`);
  } catch (error) {
    return `Network error: ${error.message}`;
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

  if (data === 'dialog') {
    showToast('Success', 'Connected to Telegram', 'success');
    goToStep(2);
  } else {
    showToast("Connection failed", data || "No response from server.", "error");
  }
};

const resendBtn = document.getElementById("btn-resend");
let retryAvailableAt = 0;
let retryAllowed = false;

function refreshResendButton() {
  if (!retryAllowed) return;
  const secondsLeft = Math.max(0, Math.ceil((retryAvailableAt - Date.now()) / 1000));
  resendBtn.disabled = secondsLeft > 0;
  resendBtn.textContent = secondsLeft > 0
    ? `Try another delivery method in ${secondsLeft}s`
    : 'Try another delivery method';
}

function explainCodeDelivery(info) {
  document.getElementById("delivery-instructions").textContent =
    info.delivery || "Telegram accepted the request. Check your other devices.";
  retryAllowed = info.can_resend === true;
  retryAvailableAt = Date.now() + Math.max(0, Number(info.retry_after) || 0) * 1000;
  resendBtn.style.display = retryAllowed ? 'block' : 'none';
  refreshResendButton();
}

function parseCodeReply(raw) {
  try {
    const payload = JSON.parse(raw);
    if (payload && typeof payload === 'object') return payload;
  } catch (error) { /* Network and proxy errors may be plain text. */ }
  return {status: "error", message: raw || "No response from server."};
}

setInterval(refreshResendButton, 1000);

resendBtn.onclick = async () => {
  if (resendBtn.disabled || !retryAllowed) return;
  resendBtn.disabled = true;
  resendBtn.textContent = 'Requesting...';
  const raw = await post_body('resend_code', '{}');
  const info = parseCodeReply(raw);
  if (info.status === 'enter_code') {
    explainCodeDelivery(info);
    showToast("Telegram response", info.delivery, 'success');
  } else {
    showToast("Retry unavailable", info.message, 'error');
    retryAvailableAt = Date.now() + 30000;
    refreshResendButton();
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

  btn.disabled = true;
  const raw = await post_body("phone_request", JSON.stringify({phone: phone.trim()}));
  btn.disabled = false;
  btn.innerHTML = 'Send Code <i class="fas fa-paper-plane"></i>';

  const data = parseCodeReply(raw);
  if (data.status === 'enter_code') {
    explainCodeDelivery(data);
    showToast("Telegram response", data.delivery, 'success');
    goToStep(3);
  } else {
    showToast("Could not request code", data.message || "No response from server.", "error");
  }
};

let qrLoginActive = false;
let qrLoginFor2FA = false;
let lastQRData = "";

function renderQRLogin(info) {
  const message = document.getElementById('qr-login-status');
  const image = document.getElementById('qr-login-image');

  if (info.status === 'password') {
    qrLoginActive = false;
    qrLoginFor2FA = true;
    goToStep(4);
    showToast("Two-step verification", "Enter your Telegram cloud password.", "success");
    return;
  }
  if (info.status === 'success') {
    qrLoginActive = false;
    goToStep('success');
    showToast("Authorized", "Telegram approved your QR login.", "success");
    return;
  }
  if (info.status === 'error') {
    qrLoginActive = false;
    message.textContent = 'Could not prepare the QR login.';
    showToast("QR login failed", info.error || "Check VPS logs.", "error");
    return;
  }
  if (info.image && info.image !== lastQRData) {
    image.src = info.image;
    image.style.display = 'block';
    lastQRData = info.image;
  }
  if (info.status === 'waiting') {
    message.textContent = info.image
      ? 'Scan and confirm in Telegram. The QR refreshes automatically.'
      : 'Preparing QR code...';
  }
}

async function fetchQRStatus(endpoint) {
  try {
    const response = await fetch(API_URL + endpoint, {cache: 'no-store'});
    return await response.json();
  } catch (_) {
    return {status: 'error', error: 'Lost connection to authorization server. Check the VPS terminal.'};
  }
}

let qrPollInProgress = false;
async function pollQRLogin() {
  if (!qrLoginActive || qrPollInProgress) return;
  qrPollInProgress = true;
  try {
    renderQRLogin(await fetchQRStatus('checkqr'));
  } finally {
    qrPollInProgress = false;
  }
}

document.querySelectorAll('.open-qr-login').forEach(button => {
  button.addEventListener('click', async () => {
    qrLoginFor2FA = false;
    qrLoginActive = true;
    lastQRData = "";
    document.getElementById('qr-login-image').style.display = 'none';
    document.getElementById('qr-login-status').textContent = 'Preparing QR code...';
    goToStep('qr');
    renderQRLogin(await fetchQRStatus('qrcode'));
  });
});

document.getElementById('qr-back').onclick = () => {
  qrLoginActive = false;
  goToStep(2);
};

setInterval(pollQRLogin, 4000);

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

  // QR login has no phone verification code: only the cloud password is needed.
  if (is2faStep && qrLoginFor2FA) {
    const password = document.getElementById("password").value;
    if (!password) {
      showToast("Validation", "Enter 2FA password", "error");
      return;
    }
    const result = await post_body("twofa", JSON.stringify({twofa: password}));
    if (result === "success") {
      qrLoginFor2FA = false;
      showToast("Authorized", "Telegram approved your login.", "success");
      goToStep('success');
    } else {
      showToast("Verification failed", result || "Could not verify password.", "error");
    }
    return;
  }

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
  } else if (response === "success") {
    showToast("Welcome", "You are successfully logged in!", "success");
    document.querySelector('.step-content.active').classList.remove('active');
    document.getElementById('step-success').classList.add('active');
  } else {
    showToast("Authorization failed", response || "No response from server.", "error");
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