#data profilling
from pathlib import Path
import pandas as pd

RAW_DATA_PATH = Path("data/raw/olist")
OUTPUT_PATH = Path("data/processed/raw_data_profile.csv")

csv_files = list(RAW_DATA_PATH.glob("*.csv"))

profiles = []

for file in csv_files:
    df = pd.read_csv(file)

    profiles.append({
        "file_name": file.name,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "duplicated_rows": df.duplicated().sum(),
        "missing_values": df.isna().sum().sum()
    })

profile_df = pd.DataFrame(profiles)

print(profile_df)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
profile_df.to_csv(OUTPUT_PATH, index=False)

print(f"\nProfile saved to: {OUTPUT_PATH}")