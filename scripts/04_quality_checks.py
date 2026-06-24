from pathlib import Path
import pandas as pd

# File paths
raw_folder = Path("data/raw")
reports_folder = Path("reports/generated_csv")
reports_folder.mkdir(parents=True, exist_ok=True)

print("Starting data quality checks...\n")

# Read datasets
listings = pd.read_csv(raw_folder / "listings.csv.gz", low_memory=False)
calendar = pd.read_csv(raw_folder / "calendar.csv.gz", low_memory=False)
reviews = pd.read_csv(raw_folder / "reviews.csv.gz", low_memory=False)
neighbourhoods = pd.read_csv(raw_folder / "neighbourhoods.csv", low_memory=False)

files = {
    "listings": listings,
    "calendar": calendar,
    "reviews": reviews,
    "neighbourhoods": neighbourhoods
}

# Create empty list for store results
results = []


# 1. Missing values check
for file_name, df in files.items():

    missing = df.isna().sum()

    for column in df.columns:
        results.append({
            "check_type": "missing_values",
            "file_name": file_name,
            "column_name": column,
            "issue_count": missing[column]
        })


# 2. Duplicate rows check
for file_name, df in files.items():

    # Count duplicates values
    dup_count = df.duplicated().sum()

    # Store results 
    results.append({
        "check_type": "duplicates",
        "file_name": file_name,
        "column_name": "all_columns",
        "issue_count": dup_count
    })


# 3. Simple duplicate listings check
duplicate_check = listings[["id", "name", "host_id", "neighbourhood_cleansed", "room_type"]].copy()

possible_duplicates = duplicate_check[
    duplicate_check.duplicated(
        subset=["host_id", "name", "neighbourhood_cleansed", "room_type"],
        keep=False
    )
]

possible_duplicates.to_csv(
    reports_folder / "possible_duplicate_listings.csv",
    index=False
)

results.append({
    "check_type": "possible_duplicates",
    "file_name": "listings",
    "column_name": "host_id + name + neighbourhood + room_type",
    "issue_count": len(possible_duplicates)
})


# 4. Price cleaning (simple)

# Convert price column to a string
listings["price_clean"] = listings["price"].astype(str)

# Remove $ sign
listings["price_clean"] = listings["price_clean"].str.replace("$", "", regex=False)

# Remove ,
listings["price_clean"] = listings["price_clean"].str.replace(",", "", regex=False)

# Convert clean price value to numeric type
listings["price_clean"] = pd.to_numeric(listings["price_clean"], errors="coerce")

# Negative price check
negative_price = listings[listings["price_clean"] < 0]

results.append({
    "check_type": "invalid_price",
    "file_name": "listings",
    "column_name": "price",
    "issue_count": len(negative_price)
})


# 5. Availability check

# Check whether availability_365 is outside the valid range 0 to 365
invalid_availability = listings[
    (listings["availability_365"] < 0) |
    (listings["availability_365"] > 365)
]

results.append({
    "check_type": "invalid_availability",
    "file_name": "listings",
    "column_name": "availability_365",
    "issue_count": len(invalid_availability)
})


# 6. Latitude / longitude check
invalid_location = listings[
    (listings["latitude"] < -90) |
    (listings["latitude"] > 90) |
    (listings["longitude"] < -180) |
    (listings["longitude"] > 180)
]

results.append({
    "check_type": "invalid_location",
    "file_name": "listings",
    "column_name": "latitude/longitude",
    "issue_count": len(invalid_location)
})


# 7. Calendar validation
invalid_calendar = calendar[
    ~calendar["available"].isin(["t", "f"])
]

results.append({
    "check_type": "invalid_calendar_values",
    "file_name": "calendar",
    "column_name": "available",
    "issue_count": len(invalid_calendar)
})


# Save report
quality_df = pd.DataFrame(results)

quality_df.to_csv(
    reports_folder / "data_quality_checks.csv",
    index=False
)

print("Data quality checks completed.")
print("Reports saved in reports/generated_csv folder.")