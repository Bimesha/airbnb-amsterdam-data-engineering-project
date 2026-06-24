from pathlib import Path
import pandas as pd

# Folder path
raw_folder = Path("data/raw")
reports_folder = Path("reports/generated_csv")
reports_folder.mkdir(parents=True, exist_ok=True)

# Datasets paths
files = {
    "listings": raw_folder / "listings.csv.gz",
    "calendar": raw_folder / "calendar.csv.gz",
    "reviews": raw_folder / "reviews.csv.gz",
    "neighbourhoods": raw_folder / "neighbourhoods.csv"
}

# Create empty list for store summary details
dataset_summary = []
schema_rows = []

print("Profiling data files...\n")


for file_name, file_path in files.items():
    print(f"Profiling {file_name}")

# Read every dataset using pandas
    df = pd.read_csv(file_path)

# Store basic details about dataset
    dataset_summary.append({
        "file_name": file_name,
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": df.duplicated().sum()
    })

    # Loop through ech column
    for column in df.columns:
        # Check missing values and missing value precentage
        missing_count = df[column].isna().sum()
        missing_percentage = round((missing_count / len(df)) * 100, 2)

        sample_values = df[column].dropna().astype(str).head(3).tolist()
        
        # Check weather the column data type is numeric or not
        if pd.api.types.is_numeric_dtype(df[column]):
            min_value = df[column].min()
            max_value = df[column].max()
        else:
            min_value = ""
            max_value = ""

        # Store details
        schema_rows.append({
            "file_name": file_name,
            "column_name": column,
            "data_type": str(df[column].dtype),
            "missing_count": missing_count,
            "missing_percentage": missing_percentage,
            "min_value": min_value,
            "max_value": max_value,
            "sample_values": " | ".join(sample_values)
        })

    print("Done")
    print("-" * 50)

# Convert list into the dataframe using pandas
summary_df = pd.DataFrame(dataset_summary)
schema_df = pd.DataFrame(schema_rows)

summary_df.to_csv(reports_folder / "dataset_summary.csv", index=False)
schema_df.to_csv(reports_folder / "schema_profile.csv", index=False)

print("\nReports created:")
print("reports/generated_csv/dataset_summary.csv")
print("reports/generated_csv/schema_profile.csv")