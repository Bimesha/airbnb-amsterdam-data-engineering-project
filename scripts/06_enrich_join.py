from pathlib import Path
import pandas as pd

# File paths
processed_folder = Path("data/processed")
reports_folder = Path("reports/generated_csv")

processed_folder.mkdir(parents=True, exist_ok=True)
reports_folder.mkdir(parents=True, exist_ok=True)

print("Starting enrichment and joining step...\n")

# Read cleaned files
listings = pd.read_csv(processed_folder / "clean_listings.csv", low_memory=False)
calendar = pd.read_csv(processed_folder / "clean_calendar.csv", low_memory=False)
reviews = pd.read_csv(processed_folder / "clean_reviews.csv", low_memory=False)
neighbourhoods = pd.read_csv(processed_folder / "clean_neighbourhoods.csv", low_memory=False)

# Rename id into listing_id(if still store as id)
listings = listings.rename(columns={"id": "listing_id"})


# 1. calendar summary
# Convert availability values into boolean formats
calendar["is_available"] = calendar["is_available"].astype(str).map({
    "True": True,
    "False": False,
    "t": True,
    "f": False
})

calendar_summary = calendar.groupby("listing_id").agg(
    total_days=("date", "count"),
    available_days=("is_available", "sum")
).reset_index()

# Calculate occupancy rate
calendar_summary["occupancy_rate"] = (
    1 - (calendar_summary["available_days"] / calendar_summary["total_days"])
).round(2)


# 2. Review summary per listing
# Count reviews for each listing
review_summary = reviews.groupby("listing_id").agg(
    review_count=("review_id", "count")
).reset_index()


# 3. Join tables (Master dataset)
# Joing listing with calendar summary
listing_master = listings.merge(calendar_summary, on="listing_id", how="left")

# Join listing with review summary
listing_master = listing_master.merge(review_summary, on="listing_id", how="left")

# Fill missing values with 0
listing_master["review_count"] = listing_master["review_count"].fillna(0)
listing_master["occupancy_rate"] = listing_master["occupancy_rate"].fillna(0)


# 4. Derived features
# Host tenure (simple version)
listing_master["host_since"] = pd.to_datetime(listing_master["host_since"], errors="coerce")
listing_master["host_tenure_years"] = (
    (pd.to_datetime("today") - listing_master["host_since"]).dt.days / 365
).round(1)

# Price per bedroom
listing_master["price_per_bedroom"] = None

valid = (
    listing_master["bedrooms"].notna() &
    (listing_master["bedrooms"] > 0) &
    listing_master["price_clean"].notna()
)

listing_master.loc[valid, "price_per_bedroom"] = (
    listing_master.loc[valid, "price_clean"] /
    listing_master.loc[valid, "bedrooms"]
).round(2)

# Estimated revenue (simple)
listing_master["estimated_revenue"] = (
    listing_master["price_clean"] * listing_master["occupancy_rate"] * 365
).round(2)


# 5. Neighbourhood summary
neighbourhood_summary = listing_master.groupby("neighbourhood_cleansed").agg(
    listing_count=("listing_id", "count"),
    avg_price=("price_clean", "mean"),
    avg_rating=("review_scores_rating", "mean"),
    avg_occupancy=("occupancy_rate", "mean")
).reset_index()

# Round values
neighbourhood_summary = neighbourhood_summary.round(2)


# 6. Save outputs
calendar_summary.to_csv(processed_folder / "calendar_summary.csv", index=False)
review_summary.to_csv(processed_folder / "review_summary.csv", index=False)
listing_master.to_csv(processed_folder / "listing_master.csv", index=False)
neighbourhood_summary.to_csv(processed_folder / "neighbourhood_summary.csv", index=False)


# Report
summary = [
    {"file": "calendar_summary", "rows": len(calendar_summary)},
    {"file": "review_summary", "rows": len(review_summary)},
    {"file": "listing_master", "rows": len(listing_master)},
    {"file": "neighbourhood_summary", "rows": len(neighbourhood_summary)}
]

pd.DataFrame(summary).to_csv(
    reports_folder / "enrichment_summary.csv",
    index=False
)

print("Enrichment completed.")
print("Master dataset created: data/processed/listing_master.csv")
print("Report created: reports/generated_csv/enrichment_summary.csv")