from pathlib import Path
import pandas as pd

RAW_DATA_PATH = Path("data/raw/olist")
OUTPUT_PATH = Path("data/processed/raw_column_profile.csv")

profiles = []

csv_files = sorted(RAW_DATA_PATH.glob("*.csv"))

for file in csv_files:
    df = pd.read_csv(file)

    for column in df.columns:
        profiles.append({
            "file_name": file.name,
            "column_name": column,
            "data_type": str(df[column].dtype),
            "rows": len(df),
            "missing_count": df[column].isna().sum(),
            "missing_percentage": round(df[column].isna().mean() * 100, 2),
            "unique_values": df[column].nunique()
        })

profile_df = pd.DataFrame(profiles)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
profile_df.to_csv(OUTPUT_PATH, index=False)

print(profile_df)
print(f"\nColumn profile saved to: {OUTPUT_PATH}")