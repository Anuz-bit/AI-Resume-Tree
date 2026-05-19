import os
import json
import csv
import time
from google import genai
from google.genai import types

# -----------------------------
# Setup Gemini
# -----------------------------

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "Please set GEMINI_API_KEY first"
    )

client = genai.Client(api_key=api_key)

# -----------------------------
# Paths
# -----------------------------

resumes_folder = "dataset/resumes"
jds_folder = "dataset/jds"
output_file = "dataset/ground_truth.csv"

resume_files = sorted([
    f for f in os.listdir(resumes_folder)
    if f.endswith(".txt")
])[:20]

jd_files = sorted([
    f for f in os.listdir(jds_folder)
    if f.endswith(".txt")
])

print(f"Resumes found: {len(resume_files)}")
print(f"JDs found: {len(jd_files)}")
print(f"Total evaluations: {len(resume_files) * len(jd_files)}")
print()

ground_truth = []

# -----------------------------
# Main Loop
# -----------------------------

for jd_file in jd_files:
    jd_path = os.path.join(jds_folder, jd_file)

    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    print(f"\nProcessing JD: {jd_file}")
    print("-" * 50)

    for i, resume_file in enumerate(resume_files, 1):
        resume_path = os.path.join(
            resumes_folder,
            resume_file
        )

        with open(
            resume_path,
            "r",
            encoding="utf-8"
        ) as f:
            resume_text = f.read()

        # Trim to save tokens
        resume_trimmed = resume_text[:1200]

        prompt = f"""
You are an expert technical recruiter.

Evaluate this resume against the job description.

JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_trimmed}

Score from 0 to 100 based on:
1. Skill match
2. Education relevance
3. Experience fit
4. Overall technical suitability

Return ONLY valid JSON:

{{
  "score": 78,
  "reason": "short one-line reason"
}}

No markdown.
No explanation.
Only JSON.
"""

        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=120
                )
            )

            text = response.text.strip()

            # Clean accidental markdown
            if text.startswith("```"):
                text = text.replace(
                    "```json", ""
                ).replace(
                    "```", ""
                ).strip()

            result = json.loads(text)

            score = result.get("score", 50)
            reason = result.get("reason", "")

            print(
                f"[{i:02d}] "
                f"{resume_file} → {score}/100"
            )

        except Exception as e:
            print(
                f"[{i:02d}] "
                f"{resume_file} → ERROR: {str(e)}"
            )

            score = 50
            reason = f"fallback due to error: {str(e)}"

        ground_truth.append({
            "resume_file": resume_file,
            "jd_file": jd_file,
            "score": score,
            "reason": reason
        })

        # Avoid API rate limits
        time.sleep(2)

# -----------------------------
# Save CSV
# -----------------------------

with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "resume_file",
            "jd_file",
            "score",
            "reason"
        ]
    )

    writer.writeheader()
    writer.writerows(ground_truth)

print()
print("=" * 60)
print("GROUND TRUTH CREATED SUCCESSFULLY")
print(f"Saved to: {output_file}")
print("=" * 60)