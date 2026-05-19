import pandas as pd
import os

# Load full dataset
df = pd.read_csv("resumes_full.csv")

print("All categories:")
print(df['Category'].value_counts())
print()

# Filter to tech categories only
tech_categories = [
    'INFORMATION-TECHNOLOGY',
    'ENGINEERING', 
    'DATA-SCIENCE',
    'DEVELOPER',
    'JAVA-DEVELOPER',
    'PYTHON-DEVELOPER',
    'DOTNET-DEVELOPER',
    'DATABASE',
    'NETWORK-SECURITY-ENGINEER',
    'BUSINESS-ANALYST',
]

# Filter
tech_df = df[df['Category'].isin(tech_categories)]
print(f"Tech resumes found: {len(tech_df)}")

# Sample exactly 60
sample = tech_df.sample(60, random_state=42)
print(f"Sampled: {len(sample)} resumes")

# Create output folders
os.makedirs("dataset/resumes", exist_ok=True)
os.makedirs("dataset/results", exist_ok=True)

# Save each resume as individual .txt file
for i, (idx, row) in enumerate(sample.iterrows(), 1):
    filename = f"dataset/resumes/resume_{i:02d}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(row['Resume_str'])
    print(f"Saved: {filename} ({row['Category']})")

# Save sample metadata
sample[['ID', 'Category']].to_csv(
    "dataset/sample_metadata.csv", 
    index=False
)

print(f"\nDone! 60 resumes saved to dataset/resumes/")
print(f"Metadata saved to dataset/sample_metadata.csv")