from datasets import load_dataset
import os

print("Loading dataset...")

# Load dataset
ds = load_dataset("opensporks/resumes")
train_data = ds["train"]

# Labels we want
TECH_LABELS = {
    15: "ENGINEERING",
    20: "INFORMATION-TECHNOLOGY"
}

# Create folders
os.makedirs("dataset/resumes", exist_ok=True)
os.makedirs("dataset/results", exist_ok=True)

saved_count = 0
metadata = []

print("Extracting technical resumes...")
print()

for idx, row in enumerate(train_data):
    label = row["label"]

    if label in TECH_LABELS:
        pdf_obj = row["pdf"]

        try:
            # Extract text from PDF pages
            full_text = ""

            for page in pdf_obj.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"

            # Skip empty resumes
            if len(full_text.strip()) < 200:
                continue

            saved_count += 1

            filename = f"resume_{saved_count:02d}.txt"
            filepath = f"dataset/resumes/{filename}"

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_text)

            metadata.append(
                f"{filename},{TECH_LABELS[label]}"
            )

            print(f"Saved: {filename} ({TECH_LABELS[label]})")

            # Stop at exactly 60
            if saved_count >= 60:
                break

        except Exception as e:
            print(f"Skipped one resume: {e}")

# Save metadata
with open(
    "dataset/sample_metadata.csv",
    "w",
    encoding="utf-8"
) as f:
    f.write("filename,category\n")
    for row in metadata:
        f.write(row + "\n")

print()
print(f"Done! Saved {saved_count} resumes")
print("Location: dataset/resumes/")
print("Metadata: dataset/sample_metadata.csv")