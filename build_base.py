import os

def write_f(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

# -- HTML Wrappers --
nav = """
<nav class="navbar" id="navbar">
  <div class="nav-container row space-between items-center px-lg h-16 w-full max-w-7xl mx-auto">
    <a href="index.html" class="logo row items-center gap-2 text-primary font-600 font-body">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--blue-500)" stroke-width="2"><path d="M12 22v-6"></path><path d="M16 11l-4-4-4 4"></path><path d="M12 2v5"></path><path d="M6 16v-4"></path><path d="M18 16v-4"></path></svg>
      ResumeTree
    </a>
    <div class="nav-links row gap-8 display-md">
      <a href="howitworks.html" class="text-secondary hover-primary">How It Works</a>
      <a href="research.html" class="text-secondary hover-primary">Research</a>
      <a href="upload.html" class="text-secondary hover-primary">Upload</a>
    </div>
    <div class="nav-actions row items-center gap-4">
      <button id="theme-toggle" class="icon-btn text-secondary hover-primary">
        <svg id="moon-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        <svg id="sun-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" style="display:none;"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
      </button>
      <a href="upload.html" class="btn btn-primary">Try Free</a>
    </div>
  </div>
</nav>
<div id="toast-container" class="fixed bottom-lg right-lg col gap-2 z-50"></div>
"""

footer = """
<footer class="footer border-t border-border mt-xl py-xl px-lg">
  <div class="max-w-7xl mx-auto row space-between items-center text-tertiary text-sm">
    <div class="row items-center gap-2">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--blue-500)" stroke-width="2"><path d="M12 22v-6"></path><path d="M16 11l-4-4-4 4"></path><path d="M12 2v5"></path><path d="M6 16v-4"></path><path d="M18 16v-4"></path></svg>
      <span>© 2025 ResumeTree · IEEE Research Project</span>
    </div>
    <div class="row gap-4">
      <a href="#" class="hover-primary">GitHub</a>
      <a href="#" class="hover-primary">Research Paper</a>
      <a href="#" class="hover-primary">Contact</a>
    </div>
  </div>
</footer>
"""

def wrap_html(page_name, title, content):
    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - ResumeTree</title>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,700;1,300&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/global.css">
</head>
<body class="bg-base text-primary font-body antialiased min-h-screen col transition-colors">
    <div class="noise-overlay"></div>
    {nav}
    <main id="main-content" class="flex-1 w-full relative z-10 page-transition pt-16">
        {content}
    </main>
    {footer if page_name in ['index', 'howitworks'] else ''}
    <script src="js/global.js"></script>
    <script src="js/api.js"></script>
    <script src="js/pages/{page_name}.js"></script>
</body>
</html>"""

files = {}

# --- CSS ---
files['frontend/css/global.css'] = """
:root {
  --bg-base: #080A0F; --bg-surface: #0D1017; --bg-card: #131720; --bg-elevated: #1A2030; --bg-border: #1E2535;
  --blue-500: #2563EB; --blue-400: #3B82F6; --blue-glow: rgba(37,99,235,0.2);
  --mint-500: #10B981; --mint-400: #34D399; --amber-500: #F59E0B; --red-500: #EF4444; --purple-500: #8B5CF6;
  --text-primary: #F1F5F9; --text-secondary: #94A3B8; --text-tertiary: #475569; --text-accent: #3B82F6;
  --ease-out: cubic-bezier(0,0,0.2,1); --ease-spring: cubic-bezier(0.34,1.56,0.64,1); --ease-smooth: cubic-bezier(0.25,0.46,0.45,0.94);
}
:root.light {
  --bg-base: #FAFAFA; --bg-surface: #FFFFFF; --bg-card: #F8FAFC; --bg-elevated: #F1F5F9; --bg-border: #E2E8F0;
  --text-primary: #0F172A; --text-secondary: #475569; --text-tertiary: #94A3B8;
}
* { margin:0; padding:0; box-sizing: border-box; transition: background-color 300ms, border-color 300ms, color 300ms; }
html { scroll-behavior: smooth; }
body { background: var(--bg-base); color: var(--text-primary); font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; }
::selection { background: var(--blue-glow); color: var(--text-primary); }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--bg-border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--blue-500); }
*:focus-visible { outline: 2px solid var(--blue-400); outline-offset: 2px; }

/* Utilities */
.col { display: flex; flex-direction: column; } .row { display: flex; flex-direction: row; }
.items-center { align-items: center; } .items-start { align-items: flex-start; } .justify-center { justify-content: center; } .space-between { justify-content: space-between; }
.flex-1 { flex: 1; } .w-full { width: 100%; } .h-full { height: 100%; } .h-screen { height: 100vh; }
.max-w-7xl { max-width: 1280px; } .max-w-3xl { max-width: 760px; } .max-w-md { max-width: 560px; } .mx-auto { margin-left: auto; margin-right: auto; }
.gap-2 { gap: 8px; } .gap-4 { gap: 16px; } .gap-6 { gap: 24px; } .gap-8 { gap: 32px; }
.p-4 { padding: 16px; } .p-6 { padding: 24px; } .p-8 { padding: 32px; } .px-lg { padding-left: 32px; padding-right: 32px; }
.py-lg { padding-top: 32px; padding-bottom: 32px; } .pt-xl { padding-top: 64px; } .pb-xl { padding-bottom: 64px; }
.mt-4 { margin-top: 16px; } .mt-8 { margin-top: 32px; } .mb-2 { margin-bottom: 8px; } .mb-4 { margin-bottom: 16px; } .mb-8 { margin-bottom: 32px; }
.mt-xl { margin-top: 64px; } .mb-xl { margin-bottom: 64px; }
.text-center { text-align: center; }
.font-display { font-family: 'Fraunces', serif; } .font-body { font-family: 'Inter', sans-serif; } .font-mono { font-family: 'JetBrains Mono', monospace; font-size: 13px; }
.text-xs { font-size: 12px; } .text-sm { font-size: 14px; } .text-base { font-size: 16px; } .text-lg { font-size: 20px; } .text-xl { font-size: 24px; } .text-2xl { font-size: 32px; }
.font-500 { font-weight: 500; } .font-600 { font-weight: 600; }
.text-primary { color: var(--text-primary); } .text-secondary { color: var(--text-secondary); } .text-tertiary { color: var(--text-tertiary); } .text-accent { color: var(--text-accent); }
.text-red { color: var(--red-500); } .text-amber { color: var(--amber-500); } .text-mint { color: var(--mint-500); } .text-blue { color: var(--blue-500); }
.bg-base { background: var(--bg-base); } .bg-surface { background: var(--bg-surface); } .bg-card { background: var(--bg-card); border: 1px solid var(--bg-border); }
.border-b { border-bottom: 1px solid var(--bg-border); } .border-t { border-top: 1px solid var(--bg-border); } .border { border: 1px solid var(--bg-border); }
.rounded-sm { border-radius: 6px; } .rounded-md { border-radius: 10px; } .rounded-lg { border-radius: 16px; } .rounded-full { border-radius: 999px; }
.relative { position: relative; } .absolute { position: absolute; } .fixed { position: fixed; }
.z-10 { z-index: 10; } .z-50 { z-index: 50; }
.hidden { display: none !important; }
a { text-decoration: none; color: inherit; } .cursor-pointer { cursor: pointer; } 
ul { list-style: none; }

/* Effects */
.noise-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 50; opacity: 0.03; background-image: url('data:image/svg+xml;utf8,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E'); }
.glass-nav { background: rgba(13, 16, 23, 0.7); backdrop-filter: blur(20px); border-bottom: 1px solid var(--bg-border); position: fixed; top:0; width:100%; z-index: 40; transition: background 0.3s, border-color 0.3s; }
.glass-nav.scrolled { background: rgba(13, 16, 23, 0.95); }
.light .glass-nav { background: rgba(255, 255, 255, 0.7); } .light .glass-nav.scrolled { background: rgba(255, 255, 255, 0.95); }

/* Components */
.btn { display: inline-flex; align-items: center; justify-center; padding: 12px 24px; border-radius: 8px; font-weight: 500; font-size: 14px; cursor: pointer; transition: all 150ms var(--ease-out); border:none; color: white;}
.btn-primary { background: linear-gradient(135deg, var(--blue-500), #1D4ED8); box-shadow: 0 4px 14px var(--blue-glow); }
.btn-primary:hover { background: var(--blue-400); box-shadow: 0 0 24px rgba(37,99,235,0.4); transform: translateY(-1px); }
.btn-primary:active { transform: translateY(0); }
.btn-ghost { background: transparent; border: 1px solid var(--bg-border); color: var(--text-primary); }
.btn-ghost:hover { background: var(--bg-elevated); }
.btn-danger { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); color: var(--red-500); }
.icon-btn { background: transparent; border: none; padding: 8px; border-radius: 6px; cursor: pointer; color: var(--text-secondary); transition: background 150ms var(--ease-out); display: flex; align-items: center; justify-content: center; }
.icon-btn:hover { background: var(--bg-elevated); color: var(--text-primary); }

.card { background: var(--bg-card); border: 1px solid var(--bg-border); border-radius: 12px; padding: 24px; transition: all 200ms var(--ease-out); }
.card-hover:hover { background: var(--bg-elevated); border-color: rgba(37,99,235,0.3); box-shadow: 0 8px 32px rgba(0,0,0,0.3); }

/* Animations */
.animate-in { opacity: 0; transform: translateY(24px); animation: fadeUp 500ms var(--ease-out) forwards; }
@keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }
.page-transition { opacity: 0; transform: translateY(8px); animation: pageEnter 300ms var(--ease-out) 50ms forwards; }
@keyframes pageEnter { to { opacity: 1; transform: translateY(0); } }

.skeleton { background: linear-gradient(90deg, var(--bg-card) 25%, var(--bg-elevated) 50%, var(--bg-card) 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 6px; min-height: 20px;}
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* Badges */
.badge { padding: 3px 10px; border-radius: 20px; font-weight: 500; font-size: 11px; white-space: nowrap; }
.badge-full { background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.3); color: var(--mint-400); }
.badge-partial { background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.3); color: var(--amber-500); }
.badge-none { background: rgba(239,68,68,0.12); border: 1px solid rgba(239,68,68,0.3); color: var(--red-500); }
.badge-high { background: var(--red-500); color: white; } .badge-medium { background: var(--amber-500); color: white; } .badge-low { background: var(--text-tertiary); color: white; }

/* Chips */
.chip { font-family: 'JetBrains Mono', monospace; font-size: 11px; border-radius: 4px; padding: 2px 8px; font-weight: 600; display: inline-block; white-space: nowrap;}
.chip-exp { background: rgba(37,99,235,0.1); border: 1px solid rgba(37,99,235,0.3); color: var(--blue-400); }
.chip-proj { background: rgba(139,92,246,0.1); border: 1px solid rgba(139,92,246,0.3); color: var(--purple-500); }
.chip-edu { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); color: var(--mint-400); }
.chip-skill { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.3); color: var(--amber-500); }

/* Toasts */
.toast { background: var(--bg-elevated); border: 1px solid var(--bg-border); padding: 16px; border-radius: 8px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); transform: translateY(100px); opacity: 0; animation: toastIn 300ms var(--ease-spring) forwards; position: relative; overflow: hidden; min-width: 250px;}
.toast.out { animation: toastOut 300ms var(--ease-in) forwards; }
@keyframes toastIn { to { transform: translateY(0); opacity: 1; } } @keyframes toastOut { to { transform: translateY(50px); opacity: 0; } }
.toast-progress { position: absolute; bottom: 0; left: 0; height: 3px; background: var(--blue-500); width: 100%; transition: width linear; }
.toast.success .toast-progress { background: var(--mint-500); } .toast.error .toast-progress { background: var(--red-500); }

/* Specific Overrides */
input, textarea { background: var(--bg-card); border: 1px solid var(--bg-border); border-radius: 8px; padding: 14px 16px; color: var(--text-primary); font-family: 'Inter', sans-serif; resize: vertical; transition: border-color 0ms, box-shadow 0ms; }
input:focus, textarea:focus { outline: none; border-color: var(--blue-400); box-shadow: 0 0 0 4px var(--blue-glow); }

@media (max-width: 768px) { .display-md { display: none !important; } }
"""

# --- JS Globals & API ---
files['frontend/js/global.js'] = """
document.addEventListener('DOMContentLoaded', () => {
    // Theme toggle
    const toggleBtn = document.getElementById('theme-toggle');
    const sun = document.getElementById('sun-icon');
    const moon = document.getElementById('moon-icon');
    const html = document.documentElement;
    
    // Check local storage or pref
    const isLight = localStorage.getItem('theme') === 'light';
    if(isLight) { html.classList.remove('dark'); html.classList.add('light'); sun.style.display='none'; moon.style.display='block'; }
    
    toggleBtn?.addEventListener('click', () => {
        html.classList.toggle('dark');
        html.classList.toggle('light');
        const isDark = html.classList.contains('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        sun.style.display = isDark ? 'block' : 'none';
        moon.style.display = isDark ? 'none' : 'block';
    });

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        const nav = document.getElementById('navbar');
        if (window.scrollY > 20) nav.classList.add('scrolled');
        else nav.classList.remove('scrolled');
    });

    // Observe anims
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                entry.target.classList.add('animate-in');
                if (entry.target.dataset.counter) triggerCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    document.querySelectorAll('.scroll-fade').forEach((el, i) => {
        el.style.opacity = '0'; // hide initially
        el.style.animationDelay = `${(i%5)*80}ms`;
        observer.observe(el);
    });
});

function triggerCounter(el) {
    const target = parseInt(el.dataset.counter, 10);
    const duration = 1200;
    const start = performance.now();
    const isDecimal = el.dataset.counter.includes('.');
    
    function update(time) {
        const elapsed = time - start;
        const progress = Math.min(elapsed / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3); // ease out cubic
        const current = target * ease;
        el.textContent = isDecimal ? current.toFixed(2) : Math.floor(current);
        if (progress < 1) requestAnimationFrame(update);
        else el.textContent = target;
    }
    requestAnimationFrame(update);
}

function showToast(message, type='info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<div class="row items-center gap-2"><div class="text-sm font-500">${message}</div></div><div class="toast-progress"></div>`;
    container.appendChild(toast);
    
    const progress = toast.querySelector('.toast-progress');
    // Animate progress shrink 4s
    progress.style.transitionDuration = '4s';
    requestAnimationFrame(() => { progress.style.width = '0%'; });
    
    setTimeout(() => {
        toast.classList.add('out');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}
"""

files['frontend/js/api.js'] = """
const API_BASE = 'http://localhost:8000';

async function apiCall(endpoint, method='GET', body=null) {
    try {
        const options = { method };
        if (body) {
            if (body instanceof FormData) options.body = body;
            else { options.body = JSON.stringify(body); options.headers = { 'Content-Type': 'application/json' }; }
        }
        const res = await fetch(`${API_BASE}${endpoint}`, options);
        if (!res.ok) {
            if (res.status===401) throw new Error("Authentication failed");
            if (res.status===404) throw new Error("Resource not found");
            if (res.status===500) throw new Error("Server error — try again");
            throw new Error(`HTTP Error ${res.status}`);
        }
        return await res.json();
    } catch(err) {
        console.error("API Error:", err);
        showToast(err.message || "Cannot reach server", "error");
        throw err;
    }
}
"""

# --- Page: Landing ---
html_landing = """
<div id="hero-canvas" class="absolute top-0 left-0 w-full h-full z-0 overflow-hidden pointer-events-none"></div>
<section class="max-w-7xl mx-auto px-lg relative z-10 row items-center justify-center text-center pb-xl pt-xl" style="min-height: 90vh;">
    <div class="col items-center gap-6 max-w-3xl">
        <div class="border rounded-full px-4 py-1 text-xs font-mono text-blue bg-card animate-in">
            IEEE Research · VIT Pune · 2025
        </div>
        <h1 class="font-display text-primary animate-in" style="font-size: 72px; line-height: 1.05; letter-spacing: -0.03em; animation-delay: 250ms;">
            Resume screening<br><span class="text-blue italic font-display">that actually thinks.</span>
        </h1>
        <p class="text-secondary text-lg mb-4 animate-in" style="animation-delay: 400ms;">
            ResumeTree structures resumes as intelligent trees and uses LLM reasoning to evaluate fit. Every score is explained. Every decision is traceable.
        </p>
        <div class="row gap-4 animate-in" style="animation-delay: 550ms;">
            <a href="upload.html" class="btn btn-primary text-base">Evaluate a Resume &rarr;</a>
            <a href="howitworks.html" class="btn btn-ghost text-base">See How It Works</a>
        </div>
    </div>
</section>

<section class="max-w-7xl mx-auto px-lg py-xl z-10 relative">
    <div class="row items-center gap-6 flex-wrap justify-center">
        <div class="card col items-center flex-1 min-w-[250px] scroll-fade text-center">
            <h2 class="font-display text-4xl mb-2 text-primary" data-counter="100">0</h2>
            <p class="text-secondary text-sm font-mono">% Score Traceable</p>
        </div>
        <div class="card col items-center flex-1 min-w-[250px] scroll-fade text-center">
            <h2 class="font-display text-4xl mb-2 text-primary">0</h2>
            <p class="text-secondary text-sm font-mono">Vector Embeddings</p>
        </div>
        <div class="card col items-center flex-1 min-w-[250px] scroll-fade text-center">
            <h2 class="font-display text-4xl mb-2 text-primary">M4</h2>
            <p class="text-secondary text-sm font-mono">Chain-of-Thought</p>
        </div>
    </div>
</section>
"""
files['frontend/index.html'] = wrap_html('landing', 'AI Resume Evaluation', html_landing)

files['frontend/js/canvas.js'] = """
const canvasContainer = document.getElementById('hero-canvas');
if(canvasContainer) {
    const cvs = document.createElement('canvas');
    cvs.width = window.innerWidth; cvs.height = window.innerHeight;
    canvasContainer.appendChild(cvs);
    const ctx = cvs.getContext('2d');
    
    let nodes = [];
    for(let i=0; i<35; i++) {
        nodes.push({
            x: Math.random() * cvs.width,
            y: Math.random() * cvs.height,
            vx: (Math.random()-0.5) * 0.3,
            vy: (Math.random()-0.5) * 0.3
        });
    }
    
    function draw() {
        ctx.clearRect(0,0,cvs.width,cvs.height);
        ctx.fillStyle = 'rgba(37,99,235,0.4)';
        ctx.strokeStyle = 'rgba(37,99,235,0.12)';
        ctx.lineWidth = 1;
        
        nodes.forEach(n => {
            n.x += n.vx; n.y += n.vy;
            if(n.x<0 || n.x>cvs.width) n.vx*=-1;
            if(n.y<0 || n.y>cvs.height) n.vy*=-1;
            ctx.beginPath(); ctx.arc(n.x, n.y, 2, 0, Math.PI*2); ctx.fill();
        });
        
        for(let i=0; i<nodes.length; i++){
            for(let j=i+1; j<nodes.length; j++){
                const dx = nodes[i].x - nodes[j].x;
                const dy = nodes[i].y - nodes[j].y;
                const dist = Math.sqrt(dx*dx + dy*dy);
                if(dist < 120) {
                    ctx.beginPath(); ctx.moveTo(nodes[i].x, nodes[i].y); ctx.lineTo(nodes[j].x, nodes[j].y); ctx.stroke();
                }
            }
        }
        if(!document.hidden) requestAnimationFrame(draw);
    }
    document.addEventListener('visibilitychange', () => { if(!document.hidden) requestAnimationFrame(draw); });
    draw();
    window.addEventListener('resize', () => { cvs.width = window.innerWidth; cvs.height = window.innerHeight; });
}
"""
files['frontend/js/pages/landing.js'] = "// landing logic"

# --- Page: Upload ---
files['frontend/css/pages/upload.css'] = """
.drop-zone { border: 2px dashed var(--bg-border); background: var(--bg-card); transition: all 300ms var(--ease-spring); }
.drop-zone.dragover { border-color: var(--blue-400); background: rgba(37,99,235,0.04); }
.drop-zone.dragover svg { transform: translateY(-10px); }
.drop-zone.loaded { border: 2px solid var(--mint-400); background: rgba(16,185,129,0.04); }
.drop-zone.error { border-color: var(--red-500); animation: shake 0.5s; background: rgba(239,68,68,0.04); }
@keyframes shake { 0%,100%{transform:translateX(0);} 25%{transform:translateX(-5px);} 75%{transform:translateX(5px);} }

.progress-overlay { position: fixed; bottom: 0; left: 0; width: 100vw; height: 100vh; background: rgba(8,10,15,0.8); backdrop-filter: blur(8px); z-index: 100; display: flex; align-items: flex-end; justify-content: center; transform: translateY(100%); transition: transform 400ms var(--ease-out); }
.progress-overlay.show { transform: translateY(0); }
.progress-panel { background: var(--bg-card); width: 100%; max-width: 600px; border-radius: 16px 16px 0 0; padding: 40px; border: 1px solid var(--bg-border); border-bottom: none; }
.progress-bar { width: 100%; height: 6px; background: var(--bg-elevated); border-radius: 3px; overflow: hidden; margin-top: 16px; }
.progress-fill { height: 100%; background: var(--blue-500); width: 0%; transition: width 500ms var(--ease-smooth); }
"""
html_upload = """
<div class="col items-center max-w-md mx-auto pt-8">
    <div class="row gap-4 items-center mb-12 text-sm font-mono font-600">
        <span class="text-blue">① Upload</span>
        <span class="text-tertiary">────</span>
        <span class="text-tertiary">② Evaluate</span>
        <span class="text-tertiary">────</span>
        <span class="text-tertiary">③ Results</span>
    </div>

    <div class="w-full text-left mb-4">
        <h2 class="text-xl font-600 mb-1">Resume Document</h2>
    </div>

    <div id="upload-zone" class="drop-zone w-full rounded-lg p-8 col items-center justify-center text-center mb-8 cursor-pointer relative">
        <input type="file" id="resume-input" class="absolute w-full h-full opacity-0 cursor-pointer" accept=".pdf,.docx">
        <svg id="upload-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-tertiary mb-4 transition-transform"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="12" y1="18" x2="12" y2="12"></line><line x1="9" y1="15" x2="15" y2="15"></line></svg>
        <h3 id="upload-title" class="text-base font-500 text-primary mb-1">Drop resume here or click to browse</h3>
        <p id="upload-desc" class="text-tertiary text-sm">PDF or DOCX · Max 10MB</p>
    </div>

    <div class="w-full text-left mb-4 row space-between">
        <h2 class="text-xl font-600 mb-1">Job Description</h2>
    </div>
    
    <div class="w-full mb-8">
        <textarea id="jd-input" rows="8" class="w-full font-mono text-sm" placeholder="Paste job description text here..."></textarea>
    </div>

    <button id="evaluate-btn" class="btn btn-primary w-full justify-center text-base py-4 font-600" disabled>Evaluate Candidate &rarr;</button>
</div>

<div id="progress-overlay" class="progress-overlay">
    <div class="progress-panel col">
        <h3 class="text-xl font-600 mb-6">Evaluating Candidate Fit</h3>
        <div id="progress-steps" class="col gap-3 text-secondary text-sm font-mono">
            <div class="step" data-pct="20">○ Parsing resume...</div>
            <div class="step opacity-50" data-pct="45">○ Building career tree</div>
            <div class="step opacity-50" data-pct="65">○ Analysing job description</div>
            <div class="step opacity-50" data-pct="85">○ Reasoning about fit</div>
            <div class="step opacity-50" data-pct="100">○ Finalising scores</div>
        </div>
        <div class="progress-bar"><div id="progress-fill" class="progress-fill"></div></div>
    </div>
</div>
"""
files['frontend/upload.html'] = wrap_html('upload', 'Upload & Evaluate', html_upload)

files['frontend/js/pages/upload.js'] = """
const zone = document.getElementById('upload-zone');
const input = document.getElementById('resume-input');
const title = document.getElementById('upload-title');
const desc = document.getElementById('upload-desc');
const evaluateBtn = document.getElementById('evaluate-btn');
const jdInput = document.getElementById('jd-input');
let file = null;

function updateState() { if(file && jdInput.value.length > 20) evaluateBtn.disabled = false; else evaluateBtn.disabled = true; }

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(ev => zone.addEventListener(ev, e => { e.preventDefault(); e.stopPropagation(); }));
['dragenter', 'dragover'].forEach(ev => zone.addEventListener(ev, () => { zone.classList.add('dragover'); title.textContent = "Release to upload"; }));
['dragleave', 'drop'].forEach(ev => zone.addEventListener(ev, () => { zone.classList.remove('dragover'); }));

zone.addEventListener('drop', e => {
    const droppedFile = e.dataTransfer.files[0];
    handleFile(droppedFile);
});
input.addEventListener('change', e => { handleFile(e.target.files[0]); });
jdInput.addEventListener('input', updateState);

function handleFile(f) {
    if(!f) return;
    if(!f.name.endsWith('.pdf') && !f.name.endsWith('.docx')) {
        zone.classList.add('error'); setTimeout(()=>zone.classList.remove('error'), 500);
        showToast("Invalid file type. Please use PDF or DOCX.", "error"); return;
    }
    file = f;
    zone.classList.add('loaded');
    title.textContent = f.name;
    desc.textContent = (f.size / 1024 / 1024).toFixed(2) + " MB";
    title.classList.add('text-mint');
    updateState();
}

evaluateBtn.addEventListener('click', async () => {
    if(!file || !jdInput.value) return;
    const overlay = document.getElementById('progress-overlay');
    overlay.classList.add('show');
    const steps = document.querySelectorAll('.step');
    const fill = document.getElementById('progress-fill');
    
    // Simulate steps graphically
    let currentStep = 0;
    const stepInterval = setInterval(() => {
        if(currentStep < steps.length) {
            steps.forEach((s, i) => {
                if(i < currentStep) s.textContent = s.textContent.replace('○', '✓');
                if(i === currentStep) { s.classList.remove('opacity-50'); fill.style.width = s.dataset.pct + "%"; }
            });
            currentStep++;
        }
    }, 1500);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('jd_text', jdInput.value);

    try {
        const res = await apiCall('/evaluate', 'POST', formData);
        clearInterval(stepInterval);
        fill.style.width = "100%";
        steps.forEach(s => s.textContent = s.textContent.replace('○', '✓'));
        setTimeout(() => { window.location.href = `results.html?id=${res.eval_id || 'test_id'}`; }, 800);
    } catch(err) {
        clearInterval(stepInterval);
        overlay.classList.remove('show');
    }
});
"""

# --- Page: Results ---
html_results = """
<div id="results-skeleton" class="row h-full w-full gap-6 px-lg pt-4" style="height: calc(100vh - 80px);">
    <div class="skeleton" style="width: 280px; height: 100%;"></div>
    <div class="col flex-1 gap-6">
        <div class="skeleton" style="width: 100%; height: 120px;"></div>
        <div class="skeleton" style="width: 100%; height: 60vh;"></div>
    </div>
</div>

<div id="results-content" class="row h-full w-full max-w-[1400px] mx-auto gap-8 px-4 md:px-lg hidden relative">
    
    <!-- Left Sidebar: Tree Visualizer -->
    <aside class="w-[280px] h-full fixed md:relative bottom-0 bg-surface md:bg-transparent z-40 border-r border-border md:border-none p-4 md:p-0 col overflow-y-auto" style="max-height: 80vh;">
        <h3 class="font-600 text-sm mb-4 text-tertiary tracking-wider uppercase">Resume Tree</h3>
        <div id="tree-container" class="col gap-1 text-sm font-mono">
            <!-- Populated by JS -->
        </div>
    </aside>

    <!-- Main Panel -->
    <div class="flex-1 col pb-xl gap-8">
        
        <!-- Top Bar content implicitly handled by page structure -->
        <header class="row space-between items-center card border-blue-500/30" style="background: linear-gradient(135deg, rgba(37,99,235,0.05) 0%, var(--bg-card) 100%);">
            <div>
                <h1 id="cand-name" class="font-display text-3xl text-primary font-400">Candidate Evaluation</h1>
                <p id="cand-role" class="text-secondary mt-1">Mid Level Backend Engineer</p>
            </div>
            <div class="row gap-4">
                <a href="feedback.html" class="btn btn-primary shadow-glow">Get Feedback &rarr;</a>
            </div>
        </header>

        <!-- Dashboard -->
        <div class="row flex-wrap gap-8">
            <!-- Gauge Card -->
            <div class="card col items-center justify-center p-8 w-full md:w-auto">
                <div class="relative w-[200px] h-[200px]">
                    <svg viewBox="0 0 100 100" class="w-full h-full transform -rotate-90 stroke-current text-border">
                        <circle cx="50" cy="50" r="40" fill="none" stroke-width="8" />
                    </svg>
                    <svg viewBox="0 0 100 100" class="absolute top-0 left-0 w-full h-full transform -rotate-90 stroke-current">
                        <circle id="score-arc" cx="50" cy="50" r="40" fill="none" stroke-width="8" stroke-linecap="round" stroke-dasharray="251.2" stroke-dashoffset="251.2" />
                    </svg>
                    <div class="absolute top-0 left-0 w-full h-full col items-center justify-center">
                        <div class="row items-baseline"><span id="score-text" class="font-mono font-600 text-5xl">0</span><span class="text-tertiary">/100</span></div>
                        <span id="score-status" class="text-xs font-500 tracking-wide mt-1">Evaluating...</span>
                    </div>
                </div>
            </div>

            <!-- Dimensions -->
            <div class="card flex-1 col justify-center py-6 px-8 gap-6">
                <h3 class="font-600 text-sm mb-2 text-primary">Dimension Scores</h3>
                <div id="dimensions-container" class="col gap-4">
                    <!-- Populated by JS -->
                </div>
            </div>
        </div>

        <!-- Requirements -->
        <div class="col mt-8">
            <h2 class="font-600 text-xl mb-6 text-primary">Requirement Alignment</h2>
            <div class="col gap-4" id="reqs-container">
                <!-- Populated by JS -->
            </div>
        </div>
    </div>
</div>
"""
files['frontend/results.html'] = wrap_html('results', 'Evaluation Results', html_results)

files['frontend/css/pages/results.css'] = """
.tree-node { display: flex; align-items: center; gap: 8px; padding: 6px 8px; border-radius: 6px; cursor: pointer; transition: all 150ms var(--ease-spring); position: relative; }
.tree-node:hover { background: var(--bg-elevated); transform: scale(1.02); }
.tree-line { width: 1px; height: 100%; position: absolute; left: 11px; top: 24px; background: var(--bg-border); z-index: 0; }
.tree-indicator { width: 8px; height: 8px; border-radius: 50%; z-index: 10; flex-shrink:0; }
.req-card { border-left: 3px solid var(--bg-border); }
.req-card.full { border-left-color: var(--mint-500); }
.req-card.partial { border-left-color: var(--amber-500); }
.req-card.none { border-left-color: var(--red-500); }
.req-expand { max-height: 0; overflow: hidden; transition: max-height 300ms var(--ease-out), opacity 300ms; opacity: 0; }
.req-card.open .req-expand { max-height: 200px; opacity: 1; }
.req-card.open .chevron { transform: rotate(180deg); }
.dim-bar-track { width: 100%; height: 6px; background: var(--bg-border); border-radius: 3px; overflow: hidden; }
.dim-bar-fill { height: 100%; width: 0%; transition: width 600ms var(--ease-out); }
"""

files['frontend/js/gauge.js'] = """
function animateGauge(score) {
    const arc = document.getElementById('score-arc');
    const text = document.getElementById('score-text');
    const status = document.getElementById('score-status');
    const duration = 1500;
    const start = performance.now();
    const circumference = 2 * Math.PI * 40;
    
    let colorClass = 'text-mint';
    let statusText = 'Strong Match';
    if(score < 80) { colorClass = 'text-amber'; statusText = 'Partial Match'; }
    if(score < 60) { colorClass = 'text-red'; statusText = 'Weak Match'; }
    
    arc.classList.add(colorClass); text.classList.add(colorClass); status.classList.add(colorClass);
    status.textContent = statusText;

    function update(time) {
        const elapsed = time - start;
        const progress = Math.min(elapsed / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        const currentVal = Math.round(score * ease);
        
        text.textContent = currentVal;
        const offset = circumference - (currentVal / 100 * circumference);
        arc.style.strokeDashoffset = offset;
        
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}
"""

files['frontend/js/tree.js'] = """
function renderTree(resume_tree) {
    const cont = document.getElementById('tree-container');
    cont.innerHTML = '';
    // Mock simple render
    const nodes = [
        {id: "cand", label: "Candidate", color: "green", ml: 0},
        {id: "exp_base", label: "Experience", color: "gray", ml: 16},
        {id: "exp_1", label: "Backend Engineer", color: "green", ml: 32},
        {id: "proj_base", label: "Projects", color: "gray", ml: 16},
        {id: "proj_0", label: "Accident Pred", color: "amber", ml: 32}
    ];
    nodes.forEach(n => {
        let dot = 'bg-border';
        if(n.color==='green') dot='bg-mint-500';
        if(n.color==='amber') dot='bg-amber-500';
        if(n.color==='red') dot='bg-red-500';
        
        cont.innerHTML += `<div class="tree-node" style="margin-left: ${n.ml}px">
            <div class="tree-indicator ${dot}"></div>
            <span class="chip chip-${n.id.split('_')[0]}">${n.id}</span>
            <span class="ml-2">${n.label}</span>
        </div>`;
    });
}
"""

files['frontend/js/pages/results.js'] = """
document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const evalId = urlParams.get('id');
    if(evalId) {
        try {
            // Mock API or actual
            // const data = await apiCall(`/results/${evalId}`);
            const mockData = {
                overall_score: 78,
                dimension_scores: { "Skill Match": 80, "Experience Quality": 65, "Career Progression": 85, "Context Fit": 82 },
                matched_requirements: [
                    {text: "3+ years Python", type: "full", node: "exp_1", reasoning: "Found 4 years of Python at Infosys."},
                    {text: "AWS Cloud", type: "partial", node: "proj_0", reasoning: "Used GCP, concepts transferrable."}
                ]
            };
            
            document.getElementById('results-skeleton').style.display = 'none';
            document.getElementById('results-content').classList.remove('hidden');
            
            animateGauge(mockData.overall_score);
            renderTree({});
            
            // Dimensions
            const dimCont = document.getElementById('dimensions-container');
            let delay = 0;
            for(let [k,v] of Object.entries(mockData.dimension_scores)) {
                let col = v>=80 ? 'bg-mint-500' : (v>=60 ? 'bg-amber-500' : 'bg-red-500');
                dimCont.innerHTML += `<div class="col gap-2">
                    <div class="row space-between text-xs"><span class="text-secondary">${k}</span><span class="font-mono font-600">${v}</span></div>
                    <div class="dim-bar-track"><div class="dim-bar-fill ${col}" style="width: 0%; transition-delay: ${delay}ms"></div></div>
                </div>`;
                delay+=100;
            }
            setTimeout(() => {
                document.querySelectorAll('.dim-bar-fill').forEach((el, i) => {
                    el.style.width = Object.values(mockData.dimension_scores)[i] + "%";
                });
            }, 100);
            
            // Reqs
            const reqCont = document.getElementById('reqs-container');
            mockData.matched_requirements.forEach(r => {
                const bType = r.type==="full" ? "badge-full" : "badge-partial";
                const bText = r.type==="full" ? "✓ Full Match" : "◐ Partial";
                reqCont.innerHTML += `<div class="card req-card ${r.type} hover:bg-elevated cursor-pointer" onclick="this.classList.toggle('open')">
                    <div class="row space-between items-center">
                        <span class="text-sm font-500">${r.text}</span>
                        <div class="row gap-2 items-center">
                            <span class="badge ${bType}">${bText}</span>
                            <span class="chip chip-${r.node.split('_')[0]}">${r.node}</span>
                            <svg class="chevron transition-transform text-tertiary" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
                        </div>
                    </div>
                    <div class="req-expand mt-4 pt-4 border-t border-border">
                        <p class="text-sm text-secondary leading-relaxed">${r.reasoning}</p>
                    </div>
                </div>`;
            });
            
        } catch(e) {}
    }
});
"""

# Call writer
for p, c in files.items():
    write_f(p, c)

print("Batch 1 generated successfully: Base frameworks and upload/results skeletons.")
