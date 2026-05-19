from datasets import load_dataset
import pandas as pd
import os

print("Downloading dataset...")

# create folder if not exists
os.makedirs("dataset", exist_ok=True)

# load dataset
ds = load_dataset("opensporks/resumes")

# convert to dataframe
df = pd.DataFrame(ds['train'])

print(f"Total resumes: {len(df)}")
print()

# VERY IMPORTANT → show actual column names
print("Columns in dataset:")
print(df.columns)

print()
print("First 5 rows:")
print(df.head())

# save dataset anyway
df.to_csv("dataset/resumes_full.csv", index=False)

print()
print("Saved to dataset/resumes_full.csv")