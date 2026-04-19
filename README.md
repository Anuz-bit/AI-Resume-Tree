<div align="center">

<img src="https://img.shields.io/badge/-%F0%9F%8C%B3%20ResumeTree-0D1017?style=for-the-badge&logoColor=white" alt="ResumeTree" />

# ResumeTree

### *Resume screening that actually thinks.*

**Vectorless · Reasoning-Based · Fully Explainable**

A hierarchical tree-structured resume evaluation system powered by LLM chain-of-thought reasoning — not cosine similarity.

<br/>

[![IEEE Research](https://img.shields.io/badge/IEEE-Research%20Project-blue?style=flat-square&logo=ieee&logoColor=white)](/)
[![VIT Pune](https://img.shields.io/badge/VIT-Pune%202025-orange?style=flat-square)](/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

<br/>

```
Resume PDF  →  Hierarchical Tree  →  LLM Reasoning  →  Traceable Score + Explanation
```

<br/>

[**Try It**](#-quick-start) · [**How It Works**](#-how-it-works) · [**Research**](#-ieee-research) · [**Docs**](#-documentation)

<br/>

---

</div>

## 🧠 The Core Idea

Most resume screening tools convert your resume into a blob of numbers and run cosine similarity. The result is a score like **0.84** — with zero explanation.

**ResumeTree does the opposite.**

It preserves the full structure of a resume as a **hierarchical tree** — each job, project, and skill becomes a node with metadata. Then it hands that tree to an LLM and asks it to *reason* about candidate fit, just like a senior recruiter would.

Every score is **traced back to a specific resume node**. Every decision is **explainable**.

```
Vector DB:   Resume → [0.82, 0.14, 0.67, ...] → cosine math → 0.84  ← what does this mean?

ResumeTree:  Resume → Tree → LLM reads + reasons → 78/100
                                                    ↳ "Python match: proj_0 shows FastAPI + Django"
                                                    ↳ "Leadership: exp_0 shows team of 3 for 2 yrs"
                                                    ↳ "Gap: AWS mentioned but not demonstrated"
```

<br/>

---

## ✨ Features

| Feature | Vector DB | ResumeTree |
|---|---|---|
| Career progression visible | ❌ Flattened to numbers | ✅ Preserved as tree nodes |
| Score explainability | ❌ Just a decimal | ✅ Traced to specific nodes |
| Nuanced depth detection | ❌ Treats "basic AWS" = "deep AWS" | ✅ LLM understands context |
| Essential vs flexible reqs | ❌ Equal weight | ✅ Weighted 1.0 / 0.4 |
| Candidate feedback | ❌ Impossible | ✅ Node-traced actionable tips |
| IEEE research novelty | ❌ Well-studied baseline | ✅ Novel contribution |
| Needs vector database | ✅ Yes (Pinecone, FAISS) | ✅ No — just JSON files |

<br/>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        ResumeTree Pipeline                       │
├─────────┬───────────┬──────────┬──────────────┬────────────────┤
│   M1    │    M2     │    M3    │      M4      │      M5        │
│ Resume  │  Tree     │   JD     │  Evaluation  │   Feedback     │
│ Parser  │ Builder   │ Parser   │    Agent     │   Module       │
├─────────┼───────────┼──────────┼──────────────┼────────────────┤
│PDF/DOCX │ ResumeJSON│ JD text  │ resume_tree  │ eval_result    │
│  → JSON │  → Tree   │ → Tree   │ + jd_tree    │ → tips +       │
│         │           │          │ → EvalResult │   rewrites     │
└─────────┴───────────┴──────────┴──────────────┴────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────┐
│                     M6 · ExperimentRunner                        │
│   TF-IDF vs SBERT vs Flat-LLM vs ResumeTree · Precision@K · ρ  │
└─────────────────────────────────────────────────────────────────┘

Shared: LLMClient (SHA-256 cache · retry 3×) · CacheManager · SchemaValidator
```

<br/>

### Module Breakdown

<details>
<summary><b>M1 · ResumeParser</b> — PDF/DOCX → validated ResumeJSON</summary>
<br/>

Extracts raw text from PDF (via `pdfplumber`) or DOCX (via `python-docx`), sends to LLM with a structured extraction prompt, validates output against JSON schema.

- Temperature: `0.1` (deterministic extraction)
- Retry: 3× with exponential backoff
- Cache: SHA-256 keyed JSON files
- Validates: personal info, education, experience, skills, projects, certifications

</details>

<details>
<summary><b>M2 · TreeBuilder</b> — ResumeJSON → Hierarchical TreeNode structure</summary>
<br/>

Converts flat JSON into a tree where every node carries rich metadata. LLM generates a 2-3 sentence summary per leaf node.

```
root (Anuj Wankhade)
├── experience
│   ├── exp_0 · Backend Engineer · stage:mid · led_team:true · outcome:40% latency↓
│   └── exp_1 · Junior Dev · stage:junior · duration:24mo
├── projects
│   ├── proj_0 · CREDIX · complexity:high · has_outcome:true
│   └── proj_1 · Intellectus · tech:[FastAPI, React, ML]
├── education
│   └── edu_0 · B.Tech IT · VIT Pune · CGPA:9.2
└── skills
    └── skill_0 · Python, Django, Docker, AWS...
```

</details>

<details>
<summary><b>M3 · JDParser</b> — Raw JD text → Weighted requirement tree</summary>
<br/>

Parses job descriptions and classifies each requirement:

| Classification | Weight | Signal words |
|---|---|---|
| Essential | `1.0` | "required", "must have", "mandatory" |
| Flexible | `0.4` | "preferred", "nice to have", "plus" |

</details>

<details>
<summary><b>M4 · EvaluationAgent</b> — The core reasoning engine</summary>
<br/>

**Zero vector operations.** The LLM reads the full resume tree and JD tree, then reasons about fit across 4 dimensions:

| Dimension | Weight |
|---|---|
| Skill Match | 35% |
| Experience Quality | 30% |
| Career Progression | 20% |
| Context Fit | 15% |

Every matched requirement cites the exact `node_id` that satisfied it.
Temperature: `0.2` (consistent, deterministic reasoning)

</details>

<details>
<summary><b>M5 · FeedbackModule</b> — Gaps → Actionable candidate tips</summary>
<br/>

Generates specific, improvement tips ranked by hiring impact. **Hard constraint: no fabrication** — only reframes what already exists in the resume.

</details>

<details>
<summary><b>M6 · ExperimentRunner</b> — IEEE benchmark comparison</summary>
<br/>

Controlled experiment comparing 4 methods on the same dataset:

- TF-IDF baseline (sklearn, no LLM)
- SBERT baseline (all-MiniLM-L6-v2 + cosine similarity)  
- Flat-LLM baseline (raw text → LLM, no tree)
- **ResumeTree** (tree + LLM reasoning)

Metrics: `Precision@5`, `Precision@10`, `Spearman's ρ`

</details>

<br/>

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.11+
Gemini API key (aistudio.google.com/apikey)
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/resumetree.git
cd resumetree

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install pdfplumber python-docx google-genai jsonschema \
            pyyaml scikit-learn sentence-transformers scipy pandas
```

### Set API Key

```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "your-api-key-here"

# Mac/Linux
export GEMINI_API_KEY="your-api-key-here"

# Permanent (Windows)
[System.Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your-key", "User")
```

<br/>

---

## 💻 Usage

### Evaluate a Resume

```bash
python main.py evaluate \
  --resume data/resume.pdf \
  --jd data/job_description.txt
```

**Output:**
```
Parsing Resume...        ✓
Building Resume Tree...  ✓  (8 nodes)
Parsing Job Description. ✓  (12 requirements)
Evaluating Candidate...  ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OVERALL SCORE: 78/100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Skill Match          ████████░░  70
  Experience Quality   ██████████  85
  Career Progression   █████████░  80
  Context Fit          ██████░░░░  60

MATCHED [FULL]    req_01 → proj_0  "End-to-end ML pipeline directly matches"
MATCHED [FULL]    req_02 → exp_0   "Led team of 3 satisfies leadership req"
MATCHED [PARTIAL] req_03 → skill_0 "AWS listed but not demonstrated in depth"

STRENGTHS: Strong ML systems, Full-stack, Leadership, High CGPA
GAPS:      MLflow not mentioned, No finance domain, SQL limited

Evaluation ID: 3f9a1c2d-7b4e-4f8a-9c3d-1e2f5a6b7c8d
```

### Generate Candidate Feedback

```bash
python main.py feedback \
  --eval-id 3f9a1c2d-7b4e-4f8a-9c3d-1e2f5a6b7c8d
```

### Run IEEE Benchmark

```bash
python main.py experiment \
  --dataset data/resumes/ \
  --jd data/job_description.txt \
  --output results.csv
```

<br/>

---

## 📁 Project Structure

```
resumetree/
│
├── main.py                        # CLI entry point
│
├── shared/                        # Shared infrastructure
│   ├── llm_client.py              # LLMClient singleton · cache · retry
│   ├── cache_manager.py           # SHA-256 JSON cache
│   └── schema_validator.py        # JSON schema validation
│
├── m1_parser/
│   └── resume_parser.py           # PDF/DOCX → ResumeJSON
│
├── m2_tree/
│   └── tree_builder.py            # ResumeJSON → TreeNode hierarchy
│
├── m3_jd/
│   └── jd_parser.py               # JD text → weighted requirements
│
├── m4_eval/
│   └── eval_agent.py              # Core LLM reasoning engine
│
├── m5_feedback/
│   └── feedback_module.py         # Gap → actionable tips + rewrites
│
├── m6_experiment/
│   └── experiment_runner.py       # IEEE benchmark · 4 baselines
│
├── prompts/                       # YAML prompt files (versioned)
│   ├── extract_resume.yaml        # M1 extraction prompt
│   ├── build_tree.yaml            # M2 tree building prompt
│   ├── parse_jd.yaml              # M3 JD parsing prompt
│   ├── evaluate.yaml              # M4 evaluation prompt
│   └── feedback.yaml              # M5 feedback prompt
│
├── schemas/                       # JSON validation schemas
│   ├── resume_json.json
│   ├── tree_node.json
│   ├── jd_tree.json
│   └── eval_result.json
│
└── data/                          # Runtime data (gitignored)
    ├── parsed/                    # Cached ResumeJSON files
    ├── trees/                     # Cached tree files
    └── evals/                     # Evaluation + feedback results
```

<br/>

---

## 🔬 IEEE Research

This project is a formal IEEE research contribution investigating whether **LLM-based tree reasoning can outperform vector similarity methods** for resume screening.

### Research Gaps Addressed

1. **Resume flattening** — Vector systems destroy hierarchical career structure and progression
2. **No explainability** — Existing systems return similarity scores with zero reasoning
3. **Equal requirement weighting** — No distinction between essential and flexible requirements
4. **LLMs wasted as converters** — Models used only for embeddings, reasoning ability discarded
5. **Screening ≠ feedback** — No existing system unifies evaluation and candidate improvement
6. **No controlled benchmarking** — No fair comparison of retrieval vs reasoning approaches

### Experimental Design

| Method | Approach | LLM Used |
|---|---|---|
| TF-IDF | Term frequency cosine similarity | ❌ None |
| SBERT | `all-MiniLM-L6-v2` embeddings | ❌ Embedding only |
| Flat-LLM | Raw text → LLM (no tree) | ✅ Reasoning |
| **ResumeTree** | **Tree + LLM chain-of-thought** | ✅ Full reasoning |

### Hard Constraints

```python
# These constraints are enforced throughout the codebase
NO_VECTOR_OPERATIONS  = True   # Zero embeddings in main pipeline
NO_FABRICATION        = True   # Only score what exists in resume
SCORE_TRACEABILITY    = True   # Every score cites a node_id
SCHEMA_VALIDATION     = True   # All LLM outputs validated
```

<br/>

---

## ⚙️ Configuration

### LLM Settings

| Module | Temperature | Reason |
|---|---|---|
| M1 · ResumeParser | `0.1` | Deterministic extraction |
| M2 · TreeBuilder | `0.2` | Consistent summarization |
| M3 · JDParser | `0.2` | Reliable classification |
| M4 · EvalAgent | `0.2` | Consistent reasoning |
| M5 · Feedback | `0.4` | More creative suggestions |

### Requirement Weights

```python
ESSENTIAL_WEIGHT = 1.0   # "required", "must have"
FLEXIBLE_WEIGHT  = 0.4   # "preferred", "nice to have"
```

### Caching

All LLM responses are cached by SHA-256 hash of the input. Same resume → zero additional API calls.

```
data/
└── parsed/
    └── {sha256_of_file}.json    ← cached forever
```

<br/>

---

## 📊 Sample Output

```json
{
  "eval_id": "3f9a1c2d-7b4e-4f8a-9c3d-1e2f5a6b7c8d",
  "overall_score": 78,
  "dimension_scores": {
    "skill_match": 70,
    "experience_quality": 85,
    "career_progression": 80,
    "context_fit": 60
  },
  "matched_requirements": [
    {
      "req_id": "req_01",
      "resume_node_id": "proj_0",
      "match_type": "full",
      "reasoning": "CREDIX project demonstrates end-to-end ML pipeline with 4-model ensemble, directly satisfying the requirement for production ML system experience."
    }
  ],
  "strengths": [
    "Strong ML systems experience with SHAP explainability",
    "Full-stack capability (FastAPI + React)",
    "Demonstrated team leadership (Sponsorship Head)"
  ],
  "gaps": [
    "MLflow not explicitly mentioned",
    "Finance domain knowledge not demonstrated",
    "SQL experience limited vs MongoDB"
  ]
}
```

<br/>

---

## 🛡️ Hard Constraints

These constraints are **never violated** anywhere in the codebase:

```
🚫  NO vector embeddings in the main pipeline (M1-M5)
🚫  NO score fabrication — only what's in the resume
✅  EVERY score must cite the node_id that justified it
✅  ALL LLM outputs validated against JSON schema before use
✅  RETRY up to 3 times with exponential backoff
✅  CACHE all API calls by SHA-256 input hash
```

<br/>

---

## 🔧 Tech Stack

```
Core Pipeline
├── python-docx        Resume DOCX extraction
├── pdfplumber         Resume PDF extraction
├── google-genai       LLM API (Gemini 2.0 Flash)
├── jsonschema         Output validation
└── pyyaml             Prompt file loading

M6 Baselines Only
├── scikit-learn       TF-IDF baseline
├── sentence-transformers  SBERT baseline
└── scipy              Spearman correlation

Utilities
├── pandas             Experiment results CSV
├── uuid               Evaluation ID generation
└── hashlib            SHA-256 cache keys
```

<br/>

---

## 🗺️ Roadmap

- [x] M1 · ResumeParser (PDF + DOCX)
- [x] M2 · TreeBuilder (hierarchical nodes + metadata)
- [x] M3 · JDParser (essential vs flexible classification)
- [x] M4 · EvaluationAgent (chain-of-thought reasoning)
- [x] M5 · FeedbackModule (ranked tips + resume rewrites)
- [x] M6 · ExperimentRunner (4 baseline benchmark)
- [ ] Web interface (FastAPI + frontend)
- [ ] Batch evaluation (multiple resumes vs one JD)
- [ ] PDF feedback report export
- [ ] REST API with authentication
- [ ] Docker containerization
- [ ] IEEE paper submission

<br/>

---

## 👥 Team

**Group 11 · Vishwakarma Institute of Technology, Pune**

Built as part of IEEE research in the domain of AI-assisted recruitment systems.

<br/>

---

## 📄 License

```
MIT License · Copyright (c) 2025 ResumeTree · VIT Pune
```

Permission is hereby granted, free of charge, to any person obtaining a copy of this software to use, copy, modify, merge, publish, and distribute — subject to the MIT license terms.

<br/>

---

<div align="center">

**ResumeTree** · Built with 🌳 at VIT Pune · IEEE Research 2025

*"A model that isn't trusted, won't be used. We built the trust in."*

<br/>

[![Star this repo](https://img.shields.io/github/stars/yourusername/resumetree?style=social)](/)
[![Follow](https://img.shields.io/github/followers/yourusername?style=social)](/)

</div>