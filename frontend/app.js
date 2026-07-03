/**
 * SEBI CyberShield — Frontend Application
 * Handles: Tab switching, API calls, results rendering, chat, drag-drop
 */

// ── Config ──────────────────────────────────────────────────────────────────
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000'
  : ''; // Same origin in production

// ── State ────────────────────────────────────────────────────────────────────
let lastScanResult = null;
let lastScanType   = null;
let lastUserInput  = '';
let selectedFile   = null;
let chatHistory    = [];
let isTyping       = false;

// ── DOM Refs ─────────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  checkAPIHealth();
  initScanTabs();
  initDetailTabs();
  initImageDrop();
  initScanButtons();
  initChat();
  initResultActions();
  initNavbar();
});

// ── Navbar scroll effect ──────────────────────────────────────────────────────
function initNavbar() {
  const navbar = $('navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      navbar.style.borderBottomColor = 'rgba(255,255,255,0.12)';
    } else {
      navbar.style.borderBottomColor = '';
    }
  });
}

// ── API Health Check ──────────────────────────────────────────────────────────
async function checkAPIHealth() {
  const dot  = $('status-dot');
  const text = $('status-text');
  try {
    const res = await fetch(`${API_BASE}/api/health`, { signal: AbortSignal.timeout(5000) });
    if (res.ok) {
      const data = await res.json();
      dot.className  = 'status-dot status-online';
      const gemini   = data.gemini_available ? '✓ Gemini' : '⚠ No Gemini';
      text.textContent = gemini;
    } else {
      throw new Error('non-200');
    }
  } catch {
    dot.className  = 'status-dot status-offline';
    text.textContent = 'API Offline';
  }
}

// ── Scan Tabs ─────────────────────────────────────────────────────────────────
function initScanTabs() {
  document.querySelectorAll('.scan-tab').forEach(tab => {
    tab.addEventListener('click', () => switchScanTab(tab.dataset.tab));
    tab.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); switchScanTab(tab.dataset.tab); }
    });
  });
}

function switchScanTab(tabId) {
  document.querySelectorAll('.scan-tab').forEach(t => {
    const active = t.dataset.tab === tabId;
    t.classList.toggle('active', active);
    t.setAttribute('aria-selected', active);
  });

  document.querySelectorAll('.scan-panel-content').forEach(p => {
    const active = p.id === `panel-${tabId}`;
    p.classList.toggle('active', active);
    p.hidden = !active;
  });

  // Hide results when switching tabs
  hideResults();
}

// ── Detail Tabs ───────────────────────────────────────────────────────────────
function initDetailTabs() {
  document.querySelectorAll('.detail-tab').forEach(tab => {
    tab.addEventListener('click', () => switchDetailTab(tab.dataset.dtab));
  });
}

function switchDetailTab(tabId) {
  document.querySelectorAll('.detail-tab').forEach(t => {
    const active = t.dataset.dtab === tabId;
    t.classList.toggle('active', active);
    t.setAttribute('aria-selected', active);
  });

  document.querySelectorAll('.detail-panel').forEach(p => {
    const active = p.id === `dpanel-${tabId}`;
    p.classList.toggle('active', active);
    p.hidden = !active;
  });
}

// ── Image Drop Zone ───────────────────────────────────────────────────────────
function initImageDrop() {
  const zone    = $('drop-zone');
  const input   = $('image-file-input');
  const preview = $('drop-preview');
  const inner   = $('drop-zone-inner');
  const scanBtn = $('scan-image-btn');
  const browseBtn = $('browse-btn');

  // Click to browse
  zone.addEventListener('click', e => {
    if (e.target === browseBtn || browseBtn.contains(e.target)) {
      input.click();
    } else if (!preview.style.display || preview.style.display === 'none') {
      input.click();
    }
  });

  browseBtn.addEventListener('click', e => { e.stopPropagation(); input.click(); });

  zone.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); }
  });

  input.addEventListener('change', () => {
    if (input.files[0]) handleFileSelect(input.files[0]);
  });

  // Drag & Drop
  zone.addEventListener('dragover', e => {
    e.preventDefault();
    zone.classList.add('drag-over');
  });

  zone.addEventListener('dragleave', e => {
    if (!zone.contains(e.relatedTarget)) zone.classList.remove('drag-over');
  });

  zone.addEventListener('drop', e => {
    e.preventDefault();
    zone.classList.remove('drag-over');
    if (e.dataTransfer.files[0]) handleFileSelect(e.dataTransfer.files[0]);
  });

  function handleFileSelect(file) {
    if (!file.type.startsWith('image/')) {
      showToast('Please upload an image file (PNG, JPG, WEBP)', 'error');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      showToast('Image too large. Max file size is 5MB', 'error');
      return;
    }

    selectedFile = file;
    scanBtn.disabled = false;

    // Show preview
    const reader = new FileReader();
    reader.onload = e => {
      inner.style.display = 'none';
      preview.src = e.target.result;
      preview.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
}

// ── Scan Buttons ──────────────────────────────────────────────────────────────
function initScanButtons() {
  // Scan buttons
  $('scan-email-btn') .addEventListener('click', () => doScan('email'));
  $('scan-url-btn')   .addEventListener('click', () => doScan('url'));
  $('scan-social-btn').addEventListener('click', () => doScan('social'));
  $('scan-image-btn') .addEventListener('click', () => doScan('image'));

  // Clear buttons
  $('clear-email-btn') .addEventListener('click', () => { $('email-input').value  = ''; hideResults(); });
  $('clear-url-btn')   .addEventListener('click', () => { $('url-input').value    = ''; hideResults(); });
  $('clear-social-btn').addEventListener('click', () => { $('social-input').value = ''; hideResults(); });
  $('clear-image-btn') .addEventListener('click', clearImage);
}

function clearImage() {
  selectedFile = null;
  $('scan-image-btn').disabled = true;
  $('drop-zone-inner').style.display = '';
  $('drop-preview').style.display = 'none';
  $('drop-preview').src = '';
  $('image-file-input').value = '';
  hideResults();
}

// ── Main Scan Function ────────────────────────────────────────────────────────
async function doScan(type) {
  showLoading(type);

  try {
    let result;

    if (type === 'email') {
      const text = $('email-input').value.trim();
      if (!text) { showToast('Please paste email content to analyze', 'warning'); hideLoading(); return; }
      lastUserInput = text;
      result = await apiPost('/api/scan/email', {
        email_text: text,
        model: $('email-model').value
      });

    } else if (type === 'url') {
      let url = $('url-input').value.trim();
      if (!url) { showToast('Please enter a URL to analyze', 'warning'); hideLoading(); return; }
      // Auto-prepend https:// if no scheme provided (e.g. user pastes "google.com")
      if (!/^https?:\/\//i.test(url)) {
        url = 'https://' + url;
        $('url-input').value = url;
      }
      if (!isValidUrl(url)) { showToast('Please enter a valid URL (e.g. https://example.com)', 'warning'); hideLoading(); return; }
      lastUserInput = url;
      result = await apiPost('/api/scan/url', {
        url: url,
        model: $('url-model').value
      });

    } else if (type === 'social') {
      const text = $('social-input').value.trim();
      if (!text) { showToast('Please paste a social media message to analyze', 'warning'); hideLoading(); return; }
      lastUserInput = text;
      result = await apiPost('/api/scan/social', {
        text:   text,
        source: $('social-source').value,
        model:  $('social-model').value
      });

    } else if (type === 'image') {
      if (!selectedFile) { showToast('Please select an image first', 'warning'); hideLoading(); return; }
      lastUserInput = `Image: ${selectedFile.name}`;
      const formData = new FormData();
      formData.append('file',  selectedFile);
      formData.append('model', $('image-model').value);
      result = await apiPostForm('/api/scan/image', formData);
    }

    lastScanResult = result;
    lastScanType   = type;
    renderResults(result, type);

  } catch (err) {
    const msg = err.message || '';
    const friendlyMsg = msg.includes('Failed to fetch') || msg.includes('NetworkError') || msg.includes('Load failed')
      ? 'Cannot reach the backend server. Make sure the FastAPI server is running on port 8000.'
      : (msg || 'Analysis failed. Please try again.');
    showError(friendlyMsg);
  }
}

// ── API Helpers ───────────────────────────────────────────────────────────────
async function apiPost(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify(body),
    signal:  AbortSignal.timeout(90_000)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

async function apiPostForm(path, formData) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    body:   formData,
    signal: AbortSignal.timeout(90_000)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

function isValidUrl(str) {
  try { return ['http:', 'https:'].includes(new URL(str).protocol); } catch { return false; }
}

// ── Loading / Result States ───────────────────────────────────────────────────
function showLoading(type) {
  const container = $('results-container');
  container.hidden = false;
  $('results-loading').hidden = false;
  $('results-content').hidden = true;
  $('results-error').hidden   = true;

  const labels = { email: 'Analyzing email for phishing…', url: 'Fetching and analyzing webpage…', social: 'Analyzing social media content…', image: 'Running Gemini Vision OCR + analysis…' };
  $('loading-text').textContent = labels[type] || 'Analyzing with Gemini AI…';

  container.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function hideLoading() {
  $('results-loading').hidden = true;
}

function hideResults() {
  $('results-container').hidden = true;
  $('results-loading').hidden   = true;
  $('results-content').hidden   = true;
  $('results-error').hidden     = true;
}

function showError(message) {
  $('results-loading').hidden = true;
  $('results-content').hidden = true;
  $('results-error').hidden   = false;
  $('error-message').textContent = message;
}

// ── Render Results ────────────────────────────────────────────────────────────
function renderResults(data, type) {
  $('results-loading').hidden = true;
  $('results-error').hidden   = true;
  $('results-content').hidden = false;

  // Risk Gauge
  const score = Math.min(100, Math.max(0, data.risk_score || 0));
  animateGauge(score);

  // Threat Badge
  const threat     = data.threat || 'Unknown';
  const badge      = $('threat-badge');
  const classMap   = { 'Safe': 'threat-safe', 'Low Risk': 'threat-low', 'Medium Risk': 'threat-medium', 'High Risk': 'threat-high', 'Critical': 'threat-critical' };
  badge.className  = `threat-badge ${classMap[threat] || 'threat-medium'}`;
  badge.textContent = threat;

  // Summary
  $('result-summary-title').textContent = getScanTitle(type);
  $('result-summary-text').textContent  = data.summary || 'Analysis complete.';

  // Meta
  $('meta-scan-type').textContent = `📋 ${type.charAt(0).toUpperCase() + type.slice(1)} Scan`;
  $('meta-model').textContent     = `🤖 ${data.model_used || 'Gemini'}`;
  $('meta-confidence').textContent = data.confidence != null ? `📊 ${(data.confidence * 100).toFixed(0)}% Confidence` : '';

  // Overview Indicators
  renderIndicators(data, type);

  // Evidence
  renderEvidence(data.evidence || []);

  // Recommendations
  renderRecommendations(data.recommendations || []);

  // Raw JSON
  $('raw-json').textContent = JSON.stringify(data, null, 2);

  // Reset to overview tab
  switchDetailTab('overview');
}

function getScanTitle(type) {
  return { email: 'Email Analysis Complete', url: 'URL Analysis Complete', social: 'Social Media Analysis Complete', image: 'Image Analysis Complete' }[type] || 'Analysis Complete';
}

function animateGauge(score) {
  const fill   = $('gauge-fill');
  const label  = $('gauge-score');
  const radius = 52;
  const circ   = 2 * Math.PI * radius; // 326.726

  // Color based on score
  let color;
  if      (score <= 20) color = '#00E5A0';
  else if (score <= 40) color = '#FFD166';
  else if (score <= 60) color = '#FF8C42';
  else if (score <= 80) color = '#FF4D6A';
  else                  color = '#FF003C';

  fill.style.stroke = color;

  // Animate score number
  let current = 0;
  const step  = score / 40;
  const timer = setInterval(() => {
    current = Math.min(current + step, score);
    label.textContent = Math.round(current);
    const offset = circ - (current / 100) * circ;
    fill.style.strokeDashoffset = offset;
    if (current >= score) clearInterval(timer);
  }, 25);
}

function renderIndicators(data, type) {
  const grid = $('indicators-grid');
  grid.innerHTML = '';

  const fields = getIndicatorFields(data, type);
  fields.forEach(({ label, value }) => {
    if (value === undefined || value === null || (Array.isArray(value) && !value.length)) return;

    const card = document.createElement('div');
    card.className = 'indicator-card';

    let displayVal, valClass = '';
    if (typeof value === 'boolean') {
      displayVal = value ? 'Yes ⚠️' : 'No ✓';
      valClass   = value ? 'value-true' : 'value-false';
    } else if (Array.isArray(value)) {
      displayVal = value.slice(0,3).join(', ') + (value.length > 3 ? ` (+${value.length-3} more)` : '');
      valClass   = 'value-list';
    } else {
      displayVal = String(value);
    }

    card.innerHTML = `
      <div class="indicator-label">${escHtml(label)}</div>
      <div class="indicator-value ${valClass}">${escHtml(displayVal)}</div>
    `;
    grid.appendChild(card);
  });
}

function getIndicatorFields(data, type) {
  const common = [
    { label: 'Risk Score', value: `${data.risk_score}/100` },
    { label: 'Threat Level', value: data.threat },
    { label: 'Confidence', value: data.confidence != null ? `${(data.confidence * 100).toFixed(0)}%` : null },
  ];

  const specific = {
    email: [
      { label: 'Phishing Probability', value: data.phishing_probability != null ? `${(data.phishing_probability * 100).toFixed(0)}%` : null },
      { label: 'Urgency Manipulation', value: data.urgency_manipulation },
      { label: 'Suspicious Links', value: data.suspicious_links },
      { label: 'Social Engineering', value: data.social_engineering_indicators },
      { label: 'Financial Scam Signals', value: data.financial_scam_indicators },
      { label: 'Grammar Anomalies', value: data.grammar_anomalies },
    ],
    url: [
      { label: 'Domain', value: data.domain },
      { label: 'Page Title', value: data.page_title },
      { label: 'SEBI Impersonation', value: data.sebi_impersonation },
      { label: 'Fake Investment Promises', value: data.fake_investment_promises },
      { label: 'Scam Keywords', value: data.scam_keywords },
      { label: 'Urgency Tactics', value: data.urgency_tactics },
    ],
    social: [
      { label: 'Threat Category', value: data.threat_category },
      { label: 'Guaranteed Returns', value: data.guaranteed_returns },
      { label: 'Authority Impersonation', value: data.authority_impersonation },
      { label: 'Pump & Dump Signals', value: data.pump_dump_indicators },
      { label: 'Fake IPO Signals', value: data.fake_ipo_indicators },
      { label: 'Crypto Fraud Signals', value: data.crypto_fraud_indicators },
      { label: 'Recommended Action', value: data.recommended_action },
    ],
    image: [
      { label: 'Extracted Text Length', value: data.text_length != null ? `${data.text_length} chars` : null },
      { label: 'Extracted Text Preview', value: data.extracted_text ? data.extracted_text.slice(0, 120) + '…' : null },
    ],
  };

  return [...common, ...(specific[type] || [])].filter(f => f.value !== null && f.value !== undefined);
}

function renderEvidence(items) {
  const list = $('evidence-list');
  if (!items.length) {
    list.innerHTML = '<div class="evidence-empty">✓ No suspicious evidence found in the content</div>';
    return;
  }
  list.innerHTML = items.map(item => `<div class="evidence-item">${escHtml(String(item))}</div>`).join('');
}

function renderRecommendations(items) {
  const list = $('recommendations-list');
  if (!items.length) {
    list.innerHTML = '<div class="evidence-empty">No specific recommendations</div>';
    return;
  }
  list.innerHTML = items.map((item, i) => `
    <div class="rec-item">
      <span class="rec-number">${i + 1}</span>
      <span>${escHtml(String(item))}</span>
    </div>`).join('');
}

// ── Result Actions ────────────────────────────────────────────────────────────
function initResultActions() {
  $('download-report-btn').addEventListener('click', downloadReport);
  $('new-scan-btn').addEventListener('click', () => {
    hideResults();
    document.querySelector('.scan-section').scrollIntoView({ behavior: 'smooth' });
  });
  $('retry-btn').addEventListener('click', () => {
    hideResults();
    document.querySelector('.scan-section').scrollIntoView({ behavior: 'smooth' });
  });
}

async function downloadReport() {
  if (!lastScanResult || !lastScanType) return;

  const btn = $('download-report-btn');
  const orig = btn.innerHTML;
  btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> Generating…';
  btn.disabled  = true;

  try {
    const res = await fetch(`${API_BASE}/api/report`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({
        scan_result: lastScanResult,
        scan_type:   lastScanType,
        user_input:  lastUserInput,
        model:       'flash'
      }),
      signal: AbortSignal.timeout(120_000)
    });

    if (!res.ok) throw new Error('Report generation failed');

    const blob     = await res.blob();
    const url      = URL.createObjectURL(blob);
    const a        = document.createElement('a');
    const ts       = new Date().toISOString().slice(0,19).replace(/[T:]/g, '-');
    a.href         = url;
    a.download     = `cybershield_report_${lastScanType}_${ts}.pdf`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('📄 PDF report downloaded!', 'success');
  } catch (err) {
    showToast('Report generation failed: ' + err.message, 'error');
  } finally {
    btn.innerHTML = orig;
    btn.disabled  = false;
  }
}

// ── Chat ──────────────────────────────────────────────────────────────────────
function initChat() {
  const input   = $('chat-input');
  const sendBtn = $('chat-send-btn');

  input.addEventListener('input', () => {
    sendBtn.disabled = !input.value.trim();
    // Auto-resize
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 120) + 'px';
  });

  input.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!sendBtn.disabled) sendChat();
    }
  });

  sendBtn.addEventListener('click', sendChat);

  // Quick prompts
  document.querySelectorAll('.quick-prompt').forEach(btn => {
    btn.addEventListener('click', () => {
      input.value = btn.dataset.prompt;
      input.dispatchEvent(new Event('input'));
      sendChat();
    });
  });

  // Clear chat
  $('clear-chat-btn').addEventListener('click', clearChat);
}

async function sendChat() {
  if (isTyping) return;
  const input = $('chat-input');
  const msg   = input.value.trim();
  if (!msg) return;

  // Add user message
  addChatMsg(msg, 'user');
  chatHistory.push({ role: 'user', content: msg });
  input.value = '';
  input.style.height = 'auto';
  $('chat-send-btn').disabled = true;

  // Hide quick prompts after first message
  const qp = $('quick-prompts');
  if (qp) qp.style.display = 'none';

  // Show typing indicator
  const typingEl = addTypingIndicator();
  isTyping = true;

  try {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({
        message: msg,
        history: chatHistory.slice(-20),
        model:   $('chat-model').value
      }),
      signal: AbortSignal.timeout(60_000)
    });

    if (!res.ok) throw new Error('Chat request failed');
    const data = await res.json();

    typingEl.remove();
    const reply = data.reply || 'Sorry, I could not generate a response.';
    addChatMsg(reply, 'ai');
    chatHistory.push({ role: 'assistant', content: reply });

  } catch (err) {
    typingEl.remove();
    addChatMsg('I encountered an issue. Please check if the backend is running and try again.', 'ai');
  } finally {
    isTyping = false;
  }
}

function addChatMsg(text, role) {
  const container = $('chat-messages');
  const div = document.createElement('div');
  div.className = `chat-msg chat-msg-${role}`;

  const avatarHTML = role === 'ai'
    ? `<div class="chat-avatar" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 40 40" fill="none"><path d="M20 2L36 9V21C36 29.8 29.2 38 20 40C10.8 38 4 29.8 4 21V9L20 2Z" fill="#0d1b3e" stroke="#00F5FF" stroke-width="1.5"/><circle cx="20" cy="20" r="5" stroke="#00F5FF" stroke-width="1.5" fill="none"/><circle cx="20" cy="20" r="2" fill="#00F5FF"/></svg></div>`
    : `<div class="chat-avatar" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7B61FF" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>`;

  const formatted = role === 'ai' ? formatChatText(text) : `<p>${escHtml(text)}</p>`;
  div.innerHTML = `${avatarHTML}<div class="chat-bubble">${formatted}</div>`;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
}

function addTypingIndicator() {
  const container = $('chat-messages');
  const div = document.createElement('div');
  div.className = 'chat-msg chat-msg-ai';
  div.innerHTML = `
    <div class="chat-avatar" aria-hidden="true">
      <svg width="20" height="20" viewBox="0 0 40 40" fill="none"><path d="M20 2L36 9V21C36 29.8 29.2 38 20 40C10.8 38 4 29.8 4 21V9L20 2Z" fill="#0d1b3e" stroke="#00F5FF" stroke-width="1.5"/><circle cx="20" cy="20" r="5" stroke="#00F5FF" stroke-width="1.5" fill="none"/><circle cx="20" cy="20" r="2" fill="#00F5FF"/></svg>
    </div>
    <div class="chat-bubble typing-indicator" aria-label="CyberShield AI is typing">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>`;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
}

function clearChat() {
  const messages = $('chat-messages');
  messages.innerHTML = '';
  chatHistory = [];

  // Restore initial message
  const div = document.createElement('div');
  div.className = 'chat-msg chat-msg-ai';
  div.id = 'initial-chat-msg';
  div.innerHTML = `
    <div class="chat-avatar" aria-hidden="true">
      <svg width="20" height="20" viewBox="0 0 40 40" fill="none"><path d="M20 2L36 9V21C36 29.8 29.2 38 20 40C10.8 38 4 29.8 4 21V9L20 2Z" fill="#0d1b3e" stroke="#00F5FF" stroke-width="1.5"/><circle cx="20" cy="20" r="5" stroke="#00F5FF" stroke-width="1.5" fill="none"/><circle cx="20" cy="20" r="2" fill="#00F5FF"/></svg>
    </div>
    <div class="chat-bubble">
      <p>👋 Hello! I'm <strong>CyberShield AI</strong>, your financial safety expert powered by Google Gemini.</p>
      <p>Chat cleared. How can I help you stay safe?</p>
    </div>`;
  messages.appendChild(div);

  // Restore quick prompts
  $('quick-prompts').style.display = '';
}

// ── Text Formatting ───────────────────────────────────────────────────────────
function formatChatText(text) {
  // Escape HTML first, then apply markdown-ish formatting
  let safe = escHtml(text);

  // Bold: **text**
  safe = safe.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  // Italic: *text*
  safe = safe.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  // Inline code: `code`
  safe = safe.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Unordered lists
  safe = safe.replace(/^[•\-\*] (.+)$/gm, '<li>$1</li>');
  safe = safe.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

  // Numbered lists
  safe = safe.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

  // Paragraphs (double newlines)
  safe = safe.split(/\n\n+/).map(block => {
    block = block.trim();
    if (!block) return '';
    if (block.startsWith('<ul>') || block.startsWith('<li>')) return block;
    return `<p>${block.replace(/\n/g, '<br>')}</p>`;
  }).join('');

  return safe || `<p>${safe}</p>`;
}

// ── Toast Notifications ───────────────────────────────────────────────────────
function showToast(message, type = 'info') {
  // Remove existing toast
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.setAttribute('role', 'alert');
  toast.setAttribute('aria-live', 'assertive');
  toast.innerHTML = `<span>${escHtml(message)}</span>`;

  // Inline styles for toast (self-contained)
  const colors = { success: '#00E5A0', error: '#FF4D6A', warning: '#FFD166', info: '#00F5FF' };
  const color = colors[type] || colors.info;
  Object.assign(toast.style, {
    position: 'fixed',
    bottom: '24px',
    right:  '24px',
    padding: '12px 20px',
    borderRadius: '10px',
    background: `rgba(6,11,24,0.95)`,
    border: `1px solid ${color}`,
    color: color,
    fontSize: '0.88rem',
    fontWeight: '600',
    fontFamily: 'Inter, sans-serif',
    zIndex: '9999',
    boxShadow: `0 4px 20px rgba(0,0,0,0.5)`,
    animation: 'fadeSlideUp .3s ease both',
    maxWidth: '360px',
    backdropFilter: 'blur(12px)',
  });

  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'none';
    toast.style.opacity   = '0';
    toast.style.transition = 'opacity .3s';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// ── Utility ───────────────────────────────────────────────────────────────────
function escHtml(str) {
  if (typeof str !== 'string') return String(str ?? '');
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}
