import os

def write_f(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

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
    <link rel="stylesheet" href="css/pages/{page_name}.css">
</head>
<body class="bg-base text-primary font-body antialiased min-h-screen col transition-colors">
    <div class="noise-overlay"></div>
    {nav}
    <main id="main-content" class="flex-1 w-full relative z-10 page-transition" style="padding-top: 100px;">
        {content}
    </main>
    {footer if page_name in ['howitworks', 'research'] else ''}
    <script src="js/global.js"></script>
    <script src="js/api.js"></script>
    <script src="js/pages/{page_name}.js"></script>
</body>
</html>"""

files = {}

# --- Page: Feedback ---
files['frontend/css/pages/feedback.css'] = """
.quote-card { border-left: 4px solid var(--blue-500); background: linear-gradient(90deg, rgba(37,99,235,0.05), transparent); }
.diff-view { border-radius: 10px; overflow: hidden; display: flex; flex-direction: column; border: 1px solid var(--bg-border); }
@media (min-width: 768px) { .diff-view { flex-direction: row; } }
.diff-col { flex: 1; padding: 24px; position: relative; }
.diff-col.before { background: rgba(239,68,68,0.02); border-bottom: 1px solid var(--bg-border); }
@media (min-width: 768px) { .diff-col.before { border-bottom: none; border-right: 1px solid var(--bg-border); } }
.diff-col.after { background: rgba(16,185,129,0.02); }
.diff-top-border { position: absolute; top:0; left:0; width:100%; height:2px; }
.diff-top-border.red { background: rgba(239,68,68,0.3); }
.diff-top-border.green { background: rgba(16,185,129,0.5); }
.diff-del { background: rgba(239,68,68,0.2); color: var(--red-500); text-decoration: line-through; border-radius: 2px; padding: 0 2px; }
.diff-add { background: rgba(16,185,129,0.2); color: var(--mint-400); border-radius: 2px; padding: 0 2px; }
"""
html_feedback = """
<div class="max-w-3xl mx-auto px-6 w-full">
    <header class="mb-12 animate-in">
        <div class="row items-center gap-2 mb-4 font-mono text-xs text-tertiary">
            <span>EVALUATION</span><span class="text-primary">•</span><span class="text-blue">RECOMMENDATIONS</span>
        </div>
        <h1 class="font-display text-5xl mb-4 text-primary">Impact <span class="italic">Optimization</span></h1>
        <p class="text-secondary text-base leading-relaxed">We've identified key opportunities to elevate your professional narrative from task-based bullet points into achievement-driven stories.</p>
    </header>

    <div class="card quote-card mb-12 animate-in" style="animation-delay: 100ms;">
        <h3 class="font-600 text-sm mb-2 text-primary">Strategic Insight</h3>
        <p class="text-secondary text-sm leading-relaxed">Your resume demonstrates strong technical competence, but the experience section reads like a job description rather than a record of accomplishments. Shift your tone to emphasize <span class="text-primary font-500">results, autonomy, and underlying logic</span>. Focus on quantification where possible.</p>
    </div>

    <h2 class="font-600 text-xl border-b pb-4 mb-8 text-primary animate-in" style="animation-delay: 200ms;">Ranked by Impact</h2>
    <div class="col gap-4 mb-16 animate-in" style="animation-delay: 300ms;">
        <div class="card row items-start gap-4 hover:bg-elevated cursor-default border-l-[3px] border-l-red-500" style="border-left: 3px solid var(--red-500);">
            <div class="flex-1">
                <div class="row space-between items-center mb-1">
                    <h4 class="font-500 text-sm text-primary">Clarify Data Pipeline Scope</h4>
                    <span class="badge badge-high">HIGH</span>
                </div>
                <p class="text-xs text-tertiary italic mb-2">Gap: No explicit scalable data pipelines</p>
                <p class="text-sm text-secondary leading-relaxed">Emphasize the end-to-end nature of your existing pipeline. Mentioning how data structurally flows maps perfectly to the pipeline knowledge requirement without fabricating tools.</p>
                <div class="mt-4"><span class="chip chip-proj">proj_0</span></div>
            </div>
        </div>
    </div>

    <h2 class="font-600 text-xl border-b pb-4 mb-8 text-primary animate-in" style="animation-delay: 400ms;">Suggested Rewrites</h2>
    <section class="mb-12 animate-in" style="animation-delay: 500ms;">
        <div class="row items-center gap-3 mb-4">
            <span class="chip chip-exp">exp_1</span>
            <h3 class="font-600 text-base text-primary">Software Engineer Intern</h3>
        </div>
        <div class="diff-view bg-card mb-4">
            <div class="diff-col before">
                <div class="diff-top-border red"></div>
                <div class="font-mono text-xs text-red font-500 mb-4">Before</div>
                <p class="text-sm text-secondary leading-relaxed">Worked on the company's main web application using React and Redux. <span class="diff-del">Helped</span> backend team to integrate new REST APIs for user dashboard features.</p>
            </div>
            <div class="diff-col after">
                <div class="diff-top-border green"></div>
                <div class="font-mono text-xs text-mint font-500 mb-4">After</div>
                <p class="text-sm text-primary leading-relaxed cursor-text"><span class="diff-add">Architected high-performance UI components</span> for the core React/Redux platform. Partnered with backend engineering to seamlessly integrate REST APIs, <span class="diff-add">delivering real-time data to user dashboards used by 5,000+ daily active users</span>.</p>
            </div>
        </div>
    </section>

    <div class="col items-center mt-xl border-t pt-8 animate-in" style="animation-delay: 600ms;">
        <button id="download-pdf-btn" class="btn btn-primary">Download Feedback as PDF</button>
    </div>
</div>
"""
files['frontend/feedback.html'] = wrap_html('feedback', 'Feedback', html_feedback)
files['frontend/js/pages/feedback.js'] = """
document.getElementById('download-pdf-btn')?.addEventListener('click', () => { window.print(); });
"""

# --- Page: How it works ---
files['frontend/css/pages/howitworks.css'] = """
.timeline-card { border: 1px solid var(--bg-border); background: var(--bg-card); position: relative; border-radius: 12px; padding: 24px; }
.timeline-number { position: absolute; left: -16px; top: -16px; width: 32px; height: 32px; background: var(--blue-500); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'Fraunces', serif; font-size: 18px; }
"""
html_howitworks = """
<div class="max-w-3xl mx-auto px-6 w-full pb-xl">
    <header class="text-center mb-16 animate-in">
        <h1 class="font-display text-5xl mb-4 text-primary">How ResumeTree <span class="italic text-blue">Evaluates.</span></h1>
        <p class="text-secondary text-lg">We abandoned simplistic vector search in favor of hierarchical trees and dynamic chain-of-thought LLM reasoning.</p>
    </header>

    <div class="col gap-12 mt-12 animate-in" style="animation-delay: 200ms;">
        <div class="timeline-card">
            <div class="timeline-number">1</div>
            <h3 class="font-600 text-lg mb-2">Hierarchical Parsing</h3>
            <p class="text-secondary leading-relaxed">Unlike vector databases that flatten professional experience into meaningless strings of numbers, M1 Parser structures your resume into a JSON hierarchy preserving the exact context of every project, skill, and title.</p>
        </div>
        <div class="timeline-card">
            <div class="timeline-number">2</div>
            <h3 class="font-600 text-lg mb-2">Tree Construction</h3>
            <p class="text-secondary leading-relaxed">M2 TreeBuilder converts the hierarchy into a traversable graph. A candidate isn't a paragraph; they are an interconnected network of nodes. You learn <em>Python</em> (skill_1) which was explicitly used to build <em>Accident Predictor</em> (proj_0).</p>
        </div>
        <div class="timeline-card">
            <div class="timeline-number">3</div>
            <h3 class="font-600 text-lg mb-2">Reasoned Evaluation</h3>
            <p class="text-secondary leading-relaxed">M4 EvalAgent doesn't use cosine similarity. It reads the weighted Job Description (from M3) and navigates your career tree. It uses Gemini AI to trace explicit linkages, reasoning actively about whether your <em>proj_0</em> answers the need for <em>REST APIs</em>.</p>
        </div>
    </div>
</div>
"""
files['frontend/howitworks.html'] = wrap_html('howitworks', 'How It Works', html_howitworks)
files['frontend/js/pages/howitworks.js'] = ""

# --- Page: Research ---
files['frontend/css/pages/research.css'] = """
.table-wrapper { overflow-x: auto; border: 1px solid var(--bg-border); border-radius: 10px; }
table { width: 100%; border-collapse: collapse; text-align: left; }
th { background: var(--bg-elevated); padding: 12px 16px; font-size: 12px; font-weight: 600; text-transform: uppercase; color: var(--text-tertiary); letter-spacing: 0.5px; }
td { padding: 12px 16px; border-top: 1px solid var(--bg-border); font-family: 'JetBrains Mono', monospace; font-size: 13px; color: var(--text-secondary); }
tr:hover td { background: rgba(37,99,235,0.05); color: var(--text-primary); }
tr.highlight td { background: rgba(37,99,235,0.1); border-left: 2px solid var(--blue-500); color: var(--primary); font-weight: 600; }
"""
html_research = """
<div class="max-w-7xl mx-auto px-6 w-full pb-xl row flex-wrap gap-12">
    <div class="col flex-1 min-w-[300px] animate-in">
        <h1 class="font-display text-4xl mb-2 text-primary">Run Experiment</h1>
        <p class="text-secondary text-sm mb-8">Execute the pipeline against a benchmark dataset. Results stream in real-time.</p>
        
        <div class="card col gap-6">
            <div class="col gap-2">
                <label class="font-500 text-sm">Dataset Folder (Resumes)</label>
                <input type="file" webkitdirectory directory multiple class="w-full">
            </div>
            <div class="col gap-2">
                <label class="font-500 text-sm">Job Description (.txt)</label>
                <input type="file" accept=".txt" class="w-full">
            </div>
            <div class="col gap-2">
                <label class="font-500 text-sm">Ground Truth CSV (Optional)</label>
                <input type="file" accept=".csv" class="w-full">
            </div>
            <button class="btn btn-primary mt-2">Run Benchmark &rarr;</button>
        </div>
    </div>

    <div class="col flex-1 min-w-[400px] animate-in" style="animation-delay: 200ms;">
        <h2 class="font-600 text-xl mb-6 border-b pb-2 text-primary">Live Results</h2>
        <div class="table-wrapper bg-card">
            <table>
                <thead>
                    <tr><th>Method</th><th>P@5</th><th>P@10</th><th>Spearman ρ</th><th>Latency</th></tr>
                </thead>
                <tbody>
                    <tr><td>TF-IDF</td><td>0.72</td><td>0.68</td><td>0.65</td><td>12ms</td></tr>
                    <tr><td>SBERT</td><td>0.76</td><td>0.71</td><td>0.69</td><td>145ms</td></tr>
                    <tr><td>Flat-LLM</td><td>0.74</td><td>0.70</td><td>0.67</td><td>3200ms</td></tr>
                    <tr class="highlight"><td>ResumeTree</td><td>0.91</td><td>0.88</td><td>0.89</td><td>4100ms</td></tr>
                </tbody>
            </table>
        </div>
        <div class="row gap-4 mt-6 justify-center">
            <button class="btn btn-ghost">Export CSV</button>
            <button class="btn btn-primary">Export Report PDF</button>
        </div>
    </div>
</div>
"""
files['frontend/research.html'] = wrap_html('research', 'Research Benchmark', html_research)
files['frontend/js/pages/research.js'] = ""

for p, c in files.items():
    write_f(p, c)

print("Batch 2 generated successfully: Feedback, How It Works, Research pages.")
