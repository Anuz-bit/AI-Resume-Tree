from datasets import load_dataset
import pandas as pd
import os

print("Loading dataset...")

ds = load_dataset("opensporks/resumes")

print()
print("Dataset Features:")
print(ds["train"].features)

print()
print("Unique Labels:")
df = pd.DataFrame(ds["train"])

print(sorted(df["label"].unique()))
print()

print("Label counts:")
print(df["label"].value_counts().sort_index())