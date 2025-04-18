import pandas as pd
from sklearn.model_selection import train_test_split

# Load the data
positive_df = pd.read_csv("high_combined_interactions.tsv", sep="\t")
negative_df = pd.read_csv("random_negative_interactions.tsv", sep="\t")

# Combine and shuffle
combined_df = pd.concat([positive_df, negative_df], ignore_index=True)
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Split into train (70%), val (15%), test (15%)
train_df, temp_df = train_test_split(combined_df, test_size=0.3, random_state=42, stratify=combined_df["output"])
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df["output"])

# Save files (without header, as required by dscript)
train_df.to_csv("train.tsv", sep="\t", index=False, header=False)
val_df.to_csv("val.tsv", sep="\t", index=False, header=False)
test_df.to_csv("test.tsv", sep="\t", index=False, header=False)

print("✅ Done! Files created: train.tsv, val.tsv, test.tsv")
