from pathlib import Path
import pandas as pd
from sqlalchemy import text
from db_connection import get_engine

# File paths
processed_folder = Path("data/processed")
reports_folder = Path("reports/generated_csv")
reports_folder.mkdir(parents=True, exist_ok=True)

print("Starting data modeling and PostgreSQL load\n")

# Connect to PostgreSQL
engine = get_engine()

# Read final processed files
listing_master = pd.read_csv(processed_folder / "listing_master.csv", low_memory=False)
calendar_summary = pd.read_csv(processed_folder / "calendar_summary.csv", low_memory=False)
review_summary = pd.read_csv(processed_folder / "review_summary.csv", low_memory=False)
neighbourhood_summary = pd.read_csv(processed_folder / "neighbourhood_summary.csv", low_memory=False)

# Add city column(Useful when using muktiple cities)
listing_master["city"] = "Amsterdam"
neighbourhood_summary["city"] = "Amsterdam"


# Create neighbourhood dimension
dim_neighbourhood = (
    listing_master[["city", "neighbourhood_cleansed"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

dim_neighbourhood["neighbourhood_id"] = dim_neighbourhood.index + 1

# Add neighbourhood_id to listing_master
listing_master = listing_master.merge(
    dim_neighbourhood,
    on=["city", "neighbourhood_cleansed"],
    how="left"
)


# Create host dimension
dim_host = listing_master[[
    "host_id",
    "host_name",
    "host_since",
    "host_is_superhost",
    "host_tenure_years",
    "calculated_host_listings_count"
]].drop_duplicates(subset=["host_id"])


# Create listing dimension
dim_listing = listing_master[[
    "listing_id",
    "name",
    "host_id",
    "neighbourhood_id",
    "room_type",
    "property_type",
    "accommodates",
    "bedrooms",
    "beds",
    "minimum_nights",
    "maximum_nights"
]].drop_duplicates(subset=["listing_id"])


# Create fact table
fact_listing_performance = listing_master[[
    "listing_id",
    "host_id",
    "neighbourhood_id",
    "price_clean",
    "availability_365",
    "occupancy_rate",
    "estimated_revenue",
    "review_count",
    "review_scores_rating",
    "reviews_per_month",
    "price_per_bedroom"
]].copy()

fact_listing_performance = fact_listing_performance.rename(
    columns={
        "reviews_per_month": "review_frequency_per_month"
    }
)

# Convert important fact columns to numeric
numeric_columns = [
    "price_clean",
    "availability_365",
    "occupancy_rate",
    "estimated_revenue",
    "review_count",
    "review_scores_rating",
    "review_frequency_per_month",
    "price_per_bedroom"
]

for column in numeric_columns:
    fact_listing_performance[column] = pd.to_numeric(
        fact_listing_performance[column],
        errors="coerce"
    )


# Create PostgreSQL schema
with engine.begin() as connection:
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS analytics"))


# Load tables into PostgreSQL
dim_host.to_sql(
    "dim_host",
    engine,
    schema="analytics",
    if_exists="replace",
    index=False
)

dim_listing.to_sql(
    "dim_listing",
    engine,
    schema="analytics",
    if_exists="replace",
    index=False
)

dim_neighbourhood.to_sql(
    "dim_neighbourhood",
    engine,
    schema="analytics",
    if_exists="replace",
    index=False
)

fact_listing_performance.to_sql(
    "fact_listing_performance",
    engine,
    schema="analytics",
    if_exists="replace",
    index=False
)

listing_master.to_sql(
    "listing_master",
    engine,
    schema="analytics",
    if_exists="replace",
    index=False
)

calendar_summary.to_sql(
    "calendar_summary",
    engine,
    schema="analytics",
    if_exists="replace",
    index=False
)

review_summary.to_sql(
    "review_summary",
    engine,
    schema="analytics",
    if_exists="replace",
    index=False
)

neighbourhood_summary.to_sql(
    "neighbourhood_summary",
    engine,
    schema="analytics",
    if_exists="replace",
    index=False
)


# Create load summary report
summary = [
    {"table_name": "analytics.dim_host", "rows": len(dim_host)},
    {"table_name": "analytics.dim_listing", "rows": len(dim_listing)},
    {"table_name": "analytics.dim_neighbourhood", "rows": len(dim_neighbourhood)},
    {"table_name": "analytics.fact_listing_performance", "rows": len(fact_listing_performance)},
    {"table_name": "analytics.listing_master", "rows": len(listing_master)},
    {"table_name": "analytics.calendar_summary", "rows": len(calendar_summary)},
    {"table_name": "analytics.review_summary", "rows": len(review_summary)},
    {"table_name": "analytics.neighbourhood_summary", "rows": len(neighbourhood_summary)}
]

summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    reports_folder / "postgres_load_summary.csv",
    index=False
)

print("Data modeling and PostgreSQL load completed.")
print("Tables created in PostgreSQL analytics schema.")
print("Report saved:")
print("- reports/generated_csv/postgres_load_summary.csv")