import pathlib

css = """/* ============================================================
   SEBI CyberShield - Ultra-Premium Cyber UI v2.0
   Design: Deep Space + Electric Cyber + Glassmorphism
   ============================================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Space+Grotesk:wght@300..700&display=swap');

/* ================================================================
   CSS CUSTOM PROPERTIES
================================================================ */
:root {
  --cyan:           #00F5FF;
  --cyan-bright:    #40FDFF;
  --cyan-dim:       #00C8D4;
  --purple:         #7B61FF;
  --purple-bright:  #9B84FF;
  --purple-dim:     #5B41DF;
  --emerald:        #00E5A0;
  --orange:         #FF8C42;
  --red:            #FF4D6A;
  --red-bright:     #FF003C;
  --yellow:         #FFD166;

  /* Backgrounds */
  --bg-void:        #030509;
  --bg-primary:     #060B18;
  --bg-secondary:   #090F1E;
  --bg-card:        rgba(10, 17, 35, 0.87);
  --bg-input:       rgba(0, 0, 0, 0.4);

  /* Borders */
  --border-subtle:  rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.1);
  --border-bright:  rgba(255, 255, 255, 0.18);
  --border-cyan:    rgba(0, 245, 255, 0.3);
  --border-purple:  rgba(123, 97, 255, 0.3);

  /* Text */
  --text-primary:   #EDF2FF;
  --text-secondary: #8A9BBE;
  --text-muted:     #4A5878;
  --text-ghost:     #2A3550;

  /* Gradients */
  --grad-primary:     linear-gradient(135deg, var(--cyan) 0%, var(--purple) 100%);
  --grad-primary-rev: linear-gradient(135deg, var(--purple) 0%, var(--cyan) 100%);
  --grad-section:     linear-gradient(180deg, transparent, rgba(123,97,255,0.025), transparent);

  /* Shadows */
  --shadow-sm:          0 2px 8px rgba(0,0,0,0.3);
  --shadow-md:          0 8px 32px rgba(0,0,0,0.5);
  --shadow-lg:          0 20px 60px rgba(0,0,0,0.6);
  --shadow-glow-cyan:   0 0 40px rgba(0,245,255,0.2), 0 0 80px rgba(0,245,255,0.06);
  --shadow-glow-purple: 0 0 40px rgba(123,97,255,0.2);
  --shadow-card:        0 4px 24px rgba(0,0,0,0.4), 0 0 1px rgba(255,255,255,0.06) inset;
  --shadow-btn:         0 4px 24px rgba(0,245,255,0.25), 0 0 0 1px rgba(0,245,255,0.15) inset;
  --shadow-input-focus: 0 0 0 3px rgba(0,245,255,0.1);

  /* Layout */
  --navbar-h:   68px;
  --radius-sm:  10px;
  --radius:     14px;
  --radius-lg:  20px;
  --radius-xl:  28px;
  --radius-full:9999px;

  /* Typography */
  --font-display: 'Space Grotesk', 'Inter', system-ui, sans-serif;
  --font-sans:    'Inter', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace;

  /* Easing */
  --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-out:    cubic-bezier(0, 0, 0.2, 1);
  --t-fast:   0.15s;
  --t-normal: 0.25s;
  --t-slow:   0.4s;
}

/* ================================================================
   RESET & BASE
================================================================ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; font-size: 16px; -webkit-text-size-adjust: 100%; }

body {
  background: var(--bg-void);
  color: var(--text-primary);
  font-family: var(--font-sans);
  line-height: 1.6;
  min-height: 100vh;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

a { color: var(--cyan); text-decoration: none; transition: color var(--t-fast) var(--ease-smooth); }
a:hover { color: var(--cyan-bright); }
ul { list-style: none; }
img, svg { display: block; }
button { font-family: var(--font-sans); }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: rgba(0,245,255,0.2); border-radius: var(--radius-full); }
::-webkit-scrollbar-thumb:hover { background: rgba(0,245,255,0.4); }

::selection { background: rgba(0,245,255,0.2); color: var(--text-primary); }

/* ================================================================
   BACKGROUND SYSTEM
================================================================ */
.bg-grid {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,245,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,245,255,0.025) 1px, transparent 1px);
  background-size: 72px 72px;
  pointer-events: none;
  z-index: 0;
}

.bg-grid::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(123,97,255,0.012) 1px, transparent 1px),
    linear-gradient(90deg, rgba(123,97,255,0.012) 1px, transparent 1px);
  background-size: 24px 24px;
}

.bg-orb {
  position: fixed;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(100px);
  z-index: 0;
}

.bg-orb-1 {
  width: 800px; height: 800px;
  top: -300px; right: -250px;
  background: radial-gradient(circle, rgba(0,245,255,0.07) 0%, rgba(0,245,255,0.02) 40%, transparent 70%);
  animation: orbDrift1 25s ease-in-out infinite;
}

.bg-orb-2 {
  width: 700px; height: 700px;
  bottom: 0; left: -200px;
  background: radial-gradient(circle, rgba(123,97,255,0.07) 0%, rgba(123,97,255,0.02) 40%, transparent 70%);
  animation: orbDrift2 32s ease-in-out infinite;
}

.bg-orb-3 {
  width: 400px; height: 400px;
  top: 40%; left: 50%;
  transform: translateX(-50%);
  background: radial-gradient(circle, rgba(0,229,160,0.04) 0%, transparent 70%);
  animation: orbDrift3 20s ease-in-out infinite;
}

@keyframes orbDrift1 {
  0%, 100% { transform: translate(0,0) scale(1); }
  25%  { transform: translate(-40px, 30px) scale(1.05); }
  50%  { transform: translate(-20px,-40px) scale(0.95); }
  75%  { transform: translate(30px,  20px) scale(1.02); }
}
@keyframes orbDrift2 {
  0%, 100% { transform: translate(0,0) scale(1); }
  33% { transform: translate(35px,-25px) scale(1.04); }
  66% { transform: translate(-20px,40px) scale(0.97); }
}
@keyframes orbDrift3 {
  0%, 100% { transform: translateX(-50%) scale(1); opacity: 0.6; }
  50%       { transform: translateX(-50%) scale(1.3); opacity: 1;   }
}

/* ================================================================
   UTILITIES
================================================================ */
.gradient-text {
  background: var(--grad-primary);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.gradient-text-rev {
  background: var(--grad-primary-rev);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ================================================================
   BUTTONS
================================================================ */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 22px;
  border-radius: var(--radius);
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition:
    transform var(--t-fast) var(--ease-spring),
    box-shadow var(--t-normal) var(--ease-smooth),
    opacity var(--t-fast);
  font-family: var(--font-sans);
  letter-spacing: 0.01em;
  text-decoration: none;
  position: relative;
  overflow: hidden;
  white-space: nowrap;
}

.btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, transparent 60%);
  opacity: 0;
  transition: opacity var(--t-fast);
}

.btn:hover::before { opacity: 1; }
.btn:focus-visible { outline: 2px solid var(--cyan); outline-offset: 3px; }

.btn-primary {
  background: var(--grad-primary);
  color: #fff;
  box-shadow: var(--shadow-btn);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 40px rgba(0,245,255,0.4), 0 0 0 1px rgba(0,245,255,0.2) inset;
}

.btn-primary:active { transform: translateY(0); }

.btn-primary:disabled {
  opacity: 0.35;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-ghost {
  background: rgba(255,255,255,0.04);
  color: var(--text-secondary);
  border: 1px solid var(--border-default);
}

.btn-ghost:hover {
  background: rgba(255,255,255,0.08);
  color: var(--text-primary);
  border-color: var(--border-bright);
}

.btn-sm  { padding: 7px 14px; font-size: 0.8rem; border-radius: var(--radius-sm); }
.btn-lg  { padding: 15px 30px; font-size: 1rem; }
.btn-icon { width: 42px; height: 42px; padding: 0; border-radius: var(--radius); }

/* ================================================================
   NAVBAR
================================================================ */
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: var(--navbar-h);
  z-index: 1000;
}

.navbar::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(4,7,16,0.75);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-bottom: 1px solid var(--border-subtle);
  transition: all var(--t-slow) var(--ease-smooth);
}

.navbar.scrolled::before {
  background: rgba(4,7,16,0.95);
  border-bottom-color: var(--border-default);
  box-shadow: 0 1px 30px rgba(0,0,0,0.4), 0 0 1px rgba(0,245,255,0.08);
}

.nav-inner {
  position: relative;
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 28px;
  height: 100%;
  display: flex;
  align-items: center;
  gap: 40px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: var(--text-primary);
  flex-shrink: 0;
}

.nav-logo {
  width: 38px; height: 38px;
  animation: logoPulse 4s ease-in-out infinite;
}

@keyframes logoPulse {
  0%, 100% { filter: drop-shadow(0 0 8px rgba(0,245,255,0.5)) drop-shadow(0 0 16px rgba(0,245,255,0.2)); }
  50%       { filter: drop-shadow(0 0 16px rgba(0,245,255,0.8)) drop-shadow(0 0 30px rgba(0,245,255,0.35)); }
}

.nav-brand-text { display: flex; flex-direction: column; line-height: 1.1; gap: 1px; }

.nav-brand-name {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 700;
  background: var(--grad-primary);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.01em;
}

.nav-brand-tag {
  font-size: 0.6rem;
  color: var(--text-muted);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 500;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2px;
  margin-left: auto;
}

.nav-link {
  position: relative;
  padding: 7px 16px;
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  transition: color var(--t-fast), background var(--t-fast);
  text-decoration: none;
  letter-spacing: 0.01em;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 4px; left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 16px; height: 1.5px;
  background: var(--grad-primary);
  border-radius: var(--radius-full);
  transition: transform var(--t-normal) var(--ease-spring);
}

.nav-link:hover { color: var(--text-primary); background: rgba(255,255,255,0.05); }
.nav-link:hover::after { transform: translateX(-50%) scaleX(1); }

.nav-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-subtle);
  font-size: 0.75rem;
  color: var(--text-muted);
  background: rgba(255,255,255,0.02);
  flex-shrink: 0;
  transition: all var(--t-normal);
}

.nav-status.is-online {
  border-color: rgba(0,229,160,0.3);
  background: rgba(0,229,160,0.04);
}

.status-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.status-checking { background: var(--yellow); animation: blink 1.2s ease-in-out infinite; }
.status-online   { background: var(--emerald); box-shadow: 0 0 8px var(--emerald); }
.status-offline  { background: var(--red); }

@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.25} }

/* ================================================================
   HERO SECTION
================================================================ */
.hero {
  min-height: 100vh;
  padding: calc(var(--navbar-h) + 80px) 28px 80px;
  max-width: 1320px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 60px;
  position: relative;
  z-index: 1;
}

.hero-content { flex: 1; max-width: 660px; }

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  border-radius: var(--radius-full);
  border: 1px solid rgba(0,245,255,0.28);
  background: rgba(0,245,255,0.06);
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--cyan-dim);
  letter-spacing: 0.07em;
  text-transform: uppercase;
  margin-bottom: 28px;
  animation: fadeSlideUp 0.7s var(--ease-out) both;
  position: relative;
  overflow: hidden;
}

.hero-badge::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(0,245,255,0.08), transparent);
  animation: badgeShimmer 3s ease-in-out infinite;
}

@keyframes badgeShimmer {
  0%, 100% { transform: translateX(-100%); }
  50%       { transform: translateX(100%); }
}

.hero-badge-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--cyan);
  box-shadow: 0 0 8px var(--cyan);
  animation: dotPulse 1.5s ease-in-out infinite;
  flex-shrink: 0;
}

@keyframes dotPulse {
  0%,100% { box-shadow: 0 0 4px var(--cyan); }
  50%     { box-shadow: 0 0 12px var(--cyan), 0 0 20px rgba(0,245,255,0.4); }
}

.hero-heading {
  font-family: var(--font-display);
  font-size: clamp(2.4rem, 5.5vw, 4rem);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.03em;
  margin-bottom: 22px;
  animation: fadeSlideUp 0.7s 0.1s var(--ease-out) both;
}

.hero-subtext {
  font-size: 1.05rem;
  color: var(--text-secondary);
  line-height: 1.75;
  margin-bottom: 40px;
  max-width: 540px;
  animation: fadeSlideUp 0.7s 0.2s var(--ease-out) both;
}

.hero-actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 56px;
  animation: fadeSlideUp 0.7s 0.3s var(--ease-out) both;
}

.hero-actions .btn { padding: 14px 28px; font-size: 0.95rem; }

.hero-stats {
  display: flex;
  align-items: center;
  animation: fadeSlideUp 0.7s 0.4s var(--ease-out) both;
}

.hero-stat { display: flex; flex-direction: column; padding: 0 28px; }
.hero-stat:first-child { padding-left: 0; }

.stat-value {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 800;
  background: var(--grad-primary);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1;
  letter-spacing: -0.02em;
}

.stat-label {
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-top: 4px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 500;
}

.hero-stat-divider {
  width: 1px; height: 40px;
  background: linear-gradient(180deg, transparent, var(--border-default), transparent);
}

/* Hero Visual */
.hero-visual {
  flex: 0 0 460px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  animation: fadeSlideUp 0.7s 0.25s var(--ease-out) both;
}

.threat-orb {
  position: relative;
  width: 380px; height: 380px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.threat-ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid;
  pointer-events: none;
}

.ring-1 {
  width: 100%; height: 100%;
  border-color: rgba(0,245,255,0.08);
  animation: ringRotate 30s linear infinite;
}

.ring-2 {
  width: 78%; height: 78%;
  border-color: rgba(0,245,255,0.14);
  animation: ringRotate 20s linear infinite reverse;
  border-style: dashed;
}

.ring-3 {
  width: 56%; height: 56%;
  border-color: rgba(0,245,255,0.22);
  animation: ringPulse 4s ease-in-out infinite;
}

.ring-4 {
  width: 38%; height: 38%;
  border-color: rgba(123,97,255,0.35);
  animation: ringRotate 12s linear infinite;
}

@keyframes ringRotate { to { transform: rotate(360deg); } }

@keyframes ringPulse {
  0%,100% { transform: scale(1); opacity: 0.6; border-color: rgba(0,245,255,0.22); }
  50%     { transform: scale(1.06); opacity: 1; border-color: rgba(0,245,255,0.4); }
}

.ring-dot {
  position: absolute;
  width: 6px; height: 6px;
  background: var(--cyan);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--cyan);
}

.ring-dot-1 { top: -3px; left: 50%; transform: translateX(-50%); }
.ring-dot-2 { bottom: -3px; left: 50%; transform: translateX(-50%); }
.ring-dot-3 { left: -3px; top: 50%; transform: translateY(-50%); background: var(--purple); box-shadow: 0 0 10px var(--purple); }
.ring-dot-4 { right: -3px; top: 50%; transform: translateY(-50%); background: var(--purple); box-shadow: 0 0 10px var(--purple); }

.threat-core {
  position: relative;
  width: 120px; height: 120px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at center, rgba(0,245,255,0.12) 0%, rgba(123,97,255,0.06) 50%, transparent 70%);
  animation: coreGlow 3s ease-in-out infinite alternate;
}

@keyframes coreGlow {
  from { box-shadow: 0 0 30px rgba(0,245,255,0.25), 0 0 60px rgba(0,245,255,0.08); }
  to   { box-shadow: 0 0 60px rgba(0,245,255,0.5), 0 0 100px rgba(0,245,255,0.15), 0 0 140px rgba(123,97,255,0.08); }
}

.threat-tag {
  position: absolute;
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border: 1px solid;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 6px;
}

.threat-tag-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; }

.tag-1 {
  top: 4%; left: 50%; transform: translateX(-50%);
  background: rgba(255,77,106,0.12); border-color: rgba(255,77,106,0.4); color: #FF4D6A;
  animation: tagFloat1 5s ease-in-out infinite;
}
.tag-1 .threat-tag-dot { background: #FF4D6A; box-shadow: 0 0 6px #FF4D6A; }

.tag-2 {
  right: -24px; top: 35%;
  background: rgba(255,209,102,0.1); border-color: rgba(255,209,102,0.35); color: #FFD166;
  animation: tagFloat2 6s ease-in-out infinite 0.8s;
}
.tag-2 .threat-tag-dot { background: #FFD166; box-shadow: 0 0 6px #FFD166; }

.tag-3 {
  bottom: 4%; left: 50%; transform: translateX(-50%);
  background: rgba(123,97,255,0.12); border-color: rgba(123,97,255,0.4); color: #9B84FF;
  animation: tagFloat1 7s ease-in-out infinite 1.6s;
}
.tag-3 .threat-tag-dot { background: #9B84FF; box-shadow: 0 0 6px #9B84FF; }

.tag-4 {
  left: -32px; top: 35%;
  background: rgba(0,229,160,0.1); border-color: rgba(0,229,160,0.35); color: #00E5A0;
  animation: tagFloat2 5.5s ease-in-out infinite 2.4s;
}
.tag-4 .threat-tag-dot { background: #00E5A0; box-shadow: 0 0 6px #00E5A0; }

@keyframes tagFloat1 {
  0%,100% { transform: translateX(-50%) translateY(0); }
  50%     { transform: translateX(-50%) translateY(-10px); }
}
@keyframes tagFloat2 {
  0%,100% { transform: translateY(0); }
  50%     { transform: translateY(-10px); }
}

@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

/* ================================================================
   SHARED SECTION STYLES
================================================================ */
.section-container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 28px;
  position: relative;
  z-index: 1;
}

.section-header { text-align: center; margin-bottom: 52px; }

.section-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 14px;
  border-radius: var(--radius-full);
  background: rgba(0,245,255,0.06);
  border: 1px solid rgba(0,245,255,0.18);
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--cyan-dim);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 16px;
}

.section-title {
  font-family: var(--font-display);
  font-size: clamp(1.9rem, 3.5vw, 2.8rem);
  font-weight: 800;
  letter-spacing: -0.025em;
  line-height: 1.1;
  margin-bottom: 14px;
}

.section-subtitle {
  font-size: 1rem;
  color: var(--text-secondary);
  max-width: 500px;
  margin: 0 auto;
  line-height: 1.7;
}

/* ================================================================
   SCAN SECTION
================================================================ */
.scan-section {
  padding: 120px 0;
  position: relative;
}

.scan-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--grad-section);
  pointer-events: none;
}

.scan-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-card), var(--shadow-md);
  backdrop-filter: blur(28px) saturate(150%);
  -webkit-backdrop-filter: blur(28px) saturate(150%);
  position: relative;
}

.scan-panel::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: var(--grad-primary);
  opacity: 0.5;
  z-index: 1;
}

.scan-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-subtle);
  padding: 0 8px;
  background: rgba(0,0,0,0.25);
  overflow-x: auto;
  scrollbar-width: none;
  gap: 4px;
}
.scan-tabs::-webkit-scrollbar { display: none; }

.scan-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 20px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  cursor: pointer;
  border: none;
  background: transparent;
  border-bottom: 2px solid transparent;
  transition: color var(--t-fast), border-color var(--t-fast), background var(--t-fast);
  white-space: nowrap;
  font-family: var(--font-sans);
  margin-bottom: -1px;
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
}

.scan-tab:hover { color: var(--text-primary); background: rgba(255,255,255,0.03); }
.scan-tab:focus-visible { outline: 2px solid var(--cyan); outline-offset: -2px; }
.scan-tab.active { color: var(--cyan); border-bottom-color: var(--cyan); background: rgba(0,245,255,0.04); }

.scan-body { padding: 32px; }

.scan-panel-content { display: none; }
.scan-panel-content.active { display: block; animation: fadeIn 0.2s var(--ease-out); }

.scan-form-row { display: flex; gap: 16px; margin-bottom: 22px; }

.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group.flex-1 { flex: 1; }

.form-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
  display: flex;
  flex-direction: column;
  gap: 2px;
  letter-spacing: 0.02em;
}

.form-hint { font-size: 0.72rem; font-weight: 400; color: var(--text-muted); }

.form-input,
.form-select,
.form-textarea {
  background: var(--bg-input);
  border: 1px solid var(--border-default);
  border-radius: var(--radius);
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-size: 0.9rem;
  padding: 11px 16px;
  transition: border-color var(--t-fast), box-shadow var(--t-fast), background var(--t-fast);
  outline: none;
  width: 100%;
}

.form-input:hover, .form-select:hover, .form-textarea:hover {
  border-color: var(--border-bright);
  background: rgba(0,0,0,0.5);
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  border-color: var(--cyan);
  background: rgba(0,0,0,0.5);
  box-shadow: var(--shadow-input-focus);
}

.form-textarea { resize: vertical; min-height: 140px; font-size: 0.875rem; line-height: 1.65; }
.form-textarea::placeholder, .form-input::placeholder { color: var(--text-ghost); font-size: 0.82rem; }

.form-select {
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%238A9BBE' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 40px;
}

.form-select option { background: #0d1b3e; color: var(--text-primary); }
.form-select-sm { padding: 7px 36px 7px 12px; font-size: 0.8rem; border-radius: var(--radius-sm); }

.url-info-box {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  padding: 14px 18px;
  border-radius: var(--radius);
  background: rgba(0,245,255,0.04);
  border: 1px solid rgba(0,245,255,0.15);
  font-size: 0.84rem;
  color: var(--text-secondary);
  margin-bottom: 24px;
  line-height: 1.55;
}
.url-info-box svg { color: var(--cyan); flex-shrink: 0; margin-top: 2px; }

.scan-actions { display: flex; align-items: center; gap: 12px; margin-top: 24px; }

/* Drop Zone */
.drop-zone {
  border: 2px dashed var(--border-default);
  border-radius: var(--radius-lg);
  padding: 52px 40px;
  text-align: center;
  cursor: pointer;
  transition: border-color var(--t-normal), background var(--t-normal), box-shadow var(--t-normal);
  background: rgba(0,0,0,0.25);
  position: relative;
  overflow: hidden;
  margin-bottom: 4px;
}

.drop-zone:hover, .drop-zone.drag-over {
  border-color: var(--cyan);
  background: rgba(0,245,255,0.04);
  box-shadow: 0 0 0 1px rgba(0,245,255,0.15), var(--shadow-glow-cyan);
}

.drop-zone:focus-visible { outline: 2px solid var(--cyan); outline-offset: 3px; }
.drop-zone-inner { pointer-events: none; }

.drop-icon {
  color: var(--text-muted);
  margin-bottom: 16px;
  display: flex;
  justify-content: center;
  transition: color var(--t-normal), transform var(--t-normal) var(--ease-spring);
}

.drop-zone:hover .drop-icon { color: var(--cyan); transform: scale(1.1) translateY(-2px); }

.drop-title { font-size: 1.05rem; font-weight: 700; color: var(--text-primary); margin-bottom: 8px; }
.drop-subtitle { font-size: 0.82rem; color: var(--text-muted); margin-bottom: 20px; }
.drop-preview { width: 100%; max-height: 300px; object-fit: contain; border-radius: var(--radius); }

/* ================================================================
   RESULTS PANEL
================================================================ */
.results-container {
  margin-top: 32px;
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-card), var(--shadow-md);
  backdrop-filter: blur(28px);
  -webkit-backdrop-filter: blur(28px);
  animation: fadeSlideUp 0.4s var(--ease-out);
  position: relative;
}

.results-container::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: var(--grad-primary);
  opacity: 0.4;
}

.results-loading { padding: 80px 40px; text-align: center; }

.loading-spinner {
  position: relative;
  width: 72px; height: 72px;
  margin: 0 auto 24px;
}

.spinner-ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: var(--cyan);
  border-right-color: var(--purple);
  animation: spinRing 1s linear infinite;
}

.spinner-ring-2 {
  position: absolute;
  inset: 8px;
  border-radius: 50%;
  border: 2px solid transparent;
  border-bottom-color: var(--cyan);
  animation: spinRing 1.5s linear infinite reverse;
  opacity: 0.5;
}

.spinner-pulse {
  position: absolute;
  inset: 18px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0,245,255,0.3), transparent);
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes spinRing { to { transform: rotate(360deg); } }
@keyframes pulse {
  0%,100% { transform: scale(0.9); opacity: 0.5; }
  50%     { transform: scale(1.1); opacity: 1; }
}

.loading-text { font-size: 1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 6px; }
.loading-sub { font-size: 0.82rem; color: var(--text-muted); }

.loading-bar {
  width: 200px; height: 2px;
  background: var(--border-subtle);
  border-radius: var(--radius-full);
  margin: 20px auto 0;
  overflow: hidden;
}

.loading-bar-fill {
  height: 100%;
  background: var(--grad-primary);
  border-radius: var(--radius-full);
  animation: loadingProgress 8s ease-in-out infinite;
}

@keyframes loadingProgress {
  0%  { width: 0%; }
  80% { width: 90%; }
  100%{ width: 90%; }
}

.result-header {
  display: flex;
  align-items: flex-start;
  gap: 28px;
  padding: 32px;
  border-bottom: 1px solid var(--border-subtle);
  flex-wrap: wrap;
  background: linear-gradient(135deg, rgba(0,245,255,0.02) 0%, rgba(123,97,255,0.02) 100%);
}

.risk-gauge { position: relative; width: 128px; height: 128px; flex-shrink: 0; }

.gauge-svg {
  width: 100%; height: 100%;
  transform: rotate(-90deg);
  filter: drop-shadow(0 0 8px rgba(0,245,255,0.1));
}

.gauge-bg { fill: none; stroke: rgba(255,255,255,0.05); stroke-width: 8; }

.gauge-fill {
  fill: none;
  stroke-width: 8;
  stroke-linecap: round;
  stroke: var(--cyan);
  transition: stroke-dashoffset 1.2s cubic-bezier(0.4,0,0.2,1), stroke 0.5s;
  stroke-dasharray: 326.726;
  stroke-dashoffset: 326.726;
}

.gauge-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.gauge-score {
  font-family: var(--font-display);
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1;
  letter-spacing: -0.02em;
}

.gauge-label {
  font-size: 0.6rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-top: 3px;
  font-weight: 600;
}

.result-summary { flex: 1; min-width: 200px; }

.threat-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 14px;
  border-radius: var(--radius-full);
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 12px;
  border: 1px solid;
}

.threat-safe     { background: rgba(0,229,160,.1);  border-color: rgba(0,229,160,.35); color: var(--emerald); }
.threat-low      { background: rgba(255,209,102,.1); border-color: rgba(255,209,102,.35); color: var(--yellow); }
.threat-medium   { background: rgba(255,140,66,.1);  border-color: rgba(255,140,66,.35); color: var(--orange); }
.threat-high     { background: rgba(255,77,106,.1);  border-color: rgba(255,77,106,.35); color: var(--red); }
.threat-critical {
  background: rgba(255,0,60,.12);
  border-color: rgba(255,0,60,.5);
  color: var(--red-bright);
  box-shadow: 0 0 16px rgba(255,0,60,.15);
  animation: criticalPulse 2s ease-in-out infinite;
}

@keyframes criticalPulse {
  0%,100% { box-shadow: 0 0 16px rgba(255,0,60,.15); }
  50%     { box-shadow: 0 0 28px rgba(255,0,60,.35); }
}

.result-summary-title {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: -0.01em;
}

.result-summary-text { font-size: 0.9rem; color: var(--text-secondary); line-height: 1.65; margin-bottom: 14px; }
.result-meta { display: flex; gap: 8px; flex-wrap: wrap; }

.meta-item {
  font-size: 0.72rem;
  font-weight: 500;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border-subtle);
  color: var(--text-muted);
  font-family: var(--font-mono);
}

.result-actions { display: flex; flex-direction: column; gap: 10px; flex-shrink: 0; }

.detail-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-subtle);
  padding: 0 32px;
  background: rgba(0,0,0,0.15);
  gap: 4px;
}

.detail-tab {
  padding: 13px 18px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-muted);
  border: none;
  background: transparent;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: color var(--t-fast), border-color var(--t-fast);
  font-family: var(--font-sans);
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
}

.detail-tab:hover { color: var(--text-primary); }
.detail-tab:focus-visible { outline: 2px solid var(--cyan); }
.detail-tab.active { color: var(--cyan); border-bottom-color: var(--cyan); }

.detail-body { padding: 28px 32px; }
.detail-panel { display: none; }
.detail-panel.active { display: block; animation: fadeIn 0.2s var(--ease-out); }

.indicators-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 14px;
}

.indicator-card {
  padding: 16px 18px;
  border-radius: var(--radius);
  border: 1px solid var(--border-subtle);
  background: rgba(0,0,0,0.2);
  transition: border-color var(--t-fast), box-shadow var(--t-fast);
}

.indicator-card:hover { border-color: var(--border-default); box-shadow: var(--shadow-sm); }

.indicator-label {
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 8px;
}

.indicator-value { font-size: 0.9rem; font-weight: 600; color: var(--text-primary); word-break: break-word; }
.indicator-value.value-true  { color: var(--red); }
.indicator-value.value-false { color: var(--emerald); }
.indicator-value.value-list  { font-size: 0.82rem; font-weight: 400; color: var(--text-secondary); }

.evidence-list { display: flex; flex-direction: column; gap: 10px; }

.evidence-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 18px;
  border-radius: var(--radius);
  border: 1px solid rgba(255,77,106,0.18);
  background: rgba(255,77,106,0.04);
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.55;
  transition: border-color var(--t-fast);
}

.evidence-item:hover { border-color: rgba(255,77,106,0.35); }

.evidence-item::before {
  content: '!';
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px; height: 22px;
  border-radius: 50%;
  background: rgba(255,77,106,0.18);
  color: var(--red);
  font-size: 0.65rem;
  font-weight: 800;
  flex-shrink: 0;
  margin-top: 1px;
}

.evidence-empty { text-align: center; padding: 40px; color: var(--text-muted); font-size: 0.9rem; }

.recommendations-list { display: flex; flex-direction: column; gap: 10px; }

.rec-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 16px 18px;
  border-radius: var(--radius);
  background: rgba(0,229,160,0.04);
  border: 1px solid rgba(0,229,160,0.14);
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.55;
  transition: border-color var(--t-fast);
}

.rec-item:hover { border-color: rgba(0,229,160,0.3); }

.rec-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px; height: 24px;
  border-radius: 50%;
  background: rgba(0,229,160,0.15);
  color: var(--emerald);
  font-size: 0.72rem;
  font-weight: 800;
  flex-shrink: 0;
  border: 1px solid rgba(0,229,160,0.25);
}

.raw-json {
  background: rgba(0,0,0,0.5);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius);
  padding: 24px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--cyan-dim);
  overflow: auto;
  max-height: 420px;
  white-space: pre-wrap;
  word-break: break-all;
  line-height: 1.7;
}

.results-error { padding: 72px 40px; text-align: center; }
.error-icon { color: var(--red); margin-bottom: 18px; display: flex; justify-content: center; }
.error-title { font-family: var(--font-display); font-size: 1.25rem; font-weight: 700; margin-bottom: 10px; }
.error-message { font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 24px; max-width: 420px; margin-left: auto; margin-right: auto; line-height: 1.6; }

/* ================================================================
   CHAT SECTION
================================================================ */
.chat-section {
  padding: 120px 0;
  position: relative;
}

.chat-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 60% 50% at 50% 50%, rgba(123,97,255,0.04) 0%, transparent 70%);
  pointer-events: none;
}

.chat-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 700px;
  box-shadow: var(--shadow-card), var(--shadow-md);
  backdrop-filter: blur(28px) saturate(150%);
  -webkit-backdrop-filter: blur(28px) saturate(150%);
  position: relative;
}

.chat-wrapper::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: var(--grad-primary-rev);
  opacity: 0.5;
  z-index: 1;
}

.chat-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 22px;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(0,0,0,0.2);
  flex-shrink: 0;
}

.chat-toolbar-left { display: flex; align-items: center; gap: 12px; }

.chat-ai-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.chat-ai-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--emerald);
  box-shadow: 0 0 8px var(--emerald);
  animation: chatDotPulse 2s ease-in-out infinite;
}

@keyframes chatDotPulse {
  0%,100% { box-shadow: 0 0 4px var(--emerald); }
  50%     { box-shadow: 0 0 12px var(--emerald), 0 0 24px rgba(0,229,160,0.3); }
}

.chat-model-select { display: flex; align-items: center; gap: 10px; }
.chat-model-select .form-label { font-size: 0.78rem; margin: 0; flex-direction: row; color: var(--text-muted); }

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px 22px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  scrollbar-width: thin;
  scrollbar-color: rgba(0,245,255,0.15) transparent;
}

.chat-messages::-webkit-scrollbar { width: 4px; }
.chat-messages::-webkit-scrollbar-track { background: transparent; }
.chat-messages::-webkit-scrollbar-thumb { background: rgba(0,245,255,0.15); border-radius: var(--radius-full); }

.chat-msg {
  display: flex;
  gap: 12px;
  max-width: 82%;
  animation: fadeSlideUp 0.3s var(--ease-out) both;
}

.chat-msg-user { align-self: flex-end; flex-direction: row-reverse; }

.chat-avatar {
  width: 34px; height: 34px;
  border-radius: 50%;
  background: rgba(0,245,255,0.08);
  border: 1px solid rgba(0,245,255,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 0 10px rgba(0,245,255,0.1);
}

.chat-msg-user .chat-avatar {
  background: rgba(123,97,255,0.12);
  border-color: rgba(123,97,255,0.28);
  box-shadow: 0 0 10px rgba(123,97,255,0.15);
}

.chat-bubble {
  padding: 14px 18px;
  border-radius: 18px;
  font-size: 0.9rem;
  line-height: 1.68;
  color: var(--text-primary);
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border-subtle);
}

.chat-msg-ai .chat-bubble   { border-radius: 4px 18px 18px 18px; }
.chat-msg-user .chat-bubble { background: rgba(123,97,255,0.1); border-color: rgba(123,97,255,0.22); border-radius: 18px 4px 18px 18px; }

.chat-bubble p { margin-bottom: 8px; }
.chat-bubble p:last-child { margin-bottom: 0; }
.chat-bubble ul { margin: 8px 0 8px 16px; list-style: disc; }
.chat-bubble ul li { margin-bottom: 4px; color: var(--text-secondary); }
.chat-bubble strong { color: var(--cyan); }

.typing-indicator {
  display: flex;
  gap: 5px;
  align-items: center;
  padding: 14px 18px;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 4px 18px 18px 18px;
}

.typing-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--cyan);
  opacity: 0.4;
  animation: typingBounce 1.4s ease-in-out infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typingBounce {
  0%,100% { transform: translateY(0); opacity: 0.4; }
  50%     { transform: translateY(-6px); opacity: 1; }
}

.quick-prompts {
  display: flex;
  gap: 8px;
  padding: 12px 22px;
  overflow-x: auto;
  border-top: 1px solid var(--border-subtle);
  scrollbar-width: none;
  flex-shrink: 0;
}
.quick-prompts::-webkit-scrollbar { display: none; }

.quick-prompt {
  padding: 7px 16px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-default);
  background: rgba(255,255,255,0.03);
  color: var(--text-secondary);
  font-size: 0.78rem;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  transition: border-color var(--t-fast), color var(--t-fast), background var(--t-fast), transform var(--t-fast) var(--ease-spring);
  font-family: var(--font-sans);
}

.quick-prompt:hover {
  border-color: var(--border-cyan);
  color: var(--cyan);
  background: rgba(0,245,255,0.05);
  transform: translateY(-1px);
}

.quick-prompt:focus-visible { outline: 2px solid var(--cyan); outline-offset: 2px; }

.chat-input-area {
  padding: 16px 22px;
  border-top: 1px solid var(--border-subtle);
  flex-shrink: 0;
  background: rgba(0,0,0,0.15);
}

.chat-input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  background: rgba(0,0,0,0.4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: 8px 8px 8px 16px;
  transition: border-color var(--t-fast), box-shadow var(--t-fast);
}

.chat-input-wrapper:focus-within {
  border-color: var(--purple);
  box-shadow: 0 0 0 3px rgba(123,97,255,0.08);
}

.chat-input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-size: 0.9rem;
  padding: 6px 0;
  resize: none;
  max-height: 120px;
  overflow-y: auto;
  outline: none;
  line-height: 1.55;
}

.chat-input::placeholder { color: var(--text-muted); }

.chat-send-btn {
  width: 40px; height: 40px;
  border-radius: var(--radius-sm);
  background: var(--grad-primary);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform var(--t-fast) var(--ease-spring), box-shadow var(--t-fast), opacity var(--t-fast);
  flex-shrink: 0;
}

.chat-send-btn:hover:not(:disabled) { transform: scale(1.08); box-shadow: var(--shadow-glow-cyan); }
.chat-send-btn:active:not(:disabled) { transform: scale(0.96); }
.chat-send-btn:disabled { opacity: 0.35; cursor: not-allowed; }
.chat-send-btn:focus-visible { outline: 2px solid var(--cyan); outline-offset: 2px; }

.chat-disclaimer { font-size: 0.68rem; color: var(--text-ghost); margin-top: 10px; text-align: center; }

/* ================================================================
   ABOUT SECTION
================================================================ */
.about-section {
  padding: 120px 0;
  position: relative;
}

.about-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent, rgba(0,245,255,0.015), transparent);
  pointer-events: none;
}

.about-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 72px; align-items: start; }

.about-desc { font-size: 0.97rem; color: var(--text-secondary); line-height: 1.8; margin-bottom: 36px; }
.about-desc strong { color: var(--text-primary); }

.about-features { display: flex; flex-direction: column; gap: 18px; }

.about-feature {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  padding: 16px 18px;
  border-radius: var(--radius);
  border: 1px solid transparent;
  transition: border-color var(--t-normal), background var(--t-normal);
}

.about-feature:hover { border-color: var(--border-subtle); background: rgba(255,255,255,0.02); }

.feature-icon {
  width: 40px; height: 40px;
  border-radius: var(--radius-sm);
  background: rgba(0,245,255,0.07);
  border: 1px solid rgba(0,245,255,0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--cyan);
  flex-shrink: 0;
  transition: box-shadow var(--t-normal);
}

.about-feature:hover .feature-icon { box-shadow: 0 0 16px rgba(0,245,255,0.2); }

.about-feature strong { display: block; font-size: 0.9rem; font-weight: 700; color: var(--text-primary); margin-bottom: 4px; }
.about-feature p { font-size: 0.82rem; color: var(--text-muted); line-height: 1.55; margin: 0; }

.about-threat-types {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 32px;
  backdrop-filter: blur(28px);
  -webkit-backdrop-filter: blur(28px);
  box-shadow: var(--shadow-card);
  position: relative;
  overflow: hidden;
}

.about-threat-types::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: var(--grad-primary-rev);
  opacity: 0.5;
}

.threats-title {
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 700;
  margin-bottom: 18px;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 10px;
}

.threats-title::before {
  content: '';
  display: block;
  width: 18px; height: 2px;
  background: var(--grad-primary);
  border-radius: var(--radius-full);
}

.threat-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 32px; }

.threat-chip {
  padding: 5px 13px;
  border-radius: var(--radius-full);
  font-size: 0.72rem;
  font-weight: 700;
  border: 1px solid;
  letter-spacing: 0.02em;
  transition: transform var(--t-fast) var(--ease-spring);
  cursor: default;
}

.threat-chip:hover { transform: translateY(-1px); }

.chip-critical { background: rgba(255,0,60,.08);   border-color: rgba(255,0,60,.35);   color: #FF003C; }
.chip-high     { background: rgba(255,77,106,.08);  border-color: rgba(255,77,106,.3);  color: var(--red); }
.chip-medium   { background: rgba(255,140,66,.08);  border-color: rgba(255,140,66,.3);  color: var(--orange); }

.report-links h4 {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--text-muted);
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.report-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: var(--radius);
  border: 1px solid var(--border-subtle);
  background: rgba(255,255,255,0.02);
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 8px;
  transition: border-color var(--t-fast), color var(--t-fast), background var(--t-fast), transform var(--t-fast) var(--ease-spring);
  text-decoration: none;
}

.report-link:hover {
  border-color: var(--border-cyan);
  color: var(--cyan);
  background: rgba(0,245,255,0.04);
  transform: translateX(4px);
}

/* ================================================================
   FOOTER
================================================================ */
.footer {
  position: relative;
  z-index: 1;
  border-top: 1px solid var(--border-subtle);
}

.footer-inner {
  max-width: 1180px;
  margin: 0 auto;
  padding: 32px 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  text-align: center;
  background: rgba(0,0,0,0.15);
}

.footer-brand { display: flex; align-items: center; gap: 10px; font-size: 0.9rem; color: var(--text-secondary); font-weight: 500; }
.footer-logo { font-size: 1.2rem; filter: drop-shadow(0 0 6px rgba(0,245,255,0.4)); }
.footer-disclaimer { font-size: 0.72rem; color: var(--text-muted); max-width: 540px; line-height: 1.6; }

/* ================================================================
   REVEAL ANIMATIONS
================================================================ */
.reveal { opacity: 0; transform: translateY(28px); transition: opacity 0.7s var(--ease-out), transform 0.7s var(--ease-out); }
.reveal.visible { opacity: 1; transform: translateY(0); }
.reveal-delay-1 { transition-delay: 0.1s; }
.reveal-delay-2 { transition-delay: 0.2s; }
.reveal-delay-3 { transition-delay: 0.3s; }

/* ================================================================
   TOAST NOTIFICATIONS
================================================================ */
.toast-container {
  position: fixed;
  bottom: 28px; right: 28px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 12px;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  border-radius: var(--radius);
  border: 1px solid var(--border-default);
  background: rgba(6,11,24,0.96);
  backdrop-filter: blur(24px);
  box-shadow: var(--shadow-lg);
  font-size: 0.875rem;
  color: var(--text-primary);
  pointer-events: auto;
  max-width: 360px;
  animation: toastIn 0.35s var(--ease-spring) both;
}

.toast.toast-exit { animation: toastOut 0.25s var(--ease-smooth) both; }

.toast-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.toast-success .toast-dot { background: var(--emerald); box-shadow: 0 0 8px var(--emerald); }
.toast-error   .toast-dot { background: var(--red);     box-shadow: 0 0 8px var(--red); }
.toast-info    .toast-dot { background: var(--cyan);    box-shadow: 0 0 8px var(--cyan); }

@keyframes toastIn {
  from { opacity: 0; transform: translateX(20px) scale(0.95); }
  to   { opacity: 1; transform: translateX(0) scale(1); }
}
@keyframes toastOut {
  from { opacity: 1; transform: translateX(0) scale(1); }
  to   { opacity: 0; transform: translateX(20px) scale(0.95); }
}

/* ================================================================
   RESPONSIVE
================================================================ */
@media (max-width: 1100px) {
  .hero { gap: 40px; }
  .hero-visual { flex: 0 0 360px; }
  .threat-orb { width: 320px; height: 320px; }
}

@media (max-width: 900px) {
  .hero { flex-direction: column; text-align: center; gap: 48px; padding: calc(var(--navbar-h) + 60px) 24px 72px; }
  .hero-content { max-width: 100%; }
  .hero-actions { justify-content: center; }
  .hero-stats   { justify-content: center; }
  .hero-visual  { flex: 0 0 auto; }
  .threat-orb   { width: 280px; height: 280px; }
  .hero-subtext { max-width: 100%; }
  .about-grid { grid-template-columns: 1fr; gap: 48px; }
  .scan-form-row { flex-direction: column; }
  .result-header { flex-direction: column; align-items: stretch; }
  .result-actions { flex-direction: row; }
}

@media (max-width: 700px) {
  .nav-links { display: none; }
  .hero-stats { flex-wrap: wrap; gap: 20px; justify-content: center; }
  .hero-stat-divider { display: none; }
  .hero-stat { padding: 0 16px; }
  .scan-tab { padding: 14px 14px; font-size: 0.8rem; }
  .scan-body { padding: 20px; }
  .detail-body { padding: 20px; }
  .chat-wrapper { height: 600px; }
  .hero-visual { display: none; }
}

@media (max-width: 480px) {
  .hero-heading { font-size: 2.1rem; }
  .hero-actions .btn { padding: 12px 20px; font-size: 0.875rem; }
  .section-title { font-size: 1.75rem; }
  .scan-section, .chat-section, .about-section { padding: 80px 0; }
  .about-threat-types { padding: 22px; }
  .result-header { padding: 22px; }
  .indicators-grid { grid-template-columns: 1fr 1fr; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  html { scroll-behavior: auto; }
}
"""

pathlib.Path('style.css').write_text(css, encoding='utf-8')
print(f'Written {len(css)} chars to style.css')
