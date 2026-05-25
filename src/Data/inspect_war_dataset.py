from pathlib import Path
import pandas as pd

raw_path = Path("/home/i-igo-pc/PycharmProjects/Cobalto/datasets/raw/LC_loans_granting_model_dataset.csv")

df = pd.read_csv(raw_path, nrows=10_000, low_memory=False)

print(df.shape)
print(df.head())
print(df.columns.tolist())
print(df.dtypes)
print(df.isna().mean().sort_values(ascending=False).head(30))

if "Default" in df.columns:
    print(df["Default"].value_counts(normalize=True))