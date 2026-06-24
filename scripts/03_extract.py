from pathlib import Path
import pandas as pd

# Folder paths
raw_folder = Path("data/raw")
processed_folder = Path("data/processed")
reports_folder = Path("reports/generated_csv")


# Output Folders
processed_folder.mkdir(exist_ok=True)
reports_folder.mkdir(parents=True, exist_ok=True)

print("Starting extract step...\n")

# File paths
listings_file = raw_folder / "listings.csv.gz"
calendar_file = raw_folder / "calendar.csv.gz"
reviews_file = raw_folder / "reviews.csv.gz"
neighbourhoods_file = raw_folder / "neighbourhoods.csv"

# Columns needed from listings
listings_columns = [
    "id",
    "name",
    "host_id",
    "host_name",
    "host_since",
    "host_is_superhost",
    "neighbourhood_cleansed",
    "latitude",
    "longitude",
    "property_type",
    "room_type",
    "accommodates",
    "bathrooms_text",
    "bedrooms",
    "beds",
    "price",
    "minimum_nights",
    "maximum_nights",
    "availability_365",
    "number_of_reviews",
    "review_scores_rating",
    "reviews_per_month",
    "instant_bookable",
    "calculated_host_listings_count"
]

# Columns needed from calendar
calendar_columns = [
    "listing_id",
    "date",
    "available",
    "minimum_nights",
    "maximum_nights"
]

# Columns needed from reviews
reviews_columns = [
    "listing_id",
    "id",
    "date",
    "reviewer_id"
]

# Read datasets
listings = pd.read_csv(
    listings_file,
    usecols=listings_columns
)

calendar = pd.read_csv(
    calendar_file,
    usecols=calendar_columns
)

reviews = pd.read_csv(
    reviews_file,
    usecols=reviews_columns
)

neighbourhoods = pd.read_csv(
    neighbourhoods_file
)

# Save extracted files
listings.to_csv(
    processed_folder / "extracted_listings.csv",
    index=False
)

calendar.to_csv(
    processed_folder / "extracted_calendar.csv",
    index=False
)

reviews.to_csv(
    processed_folder / "extracted_reviews.csv",
    index=False
)

neighbourhoods.to_csv(
    processed_folder / "extracted_neighbourhoods.csv",
    index=False
)

# Create summary report
summary = []

summary.append({
    "file_name": "listings",
    "rows": len(listings),
    "columns": len(listings.columns)
})

summary.append({
    "file_name": "calendar",
    "rows": len(calendar),
    "columns": len(calendar.columns)
})

summary.append({
    "file_name": "reviews",
    "rows": len(reviews),
    "columns": len(reviews.columns)
})

summary.append({
    "file_name": "neighbourhoods",
    "rows": len(neighbourhoods),
    "columns": len(neighbourhoods.columns)
})

summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    reports_folder / "extract_summary.csv",
    index=False
)

print("Extract step completed.")

print("\nFiles created:")

print("- extracted_listings.csv")
print("- extracted_calendar.csv")
print("- extracted_reviews.csv")
print("- extracted_neighbourhoods.csv")

print("\nReport created:")
print("- reports/generated_csv/extract_summary.csv")