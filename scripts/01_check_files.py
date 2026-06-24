from pathlib import Path
import pandas as pd

# Folder path
raw_folder = Path("data/raw")

# Files needs to check
files = {
    "listings": raw_folder / "listings.csv.gz",
    "calendar": raw_folder / "calendar.csv.gz",
    "reviews": raw_folder / "reviews.csv.gz",
    "neighbourhoods": raw_folder / "neighbourhoods.csv"
}

print("Checking downloaded files...\n")

for file_name, file_path in files.items():
    print(f"Checking {file_name}")

# Check weather the files exit and read the files using pandas
    if file_path.exists():
        df = pd.read_csv(file_path)

# Print the details about those files
        print("File found:", file_path)
        print("Rows:", len(df))
        print("Columns:", len(df.columns))
        print("Column names:")
        print(list(df.columns))
        print("-" * 50) # Add a separator to readability

    else:
        print("File not found:", file_path)
        print("-" * 50)