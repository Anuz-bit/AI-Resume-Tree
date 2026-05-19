import os
import json
import csv
import time
from groq import Groq

# -----------------------------
# Setup Groq
# -----------------------------

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise ValueError("Please set GROQ_API_KEY first")

client = Groq(api_key=api_key)

# -----------------------------
# Paths
# -----------------------------

resumes_folder = "dataset/resumes"
jds_folder = "dataset/jds"
output_file = "dataset/ground_truth.csv"

resume_files = sorted([
    f for f in os.listdir(resumes_folder)
    if f.endswith(".txt")
])[:20]   # first 20 for testing

jd_files = sorted([
    f for f in os.listdir(jds_folder)
    if f.endswith(".txt")
])

print(f"Resumes found: {len(resume_files)}")
print(f"JDs found: {len(jd_files)}")
print(f"Total evaluations: {len(resume_files) * len(jd_files)}")
print()

ground_truth = []

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

Only JSON.
No markdown.
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=150
            )

            text = response.choices[0].message.content.strip()
            print("\nRAW RESPONSE:")
print(text)
            print("-" * 50)

            # remove markdown if present
            if text.startswith("```"):
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

            result = json.loads(text)

            score = result.get("score", 50)
            reason = result.get("reason", "")

            print(
                f"[{i:02d}] "
                f"{resume_file} -> {score}/100"
            )

        except Exception as e:
            print(
                f"[{i:02d}] "
                f"{resume_file} -> ERROR: {str(e)}"
            )

            score = 50
            reason = "fallback due to error"

        ground_truth.append({
            "resume_file": resume_file,
            "jd_file": jd_file,
            "score": score,
            "reason": reason
        })

        time.sleep(1)

# Save CSV
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